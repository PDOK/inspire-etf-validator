import logging

from inspire_etf_validator.constants import TEST_ENDPOINTS
from inspire_etf_validator.domain import dao_etf_validator
from inspire_etf_validator.runner import run_master_sync

logger = logging.getLogger(__name__)


def main():
    """TODO Docstring."""

    #todo: haal lijst op van alle services als die ouder is dan x aantal dagen -> cachsing inbouwen

    #todo: Run voor elke service de validaties:

        #todo: run metadtaa validatie

        #todo: run atom validatie

        #todo: run wms validatie

        #todo: run wfs validatie

        #todo: Voeg resultaten toe aan samenvatting

    #todo: Als alles klaar is spuw een samenvatting uit

    run_master_sync.run_master(TEST_ENDPOINTS)
