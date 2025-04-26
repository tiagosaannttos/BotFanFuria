import telebot
from telebot import types
import random
import time

Chave_API = "CHAVE_API_TELEGRAM"

bot = telebot.TeleBot(Chave_API)

# URLs das fotos
FURIA_LOGO_URL = "https://i.ibb.co/cK2BSVhH/logo-furia.png"  # Foto para o início (/start)
FURIA_QUIZ_LOGO_URL = "https://i.ibb.co/5xFjrQyW/lgoo-furia-quiz.png"  # Substitua por um link válido para a foto do quiz

# Lista de curiosidades
curiosidades = [
    "👕 A FURIA já mandou um uniforme `rosa choque` de respeito!",
    "🌍 Já representou o Brasil nos maiores torneios de `CS` do mundo!",
    "💰 Faturou mais de `3 milhões de dólares` em prêmios!",
    "🎯 `KSCERATO` é um monstro do CS brasileiro!",
    "🔥 O estilo `agressivo` é a alma da FURIA!",
]

# Informações sobre o futebol da FURIA
futebol_info = (
    "⚽ **FURIA no Futebol** ⚽\n"
    "Tá voando no `Campeonato Brasileiro`! 🏆\n"
    "Preparada pra brilhar em torneios mundiais, a FURIA é a nova fera do Brasil!\n"
    "🔥 `Promessa braba` do futebol nacional!"
)

# Informações atualizadas da Kings League
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

# Perguntas do quiz
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

# Dicionário para rastrear o estado do quiz por usuário
quiz_estado = {}

# Comando /start - Mostra o logo inicial e o menu
@bot.message_handler(commands=['start'])
def menu(message):
    # Enviar o logo inicial da FURIA
    try:
        bot.send_photo(
            message.chat.id,
            FURIA_LOGO_URL,  # Foto do início
            caption="🔥 **FURIA Esports na veia!** 🐆",
            parse_mode="Markdown"
        )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❗ Ops, erro ao carregar o logo: {str(e).replace('_', '\\_')}. Mas bora pro rolê!",
            parse_mode="Markdown"
        )

    # Mostrar o menu
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📊 Últimos jogos", "📅 Próximos jogos")
    markup.add("🐆 Sobre o time", "🌐 Redes sociais")
    markup.add("📚 Curiosidade", "⚽ Futebol da FURIA")
    markup.add("👑 Kings League", "❓ Quiz")

    texto = (
        "🔥 **FuriaArenaBot tá ON!** 🔥\n"
        "Teu parceiro da *FURIA Esports*! 🐆\n"
        "Escolhe uma opção e bora detonar! 👇"
    )
    bot.send_message(message.chat.id, texto, reply_markup=markup, parse_mode="Markdown")

# Função para criar botões inline das redes sociais
def redes_sociais_buttons():
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("🐦 Twitter", url="https://twitter.com/furiagg"),
        types.InlineKeyboardButton("📸 Instagram", url="https://instagram.com/furiagg")
    )
    markup.add(types.InlineKeyboardButton("🎥 YouTube", url="https://youtube.com/furia"))
    return markup

# Função para criar botões inline do quiz
def quiz_buttons(opcoes):
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = [types.InlineKeyboardButton(text=opcao, callback_data=opcao) for opcao in opcoes]
    markup.add(*buttons)
    return markup

# Função para iniciar ou continuar o quiz
def enviar_pergunta(chat_id, user_id):
    if user_id not in quiz_estado:
        quiz_estado[user_id] = {"pergunta_atual": 0, "pontuacao": 0}

    estado = quiz_estado[user_id]
    pergunta_atual = estado["pergunta_atual"]

    if pergunta_atual >= len(quiz_perguntas):
        # Fim do quiz
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

        # Enviar o logo do quiz
        try:
            bot.send_photo(
                chat_id,
                FURIA_QUIZ_LOGO_URL,  # Foto do quiz
                caption=msg_final,
                parse_mode="Markdown"
            )
        except Exception as e:
            bot.send_message(
                chat_id,
                f"{msg_final}\n❗ Ops, erro ao carregar o logo: {str(e).replace('_', '\\_')}.",
                parse_mode="Markdown"
            )

        estado["aguardando_reinicio"] = True  # Marcar que está esperando Sim/Não
        return

    # Enviar pergunta
    pergunta = quiz_perguntas[pergunta_atual]
    texto = (
        f"❓ **Quiz FURIA - {pergunta_atual + 1}/{len(quiz_perguntas)}** ❓\n"
        f"`{pergunta['pergunta']}`\n\n"
        f"Escolha uma opção:"
    )
    bot.send_message(
        chat_id,
        texto,
        reply_markup=quiz_buttons(pergunta["opcoes"]),
        parse_mode="Markdown"
    )

