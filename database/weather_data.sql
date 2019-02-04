SELECT Id, filename, [date], cast(SUBSTRING(filename,22,2)+':'+SUBSTRING(filename,24,2) as TIME) as file_time, [time], conditions, temperature, wind, UVIndex, rain, heatStress, sunrise, feelsLike, sunset, gustBft, seaTemp, humidity, pressure
FROM MScDB.dbo.weather_data;

SELECT count(filename)
FROM MScDB.dbo.weather_data;

SELECT count(distinct filename)
FROM MScDB.dbo.weather_data;

SELECT Id, filename, [date], cast(SUBSTRING(filename,22,2)+':'+SUBSTRING(filename,24,2) as TIME) as file_time, [time], conditions, temperature, wind, UVIndex, rain, heatStress, sunrise, feelsLike, sunset, gustBft, seaTemp, humidity, pressure
FROM MScDB.dbo.weather_data
order by filename desc
;

SELECT Id, filename, [date], cast(SUBSTRING(filename,22,2)+':'+SUBSTRING(filename,24,2) as TIME) as file_time, [time], conditions, temperature, wind, UVIndex, rain, heatStress, sunrise, feelsLike, sunset, gustBft, seaTemp, humidity, pressure
FROM MScDB.dbo.weather_data
where SUBSTRING(filename,14,8) = '20190204'
order by filename desc
;

SELECT *
FROM MScDB.dbo.weather_data
where temperature = 'na';

--drop table MScDB.dbo.weather_data