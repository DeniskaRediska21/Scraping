
import threading
import queue
import requests

q = queue.Queue()
out_q = queue.Queue()
flag = True

def check_proxies():
    good_proxy_list = []
    global q
    global flag
    global out_q
    print(flag)
    while (not q.empty()) and flag:
        proxy = q.get()
        try:
            res = requests.get('http://ipinfo.io/json',
                                proxies = {'http':proxy,
                                           'https': proxy})
#            res = requests.get('https://detivinternete.ru',
#                                proxies = {'http':proxy,
#                                           'https': proxy})
        except:
            continue
        if res.status_code == 200:
            print(proxy)
            out_q.put(proxy)
            flag = False
            good_proxy_list.append(proxy)
            break
    

def check_proxy(proxy_list):
    global q
    global out_q
    valid_proxies = []

    for p in proxy_list:
        q.put(p)

    t = []
    for _ in range(5):
        t.append(threading.Thread(target = check_proxies))
        t[-1].start()
    for thread in t:
        thread.join(20)
    return out_q
#

from proxy_randomizer import RegisteredProviders


rp = RegisteredProviders()
rp.parse_providers()

proxy_list = []
for proxy_ in rp.proxies:
    tmp = str(proxy_)
    proxy_list.append(tmp[:tmp.find(' ')])

check_proxy(proxy_list)

good_proxy_list = []
while not out_q.empty():
    good_proxy_list.append(q.get())

print('done')
