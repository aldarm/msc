## all imports
import numpy as np
import urllib
import bs4
import re 
import datetime
import pytz

from urllib import request

url = 'https://www.maltairport.com/weather/'

page = urllib.request.urlopen(url)

source_bytes = page.read()
source = source_bytes.decode("utf8")
page.close()

## get bs4 object
soup = bs4.BeautifulSoup(source,"html.parser")

#find last updated date and time
findupdatedate = soup.find_all("span", {"class": "date"})

#remove duplicate rows
findupdatedate_unique = set(findupdatedate)

findupdatedate_unique_str = (str(findupdatedate_unique).strip('[]'))

p_last_updated_time_temp = re.compile('Last updated: .*?[0-5][0-9]:[0-5][0-9]')

last_updated_time_temp1 = p_last_updated_time_temp.search(findupdatedate_unique_str)

last_updated_str = last_updated_time_temp1.group(0)

p_last_updated_time_temp0 = re.compile('Last updated: (.*?[0-5][0-9]:[0-5][0-9])')

last_updated_time = p_last_updated_time_temp0.sub(r'\1',last_updated_str)

## find wind
findwind = soup.find("div", {"id": "wind"})
windchildren = findwind.findChildren("div" , recursive=False)

windchildren_str = (str(windchildren).strip('[]'))

## find temperature
findtemperature = soup.find("div", {"id": "temperature"})
temperaturechildren = findtemperature.findChildren("div" , recursive=False)

temperaturechildren_str = (str(temperaturechildren).strip('[]'))

## find rainfall
findrainfall = soup.find("div", {"id": "rainfall"})
rainfallchildren = findrainfall.findChildren("div" , recursive=False)

rainfallchildren_str = (str(rainfallchildren).strip('[]'))

## find humidity
findhumidity = soup.find("div", {"id": "humidity"})
humiditychildren = findhumidity.findChildren("div" , recursive=False)

humiditychildren_str = (str(humiditychildren).strip('[]'))

#remove commas
p1 = re.compile(',')

t_wind1 = p1.sub('',windchildren_str)
t_temp1 = p1.sub('',temperaturechildren_str)
t_rain1 = p1.sub('',rainfallchildren_str)
t_humid1= p1.sub('',humiditychildren_str)

#replace with commas
p2 = re.compile('</h4><p>')

t_wind2 = p2.sub(', ',t_wind1)
t_temp2 = p2.sub(', ',t_temp1)
t_rain2 = p2.sub(', ',t_rain1)
t_humid2 = p2.sub(', ',t_humid1)

#remove first line
p3 = re.compile('<.*?"luqastation">\n')

t_wind3 = p3.sub('',t_wind2)
t_temp3 = p3.sub('',t_temp2)
t_rain3 = p3.sub('',t_rain2)
t_humid3 = p3.sub('',t_humid2)

#remove all tags
p4 = re.compile('<.*?>')

t_wind4 = p4.sub('',t_wind3)
t_temp4 = p4.sub('',t_temp3)
t_rain4 = p4.sub('',t_rain3)
t_humid4 = p4.sub('',t_humid3)

#remove bullets
p5= re.compile('●')

wind = p5.sub(last_updated_time+', wind, ',t_wind4)
temp = p5.sub(last_updated_time+', temperature, ',t_temp4)
rain = p5.sub(last_updated_time+', rainfall, ',t_rain4)
humid = p5.sub(last_updated_time+', humidity, ',t_humid4)

final_status = temp+'\n'+wind+'\n'+rain+'\n'+humid

utc_now = pytz.utc.localize(datetime.datetime.utcnow())
cet_now = utc_now.astimezone(pytz.timezone("CET"))
filetime = cet_now.strftime('%Y%m%d%H%M%S')

text_file_name = "/home/pi/weather_data/weather_details_"+filetime+".txt"

text_file = open(text_file_name, "w")
text_file.write(final_status)
text_file.close()