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

# --- PROCESSAMENTO DE ARQUIVOS ---

@bot.message_handler(content_types=['document', 'photo'])
def handle_media(message):
    uid = message.from_user.id
    if eh_banido(uid): return

    # SE FOR CLIENTE MANDANDO FOTO/COMPROVANTE
    if not eh_admin(uid):
        msg_erro = (f"⚠️ **ATENÇÃO CLIENTE!**\n\n"
                    f"Eu sou apenas um robô de entregas automáticas 🤖\n\n"
                    f"Para que seu saldo seja adicionado, você precisa enviar a **foto do comprovante** e o seu **ID** (`{uid}`) "
                    f"diretamente para o dono clicando aqui 👉 {USUARIO_SUPORTE}")
        bot.reply_to(message, msg_erro, parse_mode="Markdown")
        return

    # SE FOR ADMIN ABASTECENDO O ESTOQUE
    if message.content_type == 'document':
        nome_original = message.document.file_name
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        
        # 1. ARQUIVOS QUE COMEÇAM COM "GUEST" (Uma por Uma)
        if nome_original.lower().startswith("guest"):
            id_u = uuid.uuid4().hex[:8]
            caminho_zip = os.path.join(config["dir_estoque"], f"conta_{id_u}.zip")
            with zipfile.ZipFile(caminho_zip, 'w') as zf:
                zf.writestr(nome_original, downloaded)
            bot.reply_to(message, f"✅ **CONTA INDIVIDUAL ADICIONADA!**\n📦 Arquivo `{nome_original}` empacotado e salvo.")
            return

        # 2. LISTAS EM TXT (Massa)
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
            bot.reply_to(message, f"✅ **LISTA PROCESSADA!**\n📦 `{contas}` contas separadas e importadas com sucesso!")

# --- MENUS ---

def menu_principal(user_id):
    estoque = [f for f in os.listdir(config["dir_estoque"]) if f.endswith('.zip')]
    saldo = obter_saldo(user_id)
    msg = (f"╔═════════════════════════╗\n"
           f"     💎  **LH STORE OFICIAL** 💎\n"
           f"╚═════════════════════════╝\n\n"
           f"Olá! Bem-vindo à melhor loja de contas Garena! 🎮\n\n"
           f"🛍️ **Produto:** `{config['nome_item']}`\n"
           f"🔥 **Disponível:** `{len(estoque)}` contas\n"
           f"💵 **Valor da Unidade:** `R$ {config['preco']:.2f}`\n\n"
           f"👤 **Seu ID:** `{user_id}`\n"
           f"💰 **Seu Saldo:** `R$ {saldo:.2f}`\n\n"
           f"👇 *Navegue pelos botões abaixo:*")
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛍️ Comprar Conta", callback_data="buy"),
        types.InlineKeyboardButton("💳 Recarregar Saldo", callback_data="recharge_menu"),
        types.InlineKeyboardButton("📖 Como Funciona?", callback_data="ajuda_cliente"),
        types.InlineKeyboardButton("👨‍💻 Falar com Suporte", url=f"https://t.me/{USUARIO_SUPORTE.replace('@','')}")
    )
    if eh_admin(user_id):
        markup.add(types.InlineKeyboardButton("⚙️ Painel Gestor (Admin)", callback_data="adm_painel"))
    return msg, markup

@bot.message_handler(commands=['start', 'menu'])
def cmd_start(message):
    if eh_banido(message.from_user.id): return
    msg, markup = menu_principal(message.from_user.id)
    bot.send_message(message.chat.id, msg, reply_markup=markup, parse_mode="Markdown")

# --- GERADOR DE MENSAGEM PIX ---
def exibir_instrucoes_pix(chat_id, user_id, valor, message_id_para_editar=None):
    msg_pix = (f"💳 **SISTEMA DE PAGAMENTO PIX** 💳\n\n"
               f"Você escolheu recarregar: **R$ {valor:.2f}**\n\n"
               f"🔑 **Chave PIX:** `{MINHA_CHAVE_PIX}`\n"
               f"*(Clique na chave para copiar)*\n\n"
               f"⚠️ **PASSO A PASSO PARA APROVAÇÃO:**\n"
               f"1️⃣ Faça o Pix do valor exato.\n"
               f"2️⃣ Copie o seu ID exclusivo: `{user_id}`\n"
               f"3️⃣ Envie o comprovante e o seu ID no privado do dono: {USUARIO_SUPORTE}\n\n"
               f"⏳ *Seu saldo será liberado assim que o dono verificar!*")
    
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("⬅️ Voltar ao Início", callback_data="voltar"))
    
    if message_id_para_editar:
        try:
            bot.edit_message_text(msg_pix, chat_id, message_id_para_editar, parse_mode="Markdown", reply_markup=markup)
        except:
            bot.send_message(chat_id, msg_pix, parse_mode="Markdown", reply_markup=markup)
    else:
        bot.send_message(chat_id, msg_pix, parse_mode="Markdown", reply_markup=markup)


