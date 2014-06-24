"""
Käsittelee käyttäjän antamat komennot, ja välittää ne utubelle

"""

import shlex, os, subprocess, utube

class Kayttoliittyma:
  def __init__(self):
    self.monta = 10
    self.youtube = utube.Utube()
  
  def tulosta_asetus(self, nimi, arvo):
    print('%s: ' % nimi, end='')
    if arvo:
      print('on', end=' | ')
    else:
      print('ei', end=' | ')
      
  def tulosta_asetukset(self):
    putki = ' | '
    print("  ", end=putki)  
    self.tulosta_asetus('Video', self.youtube.asetukset['video'])
    self.tulosta_asetus('sl', self.youtube.asetukset['sl'])
      
    print("Monta: " + str(self.monta), end=putki)
    print("Nykyinen: " + self.youtube.nyk["otsake"], end=putki)
    print()
    
  def auta(self, komento):      
    avut = ['apua', 'help', 'auta']
    if komento[0] in avut:
      print("Tämä on tämmöinen utubejuttu")
      print("Komennot: ")
      print(" --video                 - vaihtaa videoon/epävideoon                     ")
      print(" --sl                    - vaihtaa hakeeko soittolistaa vai epä-          ")
      print(" --monta [n]             - monta tulosta näytetään                        ")
      print(" Hae [haku] [monta]      - hae & näytä [monta] tulosta                    ")
      print(" k [mones1] [monesn]     - mones tulos kuunnellaan                        ")
      print(" l [mones] [monesn]      - mones tulos ladataan                           ")
      print(" onk/l [haku]            - kokeile onneasi, kuuntele/lataa                ")
      print(" pois/exit/moi/quit/bye  - mene pois                                      ")
      print(" mene [mones]            - mene monenteen tulokseen                       ")
      print(" eh                      - näytä nykyisen videon ehdotukset               ")
      print(" ehk [mones]             - soittaa monennen ehdotuksen                    ")
      print(" ehl [mones]             - lataa monennen ehdotuksen                      ")
      print(" kom                     - näytä nykyisen kommentit                       ")
      print(" nyk/l                   - kuuntele/lataa nykyinen                        ")
      print(" ls, cd, pwd, mkdir      - toimivat normaalisti                           ")
      print(" tiedosto l/k nimi       - soittaa/lataa tiedoston jutut rivi kerrallaan  ")
      print(" discogsk/l              - k/l discogs release -sivun (ei master)         ")
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
            elif komento[1] == "nayta":
              print(kpl.strip() + " :")
              self.youtube.nayta_tulokset(self.monta)
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
          
  def discogs(self, komento):
    if komento[0][0 : 7] == 'discogs':
      try:
        self.youtube.discogs(komento[1], komento[0][-1])
      except Exception as e:
        print(e)
  
  def pois(self, komento):
    pois = ["bye", "exit", "quit", "moi", "pois"]
    if komento[0] in pois:
      print("_O/")
      return "pois"
    
  def nykyinen(self, komento):
    if komento[0][0:3] == 'nyk':
      if komento[0][3] == 'k':
        self.youtube.kuuntele_kpl(linkki=self.youtube.nyk['linkki'])
      elif komento[0][3] == 'l':
        self.youtube.lataa_kpl(linkki=self.youtube.nyk['linkki'])
  
  def mene(self, komento):
    if komento[0] == "mene":
      if len(komento) >= 2:
        try:
          self.youtube.mene(int(komento[1]))      
        except:
          self.youtube.mene(-1, komento[1])
          
  def ehdotus(self, komento):
    if komento[0][0:2] == 'eh':
      if self.youtube.kasittele_ehdotukset() == 1:      
        if len(komento[0]) == 2:
          self.youtube.nayta_tulokset(self.monta, ehd=True)   
        
        elif komento[0][2] == 'k':
          for i in range(1, len(komento)):
            try: self.youtube.kuuntele_kpl(ehd=int(komento[i]) - 1)
            except: pass
        
        elif komento[0][2] == 'l':
          for i in range(1, len(komento)):          
            try: self.youtube.lataa_kpl(ehd=int(komento[i]) - 1)
            except: pass
  
  def nayta(self, komento):
    if komento[0] == 'nayta':
      ehd = False
      if len(komento) > 1:
        if komento[1] == 'eh':
          ehd = True
      self.youtube.nayta_tulokset(self.monta, ehd)
  
  def kommentit(self, komento):
    if komento[0] == 'kom':
      try: mista = int(komento[1])
      except: mista = 0
      try: mihin = int(komento[2])
      except: mihin = 10
      
      self.youtube.nayta_kommentit(mista, mihin)
      
  def kasittele_komento(self, komento):
    try:
      komento = shlex.split(komento)
    except:
      print("¡Sulje sitaatit!")
      return
    
    if len(komento) < 1: return
    if self.pois(komento) == 'pois': return 'pois'
  
    if "--video" in komento: self.youtube.vaihda_asetus('video')
    if '--sl' in komento: self.youtube.vaihda_asetus('sl')
    if '--muista' in komento: self.youtube.vaihda_asetus('muista')
    
    for i in range( len(komento) ):
      if komento[i] == "--monta":
        if len(komento) >= i + 1:
          try:
            self.monta = int(komento[i + 1])
          except:
            print("¡Anna luku!")    

    if komento[0] == "hae":
      if len(komento) >= 2: 
        self.youtube.kasittele_haku(komento[1])
        self.youtube.nayta_tulokset(self.monta)      

    elif komento[0] == "l":
      for i in range(1, len(komento)):   
        try: self.youtube.lataa_kpl(int(komento[i]) - 1)            
        except: pass         
        
    elif komento[0] == "k":
      for i in range(1, len(komento)):
        try: self.youtube.kuuntele_kpl(int(komento[i]) - 1)
        except: pass
      
    elif komento[0][0:6] == "linkki":
      if komento[0][6] == "l":
        self.youtube.lataa_kpl(linkki=komento[1])
        
      elif komento[0][6] == "k":
        self.youtube.kuuntele_kpl(linkki=komento[1])

    self.nayta(komento)
    self.auta(komento)
    self.ehdotus(komento)
    self.mene(komento)
    self.nykyinen(komento)
    self.kokeile_onnea(komento)
    self.tiedosto(komento)    
    self.jarjestelmakomento(komento)
    self.discogs(komento)
    self.kommentit(komento)
      
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
          self.youtube.laita_loppuasetukset()
          return   
    
