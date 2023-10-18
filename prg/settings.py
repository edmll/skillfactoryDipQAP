# Загрузка конфигурации из файла .env
import os
from dotenv import load_dotenv
from faker import Faker
import string

load_dotenv()

# Инициализация генератора случайных данных на основе фейковых данных
fake_ru = Faker('ru_RU')
fake_firstname = fake_ru.first_name()
fake_lastname = fake_ru.last_name()
fake_phone = fake_ru.phone_number()
fake = Faker()
fake_password = fake.password()
fake_login = fake.user_name()
fake_email = fake.email()

# Получение действующих данных для авторизации из переменных окружения
valid_phone = os.getenv('phone')
valid_login = os.getenv('login')
valid_password = os.getenv('password')
invalid_ls = '242010005665'

# Предопределенные валидные данные для авторизации
valid_email = 'm0dfha@wuuvo.com'
valid_pass_reg = '!A$A&BccA2'

# Функция для генерации строки с символами русского алфавита
def generate_string_rus(n):
    return 'б' * n

# Функция для генерации строки с символами английского алфавита
def generate_string_en(n):
    return 'x' * n

# Функция возвращает английские символы
def english_chars():
    return 'qwertyuiopasdfghjklzxcvbnm'

# Функция возвращает русские символы
def russian_chars():
    return 'абвгдеёжзиклмнопрстуфхцчшщъыьэюя'

# Функция возвращает 20 популярных китайских иероглифов
def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'

# Функция возвращает специальные символы
def special_chars():
    return f'{string.punctuation}'
