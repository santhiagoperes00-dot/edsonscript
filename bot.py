import telebot
from telebot import types
import os
import json
import uuid
import zipfile
import time

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

# --- FUNÇÕES DE SUPORTE ---

def eh_admin(uid):
    return str(uid) == str(ID_DONO)

def eh_banido(uid):
    if not os.path.exists(DB_BANIDOS): return False
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

# --- GERENCIAMENTO DE MÍDIA (ESTOQUE E COMPROVANTES) ---

@bot.message_handler(content_types=['document', 'photo'])
def handle_media(message):
    uid = message.from_user.id
    if eh_banido(uid): return

    # SE FOR CLIENTE
    if not eh_admin(uid):
        bot.reply_to(message, f"❌ **ENVIO NEGADO!**\n\nEu não processo comprovantes aqui. Mande a foto do pagamento e o seu ID (`{uid}`) para o dono no privado: {USUARIO_SUPORTE}")
        return

    # SE FOR O DONO ADICIONANDO ESTOQUE
    if message.content_type == 'document':
        nome = message.document.file_name
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        
        # FILTRO: ARQUIVOS GUEST
        if nome.lower().startswith("guest"):
            id_u = uuid.uuid4().hex[:6]
            caminho = os.path.join(config["dir_estoque"], f"conta_{id_u}.zip")
            with zipfile.ZipFile(caminho, 'w') as zf:
                zf.writestr(nome, downloaded)
            bot.reply_to(message, f"✅ **CONTA GUEST ADICIONADA!**\n📦 Arquivo: `{nome}`\n🆔 Ref: `{id_u}`")
            return

        # FILTRO: LISTAS TXT
        if nome.endswith('.txt'):
            linhas = downloaded.decode('utf-8', errors='ignore').splitlines()
            c = 0
            for l in linhas:
                p = l.replace(':', ' ').split()
                if len(p) >= 2:
                    id_z = uuid.uuid4().hex[:6]
                    path = os.path.join(config["dir_estoque"], f"conta_{id_z}.zip")
                    js = {"guest_account_info": {"com.garena.msdk.guest_uid": p[0], "com.garena.msdk.guest_password": p[1]}}
                    with zipfile.ZipFile(path, 'w') as zf:
                        zf.writestr("guest100067.dat", json.dumps(js))
                    c += 1
            bot.reply_to(message, f"✅ **LISTA IMPORTADA!**\n📦 `{c}` contas adicionadas ao estoque.")

# --- MENUS PRINCIPAIS ---

def menu_principal(user_id):
    estoque = [f for f in os.listdir(config["dir_estoque"]) if f.endswith('.zip')]
    saldo = obter_saldo(user_id)
    msg = (f"╔═════════════════════════╗\n"
           f"     💎  **LH STORE OFICIAL** 💎\n"
           f"╚═════════════════════════╝\n\n"
           f"👋 Olá! Seja bem-vindo à nossa loja!\n\n"
           f"🎮 **Produto:** `{config['nome_item']}`\n"
           f"🔥 **Em Estoque:** `{len(estoque)}` unidades\n"
           f"💵 **Preço Unitário:** `R$ {config['preco']:.2f}`\n\n"
           f"💰 **Seu Saldo:** `R$ {saldo:.2f}`\n"
           f"🆔 **Seu ID:** `{user_id}`\n\n"
           f"🚀 *Escolha uma opção abaixo:*")
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton("🛒 COMPRAR AGORA", callback_data="buy")
    b2 = types.InlineKeyboardButton("💳 ADICIONAR SALDO", callback_data="recharge_menu")
    b3 = types.InlineKeyboardButton("📖 TUTORIAL", callback_data="ajuda_cliente")
    b4 = types.InlineKeyboardButton("👨‍💻 SUPORTE", url=f"https://t.me/{USUARIO_SUPORTE.replace('@','')}")
    markup.add(b1)
    markup.add(b2, b3)
    markup.add(b4)
    if eh_admin(user_id):
        markup.add(types.InlineKeyboardButton("⚙️ PAINEL DO DONO", callback_data="adm_painel"))
    return msg, markup

