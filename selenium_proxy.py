import json
import random
import zipfile
import os

from random import randint
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def set_settings(numbot, user_agent):
    blocking_hosts = (
        '*.facebook.net',
        '*.facebook.com',
        '*.google-analytics.com',
        'mc.yandex.ru',
        'vk.com')
    chrome_options = Options()
    proxy = set_proxy(chrome_options, numbot)
    if proxy:
        chrome_options = proxy
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument(f'user-agent={user_agent}')

    stringed_rules = [f'MAP {host} 127.0.0.1' for host in blocking_hosts]
    to_args = ', '.join(stringed_rules)
    chrome_options.add_argument(f'--host-rules={to_args}')

    #chrome_options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    #chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1100, 900)
    #driver = webdriver.Chrome(executable_path=f'{dir}/chromedriver', options=chrome_options)
    return driver


def set_proxy(chrome_options, numbot):
    proxy_type, proxy_host, proxy_port, proxy_user, proxy_pass = get_proxy(numbot)
    if not proxy_type:
        return False

    manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "activeTab",
                "proxy",
                "tabs",
                "debugger",
                "unlimitedStorage",
                "storage",
                "http://*/*",
                "https://*/*",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            """
    manifest_json += """"web_accessible_resources": ["/listen_response.js"],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version": "22.0.0"
        }
        """
    background_js = ''
    background_js += """
            var config = {
                    mode: "fixed_servers",
                    rules: {
                      singleProxy: {
                        scheme: "%s",
                        host: "%s",
                        port: parseInt(%s)
                      },
                      bypassList: ["localhost"]
                    }
                  };
            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
            chrome.webRequest.onAuthRequired.addListener(
                        function callbackFn(details) {
                            return {
                                authCredentials: {
                                    username: "%s",
                                    password: "%s"
                                }
                            };
                        },
                        {urls: ["<all_urls>"]},
                        ['blocking']
            );
            """ % (proxy_type, proxy_host, proxy_port, proxy_user, proxy_pass)

    dir = os.path.abspath(os.curdir)
    print(dir)
    pluginfile = f'{dir}/extensions/ext_' + str(numbot) + '.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr('manifest.json', manifest_json)
        zp.writestr('background.js', background_js)
        chrome_options.add_extension(pluginfile)
    return chrome_options


def get_proxy(numbot):
    with open('proxies.json', 'r') as proxiesjson:
        proxies = json.load(proxiesjson)
    if not proxies:
        return [0] * 5

    proxy = proxies[random.randint(0, len(proxies))]

    return parse_proxy(proxy)


def parse_proxy(proxy):
    proxy_type = 'http'
    if type(proxy).__name__ == 'str':
        proxy_user = ''
        proxy_pass = ''
        if r'://' in proxy:
            proxy_type, proxy = proxy.split(r'://')
        if '@' in proxy:
            proxy, logpass = proxy.split('@')
            proxy_user, proxy_pass = logpass.split(':')
        spl_proxy = proxy.split(':')
        proxy_host = spl_proxy[0]
        proxy_port = int(spl_proxy[1])
    elif len(proxy) == 5:
        proxy_type, proxy_host, proxy_port, proxy_user, proxy_pass = proxy
    elif len(proxy) == 4:
        proxy_host, proxy_port, proxy_user, proxy_pass = proxy
    elif len(proxy) == 3:
        proxy_type, proxy_host, proxy_port = proxy
        proxy_user = ''
        proxy_pass = ''
    elif len(proxy) == 2:
        proxy_host, proxy_port = proxy
        proxy_user = ''
        proxy_pass = ''
    else:
        print('WTF: proxies.json')
        return None
    return proxy_type, proxy_host, proxy_port, proxy_user, proxy_pass
