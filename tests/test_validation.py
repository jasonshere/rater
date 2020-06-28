# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: Test bpmf
"""

import unittest

import numpy as np

from recommender.datasets.movielens import make_ratings
from recommender.utils.validation import check_ratings


class TestValidation(unittest.TestCase):
    def setUp(self):
        self.n_user = 200
        self.n_item = 100
        self.choices = list(range(1, 10))
        self.ratings = make_ratings(
            self.n_user, self.n_item, 10, 20, self.choices)

    def test_validation(self):
        check_ratings(self.ratings, self.n_user, self.n_item,
                      max(self.choices), min(self.choices))

    def test_validation_error(self):
        with self.assertRaises(ValueError):
            check_ratings(np.eye(4), self.n_user, self.n_item, 5, 1)

        with self.assertRaises(ValueError):
            check_ratings(np.eye(3) - 2., self.n_user, self.n_item,
                          max(self.choices), min(self.choices))

        with self.assertRaises(ValueError):
            check_ratings(self.ratings, self.n_user - 1, self.n_item,
                          max(self.choices), min(self.choices))

        with self.assertRaises(ValueError):
            check_ratings(self.ratings, self.n_user, self.n_item - 10,
                          max(self.choices), min(self.choices))

        with self.assertRaises(ValueError):
            check_ratings(self.ratings, self.n_user, self.n_item,
                          max(self.choices) - 1, min(self.choices))

        with self.assertRaises(ValueError):
            check_ratings(self.ratings, self.n_user, self.n_item,
                          max(self.choices), min(self.choices) + 1)
