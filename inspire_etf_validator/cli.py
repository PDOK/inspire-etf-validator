# -*- coding: utf-8 -*-
"""TODO Docstring."""
import logging
import sys

import click
import click_log

# Setup logging before package imports.
logger = logging.getLogger(__name__)
click_log.basic_config(logger)

from inspire_etf_validator.core import main
from inspire_etf_validator.error import AppError


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
    try:
        main(result_path, enable_caching)
    except AppError:
        logger.exception("inspire_etf_validator failed:")
        sys.exit(1)


if __name__ == "__main__":
    cli()
