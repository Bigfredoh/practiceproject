import requests
from bs4 import BeautifulSoup

# Enter the City Name
cars = input("Enter the City Name: ")
search = "gta in {}".format(cars)

# URL
url = f"https://www.google.com / search?&q ={search}"

# Sending HTTP request
req = requests.get(url)

# Pulling HTTP data from internet
sor = BeautifulSoup(req.text, "html.parser")

