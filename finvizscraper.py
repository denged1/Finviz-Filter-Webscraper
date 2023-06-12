from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


####################################--Replace with any finviz filter url--######################################

#Change the url
myURL = "https://finviz.com/screener.ashx?v=111&f=fa_div_o3,sec_technology"

################################################################################################################

#Uncomment the code below and delete the current chromedriver intialization(line 20) if you'd like to try it headless
'''
headless = Options()
headless.add_argument("--headless")
chromedriver = webdriver.Chrome(options=headless)
'''
#If you haven't already, download the chrome webdriver online first to use webdriver.Chrome()
chromedriver = webdriver.Chrome()

#this function gets the urls for all the pages, and returns a list of urls
def get_page_urls(url , driver):
    driver.get(url)
    
    pages = driver.find_elements(By.CLASS_NAME, "screener-pages")
    last_page = int(pages[-1].text)
    url_list = [url]
    for i in range(1,last_page):
        text = '&r=' + str(i * 20 +1)
        url_list.append(url+text)
    return url_list

def get_ticker_symbols(url, driver):
    driver.get(url)
    #this returns a list of the elements, use driver.find_element() to get just the first element
    symbols = driver.find_elements(By.CLASS_NAME, 'screener-link-primary')

    ticker_list = []
    for i in symbols:
        #the objects in the symbols list are selenium objects, so you need to use the .text function to convert to string
        ticker_list.append(i.text)
    return ticker_list

def get_tickers(url, driver):
    url_list = get_page_urls(url, driver)
    #get the ticker symbols for all the pages
    ticker_list = []
    for i in url_list:
        ticker_list += get_ticker_symbols(i, driver)
    return ticker_list

print(get_tickers(myURL, chromedriver))

chromedriver.quit