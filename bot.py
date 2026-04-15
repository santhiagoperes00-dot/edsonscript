import telebot
from telebot import types
import time
import os
import json
import uuid
import zipfile

# ================= CONFIGURAÇÕES (LH STORE) =================
TOKEN_TELEGRAM = "8705531112:AAF0dV9xHrf_4ihgvQuBlr9ED4D8BbqOoEs"
[span_1](start_span)ID_DONO = 5658716257 #[span_1](end_span)
[span_2](start_span)ID_SECUNDARIO = 6490804782 #[span_2](end_span)
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
if not os.path.exists(config["dir_estoque"]): os.makedirs(config["dir_estoque"])
if not os.path.exists(DB_BANIDOS): open(DB_BANIDOS, "w").close()

def iniciar_json(arquivo, default):
    if not os.path.exists(arquivo):
        with open(arquivo, "w") as f: json.dump(default, f)

iniciar_json(DB_SALDOS, {})

# --- FUNÇÕES DE SEGURANÇA ---

def eh_admin(uid):
    return uid == ID_DONO or uid == ID_SECUNDARIO

def eh_banido(uid):
    with open(DB_BANIDOS, "r") as f:
        return str(uid) in f.read().splitlines()

def obter_saldo(user_id):
    try:
        with open(DB_SALDOS, "r") as f:
            saldos = json.load(f)
            return float(saldos.get(str(user_id), 0.0))
    except: return 0.0

def ajustar_saldo(user_id, valor):
    try:
        with open(DB_SALDOS, "r") as f: saldos = json.load(f)
        u_str = str(user_id)
        saldos[u_str] = round(float(saldos.get(u_str, 0.0)) + valor, 2)
        with open(DB_SALDOS, "w") as f: json.dump(saldos, f, indent=4)
        return True
    except: return False

def get_estoque():
    return [f for f in os.listdir(config["dir_estoque"]) if f.endswith('.zip') or f.endswith('.txt')]

# --- GERAÇÃO DE CONTA GARENA (.DAT -> .ZIP) ---

def criar_pacote_conta(uid_conta, senha_conta):
    id_unico = uuid.uuid4().hex[:6]
    nome_dat = "guest100067.dat" # Nome exigido pelo jogo
    nome_zip = f"conta_{id_unico}.zip"
    caminho_zip = os.path.join(config["dir_estoque"], nome_zip)

    # JSON fornecido por Pato Gerador
    dados_conta = {
        "guest_account_info": {
            "com.garena.msdk.guest_uid": str(uid_conta),
            "com.garena.msdk.guest_password": str(senha_conta)
        }
    }

    with zipfile.ZipFile(caminho_zip, 'w') as zf:
        zf.writestr(nome_dat, json.dumps(dados_conta))
    
    return nome_zip

# --- PAINEL ADMIN ---

@bot.callback_query_handler(func=lambda call: call.data == "adm_painel")
def painel_admin(call):
    if not eh_admin(call.from_user.id): return
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("➕ Add Conta (UID:Pass)", callback_data="adm_add_manual"),
        types.InlineKeyboardButton("📁 Subir Arquivo (.TXT/.ZIP)", callback_data="adm_instrucao_file"),
        types.InlineKeyboardButton("🚫 Banir Usuário", callback_data="adm_ban"),
        types.InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")
    )
    bot.edit_message_text("⚙️ **PAINEL ADMINISTRATIVO**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

# --- HANDLER DE ARQUIVOS (ADD CONTA) ---

@bot.message_handler(content_types=['document'])
def handle_admin_files(message):
    uid = message.from_user.id
    
    # Se NÃO for admin, trata como comprovante de pagamento
    if not eh_admin(uid):
        for adm in [ID_DONO, ID_SECUNDARIO]:
            markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("✅ Aprovar R$ 1", callback_data=f"apr_{uid}_1"))
            bot.send_document(adm, message.document.file_id, caption=f"📩 **RECIBO** de `{uid}`", reply_markup=markup, parse_mode="Markdown")
        bot.reply_to(message, "⏳ **Comprovante enviado!** Aguarde a aprovação.")
        return

    # Se FOR admin, valida a extensão para o estoque
    extensoes_permitidas = ['.txt', '.zip']
    nome_arquivo = message.document.file_name.lower()
    
    if any(nome_arquivo.endswith(ext) for ext in extensoes_permitidas):
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            caminho_final = os.path.join(config["dir_estoque"], message.document.file_name)
            with open(caminho_final, 'wb') as f:
                f.write(downloaded_file)
            
            bot.reply_to(message, f"✅ **ARQUIVO ACEITO!**\n📦 `{message.document.file_name}` foi adicionado ao estoque.")
        except Exception as e:
            bot.reply_to(message, f"❌ Erro ao salvar arquivo: {e}")
    else:
        bot.reply_to(message, "⚠️ **FORMATO INVÁLIDO!**\nPara o estoque, eu só aceito arquivos **.TXT** ou **.ZIP**.")

# --- COMANDOS E CALLBACKS RESTANTES ---

@bot.message_handler(commands=['start', 'menu'])
def start(message):
    if eh_banido(message.from_user.id): return
    saldo = obter_saldo(message.from_user.id)
    estoque_qtd = len(get_estoque())
    
    msg = (f"╔══════════════════════╗\n"
           f"     👑  **LH STORE** 👑\n"
           f"╚══════════════════════╝\n\n"
           f"🔥 **Estoque:** `{estoque_qtd}` unidades\n"
           f"💰 **Seu Saldo:** `R$ {saldo:.2f}`\n\n"
           f"🛒 Item: `{config['nome_item']}`\n"
           f"💵 Preço: `R$ {config['preco']:.2f}`")
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛒 Comprar", callback_data="buy"),
        types.InlineKeyboardButton("💳 Recarregar", callback_data="recharge"),
        types.InlineKeyboardButton("👨‍💻 Suporte", url=f"https://t.me/{USUARIO_SUPORTE.replace('@','')}")
    )
    if eh_admin(message.from_user.id):
        markup.add(types.InlineKeyboardButton("⚙️ Painel Admin", callback_data="adm_painel"))
    
    bot.send_message(message.chat.id, msg, reply_markup=markup, parse_mode="Markdown")

# [Restante da lógica de compra e banimento mantida conforme solicitado anteriormente...]

if __name__ == "__main__":
    print("🤖 LH STORE Online e Protegida!")
    bot.infinity_polling()
