"""
Parsii YT-sivun tarvittaviksi osasiksi.

"""

import re, requests, json
from bs4 import BeautifulSoup

def sek2min(sek):
  minuut = int(sek / 60)
  sekunn = sek % 60
  return '%i:%i' % (minuut, sekunn)

def hae_sivu(linkki, parametrit={}):
  responssi = requests.get(linkki, params=parametrit, verify=False)
  return responssi.text 

def parsi_juttu(etsittava, kohde):
  juttu = 'ei'
  if re.search(etsittava, kohde) != None:
    juttu = re.search(etsittava, kohde).group(1)
  return juttu  

def parsi_haku3(teksti):
  data = json.loads(teksti)
  kplt = data['feed']['entry']
  tulokset = []
  
  for i in range(len(kplt)):
    kpl = kplt[i]
    tulokset.append({})
    
    tulokset[i]['otsake'] = kpl['title']['$t']
    tulokset[i]['linkki'] = kpl['link'][0]['href'].split('&')[0]
    tulokset[i]['tekija'] = kpl['author'][0]['name']['$t']
    tulokset[i]['aika'] = sek2min(int(kpl['media$group']['media$content'][0]['duration']))
    tulokset[i]['sitten'] = kpl['published']['$t']
    tulokset[i]['kerrat'] = kpl['yt$statistics']['viewCount']
    tulokset[i]['ehdotukset'] = kpl['link'][1]['href'] + '?alt=json'
  return tulokset

def parsi_soittolistahaku3(teksti):
  data = json.loads(teksti)
  listat = data['feed']['entry']
  
  tulokset = []
  
  for i in range(len(listat)):
    lista = listat[i]
    tulokset.append({})
    
    tulokset[i]['otsake'] = kpl['title']['$t']
    tulokset[i]['linkki'] = kpl['link'][1]['href']
    tulokset[i]['tekija'] = kpl['author'][0]['name']['$t']
    tulokset[i]['sitten'] = kpl['published']['$t']
    #tulokset[i]['kerrat'] = kpl['yt$statistics']['viewCount']
    tulokset[i]['ehdotukset'] = kpl['link'][0]['href'] + '?alt=json'
    
  return tulokset

def parsi_haku2(teksti):
  tulokset = []
  
  soppa = BeautifulSoup(teksti)
  
  ajat = [juttu.text for juttu in soppa.find_all('span', class_='video-time')]
  nimet = [juttu.text for juttu in soppa.find_all('a', class_='yt-uix-tile-link')]
  linkit = [juttu['href'] for juttu in soppa.find_all('a', class_='yt-uix-tile-link')]
  tekijat = [juttu.text for juttu in soppa.find_all('a', class_='yt-user-name')]
  sittenit = []
  kerrat = []
  
  for juttu in soppa.select('.yt-lockup-meta'):
    lista = juttu.find_all('li')
    sittenit.append(lista[1].text)
    kerrat.append(lista[2].text)
  
  tulokset = [{'aika' : ajat[i],
               'otsake' : nimet[i],
               'linkki' : linkit[i],
               'tekija' : tekijatt[i],
               'sitten' : sittenit[i],
               'kerrat' : kerrat[i] }
              for i in range(len(ajat))]
  
  return tulokset
  
def parsi_ehdotukset2(teksti):
  tulokset = []
  
  soppa = BeautifulSoup(teksti)
  
  ajat = [juttu.text for juttu in soppa.find_all('span', class_='video-time')]
  nimet = soppa.find_all('span', attrs={'class' : 'title', 'dir' : 'ltr'})
  nimet = [juttu.text.strip() for juttu in nimet]
  linkit = [juttu['href'] for juttu in soppa.find_all('a', class_='related-video')]
  tekijat =  [juttu.text for juttu in soppa.find_all('span', class_='g-hovercard')]
  #jutska 
  #tekijat = [juttu.text for juttu in tekijat]
  #lataajat = [juttu.text for juttu in soppa.find_all('a', class_='yt-user-name')]
  #sittenit = []
  #kerrat = []
  
  #for juttu in soppa.select('.yt-lockup-meta'):
    #lista = juttu.find_all('li')
    #sittenit.append(lista[1].text)
    #kerrat.append(lista[2].text)
  
  #tulokset = [{'aika' : ajat[i],
               #'otsake' : nimet[i],
               #'linkki' : linkit[i],
               #'tekija' : lataajat[i],
               #'sitten' : sittenit[i],
               #'kerrat' : kerrat[i] }
              #for i in range(len(ajat))]
  
  return tekijat
  

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

def parsi_soittolistahaku(teksti):
  tulokset = []
  kohta = -1
  tietoAlku = -1
  tekijaAlku = -1
  mones = -1
  
  for i in range(len(teksti)):

    if "/watch?v=" in teksti[i]:
      kohta = i

    if kohta != -1:
        
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

def parsi_soittolista(teksti):
  kappaleet = []
  
  mones = -1
  kohta = -1
  for i in range(len(teksti)):
    
    if 'pl-video-title-link' in teksti[i]:
      mones += 1
      kappaleet.append({})
      linkki = re.search('href="/watch\?v=(.*?)"', teksti[i]).group(1)
      kappaleet[mones]['linkki'] = linkki
      kohta = 1
      continue
    
    if kohta == 1:
      kappaleet[mones]['nimi'] = teksti[i].strip()
      kohta = -1
  
  return kappaleet
    
def parsi_discogs(uri):
  uri = uri.split('/')
  idi = uri[-1]
  apiUri = 'http://api.discogs.com/release/%s?f=json' % idi
  paa = {'content-type' : 'application/json',
         'user-agent' : 'Stiigel/0.2 +http://stiigel.com'}
  try:
    data = json.loads(requests.get(apiUri, headers=paa).text)['resp']['release']

    artisti = data['artists'][0]['name']
    kplt = [artisti + ' ' + kpl['title'] for kpl in data['tracklist']]
    
  except Exception as e:
    print(e)
    
  return kplt
  
    
    
    
    
    
    
    
  