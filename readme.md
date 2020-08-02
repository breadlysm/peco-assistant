# Peco Scraper


An app that will collects your energy usage data from Peco and exports it to Infux or to a file. 

Peco is an energy provider in Southeast Pennsylvania. Peco is part of Exelon Energy and ooking at their other energy company sites, they look like cut and past copies with different branding. This may very well work in other Northeast US Energy companies sites as is or with slight modifications. I can only confirm this works with Peco though. 

I'm happy to coordinate modifications on this app to work with other providers. Any improvements in general would be welcomed too. 

I am not sure how far back data is stored around usage but, I was able to retrieve everything since my account started. That was midway through 2017 so it has several years worth. If there is a limit, I am not able to test. 

Most of this script is getting the correct sessions and finding the correct places to get the data. Once it collects that, the rest is simply pulling data from an API. 

This is setup to continually run. After you run the script the first time, it will continually monitor the first and last dates within your Influx db. It will base all future data requests on that last point that was submitted or if the start_date is changed, it will base it off that until it fills in the older data points.

## Notes
- Peco's site usually runs around a 1-2 days behind realtime. 
- Not all Peco users may be able to use this based on differences in the meters. 
- Data seems to update about 1x per day. It is not advised to go below 24 hours for the time_interval. 
- This is an app that scrapes web pages based on specific page elements. It is very likely that these will change and potentially break the app. 
  - These should be relatively easy to fix unless it is a site overhaul. I do plan to maintain the functionality. 

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

#intervals in hours. How often should it collect data. Peco updates 1x per day, lower than 24 hours is not advised. 
SCRAPE_INTERVAL = 24 
SCRAPE_FAIL_INTERVAL = 1

```

## Disclaimer
Use at your own discretion. This app is not in any way associated or authroized by Peco or Exelon. It was created to automatically access the usage data in your account. Their terms do limit access by robots,spiders etc. from automatic collection of information however this is data I could easily grab by myself everyday and it is not doing anything abusive. It accesses 3 pages and then hits a JSON API once per day. Nevertheless, this is against their terms and I am not responsible for any problematic outcomes you may experience by using this. See their terms here https://www.exeloncorp.com/terms-and-conditions


