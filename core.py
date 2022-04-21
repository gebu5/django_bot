from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium_proxy import set_settings
from Screenshot import Screenshot_Clipping
from utils import *
from random import randint


class Submiter:
    api_key = 'b46e6001ae026f57e89fa82f4b07b3f8'
    user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/96.0.4664.45 Safari/537.36')

    def __init__(self, bot, numbot, barcode, surname, givenname, passport, email, phone, delay, country, city, date, test_mode):
        self.delay = delay
        self.bot = bot
        self.driver = set_settings(numbot, Submiter.user_agent)
        self.barcode = barcode
        self.surname = surname
        self.givenname = givenname
        self.passport = passport
        self.email = email
        self.phone = phone
        self.country = country
        self.city = city
        self.date = date
        self.test_mode = test_mode

    def body(self, end):
        while True:
            if end.qsize():
                return None
            datas = self.first_submit()
            if datas:
                return datas
            time.sleep(self.delay)

    def first_submit(self):
        self.driver.get('https://evisaforms.state.gov/Instructions/SchedulingSystem.asp')
        time.sleep(1)

        self.driver = check_captcha(self.driver, Submiter.api_key, 0)

        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'buttontext'))
            WebDriverWait(self.driver, 5).until(element_present)
        except Exception as error:
            lprint('--Не прогрузилась страница, повтор.' + str(error))
            return False

        select = Select(self.driver.find_element(By.NAME, 'CountryCodeShow'))
        select.select_by_value(self.country)

        select = Select(self.driver.find_element(By.NAME, 'PostCodeShow'))
        select.select_by_value(self.city)
        self.driver.find_element(By.NAME, 'Submit').click()
        return self.second_submit()

    def second_submit(self):
        self.driver = check_captcha(self.driver, Submiter.api_key, 0)
        captcha = solve_captcha(self.driver, Submiter.api_key, 'needed')
        self.driver.execute_script('arguments[0].scrollIntoView(true);', self.driver.find_element(By.ID, 'CaptchaCode'))
        self.driver.find_element(By.ID, 'CaptchaCode').send_keys(captcha + Keys.ENTER)
        time.sleep(1)
        if 'Invalid CAPTCHA value entered.' in self.driver.page_source:
            self.driver.execute_script("window.history.go(-1)")
            captcha = solve_captcha(self.driver, Submiter.api_key, 'needed')
            self.driver.execute_script('arguments[0].scrollIntoView(true);',
                                       self.driver.find_element(By.ID, 'CaptchaCode'))
            self.driver.find_element(By.ID, 'CaptchaCode').clear()
            self.driver.find_element(By.ID, 'CaptchaCode').send_keys(captcha + Keys.ENTER)

        self.driver = check_captcha(self.driver, Submiter.api_key, 0)

        self.driver.find_element(By.NAME, 'nbarcode').send_keys(self.barcode)
        self.driver.find_element(By.ID, 'link4').click()

        self.driver = check_captcha(self.driver, Submiter.api_key, 0)
        return self.choose_date()

    def choose_date(self):
        self.driver = check_captcha(self.driver, Submiter.api_key, 0)
        select = Select(self.driver.find_element(By.NAME, 'nDate'))
        select.select_by_value(self.date)
        time.sleep(1)
        tbody = self.driver.find_elements(By.TAG_NAME, 'tbody')
        available_datas = tbody[-2].find_elements(By.TAG_NAME, 'a')

        if not available_datas:
            #print('Нет доступных дат')
            return False

        available_datas[randint(0, len(available_datas) - 1)].click()
        self.driver = check_captcha(self.driver, Submiter.api_key, 0)
        return self.final_submit()

    def final_submit(self):
        tbody = self.driver.find_elements(By.TAG_NAME, 'tbody')
        available_times = tbody[-2].find_elements(By.TAG_NAME, 'input')
        if not available_times:
            print('--Нет доступного времени для записи--')
            return False

        available_times[randint(0, len(available_times) - 1)].click()

        self.driver.find_element(By.ID, 'link8b').send_keys(self.surname)
        self.driver.find_element(By.ID, 'link9b').send_keys(self.givenname)
        self.driver.find_element(By.ID, 'link10b').send_keys(self.passport)
        self.driver.find_element(By.ID, 'link11b').send_keys(self.email)
        self.driver.find_element(By.ID, 'link12b').send_keys(self.phone)
        submit = self.driver.find_element(By.ID, 'linkSubmit')
        self.driver.execute_script('arguments[0].scrollIntoView(true);', submit)

        captcha = solve_captcha(self.driver, Submiter.api_key, 'needed')
        self.driver.find_element(By.ID, 'CaptchaCode').send_keys(captcha)

        self.driver.find_element(By.ID, 'confidentiality').click()

        self.send_file_telegram()

        submit.click()
        time.sleep(1)
        if 'Invalid CAPTCHA value entered.' in self.driver.page_source:
            self.driver.execute_script("window.history.go(-1)")
            captcha = solve_captcha(self.driver, Submiter.api_key, 'needed')
            self.driver.find_element(By.ID, 'CaptchaCode').clear()
            self.driver.find_element(By.ID, 'CaptchaCode').send_keys(captcha)
            submit = self.driver.find_element(By.ID, 'linkSubmit')
            self.driver.execute_script('arguments[0].scrollIntoView(true);', submit)
            submit.click()

        self.driver = check_captcha(self.driver, Submiter.api_key, 0)

        if 'PLEASE PRINT THIS PAGE FOR YOUR RECORD' in self.driver.page_source:
            self.send_file_telegram()
            return True

        lprint('Ошибка во время регистрации!')
        return 'Bad acc'

    def send_file_telegram(self):
        tries = 0
        file_name = f'{self.surname} {self.givenname}.pdf'
        while True:
            ss = Screenshot_Clipping.Screenshot()
            try:
                ss.full_Screenshot(self.driver, save_path=r'./reports', image_name=file_name)
                break
            except Exception as error:
                print('Try screenshot')
                tries += 1
                if tries == 3:
                    lprint('Cant screenshot:' + str(error))
                    raise RuntimeError('Cant screenshot')
                time.sleep(2)

        CHANNEL_NAME = '@testing_bottt' if self.test_mode else '@bottestvisa'
        self.bot.send_document(CHANNEL_NAME, document=open(f'reports/{file_name}', 'rb'))
        return True
