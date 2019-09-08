#!/usr/bin/env python
# coding: utf-8

from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

# scrapes various websites for information about Mars, and returns a dictionary
def scrape ():

    browser = init_browser()
    mars_data = {}
    
    ### NASA Mars News
    browser.visit('https://mars.nasa.gov/news/')
    html=browser.html
    soup=BeautifulSoup(html,'html.parser' )
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

    mars_data['news_headline']=news_title
    mars_data['news_teaser']=news_p

    ### JPL Mars Space Images - Featured Image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser' )
    result=soup.find('a',attrs={'class':'button fancybox'})
    full_image=result.attrs['data-fancybox-href']
    featured_image_url=f'https://www.jpl.nasa.gov{full_image}'
    mars_data['featured_image']=featured_image_url

    # download a copy of image of featured_image
    # Use the requests library to download and save the image from the `img_url` above

    # import shutil
    # response = requests.get(featured_image_url, stream=True)
    # with open('featured_img.png', 'wb') as out_file:
    #     shutil.copyfileobj(response.raw, out_file)

    # # Display the image with IPython.display
    # from IPython.display import Image
    # Image(url='featured_img.png')

    ### Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser' )
    tweets = soup.find('ol', class_='stream-items')
    mars_weather = tweets.find('p', class_="tweet-text").text
    mars_data['weather_summary']=mars_weather

    ### Mars Facts
    url = "https://space-facts.com/mars/"
    table = pd.read_html(url)
    # table[1]
    mars_facts_df=table[1]
    mars_facts_df.columns=["Parameters","Values"]
    mars_facts_df.set_index("Parameters",inplace=True)
    mars_html_table = mars_facts_df.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_data['mars_profile'] = mars_html_table

    ### Mars Hemispheres
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser' )

    hemisphere_image_urls = []
    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_url = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_url)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})
    mars_data['mars_profile'] = hemisphere_image_urls

    browser.quit()

    return mars_data
    



