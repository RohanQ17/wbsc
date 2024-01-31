import selenium.webdriver.chromium.webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.chrome.options import Options

news_site = "https://www.healthline.com/health-news"
#path = "C:/Users/ROHAN/Downloads/chrome-win64/chrome-win64"
#serv = Service(executable_path=path)
# to scrape without opening chrome driver , we will use headless mode
h_options = Options()
h_options.add_argument("--headless=new")

driver = webdriver.Chrome(options=h_options, service=ChromeService(ChromeDriverManager().install()))
driver.get(news_site)

barrels = driver.find_elements(by="xpath", value='//div[@class="css-8atqhb"]')

headlines = []
subs = []
links = []
for barrel in barrels:
    HEADLINE = barrel.find_element(by="xpath", value='./a/h2').text
    SUB = barrel.find_element(by="xpath", value='./p/a').text
    ARTICLE_LINK = barrel.find_element(by="xpath", value='./a').get_attribute("href")
    headlines.append(HEADLINE)
    subs.append(SUB)
    links.append(ARTICLE_LINK)


compile_dict = {'headline': headlines, 'sub': subs, 'full_link': links}
news_headings = pd.DataFrame(compile_dict)
news_headings.to_csv('news.csv')

driver.quit()
