""" programma om waterstanden naar Twitter te versturen """
import os
import tweepy
import waterstand

lijst = {
  'KATV': {'naam': 'Katerveer', 'water': 'IJssel', 'plaats': 'Zwolle', 'twitter': 'KATV'},
  'WIJH': {'naam': 'Wijhe', 'water': 'IJssel', 'twitter': 'WIJHE'},
  'ZUTP': {'naam': 'Zutphen-Noord', 'water': 'IJssel', 'twitter': 'ZUTP'},
}


def twitterwaterstand(key, weergavetijd, hoogtenu, hoogtemorgen):
  """ versturen van de waterstand naar Twitter """
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
    tweetbericht(gegevens.get('twitter'), bericht)
    print(f'Succesvol tweet geplaatst voor {key} met gegevens van {datum} {tijd}')


def tweetbericht(key, tekst):
  """ Tweeten van 1 bericht """
  envappkey = os.environ.get(f'TWITTER_{key}_APP_KEY')
  envappsecret = os.environ.get(f'TWITTER_{key}_APP_SECRET')
  envaccesstoken = os.environ.get(f'TWITTER_{key}_ACCESS_TOKEN')
  envaccesstokensecret = os.environ.get(f'TWITTER_{key}_ACCESS_TOKEN_SECRET')
  envbearertoken = os.environ.get(f'TWITTER_{key}_BEARER_TOKEN')
  client = tweepy.Client(bearer_token=envbearertoken,
                         consumer_key=envappkey,
                         consumer_secret=envappsecret,
                         access_token=envaccesstoken,
                         access_token_secret=envaccesstokensecret)
  client.create_tweet(text=tekst)


def main():
  """ hoofdroutine """
  for key, locaties in lijst.items():
    gegevens = waterstand.haalwaterstand(locaties.get('naam'), key)
    if gegevens['resultaat'] == 'NOK':
      tweetbericht(key, gegevens['tekst'])
    else:
      weergavetijd = gegevens['tijd']
      hoogtenu = gegevens['nu']
      hoogtemorgen = gegevens['morgen']
      twitterwaterstand(key, weergavetijd, hoogtenu, hoogtemorgen)


if __name__ == "__main__":
  main()
