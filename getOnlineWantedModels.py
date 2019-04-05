# Chaturbate Anonymous Get Online Wanted Models v.1.0.8 by horacio9a for Python 2.7.16
# coding: utf-8

import gevent, requests, sys, re, configparser
from threading import Thread
from multiprocessing import Queue
from bs4 import BeautifulSoup
Config = configparser.ConfigParser()
Config.read('config.ini')
genders = re.sub(' ', '', Config.get('settings', 'genders')).split(",")
lastPage = {'female': 100, 'couple': 100, 'trans': 100, 'male': 100}

def getOnlineModels():
    global lastPage
    global q
    global online
    if not q.empty():
        args = q.get()
        page = args[0]
        gender = args[1]
        if page < lastPage[gender]:
            attempt = 1
            while attempt <= 3:
                try:
                    timeout = gevent.Timeout(8)
                    timeout.start()
                    URL = "https://chaturbate.com/{gender}-cams/?page={page}".format(gender=gender.lower(), page=page)
                    result = requests.request('GET', URL)
                    result = result.text
                    soup = BeautifulSoup(result, 'html.parser')
                    if lastPage[gender] == 100:
                        lastPage[gender] = int(soup.findAll('a', {'class': 'endless_page_link'})[-2].string)
                    if int(soup.findAll('li', {'class': 'active'})[1].string) == page:
                        LIST = soup.findAll('ul', {'class': 'list'})[0]
                        models = LIST.find_all('div', {'class': 'title'})
                        for model in models:
                            online.append(model.find_all('a', href=True)[0].string.lower()[1:])
                    break
                except gevent.Timeout:
                    attempt = attempt + 1
                    if attempt > 3:
                        break

def getModels():
    workers = []
    for gender in genders:
        if gender == 'couple':
            for i in range(1, 3):
                q.put([i, gender])
        else:
            for i in range(1, 30):
                q.put([i, gender])
    while not q.empty():
        for i in range(10):
            t = Thread(target=getOnlineModels)
            workers.append(t)
            t.start()
        for t in workers:
            t.join()

if __name__ == '__main__':
    q = Queue()
    online = []
    workers = []
    getModels()
    online = list(set(online))
    online_model_list = online
    wanted_model_list = open(Config.get('files', 'wanted_model_list'),'r').read()
    for online_wanted_model_list in online_model_list:
      if online_wanted_model_list in wanted_model_list:
        print(online_wanted_model_list)
