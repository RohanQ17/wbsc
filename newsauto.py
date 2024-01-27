import selenium.webdriver.chromium.webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

news_site = "https://www.healthline.com/health-news"
#path = "C:/Users/ROHAN/Downloads/chrome-win64/chrome-win64"

#serv = Service(executable_path=path)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(news_site)

