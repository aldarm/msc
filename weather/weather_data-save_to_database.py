import os
import subprocess
import re
from pathlib import Path
from cryptography.fernet import Fernet


home = str(Path.home())


file = open(home+'/sql_files/pysqlkey.key', 'rb')
key = file.read() # The key will be type bytes
file.close()

cipher_suite = Fernet(key)
with open(home+'/sql_files/sql_server_pwd.bin', 'rb') as file_object:
    for line in file_object:
        encryptedpwd = line

import pyodbc
server = 'deep-learning'
database = 'MScDB'
username = 'sa'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ bytes((cipher_suite.decrypt(encryptedpwd))).decode("utf-8"))
cursor = cnxn.cursor()

weather_path = '/media/alessio/3TB/Dropbox/pi/weather_data/'

os.chdir(weather_path)

print(os.getcwd())


weather_file_name = 'weatherdatafiles.txt'


if os.path.isfile(weather_file_name):
    os.remove(weather_file_name)


#execute shell command to list all files into a text file
log = open(weather_file_name, 'a')
log.flush()  # <-- here's something not to forget!
proc = subprocess.Popen(['for f in weather_data_*.txt; do ls "$f"; done'], stdout=log, stderr=log, shell=True)

output = proc.communicate()[0] #waits for previous command to finish


weather_files = open(weather_file_name, "r",encoding='utf-8')


weather_file_filenames = weather_files.readlines()


weather_files.close()


len(weather_file_filenames)


def get_weather_data (weather_file_Content):
    try:
        conditions = weather_file_Content[1].strip('\n')
        temperature = weather_file_Content[2].strip('\n')
        wind = weather_file_Content[3].strip('\n')
        UVIndex = weather_file_Content[5].strip('\n')
        rain = weather_file_Content[7].strip('\n')
        heatStress = weather_file_Content[9].strip('\n')
        sunrise = weather_file_Content[11].strip('\n')
        feelsLike = weather_file_Content[13].strip('\n')
        sunset = weather_file_Content[15].strip('\n')
        gustBft = weather_file_Content[17].strip('\n')
        seaTemp = weather_file_Content[19].strip('\n')
        humidity = weather_file_Content[21].strip('\n')
        pressure = weather_file_Content[23].strip('\n')

        #separate date and time, and change format
        date_time = weather_file_data[24].strip('\n')

        date_criteria = re.compile('(3[01]|[12][0-9]|0?[1-9])/(1[0-2]|0?[1-9])/((?:[0-9]{2})?[0-9]{2})')
        date_result = date_criteria.search(date_time)

        #if month is less than 10, append 0
        if len(date_result.group(2)) < 2:
            month = "0"+date_result.group(2)
        else:
            month = date_result.group(2)

        #if day is less than 10, append 0
        if len(date_result.group(1)) < 2:
            day = "0"+date_result.group(1)
        else:
            day = date_result.group(1)

        date = date_result.group(3)+'-'+month+'-'+day

        time_criteria = re.compile('([0-2][0-3]|[0-1][0-9]):([0-5][0-9])$')
        time_result = time_criteria.search(date_time)
        time = time_result.group(1) + ':' + time_result.group(2)
    except:
        date = '1900-01-01'
        time = '23:59'
        condition = 'na'
        temperature = 'na'
        wind  = 'na'
        UVIndex = 'na'
        rain = 'na'
        heatStress = 'na'
        sunrise   = 'na'
        feelsLike = 'na'
        sunset  = 'na'
        gustBft  = 'na'
        seaTemp  = 'na'
        humidity  = 'na'
        pressure  = 'na'
        
    
    weather_line = {
        "filename"     : weather_file.name
        ,"date"        : date
        ,"time"        : time
        ,"conditions"  : conditions 
        ,"temperature" : temperature
        ,"wind"        : wind 
        ,"UVIndex"     : UVIndex  
        ,"rain"        : rain
        ,"heatStress"  : heatStress   
        ,"sunrise"     : sunrise  
        ,"feelsLike"   : feelsLike 
        ,"sunset"      : sunset 
        ,"gustBft"     : gustBft 
        ,"seaTemp"     : seaTemp 
        ,"humidity"    : humidity  
        ,"pressure"    : pressure 
    }
    return weather_line


def create_db_temp_table():
    tsql = "CREATE TABLE #weather_data (\
     filename NVARCHAR(50) NOT NULL\
    , date date NOT NULL\
    , time time NOT NULL\
    , conditions NVARCHAR(50) NOT NULL\
    , temperature NVARCHAR(50) NOT NULL\
    , wind NVARCHAR(50) NOT NULL\
    , UVIndex NVARCHAR(50) NOT NULL\
    , rain NVARCHAR(50) NOT NULL\
    , heatStress NVARCHAR(50) NOT NULL\
    , sunrise NVARCHAR(50) NOT NULL\
    , feelsLike NVARCHAR(50) NOT NULL\
    , sunset NVARCHAR(50) NOT NULL\
    , gustBft NVARCHAR(50) NOT NULL\
    , seaTemp NVARCHAR(50) NOT NULL\
    , humidity NVARCHAR(50) NOT NULL\
    , pressure NVARCHAR(50) NOT NULL\
    );"
    cursor.execute(tsql)



def insert_into_db_temp_table (weather_line_data):
    #Insert Query
    tsql = "INSERT INTO #weather_data\
    (filename,date,time,conditions,temperature,wind,UVIndex,rain,heatStress,sunrise,feelsLike,sunset,gustBft,seaTemp,humidity,pressure)\
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
    cursor.execute(tsql
        ,weather_line_data.get('filename')
        ,weather_line_data.get('date')
        ,weather_line_data.get('time')
        ,weather_line_data.get('conditions')
        ,weather_line_data.get('temperature')
        ,weather_line_data.get('wind')
        ,weather_line_data.get('UVIndex')
        ,weather_line_data.get('rain')
        ,weather_line_data.get('heatStress')
        ,weather_line_data.get('sunrise')
        ,weather_line_data.get('feelsLike')
        ,weather_line_data.get('sunset')
        ,weather_line_data.get('gustBft')
        ,weather_line_data.get('seaTemp')
        ,weather_line_data.get('humidity')
        ,weather_line_data.get('pressure'))



def merge_into_db ():
    tsql = "Merge into weather_data as t1            using(select * from #weather_data) as t2 \
               on t1.filename=t2.filename \
            when not matched then \
               insert values(t2.filename,t2.date,t2.time,t2.conditions,t2.temperature,t2.wind,t2.UVIndex,t2.rain,t2.heatStress,t2.sunrise,t2.feelsLike,t2.sunset,t2.gustBft,t2.seaTemp,t2.humidity,t2.pressure);"
    cursor.execute(tsql)



create_db_temp_table()



for x in range(0,len(weather_file_filenames)):
    weather_file = open(weather_file_filenames[x].strip('\n'))
    weather_file_data = weather_file.readlines()
    weather_line_dict = get_weather_data(weather_file_data)
    #insert_into_db(weather_line_dict)
    insert_into_db_temp_table(weather_line_dict)
    weather_file.close()


cursor.commit()

merge_into_db()

cursor.commit()
cursor.close()
cnxn.close()

