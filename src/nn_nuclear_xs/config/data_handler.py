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

"""Data Handling Configuration."""

from pathlib import Path


class GDRDataFormatConfig:
    """Config values for the GDR data - formatting information."""

    def __init__(self) -> None:
        """Config for gdr data specific stuff."""
        self.comment_prefix: str = "#"
        # 1-based line index containing the column names
        self.header_line_number: int = 4
        # this is used when no Format: line is present
        self.default_format: str = "2I4, 9F9.3, I5"
        # this is the regex used to find the format line
        self.format_line_regex: str = r"format\s*:\s*(?P<spec>.+)"
        # this is the regex used to parse the format line
        self.format_descriptor_regex: str = (
            r"^(?P<repeat>\d*)(?P<kind>[IFEDG])(?P<width>\d+)(?:\.(?P<decimals>\d+))?$"
        )


class DataConfig:
    """Config for downloading and processing data."""

    def __init__(self) -> None:
        """Set up all the configuration for data handling."""
        self.gdr_data_url: str = "https://www-nds.iaea.org/media-psf/atlas/gdr_all.zip"
        self.gdr_zip_path: Path = Path("data/gdr_all.zip")
        self.gdr_zip_extract_path: Path = Path("data/")

        # this is where the gdr data is extracted to
        self.slo_dat_path: Path = (
            self.gdr_zip_extract_path
            / r"gdr_parameters_exp&systematics/gdr-parameters_exp&systematics_slo.dat"
        )
        self.smlo_dat_path: Path = (
            self.gdr_zip_extract_path
            / r"gdr_parameters_exp&systematics/gdr-parameters_exp&systematics_smlo.dat"
        )

        # this is where the .dat gdr files are saved to as csv
        self.slo_csv_path: Path = Path("data/slo.csv")
        self.smlo_csv_path: Path = Path("data/smlo.csv")

        # this is the gdr data specific stuff - in the .dat file
        self.gdr_format = GDRDataFormatConfig()
