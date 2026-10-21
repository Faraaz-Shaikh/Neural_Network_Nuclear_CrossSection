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

"""Process downloaded data."""

from nn_nuclear_xs.config.app_config import cfg
from nn_nuclear_xs.data_handler.fortran_to_csv import fortran_dat_to_csv


def gdr_to_csv() -> None:
    """Convert the download GDR data to csv format."""
    fortran_dat_to_csv(
        dat_path=cfg.data_config.slo_dat_path, csv_path=cfg.data_config.slo_csv_path
    )
    fortran_dat_to_csv(
        dat_path=cfg.data_config.smlo_dat_path, csv_path=cfg.data_config.smlo_csv_path
    )
