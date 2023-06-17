from django.test import TestCase
from ..dates_and_time import *


class DatesAndTimeTestCase(TestCase):
    def test_min_to_real_time(self):
        result_1 = min_to_real_time(1)
        result_2 = min_to_real_time(55)
        result_3 = min_to_real_time(61)
        result_4 = min_to_real_time(605)
        self.assertEqual(result_1, '00:01')
        self.assertEqual(result_2, '00:55')
        self.assertEqual(result_3, '01:01')
        self.assertEqual(result_4, '10:05')

    def test_min_to_time_range(self):
        result_1 = min_to_time_range((720, 840))
        result_2 = min_to_time_range((0,))
        self.assertEqual(result_1, '12:00 - 14:00')
        self.assertEqual(result_2, '---')

    def test_convert_min_into_str_time_ranges(self):
        result_1 = convert_min_into_str_time_ranges([(720, 840)])
        result_2 = convert_min_into_str_time_ranges([(720, 840), (900, 960)])
        result_3 = convert_min_into_str_time_ranges([(720, 840), (900, 960), (1020, 1080)])
        result_4 = convert_min_into_str_time_ranges([(0,)])
        self.assertEqual(result_1, '12:00 - 14:00')
        self.assertEqual(result_2, '12:00 - 14:00, 15:00 - 16:00')
        self.assertEqual(result_3, '12:00 - 14:00, 15:00 - 16:00, 17:00 - 18:00')
        self.assertEqual(result_4, '---')

    def test_inserting_into_right_place(self):
        result_1 = inserting_into_right_place((720, 840), (720, 840))
        result_2 = inserting_into_right_place((720, 800), (720, 840))
        result_3 = inserting_into_right_place((800, 840), (720, 840))
        result_4 = inserting_into_right_place((760, 800), (720, 840))
        self.assertEqual(result_1, (0,))
        self.assertEqual(result_2, (800, 840))
        self.assertEqual(result_3, (720, 800))
        self.assertEqual(result_4, ((720, 760), (800, 840)))
        with self.assertRaises(ValueError):
            inserting_into_right_place((700, 840), (720, 840))
        with self.assertRaises(ValueError):
            inserting_into_right_place((720, 900), (720, 840))

    def test_clearing_nulls_in_available_time(self):
        result_1 = clearing_nulls_in_available_time([(0,)])
        result_2 = clearing_nulls_in_available_time([(720, 840), (900, 960)])
        result_3 = clearing_nulls_in_available_time([(720, 840), (0,), (1020, 1080)])
        result_4 = clearing_nulls_in_available_time([(720, 840), (0,), (0,)])
        self.assertEqual(result_1, [(0,)])
        self.assertEqual(result_2, [(720, 840), (900, 960)])
        self.assertEqual(result_3, [(720, 840), (1020, 1080)])
        self.assertEqual(result_4, [(720, 840)])

    def test_insert_time_range(self):
        result_1 = insert_time_range('12:00 - 14:00', [(0,)])
        result_2 = insert_time_range('12:00 - 14:00', [(720, 840)])
        result_3 = insert_time_range('12:00 - 14:00', [(720, 840), (900, 960)])
        result_4 = insert_time_range('15:00 - 16:00', [(720, 840), (900, 960), (1020, 1080)])
        self.assertEqual(result_1, [(0,)])
        self.assertEqual(result_2, [(0,)])
        self.assertEqual(result_3, [(900, 960)])
        self.assertEqual(result_4, [(720, 840), (1020, 1080)])

    def test_time_range_to_min(self):
        result_1 = time_range_to_min('12:00 - 14:00')
        result_2 = time_range_to_min('10:00 - 12:00')
        result_3 = time_range_to_min('00:00 - 00:00')
        self.assertEqual(result_1, (720, 840))
        self.assertEqual(result_2, (600, 720))
        self.assertEqual(result_3, (0,))
        with self.assertRaises(ValueError):
            time_range_to_min('---')

    def test_get_available_time_in_min(self):
        result_1 = get_available_time_in_min('12:00 - 14:00')
        result_2 = get_available_time_in_min('12:00 - 14:00, 15:00 - 16:00')
        result_3 = get_available_time_in_min('12:00 - 14:00, 15:00 - 16:00, 17:00 - 18:00')
        result_4 = get_available_time_in_min('---')
        self.assertEqual(result_1, [(720, 840)])
        self.assertEqual(result_2, [(720, 840), (900, 960)])
        self.assertEqual(result_3, [(720, 840), (900, 960), (1020, 1080)])
        self.assertEqual(result_4, [(0,)])
