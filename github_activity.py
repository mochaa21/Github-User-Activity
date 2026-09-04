import urllib.request

response = urllib.request.urlopen("https://www.google.com/")
print(response.status)
print(response.read()[:200])