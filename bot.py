import telebot
import os

# Tokenni bevosita yozamiz yoki Railway "Variables" bo'limidan olamiz
API_TOKEN = '8399170869:AAF0077BXYDH6EyHqQ7nm_Ah2NsaJtTZYPU'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Salom akajon! Railway serverida Binary Bot ishga tushdi. 🚀\nSanoq sistemalari bo'yicha yordam beraman.")

@bot.message_handler(func=lambda message: True)
def convert_number(message):
    try:
        num = int(message.text)
        binary = bin(num).replace("0b", "")
        octal = oct(num).replace("0o", "")
        hexa = hex(num).replace("0x", "").upper()
        
        javob = (f"🔢 Son: {num}\n\n"
                 f"🔹 Ikkilik: {binary}\n"
                 f"🔸 Sakkizlik: {octal}\n"
                 f"💎 O'n oltilik: {hexa}")
        
        bot.reply_to(message, javob)
    except ValueError:
        bot.reply_to(message, "Iltimos, faqat butun son kiriting, akajon!")

if __name__ == "__main__":
    print("Bot Railway-da muvaffaqiyatli ishga tushdi...")
    bot.infinity_polling()
