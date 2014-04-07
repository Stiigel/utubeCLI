"""
Kaikki itse YTiin liittyvät jutut, ja musan/videojen näyttäminen ja lataaminen

"""

import sys, re, parsija
import subprocess
import requests

class Utube:  
  def __init__(self):
    self.video = False
    self.utuAlku = "https://youtube.com/watch/?v="
    
    self.tulokset = []    
    self.ehdotukset = []
    
    self.nyk = {"otsake" : "", "linkki" : ""}
    
  def laita_video(self):
    self.video = not self.video
  
  def kasittele_haku(self, haku):    
    self.tulokset = []
    
    parametrit = { "search_query" : haku, "filters" : "video", "lclk" : "video", "hl" : "fi" }
    responssi = requests.get("https://www.youtube.com/results", params=parametrit, verify=False)
    teksti = responssi.text.split("\n")
    
    self.tulokset = parsija.parsi_haku(teksti)

  def kasittele_ehdotukset(self):
    if self.nyk["linkki"] == "":
      print("¡Kuuntele/lataa/mene ensin!")
      return
    
    self.ehdotukset = []
    
    responssi = requests.get(self.nyk["linkki"], verify=False)
    teksti = responssi.text.split("\n")
    self.ehdotukset = parsija.parsi_ehdotukset(teksti)
         
  def ota_otsake(self, linkki):
    responssi = requests.get(linkki, verify=False)
    teksti = responssi.text
    
    alku = re.search("<title>",teksti).end()
    loppu = re.search("</title>",teksti).start()
    return teksti[alku : loppu]
  
  def laita_linkki(self, mones, linkki="", ehd=-21):
    if linkki == "" and ehd == -21:
      linkki = "https://www.youtube.com/watch?v=" + self.tulokset[mones]["linkki"]
    elif linkki == "" and ehd != -21:
      linkki = "https://www.youtube.com/watch?v=" + self.ehdotukset[ehd]["linkki"]
    
    return linkki      
    
  def kuuntele_kpl(self, mones, linkki="", ehd=-21):
    linkki = self.laita_linkki(mones, linkki, ehd)
      
    prosessi = subprocess.Popen(["youtube-dl", "-g", linkki], stdout=subprocess.PIPE)
    utuLinkki, error = prosessi.communicate()
    utuLinkki = utuLinkki.rstrip()
    
    otsake = self.ota_otsake(linkki)
    
    kaskyt = ["mpv", utuLinkki, "--title", otsake]
    
    if self.video == False:
      kaskyt.append("--no-video") 
    
    subprocess.call(kaskyt)
    
    self.nyk["otsake"] = otsake
    self.nyk["linkki"] = linkki    
    
  def lataa_kpl(self, mones, linkki="", ehd=-21):
    linkki = self.laita_linkki(mones, linkki, ehd)
    
    kaskyt = ["youtube-dl", linkki, "-cit"]
    if self.video == False:
      kaskyt.append("-x")
    
    subprocess.call(kaskyt)
    
    self.nyk["otsake"] = otsake
    self.nyk["linkki"] = linkki
    
  def mene(self, mones, linkki=""):
    if linkki == "":
      self.nyk["otsake"] = self.tulokset[mones - 1]["otsake"]
      self.nyk["linkki"] = "https://www.youtube.com/watch?v=" + self.tulokset[mones - 1]["linkki"]
    else:
      self.nyk["linkki"] = linkki
      self.nyk["otsake"] = self.ota_otsake(linkki)
      
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