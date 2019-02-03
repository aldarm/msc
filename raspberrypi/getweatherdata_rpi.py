from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import datetime
import pytz

# Specifying incognito mode as you launch your browser[OPTIONAL]
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument("--headless")

# Create new Instance of Chrome in incognito mode
browser = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver', chrome_options=option)

# Go to desired website
browser.get("http://www.maltaweather.com/")

# Wait 20 seconds for page to load
timeout = 30
try:
    # Wait until the final element [Avatar link] is loaded.
    # Assumption: If Avatar link is loaded, the whole page would be relatively loaded because it is among
    # the last things to be loaded.
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='webcam']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

# Get all of the titles for the pinned repositories
# We are not just getting pure titles but we are getting a selenium object
# with selenium elements of the titles.

# find_elements_by_xpath - Returns an array of selenium objects.
titles_element = browser.find_elements_by_xpath("//div[@class='currentcontent']")

# List Comprehension to get the actual repo titles and not the selenium objects.
titles = [x.text for x in titles_element]
titles_nl = '\n'.join(titles)

utc_now = pytz.utc.localize(datetime.datetime.utcnow())
cet_now = utc_now.astimezone(pytz.timezone("CET"))
filetime = cet_now.strftime('%Y%m%d%H%M%S')

titles_str = (str(titles_nl).strip('[]'))

text_file_name = "/home/pi/weather_data/weather_data_"+filetime+".txt"

text_file = open(text_file_name, "w")
text_file.write(titles_str)
text_file.close()

#close browser when ready
browser.quit()
