import logging

from inspire_etf_validator.domain.dao_ngr import get_all_ngr_records, get_filtered_ngr_records

logger = logging.getLogger(__name__)


def main(enable_caching):
    all_ngr_records = get_all_ngr_records(enable_caching)
    atom_records = get_filtered_ngr_records(all_ngr_records, 'ATOM')
    wms_records = get_filtered_ngr_records(all_ngr_records, 'WMS')
    wfs_records = get_filtered_ngr_records(all_ngr_records, 'WFS')

    #todo: Run voor elke service de validaties:

        #todo: run metadtaa validatie

        #todo: run atom validatie

        #todo: run wms validatie

        #todo: run wfs validatie

        #todo: Voeg resultaten toe aan samenvatting

    #todo: Als alles klaar is spuw een samenvatting uit

    print('test')