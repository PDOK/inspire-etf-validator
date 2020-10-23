import json
import os
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

import requests

from inspire_etf_validator.constants import BASE_URL, NAMESPACE_PREFIXES, CACHE_FILENAME, CACHE_EXPIRATION_IN_SECONDS, \
    REQUEST_HEADERS


def get_all_ngr_records(enable_caching):
    # if there is no cache file or it is expired, create it. otherwise read the cache file
    if not os.path.isfile(CACHE_FILENAME) or __cache_is_expired():
        print("downloading ngr record data...")
        ngr_records = __get_all_ngr_records()
        for ngr_record in ngr_records:
            ngr_record.update(__get_record_info(ngr_record['uuid']))

        if enable_caching:
            print("writing all ngr record data to cache file " + CACHE_FILENAME)
            with open(CACHE_FILENAME, 'w', encoding='utf-8') as f:
                json.dump(ngr_records, f, ensure_ascii=False, indent=4)
    else:
        print("reading ngr records from cache file " + CACHE_FILENAME)
        with open(CACHE_FILENAME) as infile:
            ngr_records = json.load(infile)

    return ngr_records


def __cache_is_expired():
    file_mod_time = datetime.fromtimestamp(os.stat(CACHE_FILENAME).st_mtime)  # This is a datetime.datetime object!
    now = datetime.today()
    max_delay = timedelta(seconds=CACHE_EXPIRATION_IN_SECONDS)
    return now - file_mod_time > max_delay


def __get_all_ngr_records():
    ngr_records = []

    start_position = "1"
    while True:
        records_base_url = BASE_URL + "/srv/dut/csw-inspire?request=GetRecords&Service=CSW&Version=2.0.2&typeNames" \
                                      "=gmd:MD_Metadata&resultType=results&constraintLanguage=CQL_TEXT" \
                                      "&constraint_language_version=1.1.0&constraint=type='service'+AND" \
                                      "+organisationName='Beheer+PDOK'&startPosition=" + start_position
        print("fetching records_base_url: " + records_base_url)
        response = requests.get(records_base_url, headers=REQUEST_HEADERS)
        document = ET.fromstring(response.content)

        ex_node = document.findall("./ows:ExceptionReport", NAMESPACE_PREFIXES)
        if len(ex_node) > 0:
            exception_code = document.find("./ows:ExceptionReport/ows:Exception/[@exceptionCode]",
                                           NAMESPACE_PREFIXES).text
            if exception_code is not None:
                raise Exception("Exception in CSW response, exceptionCode: " + exception_code)

        start_position = document.find(".//csw:SearchResults/[@nextRecord]", NAMESPACE_PREFIXES).attrib['nextRecord']

        temp_records = document.findall(".//csw:SummaryRecord", NAMESPACE_PREFIXES)
        for temp_record in temp_records:
            title = temp_record.find("dc:title", NAMESPACE_PREFIXES).text
            identifier = temp_record.find("dc:identifier", NAMESPACE_PREFIXES).text
            label = title.replace(" ", "_").lower()

            temp_record_result = {"uuid": identifier, "title": title, "label": label}
            ngr_records.append(temp_record_result)

        if start_position == "0":
            break

    return ngr_records


def __get_service_type(service_access_point):
    if "/wms" in service_access_point:
        return "WMS"
    elif "/wfs" in service_access_point:
        return "WFS"
    elif "/atom" in service_access_point:
        return "ATOM"
    elif "/wcs" in service_access_point:
        return "WCS"
    elif "/wmts" in service_access_point:
        return "WMTS"
    elif "/tms" in service_access_point:
        return "TMS"
    elif "/csw" in service_access_point:
        return "CSW"
    return ""


def __get_record_info(uuid):
    result = {}

    record_info_base_url = BASE_URL + "/srv/dut/csw?service=CSW&request=GetRecordById&version=2.0.2&outputSchema=http" \
                                      "://www.isotc211.org/2005/gmd&elementSetName=full&id=" + uuid + "#MD_DataIdentification "
    print("fetching record_info_base_url: " + record_info_base_url)
    response = requests.get(record_info_base_url, headers=REQUEST_HEADERS)
    document = ET.fromstring(response.content)

    service_access_point = document.find(
        ".//gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:linkage/gmd:URL",
        NAMESPACE_PREFIXES).text
    protocol = document.find(
        ".//gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gco"
        ":CharacterString",
        NAMESPACE_PREFIXES)
    if protocol is not None:
        protocol = protocol.text
    else:
        protocol = document.find(
            ".//gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gmx"
            ":Anchor",
            NAMESPACE_PREFIXES).text
    profile_version = document.find(".//gmd:metadataStandardVersion/gco:CharacterString", NAMESPACE_PREFIXES).text

    result['pdokServiceType'] = __get_service_type(service_access_point)
    result['serviceAccessPoint'] = service_access_point
    result['metadataStandardVersion'] = profile_version
    result['protocol'] = protocol
    result['getRecordByIdUrl'] = record_info_base_url

    return result


def get_filtered_ngr_records(ngr_records, pdok_service_type):
    records = []
    for ngr_record in ngr_records:
        if ngr_record['pdokServiceType'] == pdok_service_type:
            records.append(ngr_record)
    return records
