import telebot
from telebot import types
import time
import os
import json
import uuid
import zipfile

# ================= CONFIGURAÇÕES (LH STORE) =================
# [span_2](start_span)IDs e Informações baseadas no seu perfil de administrador[span_2](end_span)
TOKEN_TELEGRAM = "8705531112:AAF0dV9xHrf_4ihgvQuBlr9ED4D8BbqOoEs"
ID_DONO = 5658716257 
ID_SECUNDARIO = 6490804782
MINHA_CHAVE_PIX = "81985923844"
USUARIO_SUPORTE = "@LH_Oficial"

config = {
    "nome_item": "CONTAS GUEST LVL 15-20",
    "preco": 0.39,
    "dir_estoque": "estoque_contas",      
    "bonus_indicacao": 0.05
}

DB_USUARIOS = "usuarios.txt"
DB_BANIDOS = "banidos.txt"
DB_SALDOS = "saldos.json" 
# ============================================================

bot = telebot.TeleBot(TOKEN_TELEGRAM)

# --- INICIALIZAÇÃO DE PASTAS E ARQUIVOS ---
if not os.path.exists(config["dir_estoque"]): 
    os.makedirs(config["dir_estoque"])

def iniciar_bancos():
    if not os.path.exists(DB_BANIDOS): open(DB_BANIDOS, "w").close()
    if not os.path.exists(DB_USUARIOS): open(DB_USUARIOS, "w").close()
    if not os.path.exists(DB_SALDOS):
        with open(DB_SALDOS, "w") as f: json.dump({}, f)

iniciar_bancos()

# --- FUNÇÕES DE SEGURANÇA E ADMINISTRAÇÃO ---

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

# --- GERADOR DE CONTA GARENA (.DAT DENTRO DE .ZIP) ---

def criar_pacote_garena(uid_conta, senha_conta):
    """Gera o guest100067.dat e salva em um .zip no estoque"""
    id_referencia = uuid.uuid4().hex[:6]
    nome_dat = "guest100067.dat"
    nome_zip = f"conta_{id_referencia}.zip"
    caminho_final = os.path.join(config["dir_estoque"], nome_zip)

    # JSON específico conforme solicitado para o jogo
    json_garena = {
        "guest_account_info": {
            "com.garena.msdk.guest_uid": str(uid_conta),
            "com.garena.msdk.guest_password": str(senha_conta)
        }
    }

    with zipfile.ZipFile(caminho_final, 'w') as zf:
        zf.writestr(nome_dat, json.dumps(json_garena))
    
    return nome_zip

# --- MENUS VISUAIS ---

def menu_principal(user_id):
    estoque = [f for f in os.listdir(config["dir_estoque"]) if f.endswith('.zip') or f.endswith('.txt')]
    saldo = obter_saldo(user_id)
    
    msg = (f"╔══════════════════════╗\n"
           f"     👑  **LH STORE** 👑\n"
           f"╚══════════════════════╝\n\n"
           f"📦 **Produto:** `{config['nome_item']}`\n"
           f"🔥 **Estoque:** `{len(estoque)}` unidades\n"
           f"💰 **Seu Saldo:** `R$ {saldo:.2f}`\n\n"
           f"👇 **Selecione uma opção abaixo:**")
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛒 Comprar", callback_data="buy"),
        types.InlineKeyboardButton("💳 Recarregar", callback_data="recharge"),
        types.InlineKeyboardButton("👨‍💻 Suporte", url=f"https://t.me/{USUARIO_SUPORTE.replace('@','')}")
    )
    if eh_admin(user_id):
        markup.add(types.InlineKeyboardButton("⚙️ Painel Admin", callback_data="adm_painel"))
    return msg, markup

# --- COMANDOS E FILTROS ---

@bot.message_handler(func=lambda m: eh_banido(m.from_user.id))
def block_ban(message):
    return # Ignora usuários banidos

@bot.message_handler(commands=['start', 'menu'])
def cmd_start(message):
    uid = message.from_user.id
    with open(DB_USUARIOS, "r+") as f:
        if str(uid) not in f.read(): f.write(f"{uid}\n")
    
    msg, markup = menu_principal(uid)
    bot.send_message(message.chat.id, msg, reply_markup=markup, parse_mode="Markdown")

# --- PAINEL ADMIN ---

