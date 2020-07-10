#!/usr/bin/env python3

from unittest import TestCase
from src.core.bruter import Bruter, BruterException


class SyncBruterTest(TestCase):
    def test_create_base_class(self):
        bruter = Bruter()
        self.assertIsNotNone(bruter)
        self.assertIsInstance(bruter, Bruter)

    def test_raise_exception_host(self):
        bruter = Bruter()

        def test_func():
            bruter.host = ""

        self.assertRaises(BruterException, test_func)
