import telebot
from telebot import types
import os
import json
import uuid
import zipfile
import io

# ================= CONFIGURAÇÕES (LH STORE) =================
TOKEN_TELEGRAM = "8705531112:AAF0dV9xHrf_4ihgvQuBlr9ED4D8BbqOoEs"
ID_DONO = 5658716257 
ID_SECUNDARIO = 6490804782
MINHA_CHAVE_PIX = "81985923844"
USUARIO_SUPORTE = "@LH_Oficial"

# Arquivos de Banco de Dados
DB_USUARIOS = "usuarios.txt"
DB_BANIDOS = "banidos.txt"
DB_SALDOS = "saldos.json" 
DB_CONFIG = "config.json"

# Carregar ou Iniciar Configurações (Preço e Nome)
def carregar_config():
    if os.path.exists(DB_CONFIG):
        with open(DB_CONFIG, "r") as f: return json.load(f)
    return {
        "nome_item": "CONTAS GUEST LVL 15-20",
        "preco": 0.39,
        "dir_estoque": "estoque_contas"
    }

def salvar_config(nova_config):
    with open(DB_CONFIG, "w") as f: json.dump(nova_config, f, indent=4)

config = carregar_config()
bot = telebot.TeleBot(TOKEN_TELEGRAM)

# --- INICIALIZAÇÃO ---
if not os.path.exists(config["dir_estoque"]): os.makedirs(config["dir_estoque"])

def iniciar_bancos():
    if not os.path.exists(DB_BANIDOS): open(DB_BANIDOS, "w").close()
    if not os.path.exists(DB_USUARIOS): open(DB_USUARIOS, "w").close()
    if not os.path.exists(DB_SALDOS):
        with open(DB_SALDOS, "w") as f: json.dump({}, f)

iniciar_bancos()

# --- FUNÇÕES CORE ---

def eh_admin(uid):
    return uid == ID_DONO or uid == ID_SECUNDARIO

def eh_banido(uid):
    with open(DB_BANIDOS, "r") as f:
        return str(uid) in f.read().splitlines()

def ajustar_saldo(user_id, valor):
    try:
        with open(DB_SALDOS, "r") as f: saldos = json.load(f)
        u_str = str(user_id)
        saldos[u_str] = round(float(saldos.get(u_str, 0.0)) + valor, 2)
        with open(DB_SALDOS, "w") as f: json.dump(saldos, f, indent=4)
        return True
    except: return False

def obter_saldo(user_id):
    try:
        with open(DB_SALDOS, "r") as f:
            saldos = json.load(f)
            return float(saldos.get(str(user_id), 0.0))
    except: return 0.0

def criar_pacote_garena(uid_c, pwd_c):
    nome_zip = f"conta_{uuid.uuid4().hex[:8]}.zip"
    caminho = os.path.join(config["dir_estoque"], nome_zip)
    conteudo_dat = {
        "guest_account_info": {
            "com.garena.msdk.guest_uid": str(uid_c).strip(),
            "com.garena.msdk.guest_password": str(pwd_c).strip()
        }
    }
    with zipfile.ZipFile(caminho, 'w') as zf:
        zf.writestr("guest100067.dat", json.dumps(conteudo_dat))
    return nome_zip

# --- PROCESSAMENTO DE ARQUIVOS (TXT/ZIP) ---

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    uid = message.from_user.id
    if eh_banido(uid): return
    if eh_admin(uid):
        ext = os.path.splitext(message.document.file_name)[1].lower()
        if ext not in ['.txt', '.zip']: return
        
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        contas = 0
        
        if ext == '.txt':
            linhas = downloaded.decode('utf-8', errors='ignore').splitlines()
            for l in linhas:
                p = l.replace(':', ' ').replace(';', ' ').split()
                if len(p) >= 2:
                    criar_pacote_garena(p[0], p[1])
                    contas += 1
        elif ext == '.zip':
            with zipfile.ZipFile(io.BytesIO(downloaded)) as z:
                for f_name in z.namelist():
                    if f_name.endswith('.txt'):
                        linhas = z.read(f_name).decode('utf-8', errors='ignore').splitlines()
                        for l in linhas:
                            p = l.replace(':', ' ').replace(';', ' ').split()
                            if len(p) >= 2:
                                criar_pacote_garena(p[0], p[1])
                                contas += 1
        bot.reply_to(message, f"✅ Adicionadas `{contas}` contas individuais.")
    else:
        for adm in [ID_DONO, ID_SECUNDARIO]:
            m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("✅ Aprovar R$ 1", callback_data=f"apr_{uid}_1"))
            bot.send_document(adm, message.document.file_id, caption=f"📩 Recibo de `{uid}`", reply_markup=m)

# --- MENUS ---

def menu_principal(user_id):
    estoque = [f for f in os.listdir(config["dir_estoque"]) if f.endswith('.zip')]
    saldo = obter_saldo(user_id)
    msg = (f"╔══════════════════════╗\n"
           f"     💎  **LH STORE** 💎\n"
           f"╚══════════════════════╝\n\n"
           f"🛒 **Produto:** `{config['nome_item']}`\n"
           f"🔥 **Em Estoque:** `{len(estoque)}` un.\n"
           f"💰 **Saldo:** `R$ {saldo:.2f}`\n"
           f"💵 **Preço:** `R$ {config['preco']:.2f}`")
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛒 Comprar", callback_data="buy"),
        types.InlineKeyboardButton("💳 Recarregar", callback_data="recharge"),
        types.InlineKeyboardButton("👨‍💻 Suporte", url=f"https://t.me/{USUARIO_SUPORTE.replace('@','')}")
    )
    if eh_admin(user_id):
        markup.add(types.InlineKeyboardButton("⚙️ Painel Gestor", callback_data="adm_painel"))
    return msg, markup

