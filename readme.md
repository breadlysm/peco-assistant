# Peco Scraper

An app that will scrape data from Peco. Exports to Infux. 
This is a WIP but with valid credentials, should get your data. 


### Dev
Used ENVs for variables as it's what I use in my docker server

PECO_LOGIN_URL = https://secure.peco.com/Pages/Login.aspx

PECO_USERNAME = *PECO LOGIN*

PECO_PASSWORD = *PECO PASSWORD*

START_DATE = 2020-07-01

I have a file named ".env" in the root of the directory that looks like
```env
# Pages
PECO_LOGIN_URL = https://secure.peco.com/Pages/Login.aspx

# User Variables
PECO_USERNAME = PECO USERNAME
PECO_PASSWORD = PECO PASSWORD

# Dates
# date billing started or when data should generate starting
START_DATE = 2020-07-01
```




