import os
import json
import requests
import threading
from bs4 import BeautifulSoup
from time import sleep

FILES = 'data.json'
VERSION = '3.0.0'

class UI:
    def __init__(self):
        self.header = '\033[95m'
        self.okblue = '\033[94m'
        self.okgreen = '\033[92m'
        self.warning = '\033[93m'
        self.fail = '\033[91m'
        self.end = '\033[0m'
        self.bold = '\033[1m'
        self.underline = '\033[4m'

    def logo(self, version):
        os.system('clear')
        print('%s PROJECT  %s================================ ' % (self.warning, self.okgreen))
        print('%s|%s ┌┬┐ ╦ ╦ ┬ ┬ ╦ ╦ ┬    ┌─┐ ╔╗╔ ┬  ┌─┐ ╔╗╔ %s|' % (self.okgreen, self.fail, self.okgreen))
        print('%s|%s  │  ║ ║ └┬┘ ║ ║ │    │ │ ║║║ │  ├┤  ║║║ %s|' % (self.okgreen, self.fail, self.okgreen))
        print('%s|%s  ┴  ╚═╝  ┴  ╚═╝ ┴─┘  └─┘ ╝╚╝ ┴─┘└─┘ ╝╚╝ %s|' % (self.okgreen, self.fail, self.okgreen))
        print('%s ============================= %sCRYPTOPLACE ' % (self.okgreen, self.warning))
        print(' %sBY : NIxON42 (%shttps://github.com/nixon42%s)' % (self.header, self.fail, self.header))
        print('                                  %s V %s  ' % (self.warning, version))
        print(self.end)

    def log(self):
        print(' %s----------------------------------------- ' % self.okgreen)
        print('%s|%s                    LOG                  %s|' % (self.okgreen, self.header, self.okgreen))
        print(' %s----------------------------------------- ' % self.okgreen)

    def pr_info(self, string):
        print('%s[INFO] %s' % (self.warning, string))

    def pr_error(self, string):
        print('%s[ERROR] %s' % (self.fail, string))
        exit()
    
    def pr_warning(self, string):
        print('%s[WARNING] %s' % (self.warning, string))

    def pr_log(self, string, ok=True):
        if ok:
            print('%s[+] %s' % (self.okgreen, string))
            return
        print('%s[-] %s' % (self.fail, string))

    def pr_next(self, string, number):
        print('\r', end='')
        print('%s%s : %d Second  ' % (self.warning, string, number), end='', flush=True)

