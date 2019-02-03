## all imports
import numpy as np
import urllib
import bs4
import time
import operator
import socket
import pickle
import re
import datetime
import pytz

from pandas import Series
import pandas as pd
from pandas import DataFrame

from urllib import request

#URL for traffic flow data; URL changed 2018-12-11
#url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRjKgM6FYj_zFtWgeEW8cA9BqB1cKvAsNGba4VReWMLx9TBVfp3R3OFcfgbI6GQ_lzKVAal94_yQz-n/pubhtml/sheet?headers=false&gid=273079857'
#url = 'https://docs.google.com/spreadsheets/u/2/d/e/2PACX-1vS-90CsDl-oWqOr24Xl1SptPXvwbxP_IO9rDhN-4C77U_bfzbRBLw0w9eyi89vknevEGtjOKjKpiYOu/pubhtml/sheet?headers=false&gid=273079857'
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTfBFuX-T75Ai500QE7xIc-uGuLlDVbrpkGcdpRvwV0IrXwaYW3YQJj72haoVaTg9hfwaCDU9TL1ul_/pubhtml?gid=745777476&amp;single=true&amp;widget=true&amp;headers=false'

page = urllib.request.urlopen(url)

#read web page contents
source_bytes = page.read()
source = source_bytes.decode("utf8")
page.close()

## get bs4 object
soup = bs4.BeautifulSoup(source,"html.parser")

## find all td tags
firstpass = soup.findAll('td')

#convert to string
firstpass_str = (str(firstpass).strip('[]'))

#identify first line
p0 = re.compile('<td class=\"s0\".*?</td>, ')

#identify empty table rows
p1 = re.compile('<td class="s\d" dir="ltr"></td>, ')

#identify all remaining tags 
p2 = re.compile('<.*?>')

#identify new (2018-12-11) AREA label 
p2a = re.compile('(AREA \d), ')

#identify row for header
p3 = re.compile('(Update), ')

#identify rows corresponding to a traffic location
p4 = re.compile('(:[0-5][0-9]:[0-5][0-9]), ')


#remove first line
t0 = p0.sub('', firstpass_str)

#remove empty table rows
t1 = p1.sub('', t0)

#remove all remaining tags
t2 = p2.sub('', t1)

#create new line for new (2018-12-11) AREA label 
t2a = p2a.sub(r'\1\n', t2)

#create new line for header
t3 = p3.sub(r'\1\n', t2a)

#create new line for each row corresponding to a traffic location; end up with row: traffic location, traffic flow, time
t4 = p4.sub(r'\1\n', t3)

#encode to utf-8
finalpass_str = t4.encode('utf-8')

#convert BeautifulSoup object to String
soup_str = str(soup)

#encode to utf-8
soup_str = soup_str.encode('utf-8')

#get current time, for filename
utc_now = pytz.utc.localize(datetime.datetime.utcnow())
cet_now = utc_now.astimezone(pytz.timezone("CET"))
filetime = cet_now.strftime('%Y%m%d%H%M%S')

#get filename
text_file_name = "/home/pi/traffic_data/traffic_data_"+filetime+".txt"

#write also source before formatting, just in case there are future website changes which could affect formatting
text_file_name_UNFORMATTED = "/home/pi/traffic_data/UNFORMATTED_traffic_data_"+filetime+".txt"

#write formatted text to file
text_file = open(text_file_name, "wb")
text_file.write(finalpass_str)
text_file.close()

#write Unformatted text to file
text_file_UNFORMATTED = open(text_file_name_UNFORMATTED, "wb")
text_file_UNFORMATTED.write(soup_str)
text_file_UNFORMATTED.close()
