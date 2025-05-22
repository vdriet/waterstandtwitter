""" programma om waterstanden naar Twitter te versturen """
import os

import tweepy
import waterstand

lijst = {
  'KATV': {'naam': 'Katerveer', 'water': 'IJssel', 'plaats': 'Zwolle', 'twitter': 'KATV'},
  'WIJH': {'naam': 'Wijhe', 'water': 'IJssel', 'twitter': 'WIJHE'},
  'ZUTP': {'naam': 'Zutphen-Noord', 'water': 'IJssel', 'twitter': 'ZUTP'},
}


def twitterwaterstand(key: str, weergavetijd: str, hoogtenu: int, hoogtemorgen: int) -> None:
  """ versturen van de waterstand naar Twitter
:param key: naam van de locatie
:type key:str
:param weergavetijd: datum en tijd van de weergave
:type weergavetijd: str
:param hoogtenu: hoogte van de laatste meting
:type hoogtenu: int
:param hoogtemorgen: verwachte hoogte van morgen
:type hoogtemorgen: int
:rtype: None
"""
  datum, tijd = weergavetijd.split()
  gegevens = lijst.get(key, {})
  if gegevens == {}:
    print(f'Geen gegevens gevonden voor {key}')
  else:
    naam = gegevens.get('naam')
    water = gegevens.get('water')
    plaats = gegevens.get('plaats')

    bericht = f'De #waterstand van de #{water} '
    if plaats is None:
      bericht = bericht + f'bij #{naam} '
    else:
      bericht = bericht + f'bij #{plaats} ({naam}) '
    if hoogtenu >= 0:
      bericht = bericht + f'was {hoogtenu} cm boven NAP op {datum} om {tijd}'
    else:
      hoogtenu = hoogtenu * -1
      bericht = bericht + f'was {hoogtenu} cm onder NAP op {datum} om {tijd}'
    if hoogtemorgen >= 0:
      bericht = bericht + f', verwachting voor morgen is {hoogtemorgen} cm boven NAP'
    else:
      hoogtemorgen = hoogtemorgen * -1
      bericht = bericht + f', verwachting voor morgen is {hoogtemorgen} cm onder NAP'
    tweetbericht(gegevens.get('twitter', ''), bericht)
    print(f'Succesvol tweet geplaatst voor {key} met gegevens van {datum} {tijd}')


def tweetbericht(key: str, tekst: str) -> None:
  """ Tweeten van 1 bericht
  :param key: naam van de locatie
  :type key: str
  :param tekst: bericht voor tweet
  :type tekst: str
  :rtype: None
  """
  envappkey: str = os.environ.get(f'TWITTER_{key}_APP_KEY', '')
  envappsecret: str = os.environ.get(f'TWITTER_{key}_APP_SECRET', '')
  envaccesstoken: str = os.environ.get(f'TWITTER_{key}_ACCESS_TOKEN', '')
  envaccesstokensecret: str = os.environ.get(f'TWITTER_{key}_ACCESS_TOKEN_SECRET', '')
  envbearertoken: str = os.environ.get(f'TWITTER_{key}_BEARER_TOKEN', '')
  client = tweepy.Client(bearer_token=envbearertoken,
                         consumer_key=envappkey,
                         consumer_secret=envappsecret,
                         access_token=envaccesstoken,
                         access_token_secret=envaccesstokensecret)
  client.create_tweet(text=tekst)


def main() -> None:
  """ hoofdroutine """
  key: str
  locaties: dict[str, str]
  for key, locaties in lijst.items():
    gegevens: dict = waterstand.haalwaterstand(locaties.get('naam', ''), key)
    if gegevens['resultaat'] == 'NOK':
      tweetbericht(key, gegevens['tekst'])
    else:
      weergavetijd: str = gegevens['tijd']
      hoogtenu: int = gegevens['nu']
      hoogtemorgen: int = gegevens['morgen']
      twitterwaterstand(key, weergavetijd, hoogtenu, hoogtemorgen)


if __name__ == "__main__":
  main()
