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

"""Setup for the loguru logger - json, file, console logs."""

import contextlib
import logging
import site
from pathlib import Path
from typing import NamedTuple

from loguru import logger
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import Traceback

from nn_nuclear_xs.config.app_config import cfg


class RotationData(NamedTuple):
    """Data for log rotation."""

    rotation_interval: str
    retention_period: str
    compression_method: str


# funnel all logging module output for other libraries through loguru
class InterceptHandler(logging.Handler):
    """Handle Intercepts."""

    def emit(self, record: logging.LogRecord) -> None:
        """Put out the log record."""
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # find caller from where originated the logged message
        frame, depth = logging.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def add_console_logging(log_level: str) -> int:
    """Handle the logs that are printed to the console."""
    # the rich handler owns console formatting
    console = Console(stderr=False)
    rich_handler = RichHandler(
        console=console,  # stdout, to match your existing setup
        rich_tracebacks=True,  # beautiful tracebacks in dev mode
        tracebacks_show_locals=True,  # show local vars in tracebacks (like diagnose=True)
        show_time=True,
        show_level=True,
        show_path=True,
        markup=True,
    )

    # below function is from claude sonnet
    def rich_sink(message) -> None:  # noqa: ANN001
        # message.record contains all loguru metadata
        record = message.record
        level = record["level"].name
        loguru_exc = record["exception"]

        # add function name to message
        decorated_msg = f"[blue]{record['function']}[/blue] {record['message']}"

        # emit through rich's handler by constructing a minimal LogRecord
        log_record = logging.LogRecord(
            name=record["name"] or "",
            level=logging.getLevelName(level),
            pathname=record["file"].path,
            lineno=record["line"],
            msg=decorated_msg,
            args=(),
            exc_info=None,
        )
        rich_handler.emit(log_record)

        # Render the traceback separately, directly via the Rich console
        if loguru_exc and loguru_exc.type and loguru_exc.value:
            tb = Traceback.from_exception(
                loguru_exc.type,
                loguru_exc.value,
                loguru_exc.traceback,
                show_locals=rich_handler.tracebacks_show_locals,
                width=console.width,
                locals_max_length=20,
                locals_max_string=200,
                suppress=site.getsitepackages(),  # suppress all install third-party packages
                # below changes were made to include 3rd party locals in tracebacks
                # if you want to revert, just uncomment above suppress line and comment below lines
                # suppress=(),
                # max_frames=10,
            )
            console.print(tb)

    return logger.add(
        rich_sink,
        level=log_level,
        diagnose=False,  # rich handles tracebacks
        backtrace=False,  # rich handles this
        enqueue=False,  # not needed for console logging
        format="{message}",  # should be plain since rich adds its own columns
        colorize=False,  # rich adds its own styling
    )


# add local human readable rotating file logging
def add_file_logs(log_file: Path, log_level: str) -> int:
    """Handle the logs that are written to file."""
    return logger.add(
        sink=log_file,
        level=log_level,
        colorize=False,
        serialize=False,
        backtrace=True,
        diagnose=True,
        enqueue=True,
    )


# this can be re-enabled depending on requirement
def set_library_log_levels() -> None:
    """Set up the log levels for various libraries."""
    intercept_handler = InterceptHandler()
    library_levels = {}
    for logger_name, log_level in library_levels.items():
        lib_logger = logging.getLogger(logger_name)
        lib_logger.handlers = [intercept_handler]
        lib_logger.setLevel(log_level)
        lib_logger.propagate = False


def setup_logging() -> None:
    """Set up full loguru logging configuration."""
    # clear the default stderr handler
    # during testing logger.remove() without args can create issues by removing
    # all handlers like my pytest log etc
    # so i am changing to remove only the stderr logger (id 0)
    with contextlib.suppress(ValueError):
        # already removed - handler called multiple times - likely during testing
        logger.remove(0)

    add_console_logging(cfg.log_config.log_level)
    add_file_logs(
        log_file=cfg.log_config.human_readable_log_file,
        log_level=cfg.log_config.log_level,
    )

    # Redirect everything from the standard logging module into loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # TODO(Danish Mohammad): #002 uncomment if required
    # set_library_log_levels()

    # for now set all other levels to WARNING
    logging.getLogger().setLevel(logging.WARNING)
