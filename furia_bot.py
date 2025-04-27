import telebot
from telebot import types
import random
import time

# API Key do Bot
Chave_API = "CHAVE_API_TELEGRAM"
bot = telebot.TeleBot(Chave_API)

# URLs das fotos
FURIA_LOGO_URL = "https://i.ibb.co/cK2BSVhH/logo-furia.png"
FURIA_QUIZ_LOGO_URL = "https://i.ibb.co/5xFjrQyW/lgoo-furia-quiz.png"

# Curiosidades
curiosidades = [
    "👕 A FURIA já mandou um uniforme `rosa choque` de respeito!",
    "🌍 Já representou o Brasil nos maiores torneios de `CS` do mundo!",
    "💰 Faturou mais de `3 milhões de dólares` em prêmios!",
    "🎯 `KSCERATO` é um monstro do CS brasileiro!",
    "🔥 O estilo `agressivo` é a alma da FURIA!",
]

# Futebol e Kings League Info
futebol_info = (
    "⚽ **FURIA no Futebol** ⚽\n"
    "Tá voando no `Campeonato Brasileiro`! 🏆\n"
    "Preparada pra brilhar em torneios mundiais, a FURIA é a nova fera do Brasil!\n"
    "🔥 `Promessa braba` do futebol nacional!"
)

kings_league_info = (
    "👑 **Kings League Brasil 2025** 👑\n"
    "Rolando desde `29/03` na `Arena Kings League`, Guarulhos! 🏟️\n"
    "Rodadas semanais até maio, e a `FURIA FC` tá na briga!\n\n"
    "📅 **Próximos Jogos**:\n"
    "🆚 `FURIA FC x Galácticos` - *28/04*\n"
    "🆚 `FURIA FC x R10 Team` - *05/05*\n"
    "🆚 `FURIA FC x G3X` - *12/05*\n\n"
    "🌍 **Kings World Cup Nations**:\n"
    "Janeiro/2025, Itália. `Kaká` (Brasil) e `Jake Paul` (EUA) lideraram!\n"
    "Final no `Allianz Stadium`! 🏆"
)

# Quiz
quiz_perguntas = [
    {
        "pergunta": "Em que ano a FURIA foi fundada? 🐆",
        "opcoes": ["2017", "2018", "2019"],
        "correta": "2017"
    },
    {
        "pergunta": "Qual jogador é ícone da FURIA no CS? 🎯",
        "opcoes": ["KSCERATO", "FalleN", "Coldzera"],
        "correta": "KSCERATO"
    },
    {
        "pergunta": "Qual é o estilo da FURIA no jogo? 🔥",
        "opcoes": ["Jogo agressivo", "Jogo defensivo", "Jogo equilibrado"],
        "correta": "Jogo agressivo"
    }
]

quiz_estado = {}

# Funções Auxiliares
def redes_sociais_buttons():
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("🐦 Twitter", url="https://twitter.com/furiagg"),
        types.InlineKeyboardButton("📸 Instagram", url="https://instagram.com/furiagg")
    )
    markup.add(types.InlineKeyboardButton("🎥 YouTube", url="https://youtube.com/furia"))
    return markup

def quiz_buttons(opcoes):
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = [types.InlineKeyboardButton(text=opcao, callback_data=opcao) for opcao in opcoes]
    markup.add(*buttons)
    return markup

def enviar_pergunta(chat_id, user_id):
    if user_id not in quiz_estado:
        quiz_estado[user_id] = {"pergunta_atual": 0, "pontuacao": 0}

    estado = quiz_estado[user_id]
    pergunta_atual = estado["pergunta_atual"]

    if pergunta_atual >= len(quiz_perguntas):
        pontuacao = estado["pontuacao"]
        msg_final = (
            f"🏆 **Fim do Quiz!** 🏆\n"
            f"Pontuação: `{pontuacao}/{len(quiz_perguntas)}`!\n"
        )
        if pontuacao == len(quiz_perguntas):
            msg_final += "🔥 `Mestre da FURIA!` Você é brabo! 🐆\n"
        elif pontuacao >= len(quiz_perguntas) // 2:
            msg_final += "💪 `Quase lá!` Mandou bem, mas dá pra melhorar! 😎\n"
        else:
            msg_final += "😅 `Tá começando!` Bora aprender mais sobre a FURIA? 🖤\n"
        msg_final += "Bora tentar de novo? Digite **Sim** ou **Não**."

        try:
            bot.send_photo(chat_id, FURIA_QUIZ_LOGO_URL, caption=msg_final, parse_mode="Markdown")
        except Exception as e:
            bot.send_message(chat_id, f"{msg_final}\n❗ Ops, erro ao carregar o logo: {str(e).replace('_', '\\_')}.", parse_mode="Markdown")

        estado["aguardando_reinicio"] = True
        return

    pergunta = quiz_perguntas[pergunta_atual]
    texto = (
        f"❓ **Quiz FURIA - {pergunta_atual + 1}/{len(quiz_perguntas)}** ❓\n"
        f"`{pergunta['pergunta']}`\n\n"
        f"Escolha uma opção:"
    )
    bot.send_message(chat_id, texto, reply_markup=quiz_buttons(pergunta["opcoes"]), parse_mode="Markdown")

