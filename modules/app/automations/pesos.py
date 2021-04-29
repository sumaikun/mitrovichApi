import requests
from bs4 import BeautifulSoup

class pesos_automation():

    def start_script(self):
        print("start pesos script")
        try:
            URL = 'https://wise.com/es/currency-converter/usd-to-cop-rate'
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            dollarContainer = soup.find("span", {"class": "text-success"})
            print("pesos value",dollarContainer.text.split(',')[0])
            return dollarContainer.text.split(',')[0]
        except Exception as e:
            print("Could not load site: "+str(e))
            return None