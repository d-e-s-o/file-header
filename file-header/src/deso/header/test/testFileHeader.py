# testFileHeader.py

#/***************************************************************************
# *   Copyright (C) 2016 deso (deso@posteo.net)                             *
# *                                                                         *
# *   This program is free software: you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation, either version 3 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU General Public License for more details.                          *
# *                                                                         *
# *   You should have received a copy of the GNU General Public License     *
# *   along with this program.  If not, see <http://www.gnu.org/licenses/>. *
# ***************************************************************************/

"""Tests for the file header checking functionality."""

from deso.execute import (
  execute,
  ProcessError,
)
from os import (
  pardir,
)
from os.path import (
  basename,
  dirname,
  join,
  realpath,
)
from random import (
  randint,
)
from sys import (
  executable,
)
from tempfile import (
  NamedTemporaryFile,
)
from unittest import (
  TestCase,
  main,
)


FILE_HEADER = realpath(join(dirname(__file__), pardir, "file-header.py"))


class TestPyfilter(TestCase):
  """A test case for testing of the file header checking functionality."""
  def testFileHeaderCheck(self):
    """Verify that incorrect file headers are flagged properly."""
    with NamedTemporaryFile(buffering=0) as f1,\
         NamedTemporaryFile(buffering=0) as f2,\
         NamedTemporaryFile(buffering=0) as f3:
      # A binary file.
      f1.write(bytes("".join(chr(randint(0, 255)) for _ in range(512)), "utf-8"))
      # Some text file without correct header.
      f2.write(bytes("# Copyright (C) 2016", "utf-8"))
      # Some text file with correct header.
      f3.write(bytes("# %s\n# Copyright (C) 2016" % (basename(f3.name)), "utf-8"))

      regex = r"%s does not contain" % basename(f1.name)
      with self.assertRaisesRegex(ProcessError, regex):
        execute(executable, FILE_HEADER, f1.name, f2.name, f3.name)

      regex = r"%s does not contain" % basename(f2.name)
      with self.assertRaisesRegex(ProcessError, regex):
        execute(executable, FILE_HEADER, f2.name, f3.name)

      execute(executable, FILE_HEADER, f3.name)

if __name__ == "__main__":
  main()
