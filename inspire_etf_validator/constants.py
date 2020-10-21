INSPIRE_ETF_ENDPOINT = "localhost:8080"

# In seconds is 3 days
CACHE_EXPIRATION = 86400

TEST_ENDPOINTS = [ {
      "protocol" : "OGC:WFS",
      "metadataStandardVersion" : "Nederlands metadata profiel op ISO 19119 voor services 2.0",
      "pdokServiceType" : "WFS",
      "getRecordByIdUrl" : "https://nationaalgeoregister.nl/geonetwork/srv/dut/csw?service=CSW&request=GetRecordById&version=2.0.2&outputSchema=http%3A%2F%2Fwww.isotc211.org%2F2005%2Fgmd&elementSetName=full&id=4f4c7848-1767-4c67-be08-87d45d07f313#MD_DataIdentification",
      "label" : "habitatrichtlijn_verspreidingsgebied_van_soorten_wfs",
      "title" : "Habitatrichtlijn verspreidingsgebied van soorten WFS",
      "uuid" : "4f4c7848-1767-4c67-be08-87d45d07f313",
      "serviceAccessPoint" : "https://geodata.nationaalgeoregister.nl/habitatrichtlijnverspreidingsgebieden/v2/wfs?request=GetCapabilities"
    }, {
      "protocol" : "OGC:WFS",
      "metadataStandardVersion" : "Nederlands metadata profiel op ISO 19119 voor services 2.0",
      "pdokServiceType" : "WFS",
      "getRecordByIdUrl" : "https://nationaalgeoregister.nl/geonetwork/srv/dut/csw?service=CSW&request=GetRecordById&version=2.0.2&outputSchema=http%3A%2F%2Fwww.isotc211.org%2F2005%2Fgmd&elementSetName=full&id=e08079df-6c19-486e-916e-5c9948cfafea#MD_DataIdentification",
      "label" : "cbs_gebiedsindelingen_(inspire_geharmoniseerd)_wfs",
      "title" : "CBS Gebiedsindelingen (INSPIRE geharmoniseerd) WFS",
      "uuid" : "e08079df-6c19-486e-916e-5c9948cfafea",
      "serviceAccessPoint" : "https://geodata.nationaalgeoregister.nl/inspire/su-vector/wfs?&request=GetCapabilities&service=WFS"
    }, {
      "protocol" : "OGC:WFS",
      "metadataStandardVersion" : "Nederlands metadata profiel op ISO 19119 voor services 2.0",
      "pdokServiceType" : "WFS",
      "getRecordByIdUrl" : "https://nationaalgeoregister.nl/geonetwork/srv/dut/csw?service=CSW&request=GetRecordById&version=2.0.2&outputSchema=http%3A%2F%2Fwww.isotc211.org%2F2005%2Fgmd&elementSetName=full&id=a8ad0d7d-ea9e-4261-bc92-772e99a41387#MD_DataIdentification",
      "label" : "adressen_v2_wfs",
      "title" : "Adressen V2 WFS",
      "uuid" : "a8ad0d7d-ea9e-4261-bc92-772e99a41387",
      "serviceAccessPoint" : "https://geodata.nationaalgeoregister.nl/inspireadressen/v2/wfs?service=wfs&request=GetCapabilities"
    }]