import urllib2

response = urllib2.urlopen('http://swansonraskin.pythonanywhere.com/memo')
html = response.read()