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

if not os.path.exists(config["dir_estoque"]): 
    os.makedirs(config["dir_estoque"])

def iniciar_bancos():
    if not os.path.exists(DB_BANIDOS): open(DB_BANIDOS, "w").close()
    if not os.path.exists(DB_SALDOS):
        with open(DB_SALDOS, "w") as f: json.dump({}, f)

iniciar_bancos()

# --- FUNÇÕES CORE ---

def eh_admin(uid):
    return str(uid) == str(ID_DONO)

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

# --- MEDIA HANDLER ---

@bot.message_handler(content_types=['document', 'photo'])
def handle_media(message):
    uid = message.from_user.id
    if eh_banido(uid): return

    if not eh_admin(uid):
        bot.reply_to(message, f"<b>⚠️ AVISO:</b> Envie comprovantes para {USUARIO_SUPORTE} com seu ID: <code>{uid}</code>", parse_mode="HTML")
        return

    if message.content_type == 'document':
        nome = message.document.file_name
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        
        if nome.lower().startswith("guest"):
            id_u = uuid.uuid4().hex[:6]
            path = os.path.join(config["dir_estoque"], f"conta_{id_u}.zip")
            with zipfile.ZipFile(path, 'w') as zf:
                zf.writestr(nome, downloaded)
            bot.reply_to(message, f"✅ <b>CONTA GUEST ADD:</b> {nome}", parse_mode="HTML")
            return

        if nome.endswith('.txt'):
            linhas = downloaded.decode('utf-8', errors='ignore').splitlines()
            c = 0
            for l in linhas:
                p = l.replace(':', ' ').split()
                if len(p) >= 2:
                    id_z = uuid.uuid4().hex[:6]
                    zp = os.path.join(config["dir_estoque"], f"conta_{id_z}.zip")
                    js = {"guest_account_info": {"com.garena.msdk.guest_uid": p[0], "com.garena.msdk.guest_password": p[1]}}
                    with zipfile.ZipFile(zp, 'w') as zf:
                        zf.writestr("guest100067.dat", json.dumps(js))
                    c += 1
            bot.reply_to(message, f"✅ <b>LISTA ADD:</b> {c} contas", parse_mode="HTML")

# --- MENUS ---

def menu_principal(user_id):
    estoque = [f for f in os.listdir(config["dir_estoque"]) if f.endswith('.zip')]
    saldo = obter_saldo(user_id)
    msg = (f"<b>╔═════════════════════════╗</b>\n"
           f"     💎  <b>LH STORE OFICIAL</b> 💎\n"
           f"<b>╚═════════════════════════╝</b>\n\n"
           f"🛒 <b>Item:</b> <code>{config['nome_item']}</code>\n"
           f"🔥 <b>Estoque:</b> <code>{len(estoque)}</code> un.\n"
           f"💰 <b>Saldo:</b> <code>R$ {saldo:.2f}</code>\n"
           f"💵 <b>Preço:</b> <code>R$ {config['preco']:.2f}</code>\n\n"
           f"🆔 <b>Seu ID:</b> <code>{user_id}</code>")
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🛒 COMPRAR", callback_data="buy"))
    markup.add(
        types.InlineKeyboardButton("💳 RECARREGAR", callback_data="btn_recharge"),
        types.InlineKeyboardButton("📖 TUTORIAL", callback_data="btn_tutorial")
    )
    markup.add(types.InlineKeyboardButton("👨‍💻 SUPORTE", url=f"https://t.me/{USUARIO_SUPORTE.replace('@','')}"))
    if eh_admin(user_id):
        markup.add(types.InlineKeyboardButton("⚙️ PAINEL ADMIN", callback_data="adm_main"))
    return msg, markup

@bot.message_handler(commands=['start', 'menu'])
def cmd_start(message):
    if eh_banido(message.from_user.id): return
    msg, markup = menu_principal(message.from_user.id)
    bot.send_message(message.chat.id, msg, reply_markup=markup, parse_mode="HTML")

