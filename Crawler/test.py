from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome()


driver.get('https://scholar.google.com/')


search_bar = driver.find_element("name", "q")
search_bar.send_keys('microservices')   # search term : "microservices"
search_bar.submit()


time.sleep(3)

first_link = driver.find_element(By.CSS_SELECTOR,'#gs_res_ccl_mid div.gs_ri div a')
profile_link = first_link.get_attribute('href')
driver.get(profile_link)

soup = BeautifulSoup(driver.page_source, 'html.parser')
name = soup.find('div', {'id': 'gsc_prf_in'}).text
university = soup.find('div', {'class': 'gsc_prf_il'}).text

if soup.find('div', {'class': 'gsc_prf_il'}).find('a'):
    university = soup.find('div', {'class': 'gsc_prf_il'}).find('a').text

interests = [i.text for i in soup.find_all('a', {'class': 'gsc_prf_inta'})]

print()
print('Publisher:', name)
print('University:', university)
print('Interests:', str(interests)[1:-1])
print()

all_articles = []
print("articles:\n")
articles = soup.find_all('tr', {'class': 'gsc_a_tr'})
for article in articles:
    title = article.find('a', {'class': 'gsc_a_at'}).text
    link = "https://scholar.google.com" + article.find('a', {'class': 'gsc_a_at'})['href']
    year = article.find('td', {'class': 'gsc_a_y'}).text
    
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    if soup.find('div', {'class': 'gsh_csp'}):
        abstract = soup.find('div', {'class': 'gsh_csp'}).text
    elif soup.find('div', {'class': 'gsh_small'}):
        abstract = soup.find('div', {'class': 'gsh_small'}).text
    else:
        abstract = "NULL"
        
        
    print('Title:', title)
    print('Link:', link)
    print('Year:', year)
    print('Abstract:\n', abstract)
    print('\n')

    article_object = {
        'title': str(title).replace(",", ""),
        'link': str(link).replace(",", ""),
        'year': str(year).replace(",", ""),
        'abstract': str(abstract).replace(",", "")
    }

    all_articles.append(article_object)

driver.quit()

df = pd.DataFrame(all_articles)
df.to_csv("articles.csv", index=False)