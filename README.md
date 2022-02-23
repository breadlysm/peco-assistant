## I have archived this repository as I am no longer a Peco Customer and can no longer test to see if things work. At last run around 9/15/2021, everything was working well. No further updates to this code will happen though. 


# Peco Assistant <img src='https://user-images.githubusercontent.com/3665468/119727590-78df0c00-be40-11eb-8261-75696a8b6d83.png' width='50'>

If you are a Peco customer, this app will collect the following stats:
- Energy usage data by hour (rounded (by Peco))
- Cost of energy by hour (est.)
- Temperature by hour (est.)

And then stores that data within a database. Currently only InfluxDB is supported. It is best run within a Docker container. 

Peco is an energy provider in Southeast Pennsylvania. Peco is part of Exelon Energy and ooking at their other energy company sites, they look like cut and past copies with different branding. This may very well work in other Northeast US Energy companies sites as is or with slight modifications. I can only confirm this works with Peco though. 

The script will begin collecting data from either 2 years ago, or the most recent date with data from the configured database. 

## Notes
- Peco's site usually runs around a 1-2 days behind realtime. 
- Not all Peco users may be able to use this based on differences in the meters. 
- Data seems to update about 1x per day. It is not advised to go below 24 hours for the time_interval. 
- This app uses selenium to log in to Peco's UI then hits API endpoints to collect the data.  \
- There is debug logging available. Just set log_level to debug
## Configuring and Running Peco Assistant
Used ENVs for variables as it's what I use in my docker server.

### Use 'docker compose'
Clone the repo to your machine. Within the repo, I've included a `docker-compose.yml`. Edit this to match your information. 

Once updated, open your favorite CLI and run `docker compose up`. The container should start up and start collecting data. 
### Use 'docker run' 

This builds automatically on Dockerhub so running the container with the needed variables should would. I've only tested in my environment. 
```shell
docker run -e "PECO_USER=replace_me_with_peco_user_email" \
-e "PECO_PASS=replace_me_with_peco_pass" \
-e "START_DATE=2020-01-01" \
-e "DB_TYPE=influxdb" \
-e "DB_HOST=192.168.1.1" \
-e "DB_PORT=8086" \
-e "DB_USER=replace_me_with_db_user" \
-e "DB_PASS=replace_me_with_db_user_pass" \
-e "DB_DBNAME=peco" \
-e "SLEEP_INTERVAL=24" \
-e "LOG_TYPE=info" \
breadlysm/peco-usage-collector
```
### Run as python script

I have a file named ".env" in the root of the directory that looks like for testing. It should work all the same as automated runs.

Once you've created that file, run the script using 
`python peco-usage-collector/peco-usage-collector/peco-usage-collector.py

```env
# User Variables
PECO_USER = {peco username}
PECO_PASS = {peco password}

# Dates
DB_TYPE = influxdb
DB_HOST = 192.168.1.1 
DB_PORT = 8086
DB_USER = {influx user} 
DB_PASS = {influx password}
DB_DBNAME = peco

#intervals in hours. How often should it collect data. Peco updates 1x per day, lower than 24 hours is not advised. 
SLEEP_INTERVAL = 24 
LOG_TYPE = info

```

## Disclaimer
Use at your own discretion. This app is not in any way associated or authroized by Peco or Exelon. It was created to automatically access the usage data in your account. Their terms do limit access by robots,spiders etc. from automatic collection of information however this is data I could easily grab by myself everyday and it is not doing anything abusive. It accesses 3 pages and then hits a JSON API once per day. Nevertheless, this is against their terms and I am not responsible for any problematic outcomes you may experience by using this. See their terms here https://www.exeloncorp.com/terms-and-conditions
