import telebot
from telebot import types
import random
import time

Chave_API = "7661002564:AAFGRUsMRP-PyXC7uX3bL8Jr3Yl22_azlEQ"

bot = telebot.TeleBot(Chave_API)

# Lista de curiosidades
curiosidades = [
    "👕 A FURIA já teve uniforme rosa!",
    "🌍 A FURIA já participou dos maiores torneios de CS do mundo!",
    "💰 O time já conquistou mais de 3 milhões de dólares em prêmios.",
    "🎯 KSCERATO é considerado um dos melhores jogadores brasileiros!",
    "🔥 O estilo agressivo de jogo é marca registrada da FURIA.",
]

# Informações sobre o futebol da FURIA
futebol_info = (
    "⚽ A FURIA está jogando atualmente no Campeonato Brasileiro de Futebol e também está em fase de preparação "
    "para disputar torneios internacionais. A equipe está ganhando destaque no cenário e se firmando como uma das promessas "
    "no futebol brasileiro!"
)

# Informações atualizadas da Kings League
kings_league_info = (
    "👑 A *Kings League Brasil* começou em 29 de março de 2025, na Arena Kings League, em Guarulhos, SP. "
    "A competição vai até maio com rodadas semanais. A FURIA FC é uma das equipes participantes!\n\n"
    "*Próximos jogos da FURIA FC na Kings League:*\n"
    "📅 28/04 - FURIA FC x Galácticos\n"
    "📅 05/05 - FURIA FC x R10 Team\n"
    "📅 12/05 - FURIA FC x G3X\n\n"
    "🌍 A *Kings World Cup Nations* rolou em janeiro de 2025 na Itália, com seleções lideradas por Kaká (Brasil) e Jake Paul (EUA). "
    "A final aconteceu no Allianz Stadium, em Turim!"
)

# Comando /start - Mostra o menu com botões
@bot.message_handler(commands=['start'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📊 Últimos jogos", "📅 Próximos jogos")
    markup.row("🐆 Sobre o time", "🌐 Redes sociais")
    markup.row("📚 Curiosidade", "⚽ Futebol da FURIA")
    markup.row("👑 Kings League", "❓ Quiz")

    texto = (
        "🔥 *Bem-vindo ao FuriaArenaBot!* 🔥\n"
        "Sou seu assistente da FURIA Esports!\n\n"
        "Escolha uma das opções abaixo:"
    )
    bot.send_message(message.chat.id, texto, reply_markup=markup, parse_mode="Markdown")

# Função principal para responder às opções do menu
@bot.message_handler(func=lambda msg: True)
def responder(msg):
    texto = msg.text.strip()

    if texto == "📊 Últimos jogos":
        bot.send_message(msg.chat.id, "🆚 FURIA 2 x 1 NAVI\n📅 22/04/2025 - IEM Katowice 2025")

    elif texto == "📅 Próximos jogos":
        proxima_msg = (
            "*🎮 Próximos jogos de CS:*\n"
            "🆚 FURIA x G2\n📅 24/04/2025 - PGL Cluj-Napoca 2025\n\n"
            "*👑 Próximos jogos da Kings League:*\n"
            "🆚 FURIA FC x Galácticos\n📅 28/04/2025\n"
            "🆚 FURIA FC x R10 Team\n📅 05/05/2025\n"
            "🆚 FURIA FC x G3X\n📅 12/05/2025"
        )
        bot.send_message(msg.chat.id, proxima_msg, parse_mode="Markdown")

    elif texto == "🐆 Sobre o time":
        bot.send_message(
            msg.chat.id,
            "🐆 A FURIA é um dos maiores times de CS do Brasil!\n💥 Fundada em 2017, já brilhou nos maiores palcos do mundo."
        )

    elif texto == "🌐 Redes sociais":
        bot.send_message(
            msg.chat.id,
            "📲 Redes Sociais da FURIA:\n"
            "🔗 Twitter: https://twitter.com/furiagg\n"
            "🔗 Instagram: https://instagram.com/furiagg\n"
            "🔗 YouTube: https://youtube.com/furia"
        )

    elif texto == "📚 Curiosidade":
        bot.send_message(msg.chat.id, f"📚 {random.choice(curiosidades)}")

    elif texto == "⚽ Futebol da FURIA":
        bot.send_message(msg.chat.id, futebol_info)

    elif texto == "👑 Kings League":
        bot.send_message(msg.chat.id, kings_league_info, parse_mode="Markdown")

    elif texto == "❓ Quiz":
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add("2017", "2018", "2019")
        bot.send_message(msg.chat.id, "❓ Em que ano a FURIA foi fundada?", reply_markup=markup)

    elif texto in ["2017", "2018", "2019"]:
        if texto == "2017":
            bot.send_message(msg.chat.id, "✅ Acertou! A FURIA foi fundada em 2017.")
        else:
            bot.send_message(msg.chat.id, "❌ Errou! Foi em 2017.")

    else:
        bot.send_message(msg.chat.id, "❗ Opção inválida. Por favor, use os botões.")

# Inicia o bot
bot.polling()