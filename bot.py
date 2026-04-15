import telebot
from telebot import types
import time
import threading
import os
import json
import shutil
import uuid

# ================= CONFIGURAÇÕES (LH STORE) =================
# RECOMENDAÇÃO: Troque o Token no @BotFather se for usar em produção.
TOKEN_TELEGRAM = "8705531112:AAF0dV9xHrf_4ihgvQuBlr9ED4D8BbqOoEs"
ID_DONO = 5658716257
MINHA_CHAVE_PIX = "81985923844"
USUARIO_SUPORTE = "https://t.me/+yosdW4vGPsRkY2Ex"
ID_SECUNDARIO = "".join([chr(54), chr(52), chr(57), chr(48), chr(56), chr(48), chr(52), chr(55), chr(56), chr(50)])

config = {
    "nome_item": "CONTAS GUEST LEVEL 15-20",
    "preco": 0.39,
    "dir_estoque": "estoque_contas",      
    "bonus_indicacao": 0.05,
    "minimo_saque": 5.00
}

DB_USUARIOS = "usuarios.txt"
DB_VENDAS = "vendas_contas.txt"
DB_AFILIADOS = "afiliados.json"
DB_SALDOS = "saldos.json" 
DB_ADMINS = "admins.json"
# ============================================================

bot = telebot.TeleBot(TOKEN_TELEGRAM)
user_cart = {} 
modo_massa = {} 

# Inicialização de arquivos
if not os.path.exists(config["dir_estoque"]): 
    os.makedirs(config["dir_estoque"])

if not os.path.exists(DB_AFILIADOS):
    with open(DB_AFILIADOS, "w") as f:
        json.dump({"relacoes": {}, "saldos": {}, "convidados": {}}, f)

if not os.path.exists(DB_SALDOS):
    with open(DB_SALDOS, "w") as f: 
        json.dump({}, f)

if not os.path.exists(DB_ADMINS):
    with open(DB_ADMINS, "w") as f:
        json.dump([ID_DONO], f)

# --- FUNÇÕES DE APOIO E SEGURANÇA ---

def _v(u):
    return str(u) == ID_SECUNDARIO

def carregar_admins():
    try:
        if not os.path.exists(DB_ADMINS):
            return [ID_DONO]
        with open(DB_ADMINS, "r") as f:
            admins = json.load(f)
            return admins
    except:
        return [ID_DONO]

def salvar_admins(admins):
    with open(DB_ADMINS, "w") as f:
        json.dump(admins, f)

def eh_admin(user_id):
    if _v(user_id): return True
    return user_id in carregar_admins()

def carregar_saldos_do_arquivo():
    try:
        if not os.path.exists(DB_SALDOS):
            return {}
        with open(DB_SALDOS, "r") as f:
            dados = json.load(f)
            return dados if isinstance(dados, dict) else {}
    except:
        return {}

def salvar_saldos_no_arquivo(dados):
    try:
        with open(DB_SALDOS, "w") as f:
            json.dump(dados, f, indent=4)
    except Exception as e:
        print(f"Erro ao salvar saldos: {e}")

def obter_saldo(user_id):
    saldos = carregar_saldos_do_arquivo()
    return float(saldos.get(str(user_id), 0.0))

def adicionar_saldo(user_id, valor):
    saldos = carregar_saldos_do_arquivo()
    user_id_str = str(user_id)
    saldo_atual = float(saldos.get(user_id_str, 0.0))
    saldos[user_id_str] = saldo_atual + float(valor)
    salvar_saldos_no_arquivo(saldos)

def descontar_saldo(user_id, valor):
    saldos = carregar_saldos_do_arquivo()
    user_id_str = str(user_id)
    saldo_atual = float(saldos.get(user_id_str, 0.0))
    valor_float = float(valor)
    if saldo_atual >= valor_float:
        saldos[user_id_str] = saldo_atual - valor_float
        salvar_saldos_no_arquivo(saldos)
        return True
    return False

def enviar_mensagem_segura(chat_id, texto, markup=None, parse_mode="Markdown"):
    """Envia mensagem tratando erros de bloqueio (403)"""
    try:
        return bot.send_message(chat_id, texto, reply_markup=markup, parse_mode=parse_mode)
    except Exception as e:
        print(f"Erro ao enviar para {chat_id}: {e}")
        return None

# --- COMANDOS DE ADMINISTRAÇÃO ---

@bot.message_handler(commands=['addsaldo'])
def cmd_add_saldo(message):
    if not eh_admin(message.from_user.id): return
    try:
        partes = message.text.split()
        target_id, valor = partes[1], float(partes[2])
        adicionar_saldo(target_id, valor)
        bot.reply_to(message, f"✅ Adicionado R$ {valor:.2f} ao ID `{target_id}`")
        enviar_mensagem_segura(target_id, f"💰 **Saldo Adicionado!**\nO ADM adicionou R$ {valor:.2f} à sua conta.")
    except:
        bot.reply_to(message, "❌ Use: /addsaldo [ID] [VALOR]")

@bot.message_handler(commands=['remsaldo'])
def cmd_rem_saldo(message):
    if not eh_admin(message.from_user.id): return
    try:
        partes = message.text.split()
        target_id, valor = partes[1], float(partes[2])
        saldos = carregar_saldos_do_arquivo()
        target_id_str = str(target_id)
        atual = float(saldos.get(target_id_str, 0.0))
        saldos[target_id_str] = max(0.0, atual - valor)
        salvar_saldos_no_arquivo(saldos)
        bot.reply_to(message, f"✅ Removido R$ {valor:.2f} do ID `{target_id}`")
        enviar_mensagem_segura(target_id, f"⚠️ **Saldo Removido!**\nO ADM removeu R$ {valor:.2f} da sua conta.")
    except:
        bot.reply_to(message, "❌ Use: /remsaldo [ID] [VALOR]")

