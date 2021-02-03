# -*- coding: utf-8 -*-
"""Script to run Inspire ETF validation for every PDOK Inspire endpoint in NGR."""
import logging
import sys

import click
import click_log

# Setup logging before package imports.
from inspire_etf_validator.constants import INSPIRE_ETF_ENDPOINT
from inspire_etf_validator.error import AppError

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

from inspire_etf_validator.core import main, generate_report


def set_level():
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger_ in loggers:
        logger_.setLevel(logger.level)
    logging.info("Set loglevels to %s.", logging.getLevelName(logger.level))


@click.group()
def cli():
    pass


@cli.command(name="inspire_etf_validator")
@click.option(
    "-r",
    "--result_path",
    required=False,
    default="../",
    help="Path pointing to a directory used for the output",
    type=click.types.Path(
        exists=True, readable=True, writable=False, allow_dash=False,
    ),
)
@click.option(
    "-c",
    "--enable-caching",
    is_flag=True,
    default=False,
    help="Enables cache for retrieving NGR inspire endpoints"
)
@click_log.simple_verbosity_option(logger)
@click.option(
    "-e",
    "--inspire_etf_endpoint",
    required=False,
    default=INSPIRE_ETF_ENDPOINT,
    help="URL of the Inspire ETF service used to validate",
)
@click.option(
    "-d",
    "--debug-mode",
    is_flag=True,
    default=False,
    help="Enables debug mode which will run tests for the first three endpoints"
)
def inspire_etf_validator_command(result_path, enable_caching, inspire_etf_endpoint, debug_mode):
    """
    This command is the main function of this tool.
    It retrieves all NGR inspire endpoints managed by PDOK.
    Then it runs the test suites in the Inspire ETF validator.
    """
    set_level()

    try:
        main(result_path, enable_caching, inspire_etf_endpoint, debug_mode)
    except AppError:
        logger.exception("inspire_etf_validator failed:")
        sys.exit(1)


@cli.command(name="report")
@click.option(
    "-r",
    "--result_path",
    required=False,
    default="../",
    help="Path pointing to a directory used for the output",
    type=click.types.Path(
        exists=True, readable=True, writable=False, allow_dash=False,
    ),
)
@click_log.simple_verbosity_option(logger)
def generate_report_command(result_path):
    """
    Used to generate aggregated summary for debugging.
    """
    set_level()
    try:
        generate_report(result_path)
    except AppError:
        logger.exception("inspire_etf_validator report failed:")
        sys.exit(1)


if __name__ == "__main__":
    cli()
