from fp.fp import FreeProxy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from proxy_randomizer import RegisteredProviders
from proxy_randomizer.proxy import Anonymity
import random


rp = RegisteredProviders()
rp.parse_providers()
random_proxy = rp.get_random_proxy()
russian = []
for proxy_ in rp.proxies:
    proxy_ = str(proxy_)
    if proxy_.find('Russian')>0:
        print(proxy_)
        russian.append(proxy_)


proxy = random.choice(russian)
proxy = FreeProxy(country_id = ['US']).get()
#proxy = str(random_proxy)
proxy = proxy[:proxy.find(' ')]
print(f'Selected proxy: {proxy}')


# define custom options for the Selenium driver
options = Options()
# free proxy server URL
options.add_argument(f'--proxy-server={proxy}')

# create the ChromeDriver instance with
# custom options
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options
)


driver.get('http://httpbin.org/ip')
#driver.get('https://detivinternete.ru/14-7/')
#driver.get('https://detivinternete.ru')

# print the IP the request comes from 
print(driver.find_element(By.TAG_NAME, "body").text)
