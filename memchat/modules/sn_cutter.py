from main import bot

def sn_cutter(message):
    if message.text and message.text[0] in "SЫ":
        sn = message.text[1:]
        bot.send_message(message.chat.id, sn)
    else:
        bot.send_message(message.chat.id, f"Это точно серийный номер? ({message.text})")