# Comando /start
@bot.message_handler(commands=['start'])
def menu(message):
    try:
        bot.send_photo(message.chat.id, FURIA_LOGO_URL, caption="🔥 **FURIA Esports na veia!** 🐆", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, f"❗ Ops, erro ao carregar o logo: {str(e).replace('_', '\\_')}. Bora pro rolê!", parse_mode="Markdown")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        "📊 Últimos jogos", "📅 Próximos jogos",
        "🐆 Sobre o time", "🌐 Redes sociais",
        "📚 Curiosidade", "⚽ Futebol da FURIA",
        "👑 Kings League", "❓ Quiz",
        "🔥 Torcer pela FURIA", "🎯 Status da Partida"
    )

    texto = (
        "🔥 **FuriaArenaBot tá ON!** 🔥\n"
        "Teu parceiro da *FURIA Esports*! 🐆\n"
        "Escolhe uma opção e bora detonar! 👇"
    )
    bot.send_message(message.chat.id, texto, reply_markup=markup, parse_mode="Markdown")

# Comando /torcer
@bot.message_handler(commands=['torcer'])
def torcer(message):
    torcida_msg = (
        "🚨 *A torcida da FURIA tá ON!* 🚨\n"
        "🎯 *Faz barulho!* Quem vai ganhar? *FURIAAAAA!* 🔥\n"
        "💥 Vamos juntos, galera! O time precisa de vocês! 🐆"
    )
    bot.send_message(message.chat.id, torcida_msg, parse_mode="Markdown")

# Comando /status
@bot.message_handler(commands=['status'])
def status_de_jogo(message):
    status = [
        "🎮 Partida em andamento: `FURIA 10 x 7 G2` - Round 18",
        "🎯 KSCERATO fez um `clutch 1v3`! 🔥",
        "💥 FURIA dominando o mapa `Inferno`!",
        "🚀 Vamos rumo à vitória, parça! 🐆"
    ]
    bot.send_message(message.chat.id, random.choice(status), parse_mode="Markdown")

# Callback do Quiz
@bot.callback_query_handler(func=lambda call: True)
def callback_quiz(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    resposta = call.data

    if user_id not in quiz_estado:
        bot.answer_callback_query(call.id, "❌ Quiz expirado! Usa o botão 'Quiz' pra começar.")
        return

    estado = quiz_estado[user_id]
    pergunta_atual = estado["pergunta_atual"]
    pergunta = quiz_perguntas[pergunta_atual]

    if resposta == pergunta["correta"]:
        estado["pontuacao"] += 1
        bot.answer_callback_query(call.id, "✅ `Acertou!` Bora pra próxima! 🔥")
    else:
        bot.answer_callback_query(call.id, f"❌ `Errou!` Era `{pergunta['correta']}`. Vamos lá! 😎")

    estado["pergunta_atual"] += 1
    enviar_pergunta(chat_id, user_id)

# Responder ao Menu
@bot.message_handler(func=lambda msg: True)
def responder(msg):
    texto = msg.text.strip().lower()
    chat_id = msg.chat.id
    user_id = msg.from_user.id

    if user_id in quiz_estado and quiz_estado[user_id].get("aguardando_reinicio"):
        if texto in ["sim", "s"]:
            del quiz_estado[user_id]
            bot.send_message(chat_id, "🔥 **Bora de novo!** Quiz reiniciado! 🐆", parse_mode="Markdown")
            enviar_pergunta(chat_id, user_id)
        elif texto in ["não", "nao", "n"]:
            del quiz_estado[user_id]
            menu(msg)
        else:
            bot.send_message(chat_id, "❗ Digite **Sim** ou **Não**, parça! 😎", parse_mode="Markdown")
        return

    if texto == "📊 últimos jogos":
        bot.send_message(chat_id, "📊 **Últimos Resultados** 📊\n🆚 `FURIA 2 x 1 NAVI`\n📅 *22/04/2025* - `IEM Katowice 2025`", parse_mode="Markdown")

    elif texto == "📅 próximos jogos":
        proxima_msg = (
            "🎮 **Próximos Jogos de CS** 🎮\n"
            "🆚 `FURIA x G2`\n📅 *24/04/2025* - `PGL Cluj-Napoca 2025`\n\n"
            "👑 **Kings League** 👑\n"
            "🆚 `FURIA FC x Galácticos` - *28/04*\n"
            "🆚 `FURIA FC x R10 Team` - *05/05*\n"
            "🆚 `FURIA FC x G3X` - *12/05*"
        )
        bot.send_message(chat_id, proxima_msg, parse_mode="Markdown")

    elif texto == "🐆 sobre o time":
        bot.send_message(chat_id, "🐆 **FURIA Esports** 🐆\nDesde `2017`, a FURIA é a fera do CS brasileiro!\n💥 Dominando palcos mundiais com `jogadas insanas`! 🖤", parse_mode="Markdown")

    elif texto == "🌐 redes sociais":
        bot.send_message(chat_id, "📲 **Conecta com a FURIA!** 📲\nFica por dentro de tudo nas redes! 👇", parse_mode="Markdown", reply_markup=redes_sociais_buttons())

    elif texto == "📚 curiosidade":
        bot.send_message(chat_id, f"📚 **Sabia disso?** 📚\n`{random.choice(curiosidades)}`", parse_mode="Markdown")

    elif texto == "⚽ futebol da furia":
        bot.send_message(chat_id, futebol_info, parse_mode="Markdown")

    elif texto == "👑 kings league":
        bot.send_message(chat_id, kings_league_info, parse_mode="Markdown")

    elif texto == "❓ quiz":
        enviar_pergunta(chat_id, user_id)

    elif texto == "🔥 torcer pela furia":
        torcer(msg)

    elif texto == "🎯 status da partida":
        status_de_jogo(msg)

    else:
        bot.send_message(chat_id, "❗ **Zoeira detectada!** Usa os botões do menu, parça! 😎", parse_mode="Markdown")

# Inicia o bot
bot.polling()
