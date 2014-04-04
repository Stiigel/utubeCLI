"""
Kaikki itse YTiin liittyvät jutut, ja musan/videojen näyttäminen ja lataaminen

"""

import sys, re
import subprocess
import requests

class Utube:
  
  def __init__(self):
    self.video = False
    self.utuAlku = "https://youtube.com/watch/?v="
    self.linkit = []
    self.ajat = []
    self.tekijat = []
    self.otsakkeet = []
    self.kerrat = []
    self.sittenit = []
    
    self.ehdotukset = []
    self.ed = {"otsake" : "", "linkki" : ""}
    
  def laita_video(self):
    self.video = not self.video
  
  def kasittele_haku(self, haku):    
    self.linkit = []
    self.ajat = []
    self.tekijat = []
    self.otsakkeet = []
    self.kerrat = []
    self.sittenit = []
    
    parametrit = { "search_query" : haku, "filters" : "video", "lclk" : "video", "hl" : "fi" }
    responssi = requests.get("https://www.youtube.com/results", params=parametrit, verify=False)
    teksti = responssi.text.split("\n")
    
    kohta = -1
    tietoAlku = -1
    tekijaAlku = -1
    for i in range(len(teksti)):
      if "/watch?v=" in teksti[i]:
        kohta = i

      if kohta != -1:
        if 'class="video-time">' in teksti[i]:
          self.ajat.append(re.search('"video-time">(.*?)</span>', teksti[i]).group(1))
          
        if 'yt-uix-sessionlink yt-uix-tile-link' in teksti[i]:
          tietoAlku = i
        
        if tietoAlku != -1:
          if 'title="' in teksti[i]:
            self.otsakkeet.append(re.search('title="(.*?)"', teksti[i]).group(1))
          
          if 'href="/watch?v=' in teksti[i]:
            self.linkit.append(re.search('href="/watch\?v=(.*?)"', teksti[i]).group(1))
            tietoAlku = -1

          if '>' in teksti[i]:
            tietoAlku = -1
        
        if 'g-hovercard yt-uix-sessionlink yt-user-name spf-link' in teksti[i]:
          tekijaAlku = i
        
        if tekijaAlku != -1:
          if 'data-name' in teksti[i]:
            self.tekijat.append(re.search('data-name="">(.*?)</a>', teksti[i]).group(1))
          if 'sitten' in teksti[i]:
            self.sittenit.append(re.search('<li>(.*?)sitten</li><li>', teksti[i]).group(1))
          if 'näyttökertaa' in teksti[i]:
            self.kerrat.append(re.search('<li>(.*?) näyttökertaa</li>',teksti[i]).group(1))
            tekijaAlku = -1
            kohta = -1 
            
  def kasittele_ehdotukset(self):
    if self.ed["linkki"] == "":
      print("¡Hae ensin!")
      return
    
    self.ehdotukset = []
    
    responssi = requests.get(self.ed["linkki"], verify=False)
    teksti = responssi.text.split("\n")
    
    kohta = -1
    tekijaKohta = -1
    mones = -1
    for i in range(len(teksti)):
      
      if '"related-video  spf-link yt-uix-sessionlink"' in teksti[i]:
        mones += 1
        kohta = i
        self.ehdotukset.append({})      
      
      if kohta != -1:
        if 'href="/watch?v=' in teksti[i]:
          linkki = re.search('href="/watch\?v=(.*?)"', teksti[i]).group(1)
          self.ehdotukset[mones]["linkki"] = linkki
          
        if '<span class="video-time">' in teksti[i]:
          aika = re.search('<span class="video-time">(.*?)</span>', teksti[i]).group(1)
          self.ehdotukset[mones]["aika"] = aika
          
        if 'class="title" title="' in teksti[i]:
          otsake = re.search('class="title" title="(.*?)"', teksti[i]).group(1)
          self.ehdotukset[mones]["otsake"] = otsake
        
        if '<span class="stat view-count">' in teksti[i]:
          kerrat = re.search('view-count">(.*?) näyttökertaa</span>', teksti[i]).group(1)
          self.ehdotukset[mones]["kerrat"] = kerrat    
          kohta = -1
          
        if "tekijä" in teksti[i]:
          tekijaKohta = i
          
        if tekijaKohta != -1:
          if "</span>" in teksti[i]:
            tekija = re.search('">(.*?)</span>', teksti[i]).group(1)
            self.ehdotukset[mones]["tekija"] = tekija
            tekijaKohta = -1
         
   
              
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
    
    self.ed["otsake"] = otsake
    self.ed["linkki"] = linkki
    
    
  def lataa_kpl(self, mones, linkki=""):
    if linkki == "":
      linkki = "https://www.youtube.com/watch?v=" + self.linkit[mones]
    
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
      if len(self.tekijat) >= i:
        tekija = self.tekijat[i]
      else:
        tekija = "ei tekijää"
        
      if len(self.otsakkeet) >= i:
        otsake = self.otsakkeet[i]
      else:
        otsake = "ei otsaketta"
        
      if len(self.ajat) >= i:
        aika = self.ajat[i]
      else:
        aika = "eipä aikaakaan"
        
      if len(self.sittenit) >= i:
        sitten = self.sittenit[i] + "sitten"
      else:
        sitten = "Eis itten"
      
      print(str(i + 1) + ". tulos: " + otsake + " | " + aika + " | " + tekija + " | " + sitten)
      
      if i >= 20:
        break