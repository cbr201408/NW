from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import os
import time
from splinter import Browser
import pandas as pd

def scrape():

	# handle Mars News
	news_url = 'https://mars.nasa.gov/news'
	chromedriver = "/usr/local/bin/chromedriver"
	os.environ["webdriver.chrome.driver"] = chromedriver
	driver = webdriver.Chrome(chromedriver)
	driver.get(news_url)
	time.sleep(5)
	html = driver.page_source
	news_soup = BeautifulSoup(html, 'lxml')
	news_results = news_soup.find_all('li', class_="slide")
	text = news_results[0].find_all('a')
	news_title = text[1].text
	news_p = text[0].find('div', class_="rollover_description_inner").text
	driver.close()

	# scrape JPL featured image
	executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	browser = Browser('chrome', **executable_path, headless=False)
	image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	browser.visit(image_url)
	browser.click_link_by_partial_text('FULL IMAGE')
	time.sleep(5)
	browser.click_link_by_partial_text('more info')
	links_found = browser.find_link_by_partial_href('images/largesize')
	featured_image_url = links_found['href']
	browser.quit()

	# scrape Mars weather
	weather_url = 'https://twitter.com/marswxreport?lang=en'
	weather_response = requests.get(weather_url)
	weather_soup = BeautifulSoup(weather_response.text, 'html.parser')
	weather_results = weather_soup.find_all('div', class_="js-tweet-text-container")
	mars_weather = weather_results[0].find('p').text

	# scrape Mars facts
	facts_url = 'https://space-facts.com/mars/'
	tables = pd.read_html(facts_url)
	df = tables[0]
	html_table = df.to_html(header=None,index=False)
	html_table = html_table.replace('\n', '')

	# scrape Mars Hemisperes
	hemisphere_image_urls =[]
	# define a function to scrape full resolution image link using splinter
	def find_hemisperes(name):
	    browser = Browser('chrome', **executable_path, headless=False)
	    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	    browser.visit(url)
	    browser.click_link_by_partial_text(name)
	    links_found = browser.find_link_by_partial_href(name.split()[0].lower())
	    url = links_found['href']
	    dic = {"title": f"{name} Hemisphere", "img_url": url}
	    hemisphere_image_urls.append(dic)
	    browser.quit()
	hemisperes_list = ['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles Marineris']
	for hemispere in hemisperes_list:
		find_hemisperes(hemispere)
		time.sleep(2)

	scrape_dic = {
		"news_title" : news_title,
		"news_p" : news_p,
		"featured_image" : featured_image_url,
		"weather" : mars_weather,
		"facts" : html_table,
		"hemispheres" : hemisphere_image_urls
	}

	return scrape_dic
