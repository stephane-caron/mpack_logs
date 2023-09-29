#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Inria
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test the main logger.
"""

import os
import tempfile
import msgpack
import unittest
from unittest import IsolatedAsyncioTestCase

from mpacklog.python.sync_logger import SyncLogger


class TestSyncLogger(IsolatedAsyncioTestCase):
    def test_put(self):
        tmp_file = tempfile.mktemp(suffix=".mpack")
        logger = SyncLogger(tmp_file)
        self.assertTrue(logger.queue.empty())
        logger.put({"foo": 42, "something": "else"})
        self.assertFalse(logger.queue.empty())

    def test_write(self):
        tmp_file = tempfile.mktemp(suffix=".mpack")
        self.assertFalse(os.path.exists(tmp_file))

        logger = SyncLogger(tmp_file)
        logger.write()
        self.assertTrue(os.path.exists(tmp_file))

    def test_write_and_read(self):
        tmp_file = tempfile.mktemp(suffix=".mpack")

        logger = SyncLogger(tmp_file)
        logger.put({"foo": 42, "something": "else"})
        logger.write()

        message = msgpack.load(open(tmp_file, "rb"))
        self.assertEqual(message, {"foo": 42, "something": "else"})

if __name__ == "__main__":
    unittest.main()
