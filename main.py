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

"""Entry point for the project."""

import argparse

from loguru import logger as log

from nn_nuclear_xs.exploration.misc import miscellaneous_function
from nn_nuclear_xs.utils.logger_setup import setup_logging


def get_args() -> argparse.Namespace:
    """Parse and get any cli arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--misc",
        default=False,
        action="store_true",
        help="run the miscellaneous_function in misc.py",
    )
    return parser.parse_args()


def main() -> None:
    """Primary entrypoint."""
    try:
        setup_logging()
        log.debug("Finished logging setup.")

        args = get_args()
        if args.misc:
            miscellaneous_function()
        log.debug("\n\n:{}:\n", "=" * 30)
    except Exception:  # noqa: BLE001
        log.exception("Error in main function")


if __name__ == "__main__":
    main()
