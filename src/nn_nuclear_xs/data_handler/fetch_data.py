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

"""Download the required data and put it in a format that is usable.

GDR parameters (8980 isotopes one) are from https://www-nds.iaea.org/PSFdatabase/atlas/gdr
The website blocks automated downloads, so the zip file must be manually downloaded and placed
in the data/ folder. All the remaining processing happens automatically.
"""

import zipfile

from nn_nuclear_xs.config.app_config import cfg


def extract_gdr_data() -> None:
    """Extract the GDR data from the file at data/gdr_all.zip.

    Ensure the gdr_all.zip file is already placed in the data/ folder.
    """
    with zipfile.ZipFile(cfg.data_config.gdr_zip_path) as gdr_zip_file:
        gdr_zip_file.extractall(path=cfg.data_config.gdr_zip_extract_path)