@bot.message_handler(commands=['start', 'menu'])
def cmd_start(message):
    if eh_banido(message.from_user.id): return
    msg, markup = menu_principal(message.from_user.id)
    bot.send_message(message.chat.id, msg, reply_markup=markup, parse_mode="Markdown")

# --- LÓGICA DE CALLBACK (BOTÕES) ---

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    # Responde o clique imediatamente para evitar que o botão trave
    bot.answer_callback_query(call.id)
    
    uid, cid, mid = call.from_user.id, call.message.chat.id, call.message.message_id
    if eh_banido(uid): return

    # --- NAVEGAÇÃO ---
    if call.data == "voltar":
        msg, markup = menu_principal(uid)
        bot.edit_message_text(msg, cid, mid, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "ajuda_cliente":
        texto = (f"📖 **COMO COMPRAR NA LH STORE**\n\n"
                 f"1️⃣ Clique em **Adicionar Saldo**.\n"
                 f"2️⃣ Escolha o valor e pague via Pix.\n"
                 f"3️⃣ Envie o comprovante e seu ID pro dono: {USUARIO_SUPORTE}.\n"
                 f"4️⃣ Assim que ele aprovar, clique em **Comprar Agora**.\n"
                 f"5️⃣ O bot entrega sua conta na hora! 🚀")
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("⬅️ ENTENDI", callback_data="voltar"))
        bot.edit_message_text(texto, cid, mid, reply_markup=markup, parse_mode="Markdown")

    # --- COMPRA ---
    elif call.data == "buy":
        estoque = [f for f in os.listdir(config["dir_estoque"]) if f.endswith('.zip')]
        if not estoque:
            bot.send_message(cid, "❌ **ESTOQUE ESGOTADO!** Aguarde a reposição.")
            return
        if obter_saldo(uid) < config["preco"]:
            bot.send_message(cid, "❌ **SALDO INSUFICIENTE!** Recarregue sua conta.")
            return
        
        item = estoque[0]
        if ajustar_saldo(uid, -config["preco"]):
            with open(os.path.join(config["dir_estoque"], item), 'rb') as f:
                bot.send_document(cid, f, caption="🎉 **CONTA ENTREGUE!**\n\nObrigado pela preferência!")
            os.remove(os.path.join(config["dir_estoque"], item))
        else: bot.send_message(cid, "❌ Erro ao processar o saldo.")

    # --- MENU DE RECARGA ---
    elif call.data == "recharge_menu":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("R$ 1", callback_data="vpix_1"),
            types.InlineKeyboardButton("R$ 3", callback_data="vpix_3"),
            types.InlineKeyboardButton("R$ 5", callback_data="vpix_5"),
            types.InlineKeyboardButton("R$ 10", callback_data="vpix_10"),
            types.InlineKeyboardButton("💎 VALOR PERSONALIZADO", callback_data="vpix_custom"),
            types.InlineKeyboardButton("⬅️ VOLTAR", callback_data="voltar")
        )
        bot.edit_message_text("💳 **MENU DE RECARGA**\nEscolha quanto deseja adicionar:", cid, mid, reply_markup=markup)

    # --- LOGICA DO PIX ---
    elif call.data.startswith("vpix_"):
        valor_str = call.data.split("_")[1]
        
        if valor_str == "custom":
            msg = bot.send_message(cid, "💎 **DIGITE O VALOR:**\n(Exemplo: `15` ou `50.50`)")
            bot.register_next_step_handler(msg, processar_custom)
        else:
            valor = float(valor_str)
            mostrar_dados_pix(cid, uid, valor)

    # --- PAINEL DO DONO ---
    elif call.data == "adm_painel":
        if not eh_admin(uid): return
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("💰 ADD SALDO", callback_data="adm_add"),
            types.InlineKeyboardButton("🏷️ ALTERAR PREÇO", callback_data="adm_price"),
            types.InlineKeyboardButton("🗑️ LIMPAR TUDO", callback_data="adm_clear"),
            types.InlineKeyboardButton("🚫 BANIR", callback_data="adm_ban"),
            types.InlineKeyboardButton("📖 INFO ADMIN", callback_data="adm_info")
        )
        markup.add(types.InlineKeyboardButton("⬅️ VOLTAR", callback_data="voltar"))
        bot.edit_message_text("🛠️ **GESTOR LH STORE**", cid, mid, reply_markup=markup)

    elif call.data == "adm_info":
        info = (f"⚙️ **FUNÇÕES DO DONO:**\n\n"
                f"✅ **Estoque:** Mande arquivos `.dat` que começam com 'guest' ou listas `.txt`.\n"
                f"✅ **Aprovar Pix:** Pegue o ID do cliente e o valor que ele pagou, clique em `ADD SALDO` e digite `ID VALOR`.")
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("⬅️ VOLTAR", callback_data="adm_painel"))
        bot.edit_message_text(info, cid, mid, reply_markup=markup)

    elif call.data == "adm_add":
        m = bot.send_message(cid, "💰 **ADD SALDO**\nDigite: `ID VALOR` (Ex: `12345 5.00`)")
        bot.register_next_step_handler(m, step_add_saldo)

    elif call.data == "adm_price":
        m = bot.send_message(cid, "🏷️ **NOVO PREÇO:**\n(Exemplo: `0.50`)")
        bot.register_next_step_handler(m, step_set_price)

    elif call.data == "adm_ban":
        m = bot.send_message(cid, "🚫 **ID PARA BANIR:**")
        bot.register_next_step_handler(m, lambda msg: [open(DB_BANIDOS, "a").write(f"{msg.text}\n"), bot.send_message(cid, "✅ Banido!")])

    elif call.data == "adm_clear":
        for f in os.listdir(config["dir_estoque"]): os.remove(os.path.join(config["dir_estoque"], f))
        bot.send_message(cid, "💣 **ESTOQUE APAGADO!**")

