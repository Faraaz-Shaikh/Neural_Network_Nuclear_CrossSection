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

"""Tests the conversion of GDR data from Fortran format to CSV."""

import difflib
from pathlib import Path

from nn_nuclear_xs.data_handler.fortran_to_csv import fortran_dat_to_csv


def assert_files_equal(expected: Path, actual: Path, context: int = 3) -> None:
    """Assert line-wise equality of two files; on failure, report a unified diff."""
    __tracebackhide__ = True  # pytest omits this frame from the traceback

    expected_bytes = expected.read_bytes()
    actual_bytes = actual.read_bytes()
    if expected_bytes == actual_bytes:
        return

    expected_lines = expected_bytes.decode(errors="replace").splitlines()
    actual_lines = actual_bytes.decode(errors="replace").splitlines()
    diff = "\n".join(
        difflib.unified_diff(
            expected_lines,
            actual_lines,
            fromfile=f"expected: {expected}",
            tofile=f"actual:   {actual}",
            n=context,
            lineterm="",
        )
    )
    if not diff:
        return
    msg = f"Files differ:\n{diff}"
    raise AssertionError(msg)


def test_fortran_dat_to_csv(
    tmp_path: Path,
    slo_dat_path: Path,
    smlo_dat_path: Path,
    slo_csv_path: Path,
    smlo_csv_path: Path,
) -> None:
    """Test conversion of GDR data from Fortran to csv."""
    output_csv_path = tmp_path / "slo.csv"
    fortran_dat_to_csv(dat_path=slo_dat_path, csv_path=output_csv_path)
    assert_files_equal(slo_csv_path, output_csv_path)

    output_csv_path = tmp_path / "smlo.csv"
    fortran_dat_to_csv(dat_path=smlo_dat_path, csv_path=output_csv_path)
    assert_files_equal(smlo_csv_path, output_csv_path)
