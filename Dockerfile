FROM python:3.8
ENV IS_DOCKER yes
# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip git poppler-utils
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# add chromedriver to path
ENV PATH="/usr/local/bin/chromedriver:${PATH}"

# set display port to avoid crash
ENV DISPLAY=:99

# upgrade pip
RUN pip install --upgrade pip

# copy and setup peco_assistant
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt 
COPY . .
RUN pip install -e ./

# start
CMD [ "python", "peco_assistant/core.py" ]
