import pkg_resources

USER_AGENT = "PDOK Inspire ETF validator " + pkg_resources.require("inspire-etf-validator")[0].version
PDOK_EMAIL = "PDOK@kadaster.nl"

INSPIRE_ETF_ENDPOINT = "http://localhost:8080/validator"
INSPIRE_ETF_API_VERSION = "v2"

SLEEP_TIME_IN_SECONDS = 5

SERVICE_TEST_IDS = {
    "atom": "EID11571c92-3940-4f42-a6cd-5e2b1c6f4d93",
    "wms": "EIDeec9d674-d94b-4d8d-b744-1309c6cae1d2",
    "wfs": "EID174edf55-699b-446c-968c-1892a4d8d5bd",
    "wcs": "EID074570ad-d720-47b3-af79-d54201793404",
    "wmts": "EID550ceacf-b3cb-47a0-b2dd-d3edb18344a9",
}
# Test ids
TID_SERVICE_MD_COMMON_REQUIREMENTS = "EID59692c11-df86-49ad-be7f-94a1e1ddd8da"
TID_CLASS_4_INSPIRE_NETWORK_SERVICES_METADATA = "EID606587df-65a8-4b7b-9eee-e0d94daaa42a"
TID_CLASS_5_INSPIRE_INVOCABLE_SPATIAL_DATA_SERVICES_METADATA = "EID8db54d8a-8578-4959-b891-5394d9f53a28"
TID_CLASS_6_INSPIRE_INTEROPERABLE_SPATIAL_DATA_SERVICES_METADATA = "EID7514777a-6cb8-499c-acd5-912496dc84e9"

# Service Categories
SC_NETWORK_SERVICE = "Network Service"
SC_SDS_INVOCABLE = "SDS-invocable"
SC_SDS_INTEROPERABLE = "SDS-interoperable"

METADATA_TEST_IDS = {
    None: TID_SERVICE_MD_COMMON_REQUIREMENTS,
    SC_NETWORK_SERVICE: TID_CLASS_4_INSPIRE_NETWORK_SERVICES_METADATA,
    SC_SDS_INVOCABLE: TID_CLASS_5_INSPIRE_INVOCABLE_SPATIAL_DATA_SERVICES_METADATA,
    SC_SDS_INTEROPERABLE: TID_CLASS_6_INSPIRE_INTEROPERABLE_SPATIAL_DATA_SERVICES_METADATA,
}

URL_NGR = "https://nationaalgeoregister.nl/geonetwork"

CACHE_FILENAME = "../ngr_records_cache.json"
DETAIL_OUTPUT_PATH = "run_detail_result"
RUN_MASTER_RESULT_PATH = "run_master_result.json"

CACHE_EXPIRATION_IN_SECONDS = 86400  # is 1 day

REQUEST_HEADERS = {"User-Agent": "pdok.nl (inspire-etf-validator)"}

NAMESPACE_PREFIXES = {
    "csw": "http://www.opengis.net/cat/csw/2.0.2",
    "gmd": "http://www.isotc211.org/2005/gmd",
    "dc": "http://purl.org/dc/elements/1.1/",
    "gco": "http://www.isotc211.org/2005/gco",
    "gmx": "http://www.isotc211.org/2005/gmx",
    "ows": "http://www.opengis.net/ows",
    "srv": "http://www.isotc211.org/2005/srv",
    "xlink": "http://www.w3.org/1999/xlink",
}

LOG_LINE_SEPARATOR = (
    "-------------------------------------------------------------------------------"
)

MAX_RETRY = 7
