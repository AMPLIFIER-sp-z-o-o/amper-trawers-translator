import json

import requests
import xmltodict

def build_trawers_request_header(body_length, url):
    if not url.endswith('/'):
        url = url + '/'
    return {
        'Host': url,
        'Content-Type': 'application/soap_xml; charset=utf-8',
        'Content-Length': body_length,
        'SOAPAction': f'{url}TrawersSOA/TableGet'
    }


def parse_xml_to_json(xml):
    try:
        doc_data = xml.split('<records>', 1)
        doc_data = doc_data[1].split('</records>', 1)[0]
        doc_data = "<records>" + doc_data + "</records>"
        data = xmltodict.parse(doc_data)
        data = json.loads(json.dumps(data))
        try:
            for record, rec_value in data['records'].items():
                pass
            if type(rec_value) == dict:
                list_return = [rec_value]
                return list_return
            return rec_value
        except Exception as ex:
            print(ex)
            return {}
    except Exception as ex:
        print(ex)
        return {}


def get_records_trawers(system='NA', table_id='199', query='', fields=None, url=None):
    if not url:
        from app.cli import TRAWERS_SOA_URL
        url = TRAWERS_SOA_URL
    fields_xml = ''
    for field in fields:
        fields_xml += f'<{field}/>'
    fields_xml = f'<fields>{fields_xml}</fields>'

    body = f'<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns="http://tres.pl/Trawers"><soapenv:Header/><soapenv:Body><TableGet><system>{system}</system><tableId>{table_id}</tableId>{fields_xml}{query}</TableGet></soapenv:Body></soapenv:Envelope>'
    headers = build_trawers_request_header(body, url)
    try:
        response = requests.post(url, data=body.encode('utf-8'), headers=headers)
        return parse_xml_to_json(response.text)
    except Exception as ex:
        print(f"ERROR! Exception: {ex}")
        exit()


