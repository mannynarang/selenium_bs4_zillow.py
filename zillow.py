import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests

# ser = Service("chromedriver.exe")
# op = webdriver.ChromeOptions()
# driver = webdriver.Chrome(service=ser, options=op)

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

html_doc = 'https://www.zillow.com/san-francisco-ca/rentals/2-_beds/1.0-_baths/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.70318118457031%2C%22east%22%3A-122.16347781542969%2C%22south%22%3A37.607232648764246%2C%22north%22%3A37.942970095468034%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A2%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22baths%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D'
website = requests.get(url=html_doc, headers=headers)

soup = BeautifulSoup(website.text, 'html.parser')

all_link_elements = soup.select("div.list-card-info")

info_list = []
for x in all_link_elements:
    try:
        if x.text != "":
            if "http" in x.find('a')['href']:
                info_list.append(
                    f"{x.text.split('$')[0]} | {x.find('a')['href']} | {x.find(name='div', class_='list-card-price').text}")
            else:
                # print(x.text.split('|')[1].split('$')[1][:5])
                # print(x.find(name='div', class_='list-card-price').text[:7])
                info_list.append(

                    f"{x.text.split('|')[1].split('$')[0]} | https://zillow.com{x.find('a')['href']} | {x.find(name='div', class_='list-card-price').text[:7]}")
    except:
        pass
print(info_list)

ser = Service("chromedriver.exe")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)

driver.get('https://forms.gle/Uu5pf61qn9twSGVJ7')
time.sleep(3)
for info in info_list:
    address = driver.find_element(by=By.XPATH,
                                  value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address.send_keys(info.split('|')[0])

    rent = driver.find_element(by=By.XPATH,
                               value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    rent.send_keys(info.split('|')[2])

    link = driver.find_element(by=By.XPATH,
                               value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link.send_keys(info.split('|')[1])

    submit = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    time.sleep(20)
    submit.click()
    driver.get('https://forms.gle/Uu5pf61qn9twSGVJ7')

driver.close()
