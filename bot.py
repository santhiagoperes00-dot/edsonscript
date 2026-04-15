import telebot
from telebot import types
import time
import os
import json
import shutil

# ================= CONFIGURAÇÕES (LH STORE) =================
TOKEN_TELEGRAM = "8705531112:AAF0dV9xHrf_4ihgvQuBlr9ED4D8BbqOoEs"
ID_DONO = 5658716257
ID_SECUNDARIO = 6490804782 # Segundo ID para logs
MINHA_CHAVE_PIX = "81985923844"
USUARIO_SUPORTE = "@LH_Oficial"

config = {
    "nome_item": "CONTAS GUEST LEVEL 15-20",
    "preco": 0.39,
    "dir_estoque": "estoque_contas",      
    "bonus_indicacao": 0.05
}

DB_USUARIOS = "usuarios.txt"
DB_VENDAS = "vendas_contas.txt"
DB_AFILIADOS = "afiliados.json"
DB_SALDOS = "saldos.json" 
# ============================================================

bot = telebot.TeleBot(TOKEN_TELEGRAM)
user_cart = {} 

# Inicialização de Pastas e Arquivos
for path in [config["dir_estoque"]]:
    if not os.path.exists(path): os.makedirs(path)

def iniciar_json(arquivo, default):
    if not os.path.exists(arquivo):
        with open(arquivo, "w") as f: json.dump(default, f)

iniciar_json(DB_AFILIADOS, {"relacoes": {}, "convidados": {}})
iniciar_json(DB_SALDOS, {})

# --- FUNÇÕES DE SEGURANÇA E SALDO ---

def enviar_seguro(chat_id, texto, markup=None):
    try:
        return bot.send_message(chat_id, texto, reply_markup=markup, parse_mode="Markdown")
    except: return None

def obter_saldo(user_id):
    try:
        with open(DB_SALDOS, "r") as f:
            saldos = json.load(f)
            return float(saldos.get(str(user_id), 0.0))
    except: return 0.0

def ajustar_saldo(user_id, valor):
    try:
        with open(DB_SALDOS, "r") as f: saldos = json.load(f)
        user_id_str = str(user_id)
        saldos[user_id_str] = round(float(saldos.get(user_id_str, 0.0)) + valor, 2)
        with open(DB_SALDOS, "w") as f: json.dump(saldos, f, indent=4)
        return True
    except: return False

def get_estoque():
    return [f for f in os.listdir(config["dir_estoque"]) if os.path.isfile(os.path.join(config["dir_estoque"], f))]

# --- MENUS PRINCIPAIS ---

def menu_principal(user_id):
    saldo = obter_saldo(user_id)
    estoque_qtd = len(get_estoque())
    
    msg = (f"╔══════════════════════╗\n"
           f"     👑  *LH STORE* 👑\n"
           f"╚══════════════════════╝\n\n"
           f"📦 *Produto:* `{config['nome_item']}`\n"
           f"💵 *Preço Unitário:* `R$ {config['preco']:.2f}`\n"
           f"🔥 *Estoque Disponível:* `{estoque_qtd}`\n\n"
           f"👤 *Seu ID:* `{user_id}`\n"
           f"💰 *Seu Saldo:* `R$ {saldo:.2f}`\n\n"
           f"👇 *Escolha uma opção abaixo:*")
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛒 Comprar Agora", callback_data="buy"),
        types.InlineKeyboardButton("💳 Recarregar", callback_data="recharge"),
        types.InlineKeyboardButton("👥 Afiliados", callback_data="affiliate"),
        types.InlineKeyboardButton("👨‍💻 Suporte", url=f"https://t.me/{USUARIO_SUPORTE.replace('@','')}")
    )
    return msg, markup

# --- HANDLERS DE COMANDO ---

@bot.message_handler(commands=['start', 'menu'])
def start(message):
    uid = message.from_user.id
    # Registro de novo usuário
    if not os.path.exists(DB_USUARIOS): open(DB_USUARIOS, "w").close()
    with open(DB_USUARIOS, "r+") as f:
        if str(uid) not in f.read():
            f.write(f"{uid}\n")
            # Lógica de indicação simples
            args = message.text.split()
            if len(args) > 1:
                indicador = args[1]
                if indicador != str(uid):
                    ajustar_saldo(indicador, config["bonus_indicacao"])
                    enviar_seguro(indicador, f"🎊 *Bônus!* Você recebeu R$ {config['bonus_indicacao']} por um novo convite!")

    msg, markup = menu_principal(uid)
    bot.send_message(message.chat.id, msg, reply_markup=markup, parse_mode="Markdown")

