from selenium import webdriver
from bs4 import BeautifulSoup
import json

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')

try:
    browser = webdriver.Chrome(chrome_options=options)

    url = "http://www.wipo.int/branddb/en/"

    browser.get(url)
    browser.implicitly_wait(10)
except Exception as e:
    print e

elements = browser.find_element_by_xpath('//*[@id="source_filter"]/div[1]/div/div[6]/div')

html = elements.get_attribute('innerHTML')

soup = BeautifulSoup(html, 'html.parser')

links = soup.find_all('a')

data = {}

for link in links:
	region_code = link.label.get_text()
	if link.label.get_text()[-2:] == 'TM':
		region_code = link.label.get_text()[:2]

	data[region_code] = {}
	data[region_code]['description'] = link.get('aria-label')
	data[region_code]['count'] = link.find('div', 
			class_='facetCount').get_text()

print json.dumps(data, indent=4, sort_keys=True)

browser.quit()

