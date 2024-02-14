import selenium.webdriver.chromium.webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import os
import sys
import os
import smtplib
import ssl
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders
# export the file into same folder as executable
path_for_app = os.path.dirname(sys.executable)
#using the curr date as filename for the news extracted
current_time = datetime.now()
mdy = current_time.strftime("%m%d%y")
if mdy is None:
    mdy = "latest"
news_site = "https://www.healthline.com/health-news"
#path = "C:/Users/ROHAN/Downloads/chrome-win64/chrome-win64"
#serv = Service(executable_path=path)
# to scrape without opening chrome driver , we will use headless mode
h_options = Options()
h_options.add_argument("--headless=new")

driver = webdriver.Chrome(options=h_options, service=ChromeService(ChromeDriverManager().install()))
if driver is None:
    print("no driver could be accessed")

driver.get(news_site)

barrels = driver.find_elements(by="xpath", value='//div[@class="css-8atqhb"]')

headlines = []
subs = []
links = []
for barrel in barrels:
    HEADLINE = barrel.find_element(by="xpath", value='./a/h2').text
    SUB = barrel.find_element(by="xpath", value='./p/a').text
    ARTICLE_LINK = barrel.find_element(by="xpath", value='./a').get_attribute("href")
    if HEADLINE is not None:
        headlines.append(HEADLINE)
    if SUB is not None:
        subs.append(SUB)
    if ARTICLE_LINK is not None:
        links.append(ARTICLE_LINK)
    else:
        print("no data found try again")
        driver.quit()


name_file = f'news-{mdy}.csv'
compile_dict = {'headline': headlines, 'sub': subs, 'full_link': links}
news_headings = pd.DataFrame(compile_dict)
news_headings.to_csv(name_file)
#final = os.path.join(path_for_app, name_file)
#news_headings.to_csv(final)

driver.quit()


# Define email sender and receiver
email_sender = 'autorelay17@gmail.com'
email_password = 'dzharbhxgttaiyhy'
receiver = input(str("please enter your email address: "))
email_receiver = receiver

# Set the subject and body of the email
subject = 'Check out latest health news'
body = ""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

# Make the message multipart
em.add_alternative(body, subtype='html')

# Attach the image file
with open(name_file, 'rb') as attachment_file:
    file_data = attachment_file.read()
    file_name = attachment_file.name.split("/")[-1]

attachment = MIMEBase('application', 'octet-stream')
attachment.set_payload(file_data)
encoders.encode_base64(attachment)
attachment.add_header('Content-Disposition', f'attachment; filename="{file_name}"')
em.attach(attachment)

# Add SSL (layer of security)
context = ssl.create_default_context()

# Log in and send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
