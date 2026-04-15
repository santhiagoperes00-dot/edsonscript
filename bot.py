import telebot
from telebot import types
import time
import os
import json
import uuid
import zipfile
import io

# ================= CONFIGURAÇÕES (LH STORE) =================
TOKEN_TELEGRAM = "8705531112:AAF0dV9xHrf_4ihgvQuBlr9ED4D8BbqOoEs"
ID_DONO = 8308508544 
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

# --- INICIALIZAÇÃO ---
if not os.path.exists(config["dir_estoque"]): 
    os.makedirs(config["dir_estoque"])

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
    """Cria o .dat e zips para o estoque"""
    nome_zip = f"conta_{uuid.uuid4().hex[:8]}.zip"
    caminho = os.path.join(config["dir_estoque"], nome_zip)
    conteudo_dat = {
        "guest_account_info": {
            "com.garena.msdk.guest_uid": str(uid_c),
            "com.garena.msdk.guest_password": str(pwd_c)
        }
    }
    with zipfile.ZipFile(caminho, 'w') as zf:
        zf.writestr("guest100067.dat", json.dumps(conteudo_dat))
    return nome_zip

# --- PROCESSAMENTO DE ARQUIVOS EM MASSA ---

@bot.message_handler(content_types=['document'])
def handle_bulk_upload(message):
    uid = message.from_user.id
    if eh_banido(uid): return

    # SE FOR ADMIN: Processa contas para o estoque
    if eh_admin(uid):
        ext = os.path.splitext(message.document.file_name)[1].lower()
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        contas_add = 0

        # Caso 1: Arquivo TXT com várias linhas (UID SENHA)
        if ext == '.txt':
            linhas = downloaded_file.decode('utf-8').splitlines()
            for linha in linhas:
                partes = linha.replace(':', ' ').split()
                if len(partes) >= 2:
                    criar_pacote_garena(partes[0], partes[1])
                    contas_add += 1
            bot.reply_to(message, f"✅ **Processamento Concluído!**\n📦 `{contas_add}` contas individuais foram criadas no estoque.")

        # Caso 2: Arquivo ZIP (Extrai e processa TXTs dentro dele)
        elif ext == '.zip':
            with zipfile.ZipFile(io.BytesIO(downloaded_file)) as z:
                for filename in z.namelist():
                    if filename.endswith('.txt'):
                        with z.open(filename) as f:
                            linhas = f.read().decode('utf-8').splitlines()
                            for linha in linhas:
                                partes = linha.replace(':', ' ').split()
                                if len(partes) >= 2:
                                    criar_pacote_garena(partes[0], partes[1])
                                    contas_add += 1
            bot.reply_to(message, f"📦 **Extração Completa!**\nForam geradas `{contas_add}` contas a partir do ZIP.")
        else:
            bot.reply_to(message, "❌ Envie apenas `.txt` ou `.zip` contendo listas de contas.")

    # SE FOR USUÁRIO: Envia para o ADM como comprovante
    else:
        bot.reply_to(message, "⏳ **Comprovante enviado!** Aguarde a verificação do ADM.")
        for adm in [ID_DONO, ID_SECUNDARIO]:
            markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("✅ Aprovar R$ 1", callback_data=f"apr_{uid}_1"))
            bot.send_document(adm, message.document.file_id, caption=f"📩 **RECIBO** de `{uid}`", reply_markup=markup)

# --- MENUS E COMANDOS ---

def menu_principal(user_id):
    estoque = [f for f in os.listdir(config["dir_estoque"]) if f.endswith('.zip')]
    saldo = obter_saldo(user_id)
    msg = (f"╔══════════════════════╗\n"
           f"     👑  **LH STORE** 👑\n"
           f"╚══════════════════════╝\n\n"
           f"🔥 **Estoque:** `{len(estoque)}` unidades\n"
           f"💰 **Seu Saldo:** `R$ {saldo:.2f}`\n\n"
           f"🛒 Item: `{config['nome_item']}`\n"
           f"💵 Valor: `R$ {config['preco']:.2f}`")
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛒 Comprar", callback_data="buy"),
        types.InlineKeyboardButton("💳 Recarregar", callback_data="recharge"),
        types.InlineKeyboardButton("👨‍💻 Suporte", url=f"https://t.me/{USUARIO_SUPORTE.replace('@','')}")
    )
    if eh_admin(user_id):
        markup.add(types.InlineKeyboardButton("⚙️ Painel Admin", callback_data="adm_painel"))
    return msg, markup

@bot.message_handler(commands=['start', 'menu'])
def cmd_start(message):
    if eh_banido(message.from_user.id): return
    msg, markup = menu_principal(message.from_user.id)
    bot.send_message(message.chat.id, msg, reply_markup=markup, parse_mode="Markdown")

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
            bot.answer_callback_query(call.id, "❌ Estoque vazio!", show_alert=True)
            return
        if obter_saldo(uid) < config["preco"]:
            bot.answer_callback_query(call.id, "❌ Saldo insuficiente!", show_alert=True)
            return
        
        item = estoque[0]
        caminho = os.path.join(config["dir_estoque"], item)
        if ajustar_saldo(uid, -config["preco"]):
            with open(caminho, 'rb') as f:
                bot.send_document(cid, f, caption="✅ **Sua conta chegou!**\nUse com sabedoria. 👑")
            os.remove(caminho)
        else:
            bot.answer_callback_query(call.id, "❌ Erro técnico.")

    elif call.data == "adm_painel":
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("🚫 Banir ID", callback_data="adm_ban"),
            types.InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")
        )
        bot.edit_message_text("⚙️ **ADMIN:** Envie um arquivo `.txt` com várias contas (UID SENHA) para abastecer tudo de uma vez.", cid, mid, reply_markup=markup)

    elif call.data == "adm_ban":
        msg = bot.send_message(cid, "🚫 Digite o **ID** do usuário para banir:")
        bot.register_next_step_handler(msg, lambda m: [open(DB_BANIDOS, "a").write(f"{m.text}\n"), bot.send_message(cid, "✅ Banido!")])

    elif call.data.startswith("apr_"):
        _, target_id, valor = call.data.split("_")
        ajustar_saldo(target_id, float(valor))
        bot.send_message(target_id, f"✅ **R$ {valor} adicionados ao seu saldo!**")
        bot.edit_message_caption(f"✅ Aprovado para {target_id}", cid, mid)

if __name__ == "__main__":
    print("🚀 LH STORE PRONTA PARA VENDAS EM MASSA!")
    bot.infinity_polling()