@bot.message_handler(commands=['start', 'menu'])
def cmd_start(message):
    if eh_banido(message.from_user.id): return
    msg, markup = menu_principal(message.from_user.id)
    bot.send_message(message.chat.id, msg, reply_markup=markup, parse_mode="Markdown")

# --- CALLBACKS E NOVAS FUNÇÕES ADMIN ---

@bot.callback_query_handler(func=lambda call: True)
def calls(call):
    uid, cid, mid = call.from_user.id, call.message.chat.id, call.message.message_id
    if eh_banido(uid): return

    if call.data == "voltar":
        msg, markup = menu_principal(uid)
        bot.edit_message_text(msg, cid, mid, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "buy":
        estoque = [f for f in os.listdir(config["dir_estoque"]) if f.endswith('.zip')]
        if not estoque:
            bot.answer_callback_query(call.id, "❌ Sem estoque!", show_alert=True)
            return
        if obter_saldo(uid) < config["preco"]:
            bot.answer_callback_query(call.id, "❌ Saldo insuficiente!", show_alert=True)
            return
        
        item = estoque[0]
        if ajustar_saldo(uid, -config["preco"]):
            with open(os.path.join(config["dir_estoque"], item), 'rb') as f:
                bot.send_document(cid, f, caption="✅ Entrega concluída!")
            os.remove(os.path.join(config["dir_estoque"], item))
        else: bot.answer_callback_query(call.id, "❌ Erro.")

    elif call.data == "recharge":
        bot.edit_message_text(f"💳 PIX: `{MINHA_CHAVE_PIX}`\nEnvie o comprovante.", cid, mid, parse_mode="Markdown")

    # --- NOVO PAINEL ADMIN ---
    elif call.data == "adm_painel":
        if not eh_admin(uid): return
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("💰 Add Saldo", callback_data="adm_add_saldo"),
            types.InlineKeyboardButton("🏷️ Mudar Preço", callback_data="adm_set_price"),
            types.InlineKeyboardButton("🗑️ Limpar Estoque", callback_data="adm_clear"),
            types.InlineKeyboardButton("🚫 Banir ID", callback_data="adm_ban"),
            types.InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")
        )
        bot.edit_message_text("🛠️ **GESTÃO LH STORE**", cid, mid, reply_markup=markup)

    elif call.data == "adm_add_saldo":
        m = bot.send_message(cid, "💰 Digite o **ID** e o **VALOR** (ex: `5658716257 10.50`):")
        bot.register_next_step_handler(m, processar_add_saldo)

    elif call.data == "adm_set_price":
        m = bot.send_message(cid, "🏷️ Digite o **novo preço** (ex: `0.50`):")
        bot.register_next_step_handler(m, processar_set_price)

    elif call.data == "adm_clear":
        for f in os.listdir(config["dir_estoque"]): os.remove(os.path.join(config["dir_estoque"], f))
        bot.answer_callback_query(call.id, "💣 Estoque limpo!", show_alert=True)
        calls(types.CallbackQuery(id=call.id, from_user=call.from_user, chat_instance=None, message=call.message, data="adm_painel"))

    elif call.data == "adm_ban":
        m = bot.send_message(cid, "🚫 ID para banir:")
        bot.register_next_step_handler(m, lambda msg: [open(DB_BANIDOS, "a").write(f"{msg.text}\n"), bot.send_message(cid, "✅ Banido!")])

    elif call.data.startswith("apr_"):
        _, target, val = call.data.split("_")
        ajustar_saldo(target, float(val))
        bot.send_message(target, f"✅ R$ {val} adicionados!")
        bot.edit_message_caption(f"✅ Aprovado para {target}", cid, mid)

# --- PROCESSADORES DE ETAPA (STEP HANDLERS) ---

def processar_add_saldo(message):
    try:
        partes = message.text.split()
        target_id, valor = partes[0], float(partes[1])
        if ajustar_saldo(target_id, valor):
            bot.reply_to(message, f"✅ Adicionado R$ {valor} ao ID `{target_id}`")
            bot.send_message(target_id, f"💰 **LH STORE:** O administrador adicionou R$ {valor} ao seu saldo!")
        else: raise Exception
    except:
        bot.reply_to(message, "❌ Erro! Use o formato: `ID VALOR` (ex: `12345678 5.00`) ")

def processar_set_price(message):
    try:
        novo_preco = float(message.text.replace(',', '.'))
        config["preco"] = novo_preco
        salvar_config(config)
        bot.reply_to(message, f"✅ Preço das contas alterado para: **R$ {novo_preco:.2f}**")
    except:
        bot.reply_to(message, "❌ Erro! Digite apenas o número (ex: `0.45`) ")

if __name__ == "__main__":
    print("🤖 LH STORE — GESTÃO COMPLETA ATIVA!")
    bot.infinity_polling()
