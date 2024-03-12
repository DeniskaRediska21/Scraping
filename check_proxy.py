
import threading
import queue
import requests
from proxy_randomizer import RegisteredProviders
def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get('http://ipinfo.io/json',
                                proxies = {'http':proxy,
                                           'https': proxy})
        except:
            continue
        if res.status_code == 200:
            print(proxy)

def check_proxy(proxy_list):
    global q
    valid_proxies = []

    for p in proxy_list:
        q.put(p)

    for _ in range(10):
        threading.Thread(target = check_proxies).start()




rp = RegisteredProviders()
rp.parse_providers()


proxy_list = []
for proxy_ in rp.proxies:
    tmp = str(proxy_)
    proxy_list.append(tmp[:tmp.find(' ')])

q = queue.Queue()
check_proxy(proxy_list)