# --- CALLBACKS GERAIS ---

@bot.callback_query_handler(func=lambda call: True)
def calls(call):
    uid, cid, mid = call.from_user.id, call.message.chat.id, call.message.message_id
    if eh_banido(uid): return

    # VOLTAR PRO MENU
    if call.data == "voltar":
        msg, markup = menu_principal(uid)
        bot.edit_message_text(msg, cid, mid, reply_markup=markup, parse_mode="Markdown")

    # AJUDA CLIENTE
    elif call.data == "ajuda_cliente":
        texto = (f"📖 **COMO UTILIZAR O BOT** 📖\n\n"
                 f"**1.** Clique em `💳 Recarregar Saldo` e escolha um valor.\n"
                 f"**2.** Copie a chave Pix, faça o pagamento e mande o comprovante para {USUARIO_SUPORTE}.\n"
                 f"**3.** Quando o dono aprovar, seu saldo aparecerá no bot.\n"
                 f"**4.** Clique em `🛍️ Comprar Conta`. O bot descontará do seu saldo e enviará o arquivo `.zip` da sua conta na mesma hora!\n\n"
                 f"✅ É rápido, fácil e 100% automático!")
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("⬅️ Entendi, Voltar", callback_data="voltar"))
        bot.edit_message_text(texto, cid, mid, parse_mode="Markdown", reply_markup=markup)

    # COMPRAR
    elif call.data == "buy":
        estoque = [f for f in os.listdir(config["dir_estoque"]) if f.endswith('.zip')]
        if not estoque:
            bot.answer_callback_query(call.id, "❌ Poxa, estamos sem estoque no momento!", show_alert=True)
            return
        if obter_saldo(uid) < config["preco"]:
            bot.answer_callback_query(call.id, "❌ Seu saldo é insuficiente! Recarregue primeiro.", show_alert=True)
            return
        
        item = estoque[0]
        if ajustar_saldo(uid, -config["preco"]):
            with open(os.path.join(config["dir_estoque"], item), 'rb') as f:
                bot.send_document(cid, f, caption="🎉 **Compra aprovada com sucesso!**\n\nObrigado por comprar na LH STORE! Aqui está o arquivo da sua conta.")
            os.remove(os.path.join(config["dir_estoque"], item))
        else: bot.answer_callback_query(call.id, "❌ Ocorreu um erro ao processar o saldo.")

    # MENU DE RECARGA
    elif call.data == "recharge_menu":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("💵 R$ 1,00", callback_data="pix_1"),
            types.InlineKeyboardButton("💵 R$ 3,00", callback_data="pix_3"),
            types.InlineKeyboardButton("💵 R$ 5,00", callback_data="pix_5"),
            types.InlineKeyboardButton("💵 R$ 10,00", callback_data="pix_10"),
            types.InlineKeyboardButton("💎 Outro Valor", callback_data="pix_custom")
        )
        markup.add(types.InlineKeyboardButton("⬅️ Voltar", callback_data="voltar"))
        bot.edit_message_text("💳 **ESCOLHA O VALOR DA SUA RECARGA**\nSelecione um valor fixo ou digite um valor personalizado:", cid, mid, reply_markup=markup)

    # PROCESSAMENTO DOS BOTÕES DE PIX
    elif call.data.startswith("pix_") and call.data != "pix_custom":
        valor = float(call.data.split("_")[1])
        exibir_instrucoes_pix(cid, uid, valor, mid)

    # PIX PERSONALIZADO
    elif call.data == "pix_custom":
        msg = bot.send_message(cid, "💎 **VALOR PERSONALIZADO**\n\nDigite no chat o valor que você deseja recarregar (Apenas números, Ex: `15.50` ou `20`):")
        bot.register_next_step_handler(msg, processar_pix_custom)

    # --- ÁREA GESTOR (ADMIN) ---
    elif call.data == "adm_painel":
        if not eh_admin(uid): return
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("💰 Add Saldo Manual", callback_data="adm_add_saldo"),
            types.InlineKeyboardButton("🏷️ Alterar Preço", callback_data="adm_set_price"),
            types.InlineKeyboardButton("🗑️ Esvaziar Estoque", callback_data="adm_clear"),
            types.InlineKeyboardButton("🚫 Banir Cliente", callback_data="adm_ban"),
            types.InlineKeyboardButton("❓ Ajuda / Instruções", callback_data="adm_ajuda")
        )
        markup.add(types.InlineKeyboardButton("⬅️ Voltar ao Início", callback_data="voltar"))
        bot.edit_message_text("🛠️ **PAINEL DE GESTÃO - LH STORE**\nSelecione a ação desejada abaixo:", cid, mid, reply_markup=markup)

    elif call.data == "adm_ajuda":
        texto = (f"⚙️ **INSTRUÇÕES DO GESTOR** ⚙️\n\n"
                 f"📥 **Como adicionar estoque:**\n"
                 f"- Mande um arquivo chamado `guest100067.dat` direto aqui no bot. Ele vai empacotar e salvar.\n"
                 f"- Ou mande um `.txt` com várias linhas (UID SENHA). Ele cria dezenas de contas de uma vez.\n\n"
                 f"💸 **Aprovando Saldo:**\n"
                 f"Quando o cliente te mandar o Pix no privado, copie o ID dele, venha no painel, clique em `💰 Add Saldo Manual` e digite `ID VALOR`.")
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("⬅️ Voltar ao Painel", callback_data="adm_painel"))
        bot.edit_message_text(texto, cid, mid, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "adm_add_saldo":
        m = bot.send_message(cid, "💰 **ADICIONAR SALDO**\n\nDigite o comando no formato `ID VALOR`\nExemplo: `5658716257 10.00`")
        bot.register_next_step_handler(m, processar_add_saldo)

    elif call.data == "adm_set_price":
        m = bot.send_message(cid, "🏷️ **ALTERAR PREÇO**\n\nDigite o novo valor das contas (Apenas números).\nExemplo: `0.50` ou `1.20`:")
        bot.register_next_step_handler(m, processar_set_price)

    elif call.data == "adm_clear":
        for f in os.listdir(config["dir_estoque"]): os.remove(os.path.join(config["dir_estoque"], f))
        bot.answer_callback_query(call.id, "💣 Todo o estoque foi deletado!", show_alert=True)
        calls(types.CallbackQuery(id=call.id, from_user=call.from_user, chat_instance=None, message=call.message, data="adm_painel"))

    elif call.data == "adm_ban":
        m = bot.send_message(cid, "🚫 **BANIR CLIENTE**\n\nCole aqui o ID do engraçadinho:")
        bot.register_next_step_handler(m, lambda msg: [open(DB_BANIDOS, "a").write(f"{msg.text}\n"), bot.send_message(cid, "✅ ID banido permanentemente!")])

# --- STEPS DE PROCESSAMENTO ---

def processar_pix_custom(message):
    try:
        valor_digitado = float(message.text.replace(',', '.'))
        if valor_digitado < 1.0:
            bot.reply_to(message, "❌ O valor mínimo de recarga é R$ 1.00. Tente novamente clicando em Recarregar.")
            return
        exibir_instrucoes_pix(message.chat.id, message.from_user.id, valor_digitado)
    except:
        bot.reply_to(message, "❌ Valor inválido! Por favor, digite apenas números. Tente novamente clicando em Recarregar no menu.")

def processar_add_saldo(message):
    try:
        p = message.text.split()
        if ajustar_saldo(p[0], float(p[1])):
            bot.reply_to(message, f"✅ SUCESSO!\n**R$ {p[1]}** adicionados à carteira do ID `{p[0]}`")
            try: bot.send_message(p[0], f"🎉 **BOA NOTÍCIA!**\n\nO dono acaba de aprovar sua recarga!\n**+ R$ {p[1]}** foram adicionados ao seu saldo. Você já pode fazer suas compras!")
            except: pass
    except: bot.reply_to(message, "❌ Formato incorreto! Use sempre: `ID VALOR`")

def processar_set_price(message):
    try:
        np = float(message.text.replace(',', '.'))
        config["preco"] = np
        salvar_config(config)
        bot.reply_to(message, f"✅ Feito! O preço de todas as contas agora é: **R$ {np:.2f}**")
    except: bot.reply_to(message, "❌ Digite apenas o valor numérico (ex: 0.40).")

if __name__ == "__main__":
    print("🚀 LH STORE ONLINE E 100% PROFISSIONAL!")
    bot.infinity_polling()
