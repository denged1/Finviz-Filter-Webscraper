# Finviz-Filter-Webscraper
Python code to webscrape the tickers off any finviz screener url using Selenium.
<br>
<br>
<br>
If you've ever used filters/screeners on finviz.com, you would know that they are incredibly powerful. The site gives you many different customization options, such as filtering by insider ownership, operating margins, analyst recomendations, and P/E; just to name a few. If you haven't tried it out I would recommend playing around with it. It's honestly pretty cool; all the filter options can be customized in this url.
https://finviz.com/screener.ashx?v=111&ft=4


To utilize this code you first need to install Selenium using ```pip install selenium```. Additionally, you need to have the chrome browser installed and have the chrome webdriver downloaded. You can download the chrome webdriver here https://chromedriver.chromium.org/downloads, pay attention to see if the chrome webdriver you are downloading supports your version of chrome. If you aren't sure how to check your chrome version here are some instructions to do so. https://www.lifewire.com/check-version-of-chrome-5222040

Finally, just copy paste the url of your customized filter into the string ```myURL``` and run the code. From there it just prints the tickers, but you can customize the code to store the tickers on a csv, plug them into a trading algo, etc. The world is your oyster!

<br>
<br>
<br>

Also I would like to mention, that although this code seems naive and slow(which it is), it was the best that I could do for now. I noticed that when I ran it using a headless, the website information wouldn't load properly. As a result, when I scraped the page numbers, I would get nothing, leading to an out of bounds exception when I generated the list of urls to scrape from. I'm not entirely sure why that's the case, but I left the headless code in there if anyone can make it work for them.

Addtionally, because the page numbers and tickers are generated using JavaScript we can't use something like BeautifulSoup to parse directly through the HTML to get the data faster. When you use BeautifulSoup to parse the HTML of a webpage, you're only getting the initial HTML that's sent by the server. Any changes to the page that are made by JavaScript after the page loads will not be reflected in the intial HTML.

Many web applications use asynchronous loading, which uses JavaScript to fetch data from a server and update the page after it has initially loaded. Because the data is loaded in the background after the initial page loads, it won't be present in the initial HTML that BeautifulSoup sees.

In contrast, Selenium actually runs the JavaScript code, so it can interact with and scrape data from webpages that use JavaScript to load or display data, but this comes at the expense of speed. Since Selenium is running JavaScript and actually rendering a webpage, it is much slower than just parsing HTML.

<br>
<br>
<br>
I would really appreciate it if anyone who knows how to optimize this code further could open an issue on GitHub.
The full code can be found below or in file format in the repository. 

I hope this was helpful!
<br>
<br>

```python
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


####################################--Replace with any finviz filter url--######################################

#Change the url
myURL = "https://finviz.com/screener.ashx?v=111&f=fa_div_o3,sec_technology"

################################################################################################################

#Uncomment the code below and delete the current chromedriver intialization(line 21) if you'd like to try it headless
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

```
