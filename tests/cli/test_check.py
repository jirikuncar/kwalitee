# -*- coding: utf-8 -*-
##
## This file is part of Invenio-Kwalitee
## Copyright (C) 2014 CERN.
##
## Invenio-Kwalitee is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio-Kwalitee is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio-Kwalitee; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
##
## In applying this licence, CERN does not waive the privileges and immunities
## granted to it by virtue of its status as an Intergovernmental Organization
## or submit itself to any jurisdiction.

from __future__ import unicode_literals

import os
import sys
import shutil
import tempfile
import subprocess
from io import StringIO
from unittest import TestCase
from hamcrest import assert_that, has_item, has_items, has_length, is_not
from invenio_kwalitee.cli.check import message


class CheckCliTest(TestCase):

    """Test command `kwalitee check message [OPTIONS]`."""

    def setUp(self):
        self.path = tempfile.mkdtemp()
        self.cwd = os.getcwd()
        self.stderr = sys.stderr
        sys.stderr = StringIO("")
        os.chdir(self.path)

    def tearDown(self):
        os.chdir(self.cwd)
        sys.stderr = self.stderr
        shutil.rmtree(self.path)

    def call(self, *args):
        """Exectute a command."""
        return subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.path
        ).wait()

    def test_install_hooks(self):
        """Test install hooks."""
        self.call("git", "init")
        self.call("touch", "README.rst")
        self.call("git", "add", "README.rst")
        self.call("git", "commit", "-m", "'empty README'")

        sys_stdout = sys.stdout
        sys.stdout = StringIO("")

        # call check on HEAD
        message()
        errors = sys.stdout.getvalue().split("\n")
        assert_that(errors,
                    has_items("1: M110 missing component name",
                              "1: M101 signature is missing",
                              "1: M100 needs more reviewers"))
        # restore output
        sys.stdout = sys_stdout
