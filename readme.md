# Peco Scraper

An app that will collects your energy usage data from Peco and exports it to Infux or to a file. 
This is a WIP but with valid credentials, should get your data. 

I am not sure how far back data is stored around usage but, I was able to retrieve everything since my account started. That was midway through 2017 so it has several years worth. If there is a limit, I am not able to test. 

Most of this script is getting the correct sessions and finding the correct places to get the data. Once it collects that, the rest is simply pulling data from an API. 

This is setup to continually run. After you run the script the first time, I suggest setting the start date more recent so you don't pull everything, each iteration. 

## Future improvements.
- Put it in Docker. 
- Call influxdb to see what the last point of data was and pull everything from that point to the current time. Current the script pulls everything from the start date until now.
  - I suggest after an intial run to set the start date more recent so it's not pulling years of data each run. 
- Peco has a set of temperatures on their dash, I'd like to extract that as well and include it as a measurement within Influx. 


### Dev
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




