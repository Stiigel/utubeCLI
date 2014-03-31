import sys, re
import subprocess
import requests
import shlex
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
     
  def tulosta_asetukset(self, monta):
    print("    ", end="")
    
    print("| Video: ", end="")
    if self.video == True:
      print("on", end="")
    else:
      print("ei", end="")
      
    print(" | Monta: " + str(monta), end="")

    print(" |")
    
  def auta(self):
    print("Tämä on tämmöinen utubejuttu")
    print("Komennot: ")
    print(" --video            - vaihtaa videoon/epävideoon")
    print(" --monta [n]        - monta tulosta näytetään")
    print(" Hae [haku] [monta] - hae & näytä [monta] tulosta")
    print(" k [mones]          - mones tulos kuunnellaan")
    print(" l [mones]          - mones tulos ladataan")
    print(" onk/l [haku]       - kokeile onneasi, kuuntele/lataa")

    
  def kasittele_haku2(self, haku):    
    parametrit = { "search_query" : haku, "filters" : "video", "lclk" : "video", "hl" : "fi" }
    responssi = requests.get("https://www.youtube.com/results", params=parametrit, verify=False)
    teksti = responssi.text    
    persilja = parsija.Parsija(teksti)
    
    self.linkit = persilja.ota_linkit()
    self.ajat = persilja.ota_ajat()
    self.tekijat = persilja.ota_tekijat()
    self.otsakkeet = persilja.ota_hakuOtsakkeet()   
    
    
  def kasittele_haku(self, haku):
    self.linkit = []
    self.ajat = []
    self.tekijat = []
    self.otsakkeet = []
    
    parametrit = { "search_query" : haku, "filters" : "video", "lclk" : "video" }
    responssi = requests.get("https://www.youtube.com/results", params=parametrit, verify=False)
    teksti = responssi.text.split("\n")
    
    kohta = -1
    mones = 0
    
    for i in range(len(teksti)):
      alku = 'class="ux-thumb-wrap yt-uix-sessionlink contains-addto spf-link'
      if alku in teksti[i]:
        kohta = i
        
      if kohta != -1:
        katso = '/watch?v='
        paikka = teksti[i].find(katso)
        #paikka = re.search(katso, teksti[i])
        if paikka != -1:
          mones += 1
          linkki = teksti[i][paikka + len(katso) : paikka + len(katso) + 11]
          #linkki = teksti[i][paikka.end() : paikka.end() + 11]
          self.linkit.append(linkki)
        
        alku = re.search('<span class="video-time">', teksti[i])
        loppu = re.search('</span>', teksti[i])
        
        if alku != None and mones > 0:
          self.tayta(self.ajat, self.linkit, "ei aikaa")
          
          self.ajat.append( teksti[i][alku.end() : loppu.start()])
          kohta = -1
      
      tekijaJuttu = 'class="g-hovercard yt-uix-sessionlink yt-user-name spf-link'
      
      if tekijaJuttu in teksti[i] and mones > 0:
        tekijaAlku = re.search('data-name="">', teksti[i])
        tekijaLoppu = re.search('</a>', teksti[i])
        
        if tekijaAlku != None:
          self.tayta(self.tekijat, self.linkit, "Ei tekijää")
          self.tekijat.append( teksti[i][tekijaAlku.end() : tekijaLoppu.start()])    
          
    self.tayta(self.ajat, self.linkit, "ei aikaa", 0)
    self.tayta(self.tekijat, self.linkit, "Ei tekijää", 0)
    
  def tayta(self, lista, lista2, lisays, vahennys=1):
    while len(lista) < len(lista2) - vahennys:
      taulukko.append(lisays)
        
        
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
        #otsake = self.otsakkeet[i]
        otsake = self.ota_otsake(self.utuAlku + self.linkit[i])
      except:
        otsake = "ei otsaketta"
      try:
        aika = self.ajat[i]
      except:
        aika = "eipä aikaakaan"
      
      print(str(i + 1) + ". tulos: " + otsake + " | " + aika + " | " + tekija)
      
      if i >= 20:
        break
    
  def paa(self): 
    monta = 10
    while True:
      self.tulosta_asetukset(monta)
      try:
        komento = shlex.split(input(" > "))
      except:
        print("¡Sulje sitaatit!")
        continue
      
      if len(komento) == 0:
        continue
      
      if "--video" in komento:
        self.video = not self.video 
        
      for i in range( len(komento) ):
        if komento[i] == "--monta":
          if len(komento) >= i + 1:
            monta = int(komento[i + 1])
      
      pois = ["bye", "exit", "quit", "moi"]
      if komento[0] in pois:
        print("_O/ \O_ _O/ \O_")
        break     
      
      if komento[0] == "hae":
        try: 
          self.kasittele_haku(komento[1])          
          monta = int(komento[2])
          self.nayta_tulokset(monta)         
            
        except:
          self.nayta_tulokset(monta)
        
      if komento[0][0 : 2] == "on":
        try:
          try:
            mones = int(komento[2])
          except:
            mones = 1
          self.kasittele_haku(komento[1])
          if komento[0][2] == "k":
            self.kuuntele_kpl(mones - 1)
          
          elif komento[0][2] == "l":
            self.lataa_kpl(mones - 1)
            
        except:
          print("¡Fetaliikennemerkki bärs!")
          
      elif komento[0] == "l":
        try:
          for i in range(1, len(komento)):          
            self.lataa_kpl(int(komento[i]) - 1)
            
        except:
          self.lataa_kpl(0)
          
      elif komento[0] == "k":
        try:
          for i in range(1, len(komento)):
            self.kuuntele_kpl(int(komento[i]) - 1)
        except:
          self.kuuntele_kpl(0)
      
      elif komento[0] == "help" or komento[0] == "apua":
        self.auta()
        
      elif komento[0][0:6] == "linkki":
        if komento[0][6] == "l":
          self.lataa_kpl(0, linkki=komento[1])
          
        elif komento[0][6] == "k":
          self.kuuntele_kpl(0, linkki=komento[1])
          
      elif komento[0] == "sika":
        self.kasittele_haku("Kissa")

      
utube = Utube()
utube.paa()
    
  