# --- CALLBACKS (BOTÕES) ---

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.from_user.id
    cid = call.message.chat.id
    mid = call.message.message_id

    if call.data == "voltar":
        msg, markup = menu_principal(uid)
        bot.edit_message_text(msg, cid, mid, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "recharge":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ Já enviei o comprovante", callback_data="confirm_pix"))
        markup.add(types.InlineKeyboardButton("⬅️ Voltar", callback_data="voltar"))
        
        texto_pix = (f"💳 *RECARGA VIA PIX*\n\n"
                     f"Para adicionar saldo, envie o valor desejado para a chave abaixo:\n\n"
                     f"🔑 *Chave Pix:* `{MINHA_CHAVE_PIX}`\n\n"
                     f"⚠️ *Após enviar, mande o COMPROVANTE (Foto/PDF) aqui no chat.*")
        bot.edit_message_text(texto_pix, cid, mid, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "affiliate":
        link = f"https://t.me/{bot.get_me().username}?start={uid}"
        texto = (f"👥 *SISTEMA DE AFILIADOS*\n\n"
                 f"Ganhe bônus por cada amigo que iniciar o bot pelo seu link!\n\n"
                 f"💰 *Recompensa:* `R$ {config['bonus_indicacao']:.2f}` por amigo.\n"
                 f"🔗 *Seu Link:* `{link}`")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ Voltar", callback_data="voltar"))
        bot.edit_message_text(texto, cid, mid, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "buy":
        estoque = get_estoque()
        if not estoque:
            bot.answer_callback_query(call.id, "❌ Estoque vazio no momento!", show_alert=True)
            return
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ Confirmar Compra", callback_data="confirm_buy"))
        markup.add(types.InlineKeyboardButton("⬅️ Voltar", callback_data="voltar"))
        
        bot.edit_message_text(f"🛒 *CONFIRMAÇÃO*\n\nItem: `{config['nome_item']}`\nValor: `R$ {config['preco']:.2f}`\n\nDeseja finalizar a compra?", cid, mid, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "confirm_buy":
        saldo = obter_saldo(uid)
        estoque = get_estoque()
        
        if saldo < config["preco"]:
            bot.answer_callback_query(call.id, "❌ Saldo insuficiente! Recarregue primeiro.", show_alert=True)
            return
        
        if not estoque:
            bot.answer_callback_query(call.id, "❌ Alguém acabou de comprar o último item!", show_alert=True)
            return

        # Processar Venda
        item_nome = estoque[0]
        caminho_item = os.path.join(config["dir_estoque"], item_nome)
        
        if ajustar_saldo(uid, -config["preco"]):
            with open(caminho_item, 'rb') as f:
                bot.send_document(cid, f, caption="✅ *COMPRA REALIZADA!*\nAqui está o seu produto. Obrigado pela preferência! 👑")
            
            # Remove do estoque
            os.remove(caminho_item)
            
            # Log para Admins
            log_msg = f"💰 *VENDA REALIZADA*\n👤 Cliente: `{uid}`\n📦 Item: `{item_nome}`"
            for adm in [ID_DONO, ID_SECUNDARIO]:
                try: bot.send_message(adm, log_msg, parse_mode="Markdown")
                except: pass
        else:
            bot.answer_callback_query(call.id, "❌ Erro ao processar pagamento.")

# --- RECEBIMENTO DE COMPROVANTES ---

@bot.message_handler(content_types=['photo', 'document'])
def handle_comprovante(message):
    uid = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else uid
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Aprovar R$ 1,00", callback_data=f"adm_add_{uid}_1"),
        types.InlineKeyboardButton("✅ Aprovar R$ 5,00", callback_data=f"adm_add_{uid}_5")
    )
    
    bot.reply_to(message, "⏳ *Comprovante enviado!* Nossa equipe vai analisar e o saldo cairá em instantes.")
    
    for adm in [ID_DONO, ID_SECUNDARIO]:
        try:
            info = f"📩 *NOVO COMPROVANTE*\n👤 Usuário: {username}\n🆔 ID: `{uid}`"
            if message.content_type == 'photo':
                bot.send_photo(adm, message.photo[-1].file_id, caption=info, reply_markup=markup, parse_mode="Markdown")
            else:
                bot.send_document(adm, message.document.file_id, caption=info, reply_markup=markup, parse_mode="Markdown")
        except: pass

@bot.callback_query_handler(func=lambda call: call.data.startswith("adm_add_"))
def admin_add_saldo(call):
    # adm_add_ID_VALOR
    partes = call.data.split("_")
    target_id = partes[2]
    valor = float(partes[3])
    
    if ajustar_saldo(target_id, valor):
        bot.answer_callback_query(call.id, f"✅ Saldo de R$ {valor} adicionado!")
        enviar_seguro(target_id, f"✅ *PAGAMENTO APROVADO!*\n\n`R$ {valor:.2f}` foram adicionados ao seu saldo.")
        bot.edit_message_caption(f"✅ Aprovado para {target_id} (R$ {valor})", call.message.chat.id, call.message.message_id)

# --- REPOSIÇÃO (APENAS ADM) ---

@bot.message_handler(commands=['addestoque'])
def add_estoque(message):
    if message.from_user.id != ID_DONO: return
    bot.reply_to(message, "📂 Envie o arquivo (.txt ou .zip) para adicionar ao estoque.")

@bot.message_handler(func=lambda m: m.from_user.id == ID_DONO, content_types=['document'])
def salvar_estoque(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    nome_final = os.path.join(config["dir_estoque"], message.document.file_name)
    
    with open(nome_final, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    bot.reply_to(message, f"📦 *Item adicionado!* Total no estoque: {len(get_estoque())}")

# ============================================================

if __name__ == "__main__":
    print("🤖 LH STORE iniciada com sucesso!")
    bot.infinity_polling()
