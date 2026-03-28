import telebot
from telebot import types

API_TOKEN = '8399170869:AAF0077BXYDH6EyHqQ7nm_Ah2NsaJtTZYPU'
bot = telebot.TeleBot(API_TOKEN)

# Foydalanuvchi tanlovini saqlash uchun lug'at
user_states = {}

def main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton("⬅️ 2-likdan")
    item2 = types.KeyboardButton("⬅️ 8-likdan")
    item3 = types.KeyboardButton("⬅️ 10-likdan")
    item4 = types.KeyboardButton("⬅️ 16-likdan")
    item5 = types.KeyboardButton("🧮 Kalkulyator")
    item6 = types.KeyboardButton("📞 Biz bilan bog'lanish")
    markup.add(item1, item2, item3, item4, item5, item6)
    return markup

def convert_keyboard(exclude_base):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    bases = ["2-likka ➡️", "8-likka ➡️", "10-likka ➡️", "16-likka ➡️"]
    for b in bases:
        if exclude_base not in b:
            markup.add(types.KeyboardButton(b))
    markup.add(types.KeyboardButton("⬅️ Orqaga"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Sanoq sistemasini tanlang, akajon:", reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text

    if text == "⬅️ Orqaga":
        user_states.pop(chat_id, None)
        bot.send_message(chat_id, "Asosiy menyu:", reply_markup=main_keyboard())
        
    elif "likdan" in text:
        base = text.split("-")[0].replace("⬅️ ", "")
        user_states[chat_id] = {'from': int(base)}
        bot.send_message(chat_id, f"{base}-likdan qaysi biriga o'tkazamiz?", reply_markup=convert_keyboard(base))

    elif "likka ➡️" in text:
        target = text.split("-")[0]
        if chat_id in user_states:
            user_states[chat_id]['to'] = int(target)
            bot.send_message(chat_id, f"Endi {user_states[chat_id]['from']}-likdagi sonni kiriting:", reply_markup=types.ReplyKeyboardRemove())

    elif chat_id in user_states and 'to' in user_states[chat_id]:
        try:
            from_base = user_states[chat_id]['from']
            to_base = user_states[chat_id]['to']
            
            # Sonni o'nlikka o'tkazish
            val = int(message.text, from_base)
            
            # O'nlikdan kerakli sistemaga
            if to_base == 2: res = bin(val).replace("0b", "")
            elif to_base == 8: res = oct(val).replace("0o", "")
            elif to_base == 10: res = str(val)
            elif to_base == 16: res = hex(val).replace("0x", "").upper()
            
            bot.send_message(chat_id, f"✅ Natija: {res}", reply_markup=main_keyboard())
            user_states.pop(chat_id, None)
        except:
            bot.send_message(chat_id, "Xato kiritdingiz! Iltimos, sonni tekshiring.")

    elif text == "📞 Biz bilan bog'lanish":
        bot.send_message(chat_id, "Admin: @Sizning_Username")

bot.infinity_polling()
