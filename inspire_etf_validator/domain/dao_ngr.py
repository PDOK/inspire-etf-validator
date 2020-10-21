from inspire_etf_validator.constants import TEST_ENDPOINTS


def get_all_ngr_records():
    result = TEST_ENDPOINTS

    #todo: check of er een cache file is en dat ie niet oude is dan `CACHE_EXPIRATION`

    #todo: Geen cache dan zelf ophalen `__get_all_ngr_records`

    return result


def __get_all_ngr_records():

    #todo: haal ngr per 10 op -> zie code anton of roel

    #todo: schrijf weg naar bestand -> overschijven

    pass


def get_atom_ngr_records():
    pass


def get_wms_ngr_records():
    pass


def get_wfs_ngr_records():
    pass
