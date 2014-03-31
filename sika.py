from parsija import *
import requests

haku = "BLaze bayley"
parametrit = { "search_query" : haku, "filters" : "video", "lclk" : "video", "hl" : "fi" }
responssi = requests.get("https://www.youtube.com/results", params=parametrit, verify=False)
teksti = responssi.text  

persilja = Parsija(teksti)

linkit = persilja.ota_linkit()
ajat = persilja.ota_ajat()
tekijat = persilja.ota_tekijat()
otsakkeet = persilja.ota_hakuOtsakkeet() 

print(linkit)