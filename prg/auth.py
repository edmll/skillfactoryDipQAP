import ast  # Импортируем модуль ast
import time  # Импортируем модуль time
import os  # Импортируем модуль os

from pages.base import BasePage  # Импортируем BasePage из модуля pages.base
from pages.locators import *  # Импортируем все локаторы из модуля pages.locators

class RegPage(BasePage):
    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)  # Вызываем конструктор родительского класса BasePage
        self.first_name = driver.find_element(*RegLocators.REG_FIRSTNAME)  # Находим элемент имени
        self.last_name = driver.find_element(*RegLocators.REG_LASTNAME)  # Находим элемент фамилии
        self.email = driver.find_element(*RegLocators.REG_ADDRESS)  # Находим элемент адреса электронной почты
        self.password = driver.find_element(*RegLocators.REG_PASSWORD)  # Находим элемент пароля
        self.pass_conf = driver.find_element(*RegLocators.REG_PASS_CONFIRM)  # Находим элемент подтверждения пароля
        self.btn = driver.find_element(*RegLocators.REG_REGISTER)  # Находим элемент кнопки регистрации

    def enter_firstname(self, value):
        self.first_name.send_keys(value)  # Вводим значение в поле имени

    def enter_lastname(self, value):
        self.last_name.send_keys(value)  # Вводим значение в поле фамилии

    def enter_email(self, value):
        self.email.send_keys(value)  # Вводим значение в поле адреса электронной почты

    def enter_password(self, value):
        self.password.send_keys(value)  # Вводим значение в поле пароля

    def enter_pass_conf(self, value):
        self.pass_conf.send_keys(value)  # Вводим значение в поле подтверждения пароля

    def btn_click(self):
        self.btn.click()  # Кликаем по кнопке регистрации


class AuthPage(BasePage):
    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)  # Вызываем конструктор родительского класса BasePage
        url = os.getenv('MAIN_URL') or 'https://b2c.passport.rt.ru'  # Получаем URL из переменной окружения или используем значение по умолчанию
        driver.get(url)  # Открываем URL в браузере
        self.username = driver.find_element(*AuthLocators.AUTH_USERNAME)  # Находим элемент имени пользователя
        self.password = driver.find_element(*AuthLocators.AUTH_PASS)  # Находим элемент пароля
        self.btn = driver.find_element(*AuthLocators.AUTH_BTN)  # Находим элемент кнопки входа
        self.reg_in = driver.find_element(*AuthLocators.AUTH_REG_IN)  # Находим элемент ссылки на страницу регистрации
        self.active_tab = driver.find_element(*AuthLocators.AUTH_ACTIVE_TAB)  # Находим элемент активной вкладки

    def enter_username(self, value):
        self.username.send_keys(value)  # Вводим значение в поле имени пользователя

    def enter_password(self, value):
        self.password.send_keys(value)  # Вводим значение в поле пароля

    def btn_click_enter(self):
        self.btn.click()  # Кликаем по кнопке входа
        time.sleep(10)  # Приостанавливаем выполнение программы на 10 секунд

    def enter_reg_page(self):
        self.reg_in.click()  # Кликаем по ссылке на страницу регистрации
        time.sleep(10)  # Приостанавливаем выполнение программы на 10 секунд

    def active_tab(self):
        self.active_tab()  # Вызываем метод active_tab() - возможно, здесь должно быть что-то иное

    def check_color(self, elem):
        rgba = elem.value_of_css_property('color')  # Получаем свойство цвета элемента
        r, g, b, alpha = ast.literal_eval(rgba.strip('rgba'))  # Разбираем RGBA-значение цвета
        hex_value = '#%02x%02x%02x' % (r, g, b)  # Преобразуем цвет в формат HEX
        return hex_value  # Возвращаем значение цвета


class NewPassPage(BasePage):
    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)  # Вызываем конструктор родительского класса BasePage
        url = 'https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/reset-credentials'  # Устанавливаем URL страницы
        driver.get(url)  # Открываем URL в браузере
        self.username = driver.find_element(*NewPassLocators.NEWPASS_ADDRESS)  # Находим элемент адреса электронной почты
        self.btn = driver.find_element(*NewPassLocators.NEWPASS_BTN_CONTINUE)  # Находим элемент кнопки "Продолжить"

    def enter_username(self, value):
        self.username.send_keys(value)  # Вводим значение в поле адреса электронной почты

    def btn_click_continue(self):
        self.btn.click()  # Кликаем по кнопке "Продолжить"
        time.sleep(10)  # Приостанавливаем выполнение программы на 10 секунд
