import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import getpass

# Настройки браузера
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--incognito")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-infobars")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-notifications")
options.add_argument("--disable-automation")

# Функция для генерации случайных данных пользователя
def generate_random_user():
    fake = Faker()
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = fake.user_name() + str(random.randint(1000, 9999))
    password = fake.password()
    return first_name, last_name, username, password

# Функция для заполнения формы регистрации
def fill_registration_form(driver, first_name, last_name, username, password):
    driver.get("https://accounts.google.com/signup")
    driver.find_element(By.ID, "firstName").send_keys(first_name)
    driver.find_element(By.ID, "lastName").send_keys(last_name)
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.NAME, "Passwd").send_keys(password)
    driver.find_element(By.NAME, "ConfirmPasswd").send_keys(password)
    driver.find_element(By.XPATH, "//span[contains(text(),'Далее')]").click()

# Telegram bot setup

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Запустить веб-приложение Telegram", callback_data='start_web_app')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Хотите запустить веб-приложение для регистрации в Telegram?', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'start_web_app':
        # Здесь вы можете добавить логику для запуска веб-приложения Telegram
        await query.edit_message_text(text="Запускаем веб-приложение Telegram...")
        # Пример запуска веб-приложения через Selenium
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        first_name, last_name, username, password = generate_random_user()
        fill_registration_form(driver, first_name, last_name, username, password)
        time.sleep(10)
        driver.quit()

def main():
    telegram_token = getpass.getpass(prompt='Введите токен Telegram бота: ')
    
    application = ApplicationBuilder().token(telegram_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()

if __name__ == '__main__':
    main()
