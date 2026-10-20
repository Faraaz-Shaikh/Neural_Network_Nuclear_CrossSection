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

"""Logging Configuration."""

from pathlib import Path


class LogConfig:
    """Config for the loguru logs."""

    def __init__(self) -> None:
        """Config values setup and log folder creation."""
        self.log_dir: Path = Path("logs")
        self.human_readable_log_file: Path = self.log_dir / "nn_nuclear_xs.log"
        self.log_level: str = "DEBUG"

        self._create_log_folder()

    def _create_log_folder(self) -> None:
        """Create the logs folder."""
        self.log_dir.mkdir(exist_ok=True)
