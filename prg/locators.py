from selenium.webdriver.common.by import By  # Импортируем модуль By из selenium.webdriver.common

class AuthLocators:
    """Локаторы страницы авторизации"""
    AUTH_USERNAME = (By.ID, 'username')  # Локатор поля "Имя пользователя"
    AUTH_PASS = (By.ID, 'password')  # Локатор поля "Пароль"
    AUTH_BTN = (By.ID, 'kc-login')  # Локатор кнопки "Войти"
    AUTH_FORM_ERROR = (By.XPATH, "//span[@id='form-error-message']")  # Локатор сообщения об ошибке формы
    AUTH_MESS_ERROR = (By.CSS_SELECTOR, '.rt-input-container__meta--error')  # Локатор сообщения об ошибке
    AUTH_REG_IN = (By.XPATH, "//a[@id='kc-register']")  # Локатор ссылки "Зарегистрироваться"
    AUTH_REG_IN_TEMP_CODE = (By.ID, 'back_to_otp_btn')  # Локатор кнопки "Вернуться к одноразовому коду"
    AUTH_ACTIVE_TAB = (By.CSS_SELECTOR, '.rt-tab.rt-tab--small.rt-tab--active')  # Локатор активной вкладки
    AUTH_FORGOT_PASSWORD = (By.ID, 'forgot_password')  # Локатор ссылки "Забыли пароль"

class RegLocators:
    """Локаторы страницы регистрации"""
    REG_FIRSTNAME = (By.XPATH, "//input[@name='firstName']")  # Локатор поля "Имя"
    REG_LASTNAME = (By.XPATH, "//input[@name='lastName']")  # Локатор поля "Фамилия"
    REG_REGION = (By.XPATH, "//input[@autocomplete='new-password'][0]")  # Локатор поля "Регион" (похоже на ошибка)
    REG_ADDRESS = (By.ID, 'address')  # Локатор поля "Адрес"
    REG_PASSWORD = (By.ID, 'password')  # Локатор поля "Пароль"
    REG_PASS_CONFIRM = (By.XPATH, "//input[@id='password-confirm']")  # Локатор поля "Подтверждение пароля"
    REG_REGISTER = (By.XPATH, "//button[@name='register']")  # Локатор кнопки "Зарегистрироваться"
    REG_CARD_MODAL = (By.XPATH, "//h2[@class='card-modal__title']")  # Локатор заголовка модального окна

class NewPassLocators:
    """Локаторы страницы восстановления пароля"""
    NEWPASS_ADDRESS = (By.ID, 'username')  # Локатор поля "Адрес электронной почты"
    NEWPASS_BTN_CONTINUE = (By.ID, 'reset')  # Локатор кнопки "Продолжить"
    NEWPASS_ONETIME_CODE = (By.XPATH, '//input[@inputmode="numeric"]')  # Локатор поля "Одноразовый код"
    NEWPASS_NEW_PASS = (By.ID, 'password-new')  # Локатор поля "Новый пароль"
    NEWPASS_NEW_PASS_CONFIRM = (By.ID, 'password-confirm')  # Локатор поля "Подтверждение нового пароля"
    NEWPASS_BTN_SAVE = (By.XPATH, '//button[@id="t-btn-reset-pass"]')  # Локатор кнопки "Сохранить"
