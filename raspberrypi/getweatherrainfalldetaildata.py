## all imports
import numpy as np
import urllib
import bs4
import re 
import datetime
import pytz

from urllib import request

url = 'https://www.maltairport.com/weather/detailed-forecast/'

page = urllib.request.urlopen(url)

source_bytes = page.read()
source = source_bytes.decode("utf8")
page.close()

## get bs4 object
soup = bs4.BeautifulSoup(source,"html.parser")


#find last updated date and time
findrainfall = soup.find_all("table", {"class": "rainfall-data"})

findrainfall_str = (str(findrainfall).strip('[]'))

p1 = re.compile('</td></tr>')

t1 = p1.sub('\n',findrainfall_str)

p2 = re.compile('</td><td>')

t2 = p2.sub(', ',t1)

p3 = re.compile('</th>\n')

t3 = p3.sub(',',t2)

p4 = re.compile('<.*?>')

t4 = p4.sub('',t3)

p5 = re.compile(' \*\d')

t5 = p5.findall(t4)

t5 = p5.sub('',t4)

p6 = re.compile('\n\nLocation')

t6 = p6.sub('Location',t5)

p7 = re.compile(' X')

t7 = p7.sub('X',t6)

p8 = re.compile('Total,')

t8 = p8.sub('Total (mm)',t7)

p9 = re.compile('24 Hour')

t9 = p9.sub('24 Hour (mm)',t8)



p10 = re.compile('\nAverage\n\d{1,5}.\d{1,5}\smm\n\d{1,5}.\d{1,5}\smm')

t10 = p10.sub('',t9)

p11 = re.compile(r'\n\s*$')

t11 = p11.sub('',t10)

p12 = re.compile('\smm')

t12 = p12.sub('',t11)

p13 = re.compile('(^)')

t13 = p13.sub(r'\1test, ',t12)

final_rainfall = t12

utc_now = pytz.utc.localize(datetime.datetime.utcnow())
cet_now = utc_now.astimezone(pytz.timezone("CET"))
filetime = cet_now.strftime('%Y%m%d%H%M%S')

final_rainfall = ('Time: '+ cet_now.strftime('%Y-%m-%d %H:%M:%S')+'\n'+final_rainfall)

text_file_name = "/home/pi/weather_data/weather_rainfall_details_"+filetime+".txt"

text_file = open(text_file_name, "w")
text_file.write(final_rainfall)
text_file.close()
