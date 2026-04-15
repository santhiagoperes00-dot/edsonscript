import telebot
from telebot import types
import time
import os
import json
import shutil
import uuid

# ================= CONFIGURAÇÕES (LH STORE) =================
TOKEN_TELEGRAM = "8705531112:AAF0dV9xHrf_4ihgvQuBlr9ED4D8BbqOoEs"
ID_DONO = 5658716257
ID_SECUNDARIO = 6490804782  # Segundo ID para logs de segurança
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

# --- INICIALIZAÇÃO DE SISTEMA ---
if not os.path.exists(config["dir_estoque"]): 
    os.makedirs(config["dir_estoque"])

def iniciar_json(arquivo, default):
    if not os.path.exists(arquivo):
        with open(arquivo, "w") as f: json.dump(default, f)

iniciar_json(DB_AFILIADOS, {"relacoes": {}, "convidados": {}})
iniciar_json(DB_SALDOS, {})

# --- FUNÇÕES DE APOIO ---

def eh_admin(user_id):
    return user_id == ID_DONO or user_id == ID_SECUNDARIO

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
        u_str = str(user_id)
        saldos[u_str] = round(float(saldos.get(u_str, 0.0)) + valor, 2)
        with open(DB_SALDOS, "w") as f: json.dump(saldos, f, indent=4)
        return True
    except: return False

def get_estoque():
    return [f for f in os.listdir(config["dir_estoque"]) if os.path.isfile(os.path.join(config["dir_estoque"], f))]

# --- MENUS VISUAIS ---

def menu_principal(user_id):
    saldo = obter_saldo(user_id)
    estoque_qtd = len(get_estoque())
    msg = (f"╔══════════════════════╗\n"
           f"     👑  *LH STORE* 👑\n"
           f"╚══════════════════════╝\n\n"
           f"📦 *Produto:* `{config['nome_item']}`\n"
           f"💵 *Preço Unitário:* `R$ {config['preco']:.2f}`\n"
           f"🔥 *Estoque:* `{estoque_qtd}` unidades\n\n"
           f"👤 *Seu ID:* `{user_id}`\n"
           f"💰 *Seu Saldo:* `R$ {saldo:.2f}`\n\n"
           f"👇 *Selecione uma opção:*")
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛒 Comprar", callback_data="buy"),
        types.InlineKeyboardButton("💳 Recarregar", callback_data="recharge"),
        types.InlineKeyboardButton("👥 Afiliados", callback_data="affiliate"),
        types.InlineKeyboardButton("👨‍💻 Suporte", url=f"https://t.me/{USUARIO_SUPORTE.replace('@','')}")
    )
    if eh_admin(user_id):
        markup.add(types.InlineKeyboardButton("⚙️ Painel Admin", callback_data="adm_painel"))
    return msg, markup

# --- COMANDOS PRINCIPAIS ---

@bot.message_handler(commands=['start', 'menu'])
def start(message):
    uid = message.from_user.id
    if not os.path.exists(DB_USUARIOS): open(DB_USUARIOS, "w").close()
    
    with open(DB_USUARIOS, "r+") as f:
        content = f.read()
        if str(uid) not in content:
            f.write(f"{uid}\n")
            args = message.text.split()
            if len(args) > 1 and args[1] != str(uid):
                ajustar_saldo(args[1], config["bonus_indicacao"])
                enviar_seguro(args[1], f"🎊 *Bônus!* Você ganhou R$ {config['bonus_indicacao']} por indicar um amigo!")

    msg, markup = menu_principal(uid)
    bot.send_message(message.chat.id, msg, reply_markup=markup, parse_mode="Markdown")

# --- PAINEL ADMINISTRATIVO (/admin) ---

@bot.message_handler(commands=['admin'])
def cmd_admin(message):
    if not eh_admin(message.from_user.id): return
    abrir_painel_admin(message.chat.id)

def abrir_painel_admin(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("➕ Add Conta (Texto)", callback_data="adm_add_txt"),
        types.InlineKeyboardButton("📁 Ver Estoque", callback_data="adm_ver_est"),
        types.InlineKeyboardButton("📢 Aviso Geral", callback_data="adm_broadcast"),
        types.InlineKeyboardButton("⬅️ Sair", callback_data="voltar")
    )
    bot.send_message(chat_id, "⚙️ *PAINEL DE CONTROLE*\nGerencie sua loja abaixo:", reply_markup=markup, parse_mode="Markdown")

