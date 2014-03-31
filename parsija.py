"""
Parsii YT-sivun tarvittaviksi osasiksi.
Toimii surkeasti.

"""

import re

class Parsija:  
  def __init__(self, sivu):
    self.sivu = sivu
    self.alku = 'class="ux-thumb-wrap yt-uix-sessionlink contains-addto spf-link'
    self.alku = self.sivu.find(self.alku)    
    
  def ota_linkit(self):
    linkit = re.findall('/watch\?v=(.*?)"', self.sivu[self.alku:])
    
    for i in range(1, len(linkit)):
      if linkit[i] == linkit[i - 1]:
        linkit[i] = ""
      
    return linkit
    
  def ota_ajat(self):
    ajat = re.findall('<span class="video-time">(.*?)</span>', self.sivu[self.alku:])
    for i in ajat:
      if i == "__length_seconds__":
        ajat.remove(i)
    
    return ajat
    
  def ota_tekijat(self):
    tekijat = re.findall('data-name="">(.*?)</a>', self.sivu[self.alku:])
    return tekijat
  
  def ota_hakuOtsakkeet(self):
    otsakkeet = re.findall('title="(.*?)"[ ]*[\n]*[ ]*data-sessionlink', self.sivu[self.alku:])
    for i in otsakkeet:
      if i == "__title__":
        otsakkeet.remove(i)
      
    return otsakkeet
  
  def ota_kerrat(self):
    kerrat = re.findall('sitten</li><li>(.*?) näyttökertaa</li>[ ]* </ul>', self.sivu[self.alku:])
    for i in kerrat:
      if i == "__views__":
        kerrat.remove(i)  
    
    return kerrat
  
  def ota_otsake(self, linkki):
    responssi = request.get(linkki, verify=False)
    sivu = responssi.text
    
    alku = re.search("<title>", sivu).end()
    loppu = re.search("</title>", sivu).start()
    
    return teksti[alku : loppu]
  