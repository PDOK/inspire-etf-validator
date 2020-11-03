# -*- coding: utf-8 -*-
"""TODO Docstring."""
import logging
import sys

import click
import click_log

# Setup logging before package imports.
logger = logging.getLogger(__name__)
click_log.basic_config(logger)

from inspire_etf_validator.core import main, generate_report
from inspire_etf_validator.error import AppError


def set_level(only_set_package_loglevel=True):
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
        exists=True,
        readable=True,
        writable=False,
        allow_dash=False,
    ),
)
@click.option('--enable-caching', is_flag=True, default=False)
@click_log.simple_verbosity_option(logger)
def inspire_etf_validator_command(result_path, enable_caching):
    """
    TODO Docstring.
    """
    set_level()

    try:
        main(result_path, enable_caching)
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
        exists=True,
        readable=True,
        writable=False,
        allow_dash=False,
    ),
)
@click_log.simple_verbosity_option(logger)
def generate_report_command(result_path):
    set_level()
    try:
        generate_report(result_path)
    except AppError:
        logger.exception("inspire_etf_validator report failed:")
        sys.exit(1)


if __name__ == "__main__":
    cli()
