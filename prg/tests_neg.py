import time
import pytest
from pages.auth import AuthPage
from pages.settings import AuthLocators

# Общая функция для ввода пароля и подтверждения пароля
def input_new_pass(elem_new_pass, elem_conf_pass, new_pass):
    elem_new_pass.clear()
    elem_new_pass.send_keys(new_pass)
    time.sleep(3)
    elem_conf_pass.clear()
    elem_conf_pass.send_keys(new_pass)
    time.sleep(3)

# Метки для тестов
@pytest.mark.auth
@pytest.mark.negative

# Параметризованный тест для проверки авторизации с различными вводами
@pytest.mark.parametrize('username', [fake_phone, fake_login, invalid_ls, valid_phone, valid_email, valid_login],
                         ids=['fake phone', 'fake login', 'fake service account', 'valid phone', 'valid login', 'valid email'])
def test_auth_page_various_inputs(browser, username):
    page = AuthPage(browser)
    page.enter_username(username)
    page.enter_password(valid_password)
    page.btn_click_enter()
    browser.implicitly_wait(10)

    error_mess = browser.find_element(*AuthLocators.AUTH_FORM_ERROR)
    forgot_pass = browser.find_element(*AuthLocators.AUTH_FORGOT_PASSWORD)

    if username in [fake_phone, fake_login, invalid_ls]:
        # Проверка для фейковых входов
        assert error_mess.text == 'Неверный логин или пароль'
        assert page.check_color(forgot_pass) == '#ff4f12'
    else:
        # Проверка для валидных входов
        assert error_mess.text == 'Неверный логин или пароль'
        assert page.check_color(forgot_pass) == '#ff4f12'

# Тест для проверки авторизации с пустым номером телефона, почтой, логином или лицевым счетом
def test_auth_page_empty_inputs(browser):
    page = AuthPage(browser)
    page.enter_username('')
    page.enter_password(valid_password)
    page.btn_click_enter()
    browser.implicitly_wait(10)

    error_mess = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)

    # Проверяем, что сообщение об ошибке отображается корректно
    assert error_mess.text == 'Введите номер телефона' or error_mess.text == 'Введите адрес'

# Тест для проверки ввода разных паролей и проверок пароля
def test_password_checks(browser):
    page = AuthPage(browser)

    elem_new_pass = browser.find_element(*AuthLocators.NEWPASS_NEW_PASS)
    elem_conf_pass = browser.find_element(*AuthLocators.NEWPASS_NEW_PASS_CONFIRM)

    # 1. Новый пароль - менее 8 символов
    new_pass = valid_pass_reg[:7]
    input_new_pass(elem_new_pass, elem_conf_pass, new_pass)

    error_mess = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_mess.text == 'Длина пароля должна быть не менее 8 символов'

    # 2. Новый пароль - более 20 символов
    new_pass = valid_pass_reg[:7] * 3
    input_new_pass(elem_new_pass, elem_conf_pass, new_pass)

    error_mess = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_mess.text == 'Длина пароля должна быть не более 20 символов'

    # 3. Новый пароль - пароль не содержит заглавные буквы
    new_pass = valid_pass_reg.lower()
    input_new_pass(elem_new_pass, elem_conf_pass, new_pass)

    error_mess = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_mess.text == 'Пароль должен содержать хотя бы одну заглавную букву'

    # 4. Новый пароль - пароль не содержит строчные буквы
    new_pass = valid_pass_reg.upper()
    input_new_pass(elem_new_pass, elem_conf_pass, new_pass)

    error_mess = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_mess.text == 'Пароль должен содержать хотя бы одну прописную букву'

    # 5. Новый пароль - пароль включает в себя русскую букву
    new_pass = f'{valid_pass_reg}{generate_string_rus(1)}'
    input_new_pass(elem_new_pass, elem_conf_pass, new_pass)

    error_mess = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_mess.text == 'Пароль должен содержать только латинские буквы'

    # 6. Новый пароль - пароль не содержит ни одной цифры или спецсимвола
    new_pass = valid_pass_reg
    for i in new_pass:
        if i.isdigit() or i in special_chars():
            new_pass = new_pass.replace(i, 'x')
    input_new_pass(elem_new_pass, elem_conf_pass, new_pass)

    error_mess = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_mess.text == 'Пароль должен содержать хотя бы 1 спецсимвол или хотя бы одну цифру'

    # 7. Новый пароль отличается от пароля в поле 'Подтверждение пароля'.
    elem_new_pass.send_keys(Keys.COMMAND, 'a')
    elem_new_pass.send_keys(Keys.DELETE)
    new_pass = f'{valid_pass_reg[:8]}{generate_string_en(2)}'
    elem_new_pass.send_keys(new_pass)
    time.sleep(3)

    elem_conf_pass.send_keys(Keys.COMMAND, 'a')
    elem_conf_pass.send_keys(Keys.DELETE)
    new_conf_pass = f'{valid_pass_reg[:8]}{generate_string_en(4)}'
    elem_conf_pass.send_keys(new_conf_pass)
    time.sleep(3)

    browser.find_element(*AuthLocators.NEWPASS_BTN_SAVE).click()

    error_mess = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_mess.text == 'Пароли не совпадают'

    # 8. Новый пароль - идентичен предыдущему
    new_pass = valid_pass_reg
    input_new_pass(elem_new_pass, elem_conf_pass, new_pass)
    browser.find_element(*AuthLocators.NEWPASS_BTN_SAVE).click()

    error_mess = browser.find_element(*AuthLocators.AUTH_FORM_ERROR)
    assert error_mess.text == 'Этот пароль уже использовался, укажите другой пароль'
