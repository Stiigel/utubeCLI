"""
Kaikki itse YTiin liittyvät jutut, ja musan/videojen näyttäminen ja lataaminen

"""

import sys, re, parsija, subprocess, requests

class Utube:  
  def __init__(self):
    self.video = False
    self.sl = False

    self.tulokset = []    
    self.ehdotukset = []
    
    self.nyk = {"otsake" : "", "linkki" : ""}
    
  def laita_video(self):
    self.video = not self.video
    
  def laita_sl(self):
    self.sl = not self.sl
  
  def kasittele_haku(self, haku):    
    self.tulokset = []
    
    parametrit = {'q' : haku, 'alt' : 'json', 'v' : '2'}
    
    juttu = 'videos/'
    if self.sl:
      juttu = 'playlists/snippets/'
      
    uri = 'https://gdata.youtube.com/feeds/api/' + juttu
    
    teksti = requests.get(uri, params=parametrit, verify=False).text
    
    self.tulokset = parsija.parsi_haku(teksti, soittolista)
         
  def kasittele_ehdotukset(self):
    if self.nyk["linkki"] == "":
      print("¡Kuuntele/lataa/mene ensin!")
      return -1
    
    linkki = 'https://gdata.youtube.com/feeds/api/videos/%s/related?v=2&alt=json'    
    tunnus = parsija.ota_tunnus(self.nyk['linkki'])
    
    teksti = requests.get(linkki % tunnus, verify=False).text 
    self.ehdotukset = parsija.parsi_haku(teksti)
    return 1
  
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
    
    if self.video == False:
      kaskyt.append("--no-video") 
      
    subprocess.call(kaskyt)
    
    self.nyk["otsake"] = otsake
    self.nyk["linkki"] = linkki    
    
  def lataa_kpl(self, mones=-1, linkki="", ehd=-1):
    linkki = self.laita_linkki(mones, linkki, ehd)
    
    kaskyt = ["youtube-dl", linkki, "-cit"]
    if self.video == False:
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
     
      jutut = ['otsake', 'aika', 'tekija', 'kerrat', 'sitten']
      if lista[i]['tyyppi'] == 'soittolista':
        jutut.remove('aika')
        jutut.remove('kerrat')
      
      print("%i. tulos: " % (i + 1), end='')
      for juttu in jutut:
        print('%s' % lista[i][juttu], end=' | ')
      print()      

  def kuuntele_soittolista(self, linkki):
    responssi = requests.get(linkki, verify=False)
    kplt = parsija.parsi_soittolista(responssi.text)

    for kpl in kplt:
      linkki = 'https://www.youtube.com/watch?v=' + kpl['linkki']
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
    