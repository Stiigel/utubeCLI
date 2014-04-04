"""
Käsittelee käyttäjän antamat komennot, ja välittää ne utubelle

"""

import shlex
import utube

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
    print(" | Edellinen: " + self.youtube.ed["otsake"], end="")
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
    
  def aloita(self, apu=False):
    pois = ["bye", "exit", "quit", "moi", "pois"]
    
    if apu == True:
      self.auta()
      
    while True:
      self.tulosta_asetukset()
      try:
        komento = shlex.split(input(" > "))
      except:
        print("¡Sulje sitaatit!")
        continue
      
      if len(komento) == 0:
        continue
      
      if "--video" in komento:
        self.youtube.laita_video()
      
      for i in range( len(komento) ):
        if komento[i] == "--monta":
          if len(komento) >= i + 1:
            try:
              self.monta = int(komento[i + 1])
            except:
              print("¡Anna luku!")
      
      if komento[0] in pois:
        print("_O/")
        break

      if komento[0] == "hae":
        if len(komento) >= 2: 
          self.youtube.kasittele_haku(komento[1])     
          if len(komento) >= 3:
            self.monta = int(komento[2])
          self.youtube.nayta_tulokset(self.monta)      
          
      if komento[0] == "ehd":
        self.youtube.kasittele_ehdotukset()
        if len(komento) >= 2:
          self.monta = int(komento[1])
        self.youtube.nayta_ehdotukset(self.monta)
        

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
      
      elif komento[0] == "help" or komento[0] == "apua":
        self.auta()
        
      elif komento[0][0:6] == "linkki":
        if komento[0][6] == "l":
          self.youtube.lataa_kpl(0, linkki=komento[1])
          
        elif komento[0][6] == "k":
         self.youtube.kuuntele_kpl(0, linkki=komento[1])
          
      elif komento[0] == "sika":
        self.youtube.kasittele_haku("Kissa")

      
        
    