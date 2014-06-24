"""
Parsii YT-sivun tarvittaviksi osasiksi.

"""

import requests, json
from bs4 import BeautifulSoup

def ota_tunnus(linkki):
  maareet = {}
  for maare in linkki.split('?')[-1].split('&'):
    juttu = maare.split('=')
    maareet[juttu[0]] = juttu[1]
  
  if 'v' in maareet:
    return maareet['v']
  elif 'list' in maareet:
    return maareet['list']  
  return 'ouo'  
  
def sek2tun(sek):
  minuut = int(sek / 60)
  tunnit = int(minuut/60)
  minuut = minuut % 60
  sekunn = sek % 60
  return '%02d:%02d:%02d' % (tunnit, minuut, sekunn)

def parsi_haku(teksti, sl=False):
  data = json.loads(teksti)
  kplt = data['feed']['entry']
  tulokset = []  
  tyyppi = 'soittolista' if sl else 'kappale' 
  
  for i in range(len(kplt)):
    kpl = kplt[i]
    tulokset.append({})
   
    tulokset[i]['tyyppi'] = tyyppi
    tulokset[i]['otsake'] = kpl['title']['$t']
    tulokset[i]['tekija'] = kpl['author'][0]['name']['$t']
    tulokset[i]['sitten'] = kpl['published']['$t']
    tulokset[i]['ehdotukset'] = kpl['link'][1]['href'] + '?alt=json'
    if sl:
      tulokset[i]['linkki'] = kpl['link'][1]['href'].split('&')[0]
    else:
      tulokset[i]['linkki'] = kpl['link'][0]['href'].split('&')[0]
      tulokset[i]['aika'] = sek2tun(int(kpl['media$group']['media$content'][0]['duration']))
      tulokset[i]['kerrat'] = kpl['yt$statistics']['viewCount']
      
  return tulokset

def parsi_soittolista(teksti):
  kappaleet = []
  
  soppa = BeautifulSoup(teksti)
  videot = soppa.find_all('a', class_='pl-video-title-link')
  
  for i in range(len(videot)):
    kappaleet.append({})
    kappaleet[i]['nimi'] = videot[i].text.strip()
    kappaleet[i]['linkki'] = ota_tunnus(videot[i]['href'])
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
