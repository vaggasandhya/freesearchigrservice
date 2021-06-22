# To enable ssh & remote debugging on app service change the base image to the one below

FROM mcr.microsoft.com/azure-functions/python:3.0-python3.7

COPY requirements.txt /
RUN pip install -r /requirements.txt

RUN apt-get clean
RUN apt-get remove
COPY . /home/site/wwwroot

RUN apt-get update

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz && \
    tar -zxf geckodriver-v0.26.0-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-v0.26.0-linux64.tar.gz

RUN wget -O ~/FirefoxSetup.tar.bz2 'https://download.mozilla.org/?product=firefox-latest&os=linux64' 
RUN apt-get install bzip2 
RUN tar xjf ~/FirefoxSetup.tar.bz2 -C /opt/
RUN apt -y install libgtk-3-0 libdbus-glib-1-2 xvfb
RUN ln -s /opt/firefox/firefox /usr/bin/firefox
RUN export PATH="$PATH:/opt/firefox"
RUN apt-get update -y
RUN apt-get install -y poppler-utils
RUN chmod -R 777 /opt/
RUN export PATH="$PATH:/home/site/wwwroot"
RUN pip install bs4 selenium
RUN pip install Unidecode
RUN pip install unicodedata2
RUN cd /home/site/wwwroot && \
    pip install -r requirements.txt