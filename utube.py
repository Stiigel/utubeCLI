"""
Kaikki itse YTiin liittyvät jutut, ja musan/videojen näyttäminen ja lataaminen

"""

import sys, re
import subprocess
import requests
from parsija import *

class Utube:
  
  def __init__(self):
    self.video = False
    self.utuAlku = "https://youtube.com/watch/?v="
    
    self.tulokset = []    
    self.ehdotukset = []
    
    self.ed = {"otsake" : "", "linkki" : ""}
    
  def laita_video(self):
    self.video = not self.video
  
  def kasittele_haku(self, haku):    
    self.tulokset = []
    
    parametrit = { "search_query" : haku, "filters" : "video", "lclk" : "video", "hl" : "fi" }
    responssi = requests.get("https://www.youtube.com/results", params=parametrit, verify=False)
    teksti = responssi.text.split("\n")
    parsija = Parsija()
    
    self.tulokset = parsija.kasittele_haku(teksti)

  def kasittele_ehdotukset(self):
    if self.ed["linkki"] == "":
      print("¡Kuuntele/lataa/mene ensin!")
      return
    
    self.ehdotukset = []
    
    responssi = requests.get(self.ed["linkki"], verify=False)
    teksti = responssi.text.split("\n")
    parsija = Parsija()
    self.ehdotukset = parsija.kasittele_ehdotukset(teksti)
         
  def ota_otsake(self, linkki):
    responssi = requests.get(linkki, verify=False)
    teksti = responssi.text
    
    alku = re.search("<title>",teksti).end()
    loppu = re.search("</title>",teksti).start()
    return teksti[alku : loppu]
    
  def kuuntele_kpl(self, mones, linkki=""):
    if linkki == "":
      linkki = "https://www.youtube.com/watch?v=" + self.tulokset[mones]["linkki"]
    prosessi = subprocess.Popen(["youtube-dl", "-g", linkki], stdout=subprocess.PIPE)
    utuLinkki, error = prosessi.communicate()
    utuLinkki = utuLinkki.rstrip()
    
    otsake = self.ota_otsake(linkki)
    
    kaskyt = ["mpv", utuLinkki, "--title", otsake]
    
    if self.video == False:
      kaskyt.append("--no-video") 
    
    subprocess.call(kaskyt)
    
    self.ed["otsake"] = otsake
    self.ed["linkki"] = linkki
    
    
  def lataa_kpl(self, mones, linkki=""):
    if linkki == "":
      linkki = "https://www.youtube.com/watch?v=" + self.tulokset[mones]["linkki"]
    
    kaskyt = ["youtube-dl", linkki, "-cit"]
    if self.video == False:
      kaskyt.append("-x")
    
    subprocess.call(kaskyt)
    
    self.ed["otsake"] = otsake
    self.ed["linkki"] = linkki
    
  def nayta_ehdotukset(self,monta):
    if len(self.ehdotukset) == 0:
      return
    for i in range(monta):
      if len(self.ehdotukset) >= i:
        aika = self.ehdotukset[i]["aika"]
        tekija = self.ehdotukset[i]["tekija"]
        otsake = self.ehdotukset[i]["otsake"]
        linkki = self.ehdotukset[i]["linkki"]
        kerrat = self.ehdotukset[i]["kerrat"]
        print(str(i + 1) + ". tulos: " + otsake + " | " + aika + " | " + tekija)
        
  def nayta_tulokset(self, monta):
    
    for i in range(monta):      
      if len(self.tulokset) >= i:
        aika = self.tulokset[i]["aika"]
        tekija = self.tulokset[i]["tekija"]
        otsake = self.tulokset[i]["otsake"]
        linkki = self.tulokset[i]["linkki"]
        kerrat = self.tulokset[i]["kerrat"]
        sitten = self.tulokset[i]["sitten"]

      print(str(i + 1) + ". tulos: " + otsake + " | " + aika + " | " + tekija + " | " + sitten)
      
      if i >= 20:
        break