class Tuyul:
    def __init__(self, username, password, header):
        self.sess = requests.session()
        self.sess.headers.update(header)
        self.auth = {"username": username, "password": password}
        self.logout_url = 'https://cryptoplace.cloud/users/logout'
        self.main_page = 'https://cryptoplace.cloud/cryptoplace.cloud'
        self.login_url = 'https://cryptoplace.cloud/users/login'
        self.cabinet_page = 'https://cryptoplace.cloud/cabinet'
        self.claim_url = 'https://cryptoplace.cloud/bonus/get_bonus'
        self.time_to_claim = None
        self.soup = None
        self.has_login = False
        self.login()

    def logout(self):
        while True:
            try:
                self.sess.head(self.logout_url)
                self.has_login = False
                break
            except Exception as e:
                ui.pr_log('Error Occured when accessing %s, Maybe Network issue. Error : ' % self.main_page + e.__str__(), ok=False)
                ui.pr_log('Retrying in 3 Second', ok=False)
                print()
                sleep(3)

    def login(self):
        while True:
            try:
                self.sess.get(self.main_page)
                break
            except Exception as e:
                ui.pr_log('Error Occured when accessing %s, Maybe Network issue. Error : ' % self.main_page + e.__str__(), ok=False)
                ui.pr_log('Retrying in 3 Second', ok=False)
                print()
                sleep(3)
        sleep(1)

        while True:
            try:
                # print(self.auth)
                r = self.sess.post(self.login_url, data=self.auth)
                # print(r.content)
                respon = r.json()
                if respon.get('desc') == 'Successful authorization':
                    ui.pr_log('Login as %s%s%s, Success' % (ui.warning, self.auth.get('username'), ui.okgreen))
                    self.has_login = True
                else:
                    ui.pr_error('Login Failed !!, check credential', ok=False)
                break

            except Exception as e:
                ui.pr_log('Error Occured when accessing %s, Maybe Network issue. Error : ' % self.login_url + e.__str__(), ok=False)
                ui.pr_log('Retrying in 3 Second', ok=False)
                print()
                sleep(3)

    def user(self):
        if not self.has_login:
            self.login()

        while True:
            try:
                self.soup = BeautifulSoup(self.sess.get(self.cabinet_page).content, 'lxml')
                break
            except Exception as e:
                ui.pr_log(
                    'Error Occured when accessing %s, Maybe Network issue. Error : ' % self.login_url + e.__str__(),
                    ok=False)
                ui.pr_log('Retrying in 3 Second', ok=False)
                print()
                sleep(3)

        hash_speed = self.soup.find('h3', {'class': 'pr-3 mt-5 mb-3 pt-2 gh-my total gh'})
        hash_speed = str(hash_speed.text).replace('\n', '').replace(' ', '')
        running = self.soup.find('div', {'class': 'col-md-6 col-xl-4 pt-md-2 pb30 active coin-block-mine'})
        crypto = self.soup.findAll('div', {'class': 'col-md-6 col-xl-4 pt-md-2 pb30 coin-block-mine'})

        run = '%s : %s%s %s[RUNNING]' % (running.get('data-chain')[:3], ui.warning, running.get('data-balance')[:-4], ui.fail)

        coins = [run]
        for coin in crypto:
            coins.append('%s : %s%s' % (coin.get('data-chain')[:3], ui.warning, coin.get('data-balance')[:-4]))

        return hash_speed, coins

    def claim(self):
        if not self.has_login:
            self.login()

        while True:
            try:
                r = self.sess.get(self.claim_url)
                break
            except Exception as e:
                ui.pr_log('Error has occurred, Maybe Netwok Issue. Error : ' + e.__str__())
                ui.pr_log('Retrying in 3 Second ...')
                print()
                sleep(3)

        respon = r.json()
        if respon.__contains__('rediretc'):
            ui.pr_log('Error has Occured, Maybe Credential issue', ok=False)
        elif respon.__contains__('seconds_to_bonus') and respon.get('style') == 'error':
            ui.pr_log('Next Claim in %s Second' % respon.get('seconds_to_bonus'))
            n = int(respon.get('seconds_to_bonus'))
            self.logout()
            print()
            for i in range(n):
                ui.pr_next('Next Claim', n)
                n -= 1
                sleep(1)
            print()
        else:
            ui.pr_log('Success, %s. Amount : %s USD' % (respon.get('desc'), respon.get('amount_usd')))
            n = int(respon.get('seconds_to_bonus'))
            self.logout()
            print()
            for i in range(n):
                ui.pr_next('Next Claim', n)
                n -= 1
                sleep(1)
            print()


def load_data(file):
    def check_file():
        ui.pr_info('Checking Data Files ...')
        if os.listdir('.').__contains__(file):
            ui.pr_info('Read Data Files ...')
            try:
                with open(file, 'r') as r:
                    data = json.load(r)
                    r.close()
                if data['username'] != '' or data['password'] != '':
                    pass
                if len(data['headers']) == {}:
                    ui.pr_warning('Din\'t Use Custom Header')
                else:
                    return
                ui.pr_error('Username or Password  Empty !!')
            except:
                ui.pr_error('Data File Corrupt !!')
        ui.pr_error('Data File Missing')

    if __name__ == '__main__':
        check_file()
        ui.pr_info('Load Data ...')
        with open(file, 'r') as r:
            data = json.load(r)
            r.close()
        return data['username'], data['password'], data['headers']


if __name__ == '__main__':
    ui = UI()
    ui.logo(VERSION)
    c, h, t = load_data(FILES)
    ui.pr_info('Create Session ...')
    tuyul = Tuyul(c, h, t)

    sleep(1)
    ui.pr_log('All OK, starting ...')
    print()
    sleep(3)
    ui.log()
    while True:
        gh, coin = tuyul.user()

        print()
        ui.pr_log('Current Hash Speed : %s%s' % (ui.warning, gh))
        ui.pr_log('%s----------- Current Balance ------------' % ui.header)
        for _ in coin:
            ui.pr_log(_)

        ui.pr_log('Claiming Bonus Speed ...')
        tuyul.claim()
        print()





