import telebot
from telebot import types
import os
import json
import uuid
import zipfile

# ================= CONFIGURAÇÕES (LH STORE) =================
TOKEN_TELEGRAM = "8705531112:AAF0dV9xHrf_4ihgvQuBlr9ED4D8BbqOoEs"
ID_DONO = 5658716257 
MINHA_CHAVE_PIX = "81985923844"
USUARIO_SUPORTE = "@LH_Oficial"

DB_USUARIOS = "usuarios.txt"
DB_BANIDOS = "banidos.txt"
DB_SALDOS = "saldos.json" 
DB_CONFIG = "config.json"

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
    return uid == ID_DONO

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

# --- PROCESSAMENTO DE ARQUIVOS ---

@bot.message_handler(content_types=['document', 'photo'])
def handle_media(message):
    uid = message.from_user.id
    if eh_banido(uid): return

    # SE O USUÁRIO COMUM MANDAR FOTO OU ARQUIVO (ACHANDO QUE É PRA MANDAR O COMPROVANTE AQUI)
    if not eh_admin(uid):
        bot.reply_to(message, f"⚠️ **ATENÇÃO!**\nOs comprovantes não devem ser enviados aqui no bot.\n\nPor favor, envie seu comprovante e o seu ID (`{uid}`) diretamente para o dono em {USUARIO_SUPORTE} para que seu saldo seja aprovado.")
        return

    # SE FOR O DONO MANDANDO ARQUIVOS DE ESTOQUE
    if message.content_type == 'document':
        nome_original = message.document.file_name
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        
        # 1. ARQUIVOS QUE COMEÇAM COM "GUEST"
        if nome_original.lower().startswith("guest"):
            id_u = uuid.uuid4().hex[:8]
            caminho_zip = os.path.join(config["dir_estoque"], f"conta_{id_u}.zip")
            with zipfile.ZipFile(caminho_zip, 'w') as zf:
                zf.writestr(nome_original, downloaded)
            bot.reply_to(message, f"✅ **Conta Adicionada!**\n📦 Arquivo `{nome_original}` foi empacotado e salvo no estoque.")
            return

        # 2. LISTAS EM TXT
        ext = os.path.splitext(nome_original)[1].lower()
        if ext == '.txt':
            linhas = downloaded.decode('utf-8', errors='ignore').splitlines()
            contas = 0
            for l in linhas:
                p = l.replace(':', ' ').replace(';', ' ').split()
                if len(p) >= 2:
                    id_zip = uuid.uuid4().hex[:8]
                    caminho = os.path.join(config["dir_estoque"], f"conta_{id_zip}.zip")
                    js = {"guest_account_info": {"com.garena.msdk.guest_uid": p[0], "com.garena.msdk.guest_password": p[1]}}
                    with zipfile.ZipFile(caminho, 'w') as zf:
                        zf.writestr("guest100067.dat", json.dumps(js))
                    contas += 1
            bot.reply_to(message, f"✅ `{contas}` contas separadas e importadas com sucesso!")

# --- MENUS ---

def menu_principal(user_id):
    estoque = [f for f in os.listdir(config["dir_estoque"]) if f.endswith('.zip')]
    saldo = obter_saldo(user_id)
    msg = (f"╔══════════════════════╗\n"
           f"     💎  **LH STORE** 💎\n"
           f"╚══════════════════════╝\n\n"
           f"🛒 **Produto:** `{config['nome_item']}`\n"
           f"🔥 **Estoque:** `{len(estoque)}` un.\n"
           f"💰 **Saldo:** `R$ {saldo:.2f}`\n"
           f"💵 **Preço:** `R$ {config['preco']:.2f}`")
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛒 Comprar", callback_data="buy"),
        types.InlineKeyboardButton("💳 Recarregar", callback_data="recharge_menu"),
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

