import unittest
import ecoblock_test.get_data as get_data


class TestGetData(unittest.TestCase):
    def setUp(self):
        self.start_date = 1493600340
        self.end_date = 1493683140

    def test_get_load_demand(self):
        self.assertEqual(get_data.import_load_demand(self.start_date, self.end_date).shape, (24, 1))

    def test_get_ev_demand(self):
        self.assertEqual(get_data.import_ev_demand(self.start_date, self.end_date).shape, (24, 1))

    def test_get_prices_to_sell(self):
        self.assertEqual(get_data.import_pv_generation(self.start_date, self.end_date).shape, (21, 1))
