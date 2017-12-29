from django.template.loader import get_template
from django.shortcuts import render
import urllib2
import json
import feedparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

def query_google_news(query):
    '''Get a Google News RSS Feed containing stories about a specific query and return all stories'''

    raw = feedparser.parse('https://news.google.com/news/feeds?cf=all&ned=us&hl=en&q=' + query + '&output=rss')
    return raw.entries

def get_fed_news():
    '''Get the federal news from NYT in JSON format'''

    federal_news_raw = urllib2.urlopen('https://api.nytimes.com/svc/topstories/v2/politics.json?api-key=02ead59552364295afddc52d4c6bd559')
    federal_news_JSON = json.load(federal_news_raw)

    return federal_news_JSON['results']

def create_news_dict():
    '''Get news results for a bundle of topics'''

    federal = get_fed_news()
    senate = query_google_news('Senate')
    state = query_google_news('Maryland')
    moco = query_google_news('montgomery%20county%20md%20government')
    fred = query_google_news('frederick%20news%20post%20government')
    car = query_google_news('carroll%20county%20times%20government')

    return {'federal':federal, 'senate':senate, 'state':state, 'moco':moco, 'fred':fred, 'car':car}

def send_mail(message, email):
    '''Sends a message to an email'''

    container = MIMEMultipart('alternative')
    message = MIMEText(message.encode('utf-8'), 'html', 'utf-8')
    container.attach(message)

    fromaddr = 'YOUR_EMAIL'
    toaddrs  = email
    username = 'YOUR_EMAIL'
    password = 'YOUR_EMAIL_PASSWORD'
    server = smtplib.SMTP('smtp.gmail.com:587') # Mail
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, container.as_string())
    server.quit()

def send_news():
    '''Sends the news to an email address'''

    html = get_template('base/memo.html')
    news = create_news_dict()
    news['date'] = datetime.now()
    content = html.render(news)
    send_mail(content, 'TO_EMAIL_ADDRESS')

def memo(request):
    '''Send the news in memo format to an email'''

    news = create_news_dict()
    news['date'] = datetime.now()
    send_news()
    return render(request, 'base/memo.html', news)

def base(request):
    '''Visual landing page'''

    news = create_news_dict()

    return render(request, 'base/base.html', news)

