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

"""Holds generic pytest fixtures for the data_handler unit tests."""

from pathlib import Path

import pytest

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def data_dir() -> Path:
    """Read-only directory of shared test resources."""
    return DATA_DIR


@pytest.fixture(scope="session")
def slo_dat_path() -> Path:
    """Path to the GDR slo truncated data."""
    return DATA_DIR / "slo.dat"


@pytest.fixture(scope="session")
def smlo_dat_path() -> Path:
    """Path to the GDR smlo truncated data."""
    return DATA_DIR / "smlo.dat"


@pytest.fixture(scope="session")
def slo_csv_path() -> Path:
    """Path to the GDR slo csv manually written golden data."""
    return DATA_DIR / "slo.csv"


@pytest.fixture(scope="session")
def smlo_csv_path() -> Path:
    """Path to the GDR smlo csv manually written golden data."""
    return DATA_DIR / "smlo.csv"