# --- LÓGICA DE CALLBACKS ---

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid, cid, mid = call.from_user.id, call.message.chat.id, call.message.message_id

    if call.data == "voltar":
        msg, markup = menu_principal(uid)
        bot.edit_message_text(msg, cid, mid, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "recharge":
        texto = (f"💳 *RECARGA VIA PIX*\n\n🔑 Chave Pix: `{MINHA_CHAVE_PIX}`\n\n"
                 f"⚠️ Envie o *COMPROVANTE* (Foto) aqui no chat após o pagamento.")
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("⬅️ Voltar", callback_data="voltar"))
        bot.edit_message_text(texto, cid, mid, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "buy":
        estoque = get_estoque()
        if not estoque:
            bot.answer_callback_query(call.id, "❌ Sem estoque!", show_alert=True)
            return
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("✅ Confirmar", callback_data="confirm_buy"),
            types.InlineKeyboardButton("⬅️ Cancelar", callback_data="voltar")
        )
        bot.edit_message_text(f"🛒 *CONFIRMAR COMPRA*\n\nItem: `{config['nome_item']}`\nValor: `R$ {config['preco']:.2f}`", cid, mid, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "confirm_buy":
        saldo = obter_saldo(uid)
        estoque = get_estoque()
        if saldo < config["preco"]:
            bot.answer_callback_query(call.id, "❌ Saldo insuficiente!", show_alert=True)
            return
        
        item_nome = estoque[0]
        caminho = os.path.join(config["dir_estoque"], item_nome)
        if ajustar_saldo(uid, -config["preco"]):
            with open(caminho, 'rb') as f:
                bot.send_document(cid, f, caption="✅ *ENTREGA REALIZADA!*\nObrigado por comprar na LH STORE!")
            os.remove(caminho)
            with open(DB_VENDAS, "a") as v: v.write(f"{uid}:{item_nome}\n")
        else:
            bot.answer_callback_query(call.id, "❌ Erro no sistema.")

    elif call.data == "affiliate":
        link = f"https://t.me/{bot.get_me().username}?start={uid}"
        bot.edit_message_text(f"👥 *AFILIADOS*\n\nGanhe `R$ {config['bonus_indicacao']}` por convite!\n🔗 Link: `{link}`", cid, mid, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")), parse_mode="Markdown")

    # Callbacks Admin
    elif call.data == "adm_painel":
        abrir_painel_admin(cid)

    elif call.data == "adm_add_txt":
        msg = bot.send_message(cid, "📝 *DIGITE A CONTA:*\nEx: `usuario:senha123`", parse_mode="Markdown")
        bot.register_next_step_handler(msg, salvar_conta_texto)

    elif call.data == "adm_broadcast":
        msg = bot.send_message(cid, "📢 *DIGITE O AVISO:*", parse_mode="Markdown")
        bot.register_next_step_handler(msg, processar_broadcast)

# --- FUNÇÕES ADMIN ---

def salvar_conta_texto(message):
    if not message.text: return
    nome = f"conta_{uuid.uuid4().hex[:5]}.txt"
    with open(os.path.join(config["dir_estoque"], nome), "w") as f: f.write(message.text)
    bot.send_message(message.chat.id, f"✅ Conta salva: `{nome}`", parse_mode="Markdown")

def processar_broadcast(message):
    if not os.path.exists(DB_USUARIOS): return
    with open(DB_USUARIOS, "r") as f: ids = f.read().splitlines()
    for user in ids:
        try: bot.send_message(user, f"📢 *AVISO LH STORE*\n\n{message.text}", parse_mode="Markdown")
        except: pass
    bot.send_message(message.chat.id, "✅ Aviso enviado com sucesso!")

# --- GESTÃO DE COMPROVANTES ---

@bot.message_handler(content_types=['photo', 'document'])
def handle_docs(message):
    uid = message.from_user.id
    markup = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("✅ Aprovar R$ 1", callback_data=f"apr_{uid}_1"),
        types.InlineKeyboardButton("✅ Aprovar R$ 5", callback_data=f"apr_{uid}_5"),
        types.InlineKeyboardButton("💎 Outro", callback_data=f"apr_{uid}_10")
    )
    bot.reply_to(message, "⏳ *Analisando comprovante...*")
    for adm in [ID_DONO, ID_SECUNDARIO]:
        try:
            if message.content_type == 'photo':
                bot.send_photo(adm, message.photo[-1].file_id, caption=f"📩 *RECIBO* de `{uid}`", reply_markup=markup, parse_mode="Markdown")
            else:
                bot.send_document(adm, message.document.file_id, caption=f"📩 *RECIBO* de `{uid}`", reply_markup=markup, parse_mode="Markdown")
        except: pass

@bot.callback_query_handler(func=lambda call: call.data.startswith("apr_"))
def aprovar_pagamento(call):
    _, tid, valor = call.data.split("_")
    if ajustar_saldo(tid, float(valor)):
        enviar_seguro(tid, f"✅ *SALDO ADICIONADO!*\nFoi creditado `R$ {valor}` na sua conta.")
        bot.edit_message_caption(f"✅ Aprovado R$ {valor} para {tid}", call.message.chat.id, call.message.message_id)

# --- START ---
if __name__ == "__main__":
    print("--- LH STORE ONLINE ---")
    bot.infinity_polling()
