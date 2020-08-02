# Peco Scraper

An app that will collects your energy usage data from Peco and exports it to Infux or to a file. 
This is a WIP but with valid credentials, should get your data. 

I am not sure how far back data is stored around usage but, I was able to retrieve everything since my account started. That was midway through 2017 so it has several years worth. If there is a limit, I am not able to test. 

Most of this script is getting the correct sessions and finding the correct places to get the data. Once it collects that, the rest is simply pulling data from an API. 

This is setup to continually run. After you run the script the first time, it will continually monitor the first and last dates within your Influx db. It will base all future data requests on that last point that was submitted. 

## Notes
Peco's site usually runs around a 1-2 days behind realtime. 
Not all Peco users may be able to use this based on differences in meters. 

## Future improvements.
- Put it in Docker. 
- Improve logging. It exists, but it's hella noisy. 
- Peco has a set of temperatures on their dash, I'd like to extract that as well and include it as a measurement within Influx. 


## Configuring and Running Peco-scraper
Used ENVs for variables as it's what I use in my docker server.

I have a file named ".env" in the root of the directory that looks like for testing. It should work all the same as automated runs. 

```env
# User Variables
PECO_USERNAME = {peco username}
PECO_PASSWORD = {peco password}

# Dates
# date billing started or when data should generate starting
START_DATE = 2020-06-01
EXPORT_METHOD = influxdb

# Influx Settings. 
INFLUX_HOST = 192.168.1.1 
INFLUX_PORT = 8086
INFLUX_USER = {influx user} 
INFLUX_PASS = {influx passwprd}
INFLUX_DBNAME = peco 

#intervals in hours. How often should it collect data. 
SCRAPE_INTERVAL = 24 
SCRAPE_FAIL_INTERVAL = 1

```




