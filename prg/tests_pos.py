import pickle
import time
import pytest
from pages.auth import AuthPage, RegPage
from pages.registration_email import RegistrationEmail
from pages.settings import (
    valid_phone, valid_login, valid_password, valid_email, valid_pass_reg, fake_firstname, fake_lastname, fake_password
)
from selenium.webdriver.common.by import By

# Определим константы для идентификации тестов
AUTH_MARKS = [pytest.mark.auth, pytest.mark.positive, pytest.mark.xfail]
REG_MARKS = [pytest.mark.reg, pytest.mark.positive]
NEWPASS_MARKS = [pytest.mark.newpass, pytest.mark.positive]

# Тест для проверки активного таба
@pytest.mark.parametrize('username', [valid_phone, valid_email, valid_login, invalid_ls], ids=['phone', 'email', 'login', 'ls'])
@pytest.mark.usefixtures("browser")
def test_active_tab(browser, username):
    page = AuthPage(browser)
    page.enter_username(username)
    page.enter_password(valid_password)
    active_tab_text = {
        valid_phone: 'Телефон',
        valid_email: 'Почта',
        valid_login: 'Логин',
        invalid_ls: 'Лицевой счет'
    }
    assert browser.find_element(*AuthLocators.AUTH_ACTIVE_TAB).text == active_tab_text[username]

# Тест для проверки авторизации по номеру телефона и логину
@pytest.mark.parametrize('username', [valid_phone, valid_login], ids=['valid phone', 'valid login'])
@pytest.mark.usefixtures("browser")
def test_auth_page_phone_login_valid(browser, username):
    page = AuthPage(browser)
    page.enter_username(username)
    page.enter_password(valid_password)
    page.btn_click_enter()
    assert page.get_relative_link() == '/account_b2c/page'

# Тест для проверки авторизации по почте и паролю
@pytest.mark.usefixtures("browser")
def test_auth_page_email_valid(browser):
    page = AuthPage(browser)
    page.enter_username(valid_email)
    page.enter_password(valid_pass_reg)
    time.sleep(25)
    page.btn_click_enter()
    page.driver.save_screenshot('auth_by_email.png')
    with open('my_cookies.txt', 'wb') as cookies:
        pickle.dump(browser.get_cookies(), cookies)
    assert page.get_relative_link() == '/account_b2c/page'

# Класс для тестирования регистрации
class TestRegistration:
    def setup_class(self):
        self.result_email, self.status_email = RegistrationEmail().get_api_email()
        self.email_reg = self.result_email[0]

    @pytest.mark.usefixtures("browser")
    @pytest.mark.reg
    @pytest.mark.positive
    def test_get_registration_valid(browser):
        sign_at = self.email_reg.find('@')
        mail_name = self.email_reg[0:sign_at]
        mail_domain = self.email_reg[sign_at + 1:len(self.email_reg)]
        assert self.status_email == 200, 'status_email error'
        assert len(self.result_email) > 0, 'len(result_email) > 0 -> error'
        page = AuthPage(browser)
        page.enter_reg_page()
        browser.implicitly_wait(2)
        assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'
        page = RegPage(browser)
        page.enter_firstname(fake_firstname)
        browser.implicitly_wait(5)
        page.enter_lastname(fake_lastname)
        browser.implicitly_wait(5)
        page.enter_email(self.email_reg)
        browser.implicitly_wait(3)
        page.enter_password(fake_password)
        browser.implicitly_wait(3)
        page.enter_pass_conf(fake_password)
        browser.implicitly_wait(3)
        page.btn_click()
        time.sleep(30)
        result_id, status_id = RegistrationEmail().get_id_letter(mail_name, mail_domain)
        id_letter = result_id[0].get('id')
        assert status_id == 200, "status_id error"
        assert id_letter > 0, "id_letter > 0 error"
        result_code, status_code = RegistrationEmail().get_reg_code(mail_name, mail_domain, str(id_letter))
        text_body = result_code.get('body')
        reg_code = text_body[text_body.find('Ваш код : ') + len('Ваш код : '): text_body.find('Ваш код : ') + len('Ваш код : ') + 6]
        assert status_code == 200, "status_code error"
        assert reg_code != '', "reg_code != [] error"
        reg_digit = [int(char) for char in reg_code]
        browser.implicitly_wait(30)
        for i in range(0, 6):
            browser.find_elements(By.XPATH, '//input[@inputmode="numeric"]')[i].send_keys(reg_code[i])
            browser.implicitly_wait(5)
        assert page.get_relative_link() == '/account_b2c/page'
        page.driver.save_screenshot('reg_done.png')
        with open(r"../prg/Settings.py", 'r', encoding='utf8') as file:
            lines = []
            for line in file.readlines():
                if 'valid_email' in line:
                    lines.append(f"valid_email = '{str(self.email_reg)}'\n")
                elif 'valid_pass_reg' in line:
                    lines.append(f"valid_pass_reg = '{fake_password}'\n")
                else:
                    lines.append(line)
        with open(r"../prg/Settings.py", 'w', encoding='utf8') as file:
            file.writelines(lines)

@pytest.mark.usefixtures("browser")
@pytest.mark.newpass
@pytest.mark.positive
def test_forgot_password_page(browser):
    sign_at = valid_email.find('@')
    mail_name = valid_email[0:sign_at]
    mail_domain = valid_email[sign_at + 1:len(valid_email)]
    page = NewPassPage(browser)
    page.enter_username(valid_email)
    time.sleep(25)
    page.btn_click_continue()
    time.sleep(30)
    result_id, status_id = RegistrationEmail().get_id_letter(mail_name, mail_domain)
    id_letter = result_id[0].get('id')
    assert status_id == 200, "status_id error"
    assert id_letter > 0, "id_letter > 0 error"
    result_code, status_code = RegistrationEmail().get_reg_code(mail_name, mail_domain, str(id_letter))
    text_body = result_code.get('body')
    reg_code = text_body[text_body.find('Ваш код: ') + len('Ваш код: '): text_body.find('Ваш код: ') + len('Ваш код: ') + 6]
    assert status_code == 200, "status_code error"
    assert reg_code != '', "reg_code != [] error"
    reg_digit = [int(char) for char in reg_code]
    browser.implicitly_wait(30)
    for i in range(0, 6):
        browser.find_elements(*NewPassLocators.NEWPASS_ONETIME_CODE)[i].send_keys(reg_code[i])
        browser.implicitly_wait(5)
    time.sleep(10)
    new_pass = fake_password
    browser.find_element(*NewPassLocators.NEWPASS_NEW_PASS).send_keys(new_pass)
    time.sleep(3)
    browser.find_element(*NewPassLocators.NEWPASS_NEW_PASS_CONFIRM).send_keys(new_pass)
    browser.find_element(*NewPassLocators.NEWPASS_BTN_SAVE).click()
    time.sleep(60)
    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/authenticate'
    with open(r"../prg/settings.py", 'r', encoding='utf8') as file:
        lines = []
        for line in file.readlines():
            if 'valid_pass_reg' in line:
                lines.append(f"valid_pass_reg = '{fake_password}'\n")
            else:
                lines.append(line)
    with open(r"../prg/settings.py", 'w', encoding='utf8') as file:
        file.writelines(lines)