# --- CALLBACKS ---

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
                bot.send_document(cid, f, caption="✅ **Compra realizada com sucesso!**\nAqui está a sua conta.")
            os.remove(os.path.join(config["dir_estoque"], item))
        else: bot.answer_callback_query(call.id, "❌ Erro.")

    elif call.data == "recharge_menu":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("R$ 1,00", callback_data="pix_1"),
            types.InlineKeyboardButton("R$ 3,00", callback_data="pix_3"),
            types.InlineKeyboardButton("R$ 5,00", callback_data="pix_5"),
            types.InlineKeyboardButton("R$ 10,00", callback_data="pix_10"),
            types.InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")
        )
        bot.edit_message_text("💳 **ESCOLHA O VALOR DA RECARGA**", cid, mid, reply_markup=markup)

    elif call.data.startswith("pix_"):
        valor_pix = call.data.split("_")[1]
        msg_pix = (f"💳 **PAGAMENTO PIX**\n\n"
                   f"Valor da Recarga: **R$ {valor_pix},00**\n\n"
                   f"🔑 Chave PIX: `{MINHA_CHAVE_PIX}`\n\n"
                   f"⚠️ **MUITO IMPORTANTE:**\n"
                   f"Após o pagamento, envie a foto do comprovante para o dono em {USUARIO_SUPORTE} junto com o seu ID para liberação.\n"
                   f"🆔 **Seu ID:** `{uid}`")
        
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("⬅️ Voltar", callback_data="recharge_menu"))
        bot.edit_message_text(msg_pix, cid, mid, parse_mode="Markdown", reply_markup=markup)

    # --- ÁREA GESTOR ---
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
        bot.edit_message_text("🛠️ **PAINEL DE GESTÃO LH**\n\n*Abasteça o estoque enviando arquivos que comecem com 'guest' ou listas .txt.*", cid, mid, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "adm_add_saldo":
        m = bot.send_message(cid, "💰 Digite: `ID VALOR` (Ex: `5658716257 5.00`):")
        bot.register_next_step_handler(m, processar_add_saldo)

    elif call.data == "adm_set_price":
        m = bot.send_message(cid, "🏷️ Digite o novo preço (Ex: `0.40`):")
        bot.register_next_step_handler(m, processar_set_price)

    elif call.data == "adm_clear":
        for f in os.listdir(config["dir_estoque"]): os.remove(os.path.join(config["dir_estoque"], f))
        bot.answer_callback_query(call.id, "💣 Estoque zerado!", show_alert=True)
        calls(types.CallbackQuery(id=call.id, from_user=call.from_user, chat_instance=None, message=call.message, data="adm_painel"))

    elif call.data == "adm_ban":
        m = bot.send_message(cid, "🚫 Mande o ID para banir:")
        bot.register_next_step_handler(m, lambda msg: [open(DB_BANIDOS, "a").write(f"{msg.text}\n"), bot.send_message(cid, "✅ Banido com sucesso!")])

# --- STEPS (ADMINISTRATIVO) ---

def processar_add_saldo(message):
    try:
        p = message.text.split()
        if ajustar_saldo(p[0], float(p[1])):
            bot.reply_to(message, f"✅ R$ {p[1]} adicionados ao ID `{p[0]}`")
            try: bot.send_message(p[0], f"✅ **SALDO APROVADO!**\nO administrador adicionou **R$ {p[1]}** à sua conta.")
            except: pass
    except: bot.reply_to(message, "❌ Erro! Use: `ID VALOR`")

def processar_set_price(message):
    try:
        np = float(message.text.replace(',', '.'))
        config["preco"] = np
        salvar_config(config)
        bot.reply_to(message, f"✅ Preço atualizado: **R$ {np:.2f}**")
    except: bot.reply_to(message, "❌ Valor inválido.")

if __name__ == "__main__":
    print("🚀 LH STORE ONLINE - RECEBIMENTO DIRETO ATIVO!")
    bot.infinity_polling()
