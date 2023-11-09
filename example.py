import os
import requests
import json


data = {'username': 'lebron'}

x = requests.get("http://localhost:8000/user/info/",params=data)
print(x.text)