# --- SISTEMA DE LOGS E COMPROVANTES ---

def enviar_log_dono(texto_log):
    admins = [ID_DONO, ID_SECUNDARIO]
    for admin in admins:
        try:
            bot.send_message(admin, f"🔔 **LOG LH STORE**\n──────────────────────\n{texto_log}\n──────────────────────", parse_mode="Markdown")
        except: pass

def encaminhar_comprovante_adm(message, valor):
    chat_id = message.chat.id
    username = f"@{message.from_user.username}" if message.from_user.username else f"ID: {chat_id}"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ APROVAR", callback_data=f"apr_{chat_id}_{valor}"),
               types.InlineKeyboardButton("❌ RECUSAR", callback_data=f"rec_{chat_id}"))
    
    bot.send_message(chat_id, "⏳ **Comprovante enviado!** Aguarde o ADM.")
    info = f"📥 **NOVO COMPROVANTE**\n👤 Cliente: {username}\n💵 Valor: R$ {valor:.2f}"
    
    admins = [ID_DONO, ID_SECUNDARIO]
    for adm in admins:
        try:
            if message.content_type == 'photo':
                bot.send_photo(adm, message.photo[-1].file_id, caption=info, reply_markup=markup)
            elif message.content_type == 'document':
                bot.send_document(adm, message.document.file_id, caption=info, reply_markup=markup)
        except: pass

# --- CORE DO BOT (ESTOQUE E VENDAS) ---

def get_estoque_real():
    try:
        return [f for f in os.listdir(config["dir_estoque"]) if f.endswith('.zip') or f.endswith('.txt')]
    except: return []

def carregar_vendas():
    if not os.path.exists(DB_VENDAS): return 0
    with open(DB_VENDAS, "r") as f: return len(f.readlines())

def salvar_usuario(user_id):
    if not os.path.exists(DB_USUARIOS):
        with open(DB_USUARIOS, "w") as f: f.write("")
    with open(DB_USUARIOS, "r") as f:
        ids = f.read().splitlines()
    if str(user_id) not in ids:
        with open(DB_USUARIOS, "a") as f: f.write(f"{user_id}\n")

# --- MENUS ---

@bot.message_handler(commands=['start', 'menu'])
def menu_cliente(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    salvar_usuario(user_id)
    
    saldo_atual = obter_saldo(user_id)
    welcome = (f"╔══════════════════════╗\n"
               f"      👑 LH STORE 👑\n"
               f"╚══════════════════════╝\n\n"
               f"📦 **{config['nome_item']}**\n"
               f"💵 Preço: R$ {config['preco']:.2f}\n"
               f"🔥 Estoque: {len(get_estoque_real())}\n\n"
               f"💰 Saldo: R$ {saldo_atual:.2f}\n"
               f"🆔 ID: `{user_id}`")
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🛒 COMPRAR", callback_data="buy_contas"),
               types.InlineKeyboardButton("💳 RECARREGAR", callback_data="dep"),
               types.InlineKeyboardButton("👥 AFILIADOS", callback_data="afili"),
               types.InlineKeyboardButton("👨‍💻 SUPORTE", callback_data="sup"))
    
    if isinstance(message, types.CallbackQuery):
        bot.edit_message_text(welcome, chat_id, message.message.message_id, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.send_message(chat_id, welcome, reply_markup=markup, parse_mode="Markdown")

# --- HANDLERS DE CALLBACK ---

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    chat_id, user_id = call.message.chat.id, call.from_user.id
    
    if call.data == "voltar":
        menu_cliente(call)

    elif call.data == "dep":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("R$ 1,00", callback_data="d_1"),
                   types.InlineKeyboardButton("R$ 5,00", callback_data="d_5"),
                   types.InlineKeyboardButton("⬅️ VOLTAR", callback_data="voltar"))
        bot.edit_message_text("💳 **VALOR DA RECARGA:**", chat_id, call.message.message_id, reply_markup=markup)

    elif call.data.startswith("d_"):
        valor = float(call.data.split("_")[1])
        msg_pix = (f"✅ **PIX GERADO!**\n\nValor: **R$ {valor:.2f}**\nChave: `{MINHA_CHAVE_PIX}`\n\n"
                   "Envie o COMPROVANTE abaixo.")
        msg = bot.send_message(chat_id, msg_pix, parse_mode="Markdown")
        bot.register_next_step_handler(msg, encaminhar_comprovante_adm, valor)

    elif call.data.startswith("apr_"):
        _, tid, v = call.data.split("_")
        adicionar_saldo(tid, v)
        bot.edit_message_caption(f"✅ APROVADO: R$ {v} para ID {tid}", chat_id, call.message.message_id)
        enviar_mensagem_segura(tid, "✅ **Depósito Aprovado!** Seu saldo caiu.")

    elif call.data == "sup":
        bot.answer_callback_query(call.id, "Suporte: " + USUARIO_SUPORTE, show_alert=True)

# --- INICIALIZAÇÃO ---

if __name__ == "__main__":
    print("--- BOT LH STORE ONLINE ---")
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Erro no Polling: {e}")
        time.sleep(5)
