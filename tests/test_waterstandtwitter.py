import unittest
from unittest.mock import patch

import waterstandtwitter


class TestWaterstandTwitter(unittest.TestCase):

  @patch('waterstand.haalwaterstand',
         side_effect=[{'resultaat': 'OK', 'tijd': '', 'nu': '', 'morgen': ''},
                      {'resultaat': 'OK', 'tijd': '', 'nu': '', 'morgen': ''},
                      {'resultaat': 'OK', 'tijd': '', 'nu': '', 'morgen': ''},
                      ])
  @patch('waterstandtwitter.tweetbericht')
  @patch('waterstandtwitter.twitterwaterstand')
  def test_main_data(self, mock_twitterwaterstand, mock_tweetbericht, mock_haalwaterstand):
    mock_twitterwaterstand.return_value = ''
    mock_tweetbericht.return_value = ''

    waterstandtwitter.main()

    assert mock_haalwaterstand.call_count == 3
    assert mock_tweetbericht.call_count == 0
    assert mock_twitterwaterstand.call_count == 3

  @patch('waterstand.haalwaterstand',
         side_effect=[{'resultaat': 'NOK', 'tekst': 'Foutmelding'},
                      {'resultaat': 'NOK', 'tekst': 'Foutmelding'},
                      {'resultaat': 'NOK', 'tekst': 'Foutmelding'},
                      ])
  @patch('waterstandtwitter.tweetbericht')
  @patch('waterstandtwitter.twitterwaterstand')
  def test_main_nodata(self, mock_twitterwaterstand, mock_tweetbericht, mock_haalwaterstand):
    mock_twitterwaterstand.return_value = ''
    mock_tweetbericht.return_value = ''

    waterstandtwitter.main()

    assert mock_haalwaterstand.call_count == 3
    assert mock_tweetbericht.call_count == 3
    assert mock_twitterwaterstand.called == False

  @patch('waterstand.haalwaterstand',
         side_effect=[{'resultaat': 'NOK', 'tekst': 'Foutmelding'},
                      {'resultaat': 'OK', 'tijd': '', 'nu': '', 'morgen': ''},
                      {'resultaat': 'OK', 'tijd': '', 'nu': '', 'morgen': ''},
                      ])
  @patch('waterstandtwitter.tweetbericht')
  @patch('waterstandtwitter.twitterwaterstand')
  def test_main_somedata(self, mock_twitterwaterstand, mock_tweetbericht, mock_haalwaterstand):
    mock_twitterwaterstand.return_value = ''
    mock_tweetbericht.return_value = ''

    waterstandtwitter.main()

    assert mock_haalwaterstand.call_count == 3
    assert mock_tweetbericht.call_count == 1
    assert mock_twitterwaterstand.call_count == 2

  @patch('waterstandtwitter.tweetbericht')
  def test_twitterwaterstand_nokey(self, mock_tweetbericht):
    mock_tweetbericht.return_value = None
    key = 'ABCD'
    weergavetijd = '14-12 12:34'
    hoogtenu = 56
    hoogtemorgen = 78
    waterstandtwitter.twitterwaterstand(key, weergavetijd, hoogtenu, hoogtemorgen)
    assert mock_tweetbericht.called == False

  @patch('waterstandtwitter.tweetbericht')
  def test_twitterwaterstand(self, mock_tweetbericht):
    mock_tweetbericht.return_value = None
    key = 'KATV'
    weergavetijd = '14-12 12:34'
    hoogtenu = 56
    hoogtemorgen = 78
    waterstandtwitter.twitterwaterstand(key, weergavetijd, hoogtenu, hoogtemorgen)
    assert mock_tweetbericht.called
    assert mock_tweetbericht.call_count == 1

  @patch('waterstandtwitter.tweetbericht')
  def test_twitterwaterstand_altflow(self, mock_tweetbericht):
    mock_tweetbericht.return_value = None
    key = 'ZUTP'
    weergavetijd = '14-12 12:34'
    hoogtenu = -10
    hoogtemorgen = -20
    waterstandtwitter.twitterwaterstand(key, weergavetijd, hoogtenu, hoogtemorgen)
    assert mock_tweetbericht.called
    assert mock_tweetbericht.call_count == 1

  @patch('tweepy.Client.create_tweet')
  def test_tweetbericht(self, mock_create_tweet):
    mock_create_tweet.return_value = None
    key = 'ABCD'
    tekst = 'Tekst van de tweet'
    waterstandtwitter.tweetbericht(key, tekst)

    assert mock_create_tweet.called
    assert mock_create_tweet.call_count == 1
