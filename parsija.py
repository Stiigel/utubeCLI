"""
Parsii YT-sivun tarvittaviksi osasiksi.

"""

import re

def lisaa_juttu(lista, mones, tulos):
  print("Löts lölöö")

def parsi_juttu(etsittava, kohde):
  juttu = 'ei'
  if re.search(etsittava, kohde) != None:
    juttu = re.search(etsittava, kohde).group(1)
  return juttu  

def parsi_haku(teksti):
  tulokset = []
  
  kohta = -1
  tietoAlku = -1
  tekijaAlku = -1
  mones = -1
  for i in range(len(teksti)):
    if "/watch?v=" in teksti[i]:
      kohta = i

    if kohta != -1:
      if 'class="video-time">' in teksti[i] and 'video-time">__' not in teksti[i]:
        mones += 1
        tulokset.append({})
        tulokset[mones]["aika"] = parsi_juttu('"video-time">(.*?)</span>', teksti[i])
        
      if 'yt-uix-sessionlink yt-uix-tile-link' in teksti[i]:
        tietoAlku = i
      
      if tietoAlku != -1:
        if 'title="' in teksti[i]:
          tulokset[mones]["otsake"] = parsi_juttu('title="(.*?)"', teksti[i])
        
        if 'href="/watch?v=' in teksti[i]:
          tulokset[mones]["linkki"] = parsi_juttu('href="/watch\?v=(.*?)"', teksti[i])
          tietoAlku = -1

        if '>' in teksti[i]:
          tietoAlku = -1
      
      if 'g-hovercard yt-uix-sessionlink yt-user-name' in teksti[i]:
        tekijaAlku = i
      
      if tekijaAlku != -1:
        if 'data-name' in teksti[i]:
          tulokset[mones]["tekija"] = parsi_juttu('data-name="">(.*?)</a>', teksti[i])
        if 'sitten' in teksti[i]:
          tulokset[mones]["sitten"] = parsi_juttu('<li>(.*?)sitten</li><li>', teksti[i])
        if 'näyttökertaa' in teksti[i]:
          tulokset[mones]["kerrat"] = parsi_juttu('sitten</li><li>(.*?) näyttökertaa</li>',teksti[i])
          tekijaAlku = -1
          kohta = -1
          
  return tulokset

    
def parsi_ehdotukset(teksti):
  ehdotukset = []
  
  kohta = -1
  tekijaKohta = -1
  mones = -1
  for i in range(len(teksti)):
    
    if 'related-video' in teksti[i]:
      mones += 1
      kohta = i
      ehdotukset.append({})     
    
    if kohta != -1:
      if 'href="/watch?v=' in teksti[i]:
        linkki = re.search('href="/watch\?v=(.*?)"', teksti[i]).group(1)
        ehdotukset[mones]["linkki"] = linkki
        
      if '<span class="video-time">' in teksti[i]:
        aika = re.search('<span class="video-time">(.*?)</span>', teksti[i]).group(1)
        ehdotukset[mones]["aika"] = aika
        
      if 'class="title" title="' in teksti[i]:
        otsake = re.search('class="title" title="(.*?)"', teksti[i]).group(1)
        ehdotukset[mones]["otsake"] = otsake
      
      if '<span class="stat view-count">' in teksti[i]:
        kerrat = re.search('view-count">(.*?) näyttökertaa</span>', teksti[i]).group(1)
        ehdotukset[mones]["kerrat"] = kerrat    
        kohta = -1
        
      if "tekijä" in teksti[i]:
        tekijaKohta = i
        
      if tekijaKohta != -1:
        if "</span>" in teksti[i]:
          tekija = re.search('">(.*?)</span>', teksti[i]).group(1)
          ehdotukset[mones]["tekija"] = tekija
          tekijaKohta = -1
  
  return ehdotukset