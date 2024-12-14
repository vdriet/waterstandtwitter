import unittest
from unittest.mock import patch

import waterstandtwitter


class TestWaterstandTwitter(unittest.TestCase):

  @patch('waterstand.haalwaterstand')
  @patch('waterstandtwitter.tweetbericht')
  @patch('waterstandtwitter.twitterwaterstand')
  def test_main_nodata(self, mock_twitterwaterstand, mock_tweetbericht, mock_haalwaterstand):
    mock_twitterwaterstand.return_value = ''
    mock_tweetbericht.return_value = ''
    mock_haalwaterstand.return_value = {'resultaat': 'NOK'}

    waterstandtwitter.main()

    assert mock_haalwaterstand.called
    assert mock_tweetbericht.called
    assert mock_twitterwaterstand.called == False

  @patch('waterstand.haalwaterstand')
  @patch('waterstandtwitter.tweetbericht')
  @patch('waterstandtwitter.twitterwaterstand')
  def test_main_data(self, mock_twitterwaterstand, mock_tweetbericht, mock_haalwaterstand):
    mock_twitterwaterstand.return_value = ''
    mock_tweetbericht.return_value = ''
    mock_haalwaterstand.return_value = {'resultaat': 'OK', 'tijd': '', 'nu': '', 'morgen': ''}

    waterstandtwitter.main()

    assert mock_haalwaterstand.called
    assert mock_tweetbericht.called == False
    assert mock_twitterwaterstand.called

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
