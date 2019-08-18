import time
import threading
import requests
from bs4 import BeautifulSoup


class uribo:

    def __init__(self):
        uri_url = 'https://kym-web.ofc.kobe-u.ac.jp/campusweb'
        self.id = ''
        self.password = ''
        self.schedule = False

        self.session = requests.session()
        self.res = self.session.get(uri_url)
        self.soup = BeautifulSoup(self.res.text, "html.parser")

    def login(self, **kwargs):
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

        return self.session

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
        res2 = self.session.post(adress, data=login_info)
        logined = BeautifulSoup(res2.text, "html.parser")

        login_info2 = {
            'RelayState': logined.find_all('input')[0].get('value'),
            'SAMLResponse': logined.find_all('input')[1].get('value'),
            'back': logined.find('form').get('action')
        }

        adress = logined.find('form').get('action')
        self.session.post(adress, data=login_info2)
        print('Sucsess')
        return self.session

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

    uri = uribo()

    # 引数で渡す以外に以下のように指定することもできます
    # uri.id = 'YOUR USER ID'
    # uri.password = 'YOUR PASSWORD'
    # uri.schedule=True

    session = uri.login(id='YOUR USER ID',
                        password='YOUR PASSWORD',
                        )

    res = session.get('https://kym-web.ofc.kobe-u.ac.jp/campusweb')
    print(res.text)