@bot.callback_query_handler(func=lambda call: call.data == "adm_painel")
def painel_admin(call):
    if not eh_admin(call.from_user.id): return
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("➕ Add Conta (UID SENHA)", callback_data="adm_add_manual"),
        types.InlineKeyboardButton("🚫 Banir Usuário", callback_data="adm_prompt_ban"),
        types.InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")
    )
    bot.edit_message_text("⚙️ **PAINEL ADMINISTRATIVO**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

# --- LÓGICA DE DOCUMENTOS (REPOSIÇÃO VS COMPROVANTE) ---

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    uid = message.from_user.id
    ext = os.path.splitext(message.document.file_name)[1].lower()

    # Se for ADMIN adicionando ao estoque
    if eh_admin(uid):
        if ext in ['.txt', '.zip']:
            file_info = bot.get_file(message.document.file_id)
            down = bot.download_file(file_info.file_path)
            caminho = os.path.join(config["dir_estoque"], message.document.file_name)
            with open(caminho, 'wb') as f: f.write(down)
            bot.reply_to(message, f"✅ **Estoque Atualizado:** `{message.document.file_name}`")
        else:
            bot.reply_to(message, "❌ **Erro:** Só aceito `.txt` ou `.zip` para o estoque.")
    
    # Se for USUÁRIO mandando comprovante
    else:
        bot.reply_to(message, "⏳ **Comprovante recebido!** Aguarde o ADM aprovar.")
        for adm in [ID_DONO, ID_SECUNDARIO]:
            markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("✅ Aprovar R$ 1", callback_data=f"apr_{uid}_1"))
            bot.send_document(adm, message.document.file_id, caption=f"📩 **RECIBO** de `{uid}`", reply_markup=markup)

# --- PROCESSAMENTO DE PASSOS (STEP HANDLERS) ---

def processar_manual(message):
    try:
        dados = message.text.split()
        if len(dados) != 2: raise ValueError
        uid_c, pwd_c = dados[0], dados[1]
        nome = criar_pacote_garena(uid_c, pwd_c)
        bot.send_message(message.chat.id, f"✅ **Conta Zipada com Sucesso:** `{nome}`")
    except:
        bot.send_message(message.chat.id, "❌ Use o formato: `UID SENHA` (separado por espaço)")

def processar_ban(message):
    target = message.text.strip()
    with open(DB_BANIDOS, "a") as f: f.write(f"{target}\n")
    bot.send_message(message.chat.id, f"🚫 Usuário `{target}` foi banido da LH STORE.")

# --- CALLBACKS GERAIS ---

@bot.callback_query_handler(func=lambda call: True)
def calls(call):
    uid, cid, mid = call.from_user.id, call.message.chat.id, call.message.message_id
    
    if call.data == "voltar":
        msg, markup = menu_principal(uid)
        bot.edit_message_text(msg, cid, mid, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "buy":
        estoque = [f for f in os.listdir(config["dir_estoque"]) if f.endswith('.zip') or f.endswith('.txt')]
        if not estoque:
            bot.answer_callback_query(call.id, "❌ Estoque vazio!", show_alert=True)
            return
        if obter_saldo(uid) < config["preco"]:
            bot.answer_callback_query(call.id, "❌ Saldo insuficiente!", show_alert=True)
            return
        
        item = estoque[0]
        caminho = os.path.join(config["dir_estoque"], item)
        if ajustar_saldo(uid, -config["preco"]):
            with open(caminho, 'rb') as f:
                bot.send_document(cid, f, caption="✅ **Entrega automática LH STORE!**")
            os.remove(caminho)
        else: bot.answer_callback_query(call.id, "❌ Erro no processamento.")

    elif call.data == "recharge":
        bot.edit_message_text(f"💳 **RECARGA PIX**\n\nChave: `{MINHA_CHAVE_PIX}`\n\nEnvie o comprovante abaixo.", cid, mid, parse_mode="Markdown")

    elif call.data == "adm_add_manual":
        msg = bot.send_message(cid, "⌨️ Digite o **UID** e a **SENHA** (ex: `4337695213 SENHA123`):")
        bot.register_next_step_handler(msg, processar_manual)

    elif call.data == "adm_prompt_ban":
        msg = bot.send_message(cid, "🚫 Digite o **ID** do usuário para banir:")
        bot.register_next_step_handler(msg, processar_ban)

    elif call.data.startswith("apr_"):
        _, tid, v = call.data.split("_")
        ajustar_saldo(tid, float(v))
        bot.send_message(tid, f"✅ **Saldo Aprovado!** R$ {v} foram adicionados.")
        bot.edit_message_caption(f"✅ Aprovado para {tid}", cid, mid)

if __name__ == "__main__":
    print("🚀 LH STORE RODANDO...")
    bot.infinity_polling()
