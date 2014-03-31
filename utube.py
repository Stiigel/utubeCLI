import sys, re
import subprocess
import requests
import parsija

class Utube:
  
  def __init__(self):
    self.video = False
    self.utuAlku = "https://youtube.com/watch/?v="
    self.linkit = []
    self.ajat = []
    self.tekijat = []
    self.otsakkeet = []
    self.kerrat = []
    
  def laita_video(self):
    self.video = not self.video
     
  def ota_video(self):
    return self.video  
  
  def kasittele_haku(self, haku):    
    parametrit = { "search_query" : haku, "filters" : "video", "lclk" : "video", "hl" : "fi" }
    responssi = requests.get("https://www.youtube.com/results", params=parametrit, verify=False)
    teksti = responssi.text    
    persilja = parsija.Parsija(teksti)
    
    self.linkit = persilja.ota_linkit()
    self.ajat = persilja.ota_ajat()
    self.tekijat = persilja.ota_tekijat()
    self.otsakkeet = persilja.ota_hakuOtsakkeet()   
        
  def ota_otsake(self, linkki):
    responssi = requests.get(linkki, verify=False)
    teksti = responssi.text
    
    alku = re.search("<title>",teksti).end()
    loppu = re.search("</title>",teksti).start()

    return teksti[alku : loppu]
    
  def kuuntele_kpl(self, mones, linkki=""):
    if linkki == "":
      linkki = "https://www.youtube.com/watch?v=" + self.linkit[mones]
    prosessi = subprocess.Popen(["youtube-dl", "-g", linkki], stdout=subprocess.PIPE)
    utuLinkki, error = prosessi.communicate()
    utuLinkki = utuLinkki.rstrip()
    
    otsake = self.ota_otsake(linkki)
    
    kaskyt = ["mpv", utuLinkki, "--title", otsake]
    
    if self.video == False:
      kaskyt.append("--no-video") 
    
    subprocess.call(kaskyt)
    
    
  def lataa_kpl(self, mones, linkki=""):
    if linkki == "":
      linkki = "https://www.youtube.com/watch?v=" + self.linkit[mones]
    
    kaskyt = ["youtube-dl", linkki, "-cit"]
    if self.video == False:
      kaskyt.append("-x")
    
    subprocess.call(kaskyt)
    
  def nayta_tulokset(self, monta):
    for i in range(monta):
      try:
        tekija = self.tekijat[i]
      except:
        tekija = "ei tekijää"
      try:
        otsake = self.otsakkeet[i]
      except:
        otsake = "ei otsaketta"
      try:
        aika = self.ajat[i]
      except:
        aika = "eipä aikaakaan"
      
      print(str(i + 1) + ". tulos: " + otsake + " | " + aika + " | " + tekija)
      
      if i >= 20:
        break