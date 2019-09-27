#!python3

import time
import threading

import requests
from bs4 import BeautifulSoup

from selenium import webdriver

# この行は消していいです
import keys


class login(requests.Session):

    def __init__(self, **kwargs):
        super().__init__()

        uri_url = 'https://kym-web.ofc.kobe-u.ac.jp/campusweb'
        self.id = ''
        self.password = ''
        self.schedule = False

        #self.session = requests.session()
        self.res = self.get(uri_url)
        self.soup = BeautifulSoup(self.res.text, "html.parser")

        self._login_swither(**kwargs)

    def _login_swither(self, **kwargs):
        if len(kwargs) == 2:
            self.id = kwargs['id']
            self.password = kwargs['password']
        elif len(kwargs) == 3:
            self.id = kwargs['id']
            self.password = kwargs['password']
            self.schedule = kwargs['schedule']

        if self.schedule == True:
            self._login()
            self._schedule()
        else:
            self._login()

    def _login(self, **kwargs):

        self.back = self.soup.find(
            'div', class_='login').find('form').get('action')

        login_info = {
            'j_username': self.id,
            'j_password': self.password,
            '_eventId_proceed': 'ログイン',
            'back': self.back
        }
        adress = self.res.url
        res2 = self.post(adress, data=login_info)
        logined = BeautifulSoup(res2.text, "html.parser")

        login_info2 = {
            'RelayState': logined.find_all('input')[0].get('value'),
            'SAMLResponse': logined.find_all('input')[1].get('value'),
            'back': logined.find('form').get('action')
        }

        adress = logined.find('form').get('action')
        self.post(adress, data=login_info2)
        print('Sucsess')

    # 作りかけ
    def _extend(self):
        print('extend できないっす')

    def _schedule(self):
        wait = True
        interval = 60*15
        base_time = time.time()
        next_time = 0
        while True:
            t = threading.Thread(target=self._extend)
            t.start()
            if wait:
                t.join()
            next_time = ((base_time - time.time()) % interval) or interval
            time.sleep(next_time)


if __name__ == "__main__":

    # これだけでuriはうりぼーネットにログイン済みのCookieを持ったrequests.sessionと同じになります
    # Sessionと同じなので uri.get(アドレス)してもいいし何でもできます
    # keys.useridとkeys.passwdを適宜自分のものに置き換えてください
    uri = login(id=keys.userid,
                password=keys.passwd)
    res = uri.get('https://kym-web.ofc.kobe-u.ac.jp/campusweb')

    # ログインしたCookieの情報をseleniumに渡したいときは以下のようにします

    # とりまDriverの指定
    driver = webdriver.Chrome()
    # 一度なんか開いておかないとエラーが出る
    driver.get('https://example.com')

    # uriからCookieをもらう。辞書型で帰ってくる
    cookie = uri.cookies.get_dict()

    # 渡す
    for cookie_value in cookie:
        driver.add_cookie({'name': cookie_value,
                           'value': cookie[cookie_value],
                           'domain': 'kobe-u.ac.jp'})

    # ログイン後のページを表示
    driver.get('https://kym-web.ofc.kobe-u.ac.jp/campusweb')

    # driver.close()