# --- FUNÇÕES AUXILIARES ---

def mostrar_dados_pix(chat_id, user_id, valor):
    msg = (f"💳 **DADOS PARA PAGAMENTO**\n\n"
           f"💰 Valor: **R$ {valor:.2f}**\n"
           f"🔑 Chave Pix: `{MINHA_CHAVE_PIX}`\n\n"
           f"⚠️ **ATENÇÃO:**\n"
           f"Após pagar, envie o comprovante e seu ID para {USUARIO_SUPORTE}.\n"
           f"🆔 Seu ID: `{user_id}`")
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("⬅️ VOLTAR", callback_data="recharge_menu"))
    bot.send_message(chat_id, msg, parse_mode="Markdown", reply_markup=markup)

def processar_custom(message):
    try:
        val = float(message.text.replace(',', '.'))
        if val < 1: 
            bot.reply_to(message, "❌ Valor mínimo R$ 1,00.")
            return
        mostrar_dados_pix(message.chat.id, message.from_user.id, val)
    except: bot.reply_to(message, "❌ Digite apenas números.")

def step_add_saldo(message):
    try:
        p = message.text.split()
        if ajustar_saldo(p[0], float(p[1])):
            bot.reply_to(message, f"✅ Saldo de R$ {p[1]} adicionado ao ID {p[0]}")
            try: bot.send_message(p[0], f"🎉 **SALDO DISPONÍVEL!**\nSua recarga de **R$ {p[1]}** foi aprovada!")
            except: pass
    except: bot.reply_to(message, "❌ Use: `ID VALOR`")

def step_set_price(message):
    try:
        np = float(message.text.replace(',', '.'))
        config["preco"] = np
        salvar_config(config)
        bot.reply_to(message, f"✅ Novo preço: R$ {np:.2f}")
    except: bot.reply_to(message, "❌ Valor inválido.")

if __name__ == "__main__":
    print("🚀 BOT LH STORE ATUALIZADO E RODANDO!")
    bot.infinity_polling()
