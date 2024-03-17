""" Ophalen van de waterstand """
import json
from urllib.request import urlopen, Request
from datetime import datetime, timedelta

BASEURL = 'https://waterinfo.rws.nl/api/chart/get' + \
          '?mapType=waterhoogte&locationCode={}({})&values=-48,48'

def lees_json(url):
  """ haal JSON van de URL op """
  req = Request(url=url, headers={'Accept': 'application/json'})
  with urlopen(req) as response:
    content_tekst = response.read().decode('utf-8')
    content_json = json.loads(content_tekst)
    return content_json


def lees_waterstand_json(name, abbr):
  """ lees de informatie van bepaalde locatie """
  return lees_json(BASEURL.format(name,abbr))


def bepaal_standen(content_json):
  """ haal de waterstand uit de gegevens """
  laatstetijd_gemeten = content_json['t0']
  gemeten_standen = content_json['series'][0]['data']
  voorspelde_standen = content_json['series'][1]['data']

  for stand in gemeten_standen:
    if stand['dateTime'] == laatstetijd_gemeten:
      hoogtenu = stand['value']

  if laatstetijd_gemeten.endswith('Z'):
    tijdpatroon = '%Y-%m-%dT%H:%M:%SZ'
    deltatijd = 1
  else:
    tijdpatroon = '%Y-%m-%dT%H:%M:%S+02:00'
    deltatijd = 1

  laatstetijd_obj = datetime.strptime(laatstetijd_gemeten, tijdpatroon) \
                  + timedelta(hours = deltatijd)
  weergave_tijd = laatstetijd_obj.strftime('%d-%m %H:%M')
  morgen_obj = laatstetijd_obj + timedelta(days=1)
  morgen_tekst = morgen_obj.strftime(tijdpatroon)

  hoogtemorgen = hoogtenu
  for stand in voorspelde_standen:
    if stand['dateTime'] == morgen_tekst:
      hoogtemorgen = stand['value']
  return [weergave_tijd, hoogtenu, hoogtemorgen]


def haalwaterstand(name, abbr):
  """ haal de waterstand van een locatie """
  content_json = lees_waterstand_json(name, abbr)
  return bepaal_standen(content_json)
