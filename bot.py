import telebot
from telebot import types
import os
import json
import uuid
import zipfile
import io
import shutil

# ================= CONFIGURAÇÕES (LH STORE) =================
TOKEN_TELEGRAM = "8705531112:AAF0dV9xHrf_4ihgvQuBlr9ED4D8BbqOoEs"
ID_DONO = 5658716257 
ID_SECUNDARIO = 8308508544
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

# --- INICIALIZAÇÃO DO SISTEMA ---
if not os.path.exists(config["dir_estoque"]): 
    os.makedirs(config["dir_estoque"])

def iniciar_bancos():
    if not os.path.exists(DB_BANIDOS): open(DB_BANIDOS, "w").close()
    if not os.path.exists(DB_USUARIOS): open(DB_USUARIOS, "w").close()
    if not os.path.exists(DB_SALDOS):
        with open(DB_SALDOS, "w") as f: json.dump({}, f)

iniciar_bancos()

# --- FUNÇÕES INTERNAS ---

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
    """Gera o guest100067.dat dentro de um ZIP"""
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

# --- PROCESSAMENTO INTELIGENTE DE ARQUIVOS ---

@bot.message_handler(content_types=['document'])
def handle_bulk_upload(message):
    uid = message.from_user.id
    if eh_banido(uid): return

    if eh_admin(uid):
        ext = os.path.splitext(message.document.file_name)[1].lower()
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        contas_sucesso = 0
        linhas_falhas = 0

        # Lógica para arquivos TXT
        if ext == '.txt':
            conteudo = downloaded_file.decode('utf-8', errors='ignore')
            linhas = conteudo.splitlines()
            
            for linha in linhas:
                if not linha.strip(): continue
                # Limpeza inteligente: troca separadores comuns por espaço
                clean_line = linha.replace(':', ' ').replace(';', ' ').replace('|', ' ').replace(',', ' ')
                partes = clean_line.split()
                
                if len(partes) >= 2:
                    criar_pacote_garena(partes[0], partes[1])
                    contas_sucesso += 1
                else:
                    linhas_falhas += 1
            
            bot.reply_to(message, f"📊 **Relatório de Importação:**\n\n✅ Sucesso: `{contas_sucesso}`\n❌ Falhas: `{linhas_falhas}`\n📦 Estoque atualizado!")

        elif ext == '.zip':
            # Se for um ZIP, ele apenas move para o estoque (considerando que já são contas prontas)
            caminho_final = os.path.join(config["dir_estoque"], message.document.file_name)
            with open(caminho_final, 'wb') as f: f.write(downloaded_file)
            bot.reply_to(message, "✅ Arquivo ZIP adicionado diretamente ao estoque.")
    
    else:
        # Usuário enviando comprovante
        bot.reply_to(message, "⏳ **Comprovante em análise...**")
        for adm in [ID_DONO, ID_SECUNDARIO]:
            markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("✅ Aprovar R$ 1", callback_data=f"apr_{uid}_1"))
            bot.send_document(adm, message.document.file_id, caption=f"📩 **RECIBO** de `{uid}`", reply_markup=markup)

# --- INTERFACE E MENUS ---

def menu_principal(user_id):
    estoque = [f for f in os.listdir(config["dir_estoque"]) if f.endswith('.zip')]
    saldo = obter_saldo(user_id)
    msg = (f"╔══════════════════════╗\n"
           f"     💎  **LH STORE** 💎\n"
           f"╚══════════════════════╝\n\n"
           f"🛒 **Produto:** `{config['nome_item']}`\n"
           f"🔥 **Em Estoque:** `{len(estoque)}` un.\n"
           f"💰 **Saldo:** `R$ {saldo:.2f}`\n\n"
           f"✨ *Qualidade e rapidez na entrega!*")
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛒 Comprar Agora", callback_data="buy"),
        types.InlineKeyboardButton("💳 Adicionar Saldo", callback_data="recharge"),
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

# --- LÓGICA DE CALLBACKS ---

@bot.callback_query_handler(func=lambda call: True)
def handle_calls(call):
    uid, cid, mid = call.from_user.id, call.message.chat.id, call.message.message_id
    if eh_banido(uid): return

    if call.data == "voltar":
        msg, markup = menu_principal(uid)
        bot.edit_message_text(msg, cid, mid, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "buy":
        estoque = [f for f in os.listdir(config["dir_estoque"]) if f.endswith('.zip')]
        if not estoque:
            bot.answer_callback_query(call.id, "❌ Estoque esgotado no momento!", show_alert=True)
            return
        if obter_saldo(uid) < config["preco"]:
            bot.answer_callback_query(call.id, "❌ Saldo insuficiente!", show_alert=True)
            return
        
        item = estoque[0]
        caminho = os.path.join(config["dir_estoque"], item)
        if ajustar_saldo(uid, -config["preco"]):
            with open(caminho, 'rb') as f:
                bot.send_document(cid, f, caption="✅ **Entrega efetuada!**\nConfira o arquivo anexo.")
            os.remove(caminho)
        else: bot.answer_callback_query(call.id, "❌ Erro ao debitar saldo.")

    elif call.data == "recharge":
        bot.edit_message_text(f"💳 **SISTEMA DE PAGAMENTO**\n\n🔑 PIX: `{MINHA_CHAVE_PIX}`\n\nEnvie o comprovante em anexo após o envio.", cid, mid, parse_mode="Markdown")

    # --- ÁREA DO ADMINISTRADOR ---
    elif call.data == "adm_painel":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🗑️ Limpar Todo Estoque", callback_data="adm_confirm_limpar"),
            types.InlineKeyboardButton("🚫 Banir Usuário", callback_data="adm_ban"),
            types.InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")
        )
        bot.edit_message_text("🛠️ **PAINEL DE CONTROLE**\nEnvie listas `.txt` para adicionar contas em massa.", cid, mid, reply_markup=markup)

    elif call.data == "adm_confirm_limpar":
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("✅ SIM, APAGAR TUDO", callback_data="adm_execute_clear"),
            types.InlineKeyboardButton("❌ CANCELAR", callback_data="adm_painel")
        )
        bot.edit_message_text("⚠️ **ATENÇÃO!**\nDeseja realmente apagar **TODOS** os itens do estoque?", cid, mid, reply_markup=markup)

    elif call.data == "adm_execute_clear":
        arquivos = [f for f in os.listdir(config["dir_estoque"])]
        for f in arquivos: os.remove(os.path.join(config["dir_estoque"], f))
        bot.answer_callback_query(call.id, "💣 Estoque limpo com sucesso!", show_alert=True)
        handle_calls(types.CallbackQuery(id=call.id, from_user=call.from_user, chat_instance=None, message=call.message, data="adm_painel"))

    elif call.data == "adm_ban":
        msg = bot.send_message(cid, "🚫 Informe o **ID** para banimento:")
        bot.register_next_step_handler(msg, processar_ban)

    elif call.data.startswith("apr_"):
        _, target, val = call.data.split("_")
        ajustar_saldo(target, float(val))
        bot.send_message(target, f"✅ **Crédito Adicionado!** R$ {val} foram inseridos na sua conta.")
        bot.edit_message_caption(f"✅ Aprovado para o ID {target}", cid, mid)

def processar_ban(message):
    with open(DB_BANIDOS, "a") as f: f.write(f"{message.text.strip()}\n")
    bot.send_message(message.chat.id, f"✅ ID `{message.text}` banido!")

if __name__ == "__main__":
    print("🤖 LH STORE ONLINE E INTELIGENTE!")
    bot.infinity_polling()
