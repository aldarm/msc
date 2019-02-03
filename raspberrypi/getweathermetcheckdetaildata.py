## all imports
import numpy as np
import urllib
import bs4
import re 
import datetime
import pytz

from urllib import request

url = 'https://www.metcheck.com/WEATHER/now_and_next.asp?zipcode=valletta&locationID=62607&lat=35.9&lon=14.5&GL=GLOB#'

page = urllib.request.urlopen(url)

source_bytes = page.read()
source = source_bytes.decode("utf8")
page.close()

## get bs4 object
soup = bs4.BeautifulSoup(source,"html.parser")

#find last updated date and time
metcheck = soup.find("table", {"class": "ResponsiveTable"})

metcheck_str = (str(metcheck).strip('[]'))

p1 = re.compile('</tr>')

t1 = p1.sub('\n',metcheck_str)

p2 = re.compile('</td><td class="dataTableDayRow">')

t2 = p2.sub(', ',t1)

p3 = re.compile('</span>')

t3 = p3.sub('',t2)

p4 = re.compile('</center></td>')

t4 = p4.sub('',t3)

p5 = re.compile('</td>')

t5 = p5.sub(', ',t4)

p6 = re.compile('title=("Wind from.*\)")/>')

t6 = p6.sub(r'/>\1',t5)

p6a = re.compile('style="min-height:28px" title=(".*")/>,')

t6a = p6a.sub(r'/>\1',t6)

p6b = re.compile(', Conf.,')

t6b = p6b.sub('',t6a)

p7 = re.compile('<.*?>')

t7 = p7.sub('',t6b)

p8 = re.compile('☀.*?☼,')

t8 = p8.sub('',t7)

p9 = re.compile('(^\D{5,}.*)?\n\d{2}:00.*\d{2}:00.\s\n.*\n.*')

t9 = p9.sub(r'\1',t8)

p10 = re.compile('DayLight Only.*')

metcheckweather = t9[0:p10.search(t9).span(0)[0]] #get only first day of weather

utc_now = pytz.utc.localize(datetime.datetime.utcnow())
cet_now = utc_now.astimezone(pytz.timezone("CET"))
filetime = cet_now.strftime('%Y%m%d%H%M%S')

weatherchecktime = cet_now.strftime('%Y-%m-%d %H:%M:%S')

metcheckweather_final = 'weatherchecktime: '+weatherchecktime+'\n'+metcheckweather

text_file_name = "/home/pi/weather_data/weather_metcheck_details_"+filetime+".txt"

text_file = open(text_file_name, "w")
text_file.write(metcheckweather_final)
text_file.close()
