# Copyright (C) 2026 Danish Mohammad
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.

"""Holds various miscellaneous functions.

Useful while doing exploration and trying out various things.
If the code is run as `uv run main.py --misc`, then the miscellaneous_function
in this file will be executed.
"""

from loguru import logger as log


def miscellaneous_function() -> None:
    """Run the specified function in this file."""
    log.debug("In the miscellaneous_function.")
