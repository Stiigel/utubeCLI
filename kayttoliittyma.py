"""
Käsittelee käyttäjän antamat komennot, ja välittää ne utubelle

"""

import shlex, os, subprocess, utube

class Kayttoliittyma:
  def __init__(self):
    self.monta = 10
    self.youtube = utube.Utube()
    
  def tulosta_asetukset(self):
    print("    ", end="")    
    print("| Video: ", end="")
    
    if self.youtube.video == True:
      print("on", end="")
    else:
      print("ei", end="")
      
    print(" | Monta: " + str(self.monta), end="")
    print(" | Nykyinen: " + self.youtube.nyk["otsake"], end="")
    print(" |")
    
  def auta(self):
    print("Tämä on tämmöinen utubejuttu")
    print("Komennot: ")
    print(" --video                 - vaihtaa videoon/epävideoon                     ")
    print(" --monta [n]             - monta tulosta näytetään                        ")
    print(" Hae [haku] [monta]      - hae & näytä [monta] tulosta                    ")
    print(" k [mones]               - mones tulos kuunnellaan                        ")
    print(" l [mones]               - mones tulos ladataan                           ")
    print(" onk/l [haku]            - kokeile onneasi, kuuntele/lataa                ")
    print(" pois/exit/moi/quit/bye  - mene pois                                      ")
    print(" mene [mones]            - mene monenteen tulokseen                       ")
    print(" ehd                     - näytä nykyisen videon ehdotukset               ")
    print(" ehk [mones]             - soittaa monennen ehdotuksen                    ")
    print(" ehl [mones]             - lataa monennen ehdotuksen                      ")
    print(" ls, cd, pwd, mkdir      - toimivat normaalisti                           ")
    print("                         -                                                ")
  
  def jarjestelmakomento(self,komento):
    if komento[0] == "cd":
      try:
        os.chdir(komento[1])
        subprocess.call(["pwd"])
      except OSError:
        print("Ei suuchia hakemistoa")
    
    elif komento[0] == "ls":
      subprocess.call(["ls", "-p"] + komento[1:])
      
    elif komento[0] == "pwd":
      subprocess.call(["pwd"])
      
    elif komento[0] == "mkdir":
      try:
        subprocess.call(["mkdir", komento[1]])
      except:
        print("Anna kunnoll. nimi")
        
  def tiedosto(self, komento):
    if komento[0] == "tiedosto":
      if len(komento) >= 3:
        try:
          tiedosto = open(komento[2], 'r')
          kplt = tiedosto.readlines()
          tiedosto.close()
        except OSError:
          kplt = []
          print("Ei suuchia tiedostoa")
        for kpl in kplt:
          try:
            self.youtube.kasittele_haku(kpl)
            if komento[1] == "l":
              self.youtube.lataa_kpl(0)        
            elif komento[1] == "k":
              self.youtube.kuuntele_kpl(0)
          except:
            pass
          
  def kokeile_onnea(self, komento):
    if komento[0][0 : 2] == "on":
      if len(komento) >= 3:
        mones = int(komento[2])
      else:
        mones = 1
      self.youtube.kasittele_haku(komento[1])
      if len(komento[0]) >= 3:
        if komento[0][2] == "k":
          self.youtube.kuuntele_kpl(mones - 1)
      
        elif komento[0][2] == "l":
          self.youtube.lataa_kpl(mones - 1)        
    
  def kasittele_komento(self, komento):
    try:
      komento = shlex.split(komento)
    except:
      print("¡Sulje sitaatit!")
      return
  
    if "--video" in komento:
      self.youtube.laita_video()
    
    for i in range( len(komento) ):
      if komento[i] == "--monta":
        if len(komento) >= i + 1:
          try:
            self.monta = int(komento[i + 1])
          except:
            print("¡Anna luku!")
    
    pois = ["bye", "exit", "quit", "moi", "pois"]
    if komento[0] in pois:
      print("_O/")
      return "pois"

    if komento[0] == "hae":
      if len(komento) >= 2: 
        if "--sl" in komento:
          self.youtube.kasittele_haku(komento[1], soittolista=True)
        else:
          self.youtube.kasittele_haku(komento[1])
        #if len(komento) >= 3:
          #self.monta = int(komento[2])
        self.youtube.nayta_tulokset(self.monta)      
        
    if komento[0] == "ehd":
      self.youtube.kasittele_ehdotukset()
      if len(komento) >= 2:
        self.monta = int(komento[1])
      self.youtube.nayta_ehdotukset(self.monta)
    
    if komento[0] == "mene":
      if len(komento) >= 2:
        self.youtube.mene(int(komento[1]))      

    elif komento[0] == "l":
      try:
        for i in range(1, len(komento)):          
          self.youtube.lataa_kpl(int(komento[i]) - 1)            
      except:
        print("sörs")
        
    elif komento[0] == "k":
      try:
        for i in range(1, len(komento)):
          self.youtube.kuuntele_kpl(int(komento[i]) - 1)
      except:
        print("lälälä")
    
    elif komento[0] == "ehl":
      try:
        for i in range(1, len(komento)):          
          self.youtube.lataa_kpl(0, ehd=int(komento[i]) - 1)            
      except:
        print("lörs")
        
    elif komento[0] == "ehk":
      try:
        for i in range(1, len(komento)):
          self.youtube.kuuntele_kpl(0, ehd=int(komento[i]) - 1)
      except:
        print("lärä")
    elif komento[0] == "help" or komento[0] == "apua":
      self.auta()
      
    elif komento[0][0:6] == "linkki":
      if komento[0][6] == "l":
        self.youtube.lataa_kpl(0, linkki=komento[1])
        
      elif komento[0][6] == "k":
        self.youtube.kuuntele_kpl(0, linkki=komento[1])
      
    self.kokeile_onnea(komento)
    self.tiedosto(komento)    
    self.jarjestelmakomento(komento)
      
  def aloita(self, apu=False):    
    if apu == True:
      self.auta()
      
    while True:
      self.tulosta_asetukset()
      
      komennot = input(" > ")
      
      if len(komennot.strip()) == 0:
        continue
      
      for komento in komennot.split(";"):
        if self.kasittele_komento(komento) == "pois":
          return
