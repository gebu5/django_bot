import time
import requests
import json
import io
import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def solve_captcha(driver, api_key, type='accident'):
    if type == 'accident':
        images = driver.find_elements(By.TAG_NAME, 'img')
        captcha_image = images[1].screenshot_as_png
    else:
        image = driver.find_element(By.ID, 'frmconinput_CaptchaImage')
        captcha_image = image.screenshot_as_png
    im_io = io.BytesIO(captcha_image)
    solved_captcha = solve_image(api_key, im_io)
    return solved_captcha


def check_captcha(driver, api_key, numb_try):
    if numb_try == 2:
        print('Не пройдена капча')
        raise RuntimeError('Captcha')
    time.sleep(1)
    if 'What code is in the image?' in driver.page_source:
        captcha = solve_captcha(driver, api_key)
        driver.find_element(By.ID, 'ans').send_keys(captcha + Keys.ENTER)
        time.sleep(1)
        if 'What code is in the image?' in driver.page_source:
            check_captcha(driver, api_key, numb_try + 1)
    return driver


def solve_image(api_key, file, format_='png'):
    params = {
        'key': api_key,
        'method': 'post',
        'json': '1',
    }
    files = {'file': (f'captcha.{format_}', file)}
    r = requests.post('https://rucaptcha.com/in.php', data=params, files=files)
    page = r.text
    response = json.loads(r.text)
    status = response['status']
    if status:
        id = response['request']
        params = {
            'id': id,
            'action': 'get',
            'json': '1',
            'key': api_key
        }
        time.sleep(3)
        for i in range(20):
            time.sleep(i * 0.75)
            r = requests.get('https://rucaptcha.com/res.php', params=params)
            page = r.text
            response = json.loads(page)
            status = response['status']
            request = response['request']
            if status:
                return request
            if request != 'CAPCHA_NOT_READY':
                raise RuntimeError(f'Captcha error: {request}')
    else:
        raise RuntimeError(f'Captcha quest didn\'t started: {response}')
    print('rucaptcha.com: ' + page)


def lprint(mes):
    print(mes)
    with open('log.txt', 'a') as f:
        f.write(datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + ':  ' + mes + '\n')

