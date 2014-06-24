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

def parsi_aika(aika):
  aika = aika.replace('T', ' ')
  aika = aika.split('.')[0]  
  return aika

def parsi_haku(teksti, sl=False):
  data = json.loads(teksti)
  kplt = data['feed']['entry']
  tulokset = []  
  
  for i in range(len(kplt)):
    kpl = kplt[i]
    tulokset.append({})
    
    if 'video' in kpl['id']['$t']:
      tulokset[i]['tyyppi'] = 'video'
    else:
      tulokset[i]['tyyppi'] = 'sl'
      
    tulokset[i]['otsake'] = kpl['title']['$t']
    tulokset[i]['tekija'] = kpl['author'][0]['name']['$t']
    tulokset[i]['julkaistu'] = parsi_aika(kpl['published']['$t'])
    
    for linkki in kpl['link']:
      if linkki['rel'] == 'alternate':
        tulokset[i]['linkki'] = linkki['href']

    if not sl:
      tulokset[i]['ehdotukset'] = kpl['link'][1]['href'] + '?alt=json'
      tulokset[i]['aika'] = sek2tun(int(kpl['media$group']['media$content'][0]['duration']))
      tulokset[i]['kerrat'] = kpl['yt$statistics']['viewCount']
    else:
      tulokset[i]['maara'] = kpl['yt$countHint']['$t']
      
  return tulokset

def parsi_kommentit(teksti):
  data = json.loads(teksti)['feed']['entry']
  kommentit = []
  for i in range(len(data)):
    kommentti = data[i]
    kommentit.append({})
    
    kommentit[i]['nimi'] = kommentti['author'][0]['name']['$t']
    kommentit[i]['julkaistu'] = parsi_aika(kommentti['published']['$t'])
    kommentit[i]['sisalto'] = kommentti['content']['$t']
  return kommentit

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
