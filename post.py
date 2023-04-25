import requests


with open("test.sus", "rb") as f:
    res = requests.post("http://127.0.0.1/sus2svg/generate?type=x",data=f)