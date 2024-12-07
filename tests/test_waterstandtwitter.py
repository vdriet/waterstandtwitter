import unittest
from unittest.mock import patch

import waterstandtwitter


class TestWaterstandTwitter(unittest.TestCase):

  @patch('waterstand.waterstand.haalwaterstand')
  @patch('waterstandtwitter.tweetbericht')
  @patch('waterstandtwitter.twitterwaterstand')
  def test_main_nodata(self, mock_twitterwaterstand, mock_tweetbericht, mock_haalwaterstand):
    mock_twitterwaterstand.return_value = ''
    mock_tweetbericht.return_value = ''
    mock_haalwaterstand.return_value = 'dummy'

    waterstandtwitter.main()

    assert mock_haalwaterstand.called
    assert mock_tweetbericht.called
    assert mock_twitterwaterstand.called == False

  @patch('waterstand.waterstand.haalwaterstand')
  @patch('waterstandtwitter.tweetbericht')
  @patch('waterstandtwitter.twitterwaterstand')
  def test_main_data(self, mock_twitterwaterstand, mock_tweetbericht, mock_haalwaterstand):
    mock_twitterwaterstand.return_value = ''
    mock_tweetbericht.return_value = ''
    mock_haalwaterstand.return_value = {'tijd': '', 'nu': '', 'morgen': ''}

    waterstandtwitter.main()

    assert mock_haalwaterstand.called
    assert mock_tweetbericht.called == False
    assert mock_twitterwaterstand.called
