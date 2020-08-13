import urllib.request

response = urllib.request.urlopen('https://juejin.im/')

print(response.read().decode('utf-8'))

with open("juejin_demo1.html", "a", encoding="utf-8") as f:
    f.write(response.read().decode('utf-8'))