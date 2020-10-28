INSPIRE_ETF_ENDPOINT = "http://localhost:8080/validator"
INSPIRE_ETF_API_VERSION = 'v2'

SLEEP_TIME_IN_SECONDS = 8

TEST_ID_LIST = {
    "atom": "EID11571c92-3940-4f42-a6cd-5e2b1c6f4d93",
    "wms": "EIDeec9d674-d94b-4d8d-b744-1309c6cae1d2",
    "wfs": "EIDed2d3501-d700-4ff9-b9bf-070dece8ddbd",
}

URL_NGR = "https://nationaalgeoregister.nl/geonetwork"

CACHE_FILENAME = "../ngr_records_cache.json" # todo: configure path in cli signature

CACHE_EXPIRATION_IN_SECONDS = 86400  # is 1 day

REQUEST_HEADERS = {
    'User-Agent': 'pdok.nl (inspire-etf-validator)'
}

NAMESPACE_PREFIXES = {
    'csw': 'http://www.opengis.net/cat/csw/2.0.2',
    'gmd': 'http://www.isotc211.org/2005/gmd',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'gco': 'http://www.isotc211.org/2005/gco',
    'gmx': 'http://www.isotc211.org/2005/gmx',
    'ows': 'http://www.opengis.net/ows',
}

LOG_LINE_SEPARATOR = "-------------------------------------------------------------------------------"