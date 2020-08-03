FROM python:3.8-alpine

LABEL maintainer="breadlysm"
#Install git
RUN apk --update add git
RUN cd /opt && mkdir peco-scraper
RUN git clone https://github.com/breadlysm/peco-scraper.git /opt/peco-scraper

RUN pip3 install -r /opt/peco-scraper/requirements.txt 

#RUN pip3 install -r /opt/peco-scraper/requirements.txt

#CMD [ "python", "./opt/peco-scraper/pecoscraper/pecoscraper.py" ]