from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime
from selenium.webdriver.common.by import By


payload = {'where': 'news', 'sm': 'tab_jum', 'query': '데이터'}

url = 'https://search.naver.com/search.naver?where=' + payload['where'] + '&sm=' + payload['sm'] + '&query=' + payload['query']
url_2 = 'https://search.naver.com/search.naver?where=news&query=데이터&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds=2024.01.16&de=2024.01.18&docid=&related=0&mynews=1&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20240116to20240118&is_sug_officeid=0&office_category=0&service_area=0'
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
req = requests.get(url_2, headers=headers).content
soup = BeautifulSoup(req, 'html.parser')

# selenium으로 진행하는 부분
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

s = Service('C:/Users/hyun2/PycharmProjects/gitPycharm/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.get(url_2)
'https://search.naver.com/search.naver?where=news&query=데이터&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds=2024.01.16&de=2024.01.18&docid=&related=0&mynews=1&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20240116to20240118&is_sug_officeid=0&office_category=0&service_area=0'
import time

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # 페이지 끝까지 스크롤 다운
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 페이지 로딩을 기다림
    time.sleep(2)

    # 새로운 높이 계산
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        break

    last_height = new_height

date = []
category = []
press = []
title = []
document = []
link = []
summary = []


elements_link = driver.find_elements(By.CSS_SELECTOR, 'a.info')
elements_press = driver.find_elements(By.CSS_SELECTOR, 'a.info.press')

for element in elements_link:
    #link
    href = element.get_attribute('href')
    if href.startswith('https://n.news.naver.com/'):
        link.append(href)


for index, value in enumerate(link):
    driver.get(value)


    #date
    # date.append(driver.find_element('span', {'class': 'media_end_head_info_datestamp_time _ARTICLE_DATE_TIME'}).get_text())
    try:
        date.append(driver.find_element(By.CSS_SELECTOR, 'span.media_end_head_info_datestamp_time._ARTICLE_DATE_TIME').text)
    except:
        date.append(None)

    #category
    try:
        category.append(driver.find_element(By.CSS_SELECTOR, 'li.Nlist_item._LNB_ITEM.is_active > a.Nitem_link > span.Nitem_link_menu').text)
        category[index] = category[index].replace('\n', '').replace('/', '')
    except:
        category.append(None)

    #press
    try:
        press.append(driver.find_element(By.CSS_SELECTOR, 'a.media_end_linked_more_link > em').text)
    except:
        press.append(None)

    # press_tag = driver.find('span', class_='')
    # press.append(press_tag.find('strong').text)


    #title
    try:
    # title.append(driver.find('h2', {'id' : 'title_area'}).get_text())
        title.append(driver.find_element(By.CSS_SELECTOR, '#title_area > span').text)
    except:
        title.append(None)

    #document
    try:
        document.append(driver.find_element(By.CSS_SELECTOR, 'article.go_trans._article_content').text)
    except:
        document.append(None)

    #summary
    try:
        summary.append(driver.find_element(By.CSS_SELECTOR, 'strong.media_end_summary').text)
    except:
        summary.append(None)

    if summary[index] is not None:
        summary[index] = summary[index].replace('\\', '')
    else:
        summary[index] = ''


for index, value in enumerate(date):
    try:
        value = value.replace('오전', 'AM').replace('오후', 'PM')
        formatted_date = datetime.strptime(value, '%Y.%m.%d. %p %I:%M')
        date[index] = formatted_date.strftime('%Y-%m-%d %I:%M')
    except:
        pass
driver.quit()

print(len(date))
print(len(category))
print(len(press))
print(len(title))
print(len(document))
print(len(link))
print(len(summary))



# 'press' : press,
news_df = pd.DataFrame({'date' : date, 'category' : category, 'press' : press, 'title' : title, 'document' : document, 'link' : link, 'summary' : summary})
news_df.to_csv('scraping.csv', index=False, encoding='utf-8')