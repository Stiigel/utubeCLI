"""
Kaikki itse YTiin liittyvät jutut, ja musan/videojen näyttäminen ja lataaminen

"""

import sys, re, parsija, subprocess, requests, os

class Utube:  
  def __init__(self):
    self.tulokset = []    
    self.ehdotukset = []   
    self.nyk = {"otsake" : "", "linkki" : ""}    
    self.laita_alkuasetukset()    
    
  def laita_alkuasetukset(self):
    self.asetukset = {'video' : False, 'sl' : False, 'muista' : False}
    
    koti = os.path.expanduser('~')
    kansio = koti + '/.utubecli/'
    tiedosto = kansio + 'asetukset.conf'
    
    if not os.path.isdir(kansio):
      os.mkdir(kansio)
    
    if not os.path.exists(tiedosto):
      tiedosto = open(tiedosto, 'w', encoding='utf-8')
      for asetus in self.asetukset:
        tiedosto.write('%s %i\n' % (asetus, self.asetukset[asetus]))

      tiedosto.close()
    
    else:
      tiedosto = open(tiedosto, 'r', encoding='utf-8')
      rivit = [rivi.split(' ') for rivi in tiedosto.readlines()]
      tiedosto.close()
      
      for rivi in rivit:
        asetus = rivi[0]
        arvo = rivi[1]
        
        if asetus in self.asetukset:
          self.asetukset[asetus] = bool(int(arvo))
      
  def laita_loppuasetukset(self):
    if self.asetukset['muista']:
      tiedosto = open(os.path.expanduser('~') + '/.utubecli/asetukset.conf', 'w')
      for asetus in self.asetukset:
        tiedosto.write('%s %i\n' % (asetus, self.asetukset[asetus]))
      tiedosto.close()  
   
  def vaihda_asetus(self, asetus):
    self.asetukset[asetus] = not self.asetukset[asetus]
    print('%s %i' % (asetus, self.asetukset[asetus]))
  
  def kasittele_haku(self, haku):    
    parametrit = {'q' : haku, 'alt' : 'json', 'v' : '2'}
    
    juttu = 'videos/'
    if self.asetukset['sl']:
      juttu = 'playlists/snippets/'
      
    uri = 'https://gdata.youtube.com/feeds/api/' + juttu    
    teksti = requests.get(uri, params=parametrit, verify=False).text
    
    self.tulokset = parsija.parsi_haku(teksti, self.asetukset['sl'])
         
  def kasittele_ehdotukset(self):
    if self.nyk["linkki"] == "":
      print("¡Kuuntele/lataa/mene ensin!")
      return -1
    
    if 'playlist' in self.nyk['linkki']:
      print("Ei ehdotuksia soittolistioilel")
      return -1
    
    linkki = 'https://gdata.youtube.com/feeds/api/videos/%s/related?v=2&alt=json'    
    tunnus = parsija.ota_tunnus(self.nyk['linkki'])
    
    teksti = requests.get(linkki % tunnus, verify=False).text 
    self.ehdotukset = parsija.parsi_haku(teksti)
    return 1
  
  def nayta_kommentit(self, mista=0, mihin=10):
    if 'playlist' in self.nyk['linkki']:
      print("Ei komementeja soittolistoille")
      return
    
    linkki = 'https://gdata.youtube.com/feeds/api/videos/%s/comments?v=2&alt=json' 
    tunnus = parsija.ota_tunnus(self.nyk['linkki'])
    teksti = requests.get(linkki % tunnus, verify=False).text
    
    print('\nKommentit:\n')
    for kommentti in parsija.parsi_kommentit(teksti)[mista:mihin]:
      print("%s @ %s:" % (kommentti['nimi'], kommentti['julkaistu']))
      print()
      print(kommentti['sisalto'])
      print("-" * 20)
              
  def laita_otsake(self, mones=-1, linkki='', ehd=-1):
    otsake = ''
    
    if linkki != '':
      responssi = requests.get(linkki, verify=False)
      teksti = responssi.text
      otsake = re.findall('<title>(.*?)</title>', teksti)[0]
    
    elif ehd != -1:
      otsake = self.ehdotukset[mones]['otsake'] + ' - Youtube'
    elif mones != -1:
      otsake = self.tulokset[mones]['otsake'] + ' - Youtube'      
    
    print(otsake)
    return otsake
  
  def laita_linkki(self, mones=-1, linkki='', ehd=-1):
    if linkki == "" and ehd == -1:
      linkki = self.tulokset[mones]["linkki"]
    elif linkki == "" and ehd != -1:
      linkki = self.ehdotukset[ehd]["linkki"]
    
    print("Linkki: " + linkki)
    return linkki      

  def kuuntele_kpl(self, mones=-1, linkki="", ehd=-1):
    linkki = self.laita_linkki(mones, linkki, ehd)
    
    if 'playlist' in linkki:
      self.kuuntele_soittolista(linkki)
      return
      
    prosessi = subprocess.Popen(["youtube-dl", "-g", linkki], stdout=subprocess.PIPE)
    utuLinkki, error = prosessi.communicate()
    utuLinkki = utuLinkki.rstrip()
    
    otsake = self.laita_otsake(mones, linkki, ehd)
    
    kaskyt = ["mpv", utuLinkki, "--title", otsake]
    
    if not self.asetukset['video']:
      kaskyt.append("--no-video") 
      
    subprocess.call(kaskyt)
    
    self.nyk["otsake"] = otsake
    self.nyk["linkki"] = linkki    
    
  def lataa_kpl(self, mones=-1, linkki="", ehd=-1):
    linkki = self.laita_linkki(mones, linkki, ehd)
    
    kaskyt = ["youtube-dl", linkki, "-cit"]
    if not self.asetukset['video']:
      kaskyt.append("-x")
    
    subprocess.call(kaskyt)
    
  def mene(self, mones, linkki=""):
    if linkki == "":
      self.nyk["otsake"] = self.tulokset[mones - 1]["otsake"]
      self.nyk["linkki"] = self.tulokset[mones - 1]["linkki"]
    else:
      self.nyk["linkki"] = linkki
      self.nyk["otsake"] = self.laita_otsake(linkki=linkki)
  
  def nayta_tulokset(self, monta, ehd=False):    
    lista = self.ehdotukset if ehd else self.tulokset
    
    for i in range(monta):
      if len(lista) <= i:
        return
     
      jutut = ['otsake', 'aika', 'tekija', 'kerrat', 'julkaistu', 'tyyppi']
      if lista[i]['tyyppi'] == 'sl':
        jutut.remove('aika')
        jutut.remove('kerrat')
        jutut.append('maara')
      
      print("%i. tulos: " % (i + 1), end='')
      for juttu in jutut:
        print('%s' % lista[i][juttu], end=' | ')
      print()      

  def kuuntele_soittolista(self, linkki):
    responssi = requests.get(linkki, verify=False)
    kplt = parsija.parsi_soittolista(responssi.text)

    for i in range(len(kplt)):
      print("%i / %i" % ( i + 1, len(kplt)))
      linkki = 'https://www.youtube.com/watch?v=' + kplt[i]['linkki']
      self.kuuntele_kpl(0, linkki)

  def discogs(self, linkki, tapa):
    kplt = parsija.parsi_discogs(linkki)
    for kpl in kplt:
      print(kpl)
      self.kasittele_haku(kpl)
      if tapa == 'l':
        self.lataa_kpl(0)
      elif tapa == 'k':
        self.kuuntele_kpl(0)
      else:
        return
    