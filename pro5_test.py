from util import *
import unittest


class TestOmdbData(unittest.TestCase):

    def setUp(self):
        self.record_GoF = get_omdb_record('Game of Thrones',1)
        self.record_PET = get_omdb_record('Planet Earth II',1)
        self.record_BoB = get_omdb_record('Band of Brothers',1)

    def test_imdb_ID(self):
        self.assertEqual(self.record_GoF.imdbID, 'tt0944947')
        self.assertEqual(self.record_PET.imdbID, 'tt5491994')
        self.assertEqual(self.record_BoB.imdbID, 'tt0185906')

    def test_str(self):
        self.assertEqual(str(self.record_GoF), "Title: Game of Thrones imdbId: tt0944947 Totalseasons: 8")
        self.assertEqual(str(self.record_PET), "Title: Planet Earth II imdbId: tt5491994 Totalseasons: 1")
        self.assertEqual(str(self.record_BoB), "Title: Band of Brothers imdbId: tt0185906 Totalseasons: 1")


class TestSeasonData(unittest.TestCase):

    def setUp(self):
        self.season_GoF = get_season_data('tt0944947')
        self.season_PET = get_season_data('tt5491994')
        self.season_BoB = get_season_data('tt0185906')

    def test_season_length(self):
        self.assertEqual(len(self.season_GoF), 8)
        self.assertEqual(len(self.season_PET), 1)
        self.assertEqual(len(self.season_BoB), 1)

    def test_season_url(self):
        self.assertEqual(self.season_GoF["2"], "https://www.imdb.com/title/tt0944947/episodes?season=2&ref_=tt_eps_sn_2")
        self.assertEqual(self.season_PET["1"], "https://www.imdb.com/title/tt5491994/episodes?season=1&ref_=tt_eps_sn_1")
        self.assertEqual(self.season_BoB["1"], "https://www.imdb.com/title/tt0185906/episodes?season=1&ref_=tt_eps_sn_1")


class TestMapping(unittest.TestCase):


    def setUp(self):
        imdb_id="tt0944947"
        season_dict={'3': 'https://www.imdb.com/title/tt0944947/episodes?season=3&ref_=tt_eps_sn_3',
                    '1': 'https://www.imdb.com/title/tt0944947/episodes?season=1&ref_=tt_eps_sn_1',
                    '2': 'https://www.imdb.com/title/tt0944947/episodes?season=2&ref_=tt_eps_sn_2'}

        self.episode_S1 = get_episode_data(imdb_id,1,season_dict["1"])
        self.episode_S2 = get_episode_data(imdb_id,2,season_dict["2"])
        self.episode_S3 = get_episode_data(imdb_id,3,season_dict["3"])

    def test_episode_lenght(self):
        self.assertEqual(len(self.episode_S1), 10)
        self.assertEqual(len(self.episode_S2), 10)
        self.assertEqual(len(self.episode_S3), 10)

    def test_episode1_name(self):
        self.assertEqual(self.episode_S1[0][0], 'Winter Is Coming')
        self.assertEqual(self.episode_S2[0][0], 'The North Remembers')
        self.assertEqual(self.episode_S3[0][0], 'Valar Dohaeris')


if __name__ == '__main__':
    unittest.main()