# --- CALLBACK HANDLER ---

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    bot.answer_callback_query(call.id)
    uid, cid, mid = call.from_user.id, call.message.chat.id, call.message.message_id
    if eh_banido(uid): return

    # --- CLIENTE ---
    if call.data == "go_home":
        msg, markup = menu_principal(uid)
        bot.edit_message_text(msg, cid, mid, reply_markup=markup, parse_mode="HTML")

    elif call.data == "btn_tutorial":
        txt = ("<b>📖 TUTORIAL DE USO</b>\n\n"
               "<b>1. Saldo:</b> Clique em Recarregar, pague o Pix e envie o comprovante para o dono.\n"
               "<b>2. Compra:</b> Com saldo na conta, clique em Comprar. O bot envia o arquivo na hora.\n"
               "<b>3. Suporte:</b> Se tiver dúvidas, chame o dono no botão suporte.")
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("⬅️ VOLTAR", callback_data="go_home"))
        bot.edit_message_text(txt, cid, mid, reply_markup=markup, parse_mode="HTML")

    elif call.data == "btn_recharge":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("R$ 1", callback_data="px_1"),
            types.InlineKeyboardButton("R$ 3", callback_data="px_3"),
            types.InlineKeyboardButton("R$ 5", callback_data="px_5"),
            types.InlineKeyboardButton("R$ 10", callback_data="px_10"),
            types.InlineKeyboardButton("💎 OUTRO VALOR", callback_data="px_custom"),
            types.InlineKeyboardButton("⬅️ VOLTAR", callback_data="go_home")
        )
        bot.edit_message_text("💳 <b>ESCOLHA O VALOR DA RECARGA:</b>", cid, mid, reply_markup=markup, parse_mode="HTML")

    elif call.data.startswith("px_"):
        val = call.data.split("_")[1]
        if val == "custom":
            m = bot.send_message(cid, "<b>💎 DIGITE O VALOR (Ex: 20):</b>", parse_mode="HTML")
            bot.register_next_step_handler(m, process_custom_pix)
        else:
            show_pix(cid, uid, float(val), mid)

    elif call.data == "buy":
        est = [f for f in os.listdir(config["dir_estoque"]) if f.endswith('.zip')]
        if not est:
            bot.send_message(cid, "❌ <b>SEM ESTOQUE!</b>")
            return
        if obter_saldo(uid) < config["preco"]:
            bot.send_message(cid, "❌ <b>SALDO INSUFICIENTE!</b>")
            return
        item = est[0]
        if ajustar_saldo(uid, -config["preco"]):
            with open(os.path.join(config["dir_estoque"], item), 'rb') as f:
                bot.send_document(cid, f, caption="✅ <b>CONTA ENTREGUE!</b>")
            os.remove(os.path.join(config["dir_estoque"], item))
        else: bot.send_message(cid, "❌ Erro.")

    # --- ADMIN ---
    elif call.data == "adm_main":
        if not eh_admin(uid): return
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("💰 ADD SALDO", callback_data="adm_add_s"),
            types.InlineKeyboardButton("🏷️ MUDAR PREÇO", callback_data="adm_ch_p"),
            types.InlineKeyboardButton("🗑️ ZERAR ESTOQUE", callback_data="adm_del"),
            types.InlineKeyboardButton("🚫 BANIR ID", callback_data="adm_bn"),
            types.InlineKeyboardButton("⬅️ VOLTAR", callback_data="go_home")
        )
        bot.edit_message_text("🛠️ <b>PAINEL DO DONO</b>", cid, mid, reply_markup=markup, parse_mode="HTML")

    elif call.data == "adm_add_s":
        m = bot.send_message(cid, "💰 <b>DIGITE: ID VALOR</b>")
        bot.register_next_step_handler(m, step_add)

    elif call.data == "adm_ch_p":
        m = bot.send_message(cid, "🏷️ <b>NOVO PREÇO:</b>")
        bot.register_next_step_handler(m, step_price)

    elif call.data == "adm_bn":
        m = bot.send_message(cid, "🚫 <b>ID PARA BANIR:</b>")
        bot.register_next_step_handler(m, lambda msg: [open(DB_BANIDOS, "a").write(f"{msg.text}\n"), bot.send_message(cid, "✅ Banido!")])

    elif call.data == "adm_del":
        for f in os.listdir(config["dir_estoque"]): os.remove(os.path.join(config["dir_estoque"], f))
        bot.send_message(cid, "🗑️ Estoque limpo!")

# --- AUXILIARES ---

def show_pix(cid, uid, val, mid=None):
    txt = (f"💳 <b>PAGAMENTO PIX</b>\n\n"
           f"💰 Valor: <b>R$ {val:.2f}</b>\n"
           f"🔑 Chave: <code>{MINHA_CHAVE_PIX}</code>\n\n"
           f"⚠️ Envie o comprovante para {USUARIO_SUPORTE}\n"
           f"🆔 Seu ID: <code>{uid}</code>")
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("⬅️ VOLTAR", callback_data="btn_recharge"))
    if mid: bot.edit_message_text(txt, cid, mid, reply_markup=markup, parse_mode="HTML")
    else: bot.send_message(cid, txt, reply_markup=markup, parse_mode="HTML")

def process_custom_pix(m):
    try:
        v = float(m.text.replace(',', '.'))
        show_pix(m.chat.id, m.from_user.id, v)
    except: bot.reply_to(m, "❌ Valor inválido.")

def step_add(m):
    try:
        p = m.text.split()
        if ajustar_saldo(p[0], float(p[1])):
            bot.reply_to(m, "✅ Saldo adicionado!")
            try: bot.send_message(p[0], f"🎉 <b>Saldo de R$ {p[1]} liberado!</b>", parse_mode="HTML")
            except: pass
    except: bot.reply_to(m, "❌ Erro.")

def step_price(m):
    try:
        config["preco"] = float(m.text.replace(',', '.'))
        salvar_config(config)
        bot.reply_to(m, "✅ Preço alterado!")
    except: bot.reply_to(m, "❌ Erro.")

if __name__ == "__main__":
    print("🚀 LH STORE ONLINE - ERROS CORRIGIDOS!")
    bot.infinity_polling()