# Lidar com respostas do quiz
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

    # Verificar resposta
    if resposta == pergunta["correta"]:
        estado["pontuacao"] += 1
        bot.answer_callback_query(call.id, "✅ `Acertou!` Bora pra próxima! 🔥")
    else:
        bot.answer_callback_query(call.id, f"❌ `Errou!` Era `{pergunta['correta']}`. Vamos lá! 😎")

    # Avançar para próxima pergunta
    estado["pergunta_atual"] += 1
    enviar_pergunta(chat_id, user_id)

# Função principal para responder às opções do menu
@bot.message_handler(func=lambda msg: True)
def responder(msg):
    texto = msg.text.strip().lower()  # Normalizar texto pra minúsculas
    chat_id = msg.chat.id
    user_id = msg.from_user.id

    # Verificar se está esperando Sim/Não do quiz
    if user_id in quiz_estado and quiz_estado[user_id].get("aguardando_reinicio"):
        if texto in ["sim", "s"]:
            del quiz_estado[user_id]  # Resetar estado
            bot.send_message(chat_id, "🔥 **Bora de novo!** Quiz reiniciado! 🐆", parse_mode="Markdown")
            enviar_pergunta(chat_id, user_id)
        elif texto in ["não", "nao", "n"]:
            del quiz_estado[user_id]  # Resetar estado
            bot.send_message(
                chat_id,
                "😎 **Beleza, parça!** Usa o menu pra continuar curtindo a FURIA! 👇",
                parse_mode="Markdown",
                reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
                    "📊 Últimos jogos", "📅 Próximos jogos",
                    "🐆 Sobre o time", "🌐 Redes sociais",
                    "📚 Curiosidade", "⚽ Futebol da FURIA",
                    "👑 Kings League", "❓ Quiz"
                )
            )
        else:
            bot.send_message(chat_id, "❗ Digite **Sim** ou **Não**, parça! 😎", parse_mode="Markdown")
        return

    # Respostas normais do menu
    if texto == "📊 últimos jogos":
        bot.send_message(
            chat_id,
            "📊 **Últimos Resultados** 📊\n"
            "🆚 `FURIA 2 x 1 NAVI`\n"
            "📅 *22/04/2025* - `IEM Katowice 2025`",
            parse_mode="Markdown"
        )

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
        bot.send_message(
            chat_id,
            "🐆 **FURIA Esports** 🐆\n"
            "Desde `2017`, a FURIA é a fera do CS brasileiro!\n"
            "💥 Dominando palcos mundiais com `jogadas insanas`! 🖤",
            parse_mode="Markdown"
        )

    elif texto == "🌐 redes sociais":
        bot.send_message(
            chat_id,
            "📲 **Conecta com a FURIA!** 📲\n"
            "Fica por dentro de tudo nas redes! 👇",
            parse_mode="Markdown",
            reply_markup=redes_sociais_buttons()
        )

    elif texto == "📚 curiosidade":
        bot.send_message(
            chat_id,
            f"📚 **Sabia disso?** 📚\n`{random.choice(curiosidades)}`",
            parse_mode="Markdown"
        )

    elif texto == "⚽ futebol da furia":
        bot.send_message(chat_id, futebol_info, parse_mode="Markdown")

    elif texto == "👑 kings league":
        bot.send_message(chat_id, kings_league_info, parse_mode="Markdown")

    elif texto == "❓ quiz":
        enviar_pergunta(chat_id, user_id)

    else:
        bot.send_message(
            chat_id,
            "❗ **Zoeira detectada!** Usa os botões do menu, parça! 😎",
            parse_mode="Markdown"
        )

# Inicia o bot
bot.polling()