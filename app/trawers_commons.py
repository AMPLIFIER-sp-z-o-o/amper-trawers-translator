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


def get_liabilities_request(url=None):
    if not url:
        from app.cli import TRAWERS_SOA_URL
        url = TRAWERS_SOA_URL
    body = f"""
            <?xml version="1.0" encoding="UTF-8"?>
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns="http://tres.pl/Trawers">
                    <soapenv:Header/>
                    <soapenv:Body>
                        <LiabilitiesRequest>
                        </LiabilitiesRequest>
                    </soapenv:Body>
                </soapenv:Envelope>"""
    headers = {
        'Host': str(url),
        'Content-Type': 'application/soap_xml; charset=utf-8',
        'Content-Length': str(len(body)),
        'SOAPAction': str(url) + '/TrawersSOA/LiabilitiesRequest'
    }
    try:
        response = requests.post(url, data=body.encode('utf-8'), headers=headers)
        return parseXML_liabilities_request(response.text)
    except Exception as ex:
        print( f"ERROR! Exception: {ex}")
        return []


def parseXML_liabilities_request(xml):
        try:
            doc_data = xml.split('<liabilities>')[1]
            doc_data = doc_data.split('</liabilities>')[0]
            doc_data = "<records>" + doc_data + "</records>"
            data = xmltodict.parse(doc_data)
            data = json.loads(json.dumps(data))
            try:
                for record, rec_value in data['records'].items():
                    pass
                if type(rec_value) == dict:
                    list_return = []
                    list_return.append(rec_value)
                    return list_return
                return rec_value
            except Exception as ex:
                print(ex)
                return {}
        except Exception as ex:
            print(ex)
            return {}


def trawers_soa_request(content, request_type, url=None):
    if not url:
        from app.cli import TRAWERS_SOA_URL
        url = TRAWERS_SOA_URL
    headers = {
        'Host': str(url),
        'Content-Type': 'application/soap_xml; charset=utf-8',
        'Content-Length': str(len(content)),
        'SOAPAction': str(url) + f'/TrawersSOA/{request_type}'
    }

    response = requests.post(url, data=content, headers=headers)
    return response.text


def trawers_process_response(response):
    if '<result>OK</result>' in response:
        str_start = response.find('<erpKey>') + 8
        str_end = response.find('</erpKey>')
        doc_number = response[str_start: str_end]
        return [True, doc_number]
    elif 'faultstring>' in response:
        str_start = response.find('faultstring>') + 12
        error_code = response[str_start:]
        str_end = error_code.find('</')
        error_code = error_code[:str_end]
        return [False, error_code]


def get_payment_form(input):
    payment_name = ""
    payment_cash = False

    if input == "G":
        payment_name = "Gotówka"
        payment_cash = True
    elif input == "P":
        payment_name = "Przelew"
    elif input == "C":
        payment_name = "Czek"
    elif input == "K":
        payment_name = "Kompensata"
    elif input == "N":
        payment_name = "Przedpłata"
    elif input == "Z":
        payment_name = "Za pobraniem"
    elif input == "L":
        payment_name = "Karta płatnicza"
    elif input == "R":
        payment_name = "Kredyt bankowy"
    elif input == "B":
        payment_name = "Barter"
    elif input == "W":
        payment_name = "Gotówka później"
        payment_cash = True
    elif input == "O":
        payment_name = "Zapłacono"
    elif input == "T":
        payment_name = "Według kontraktu"
    elif input == "I":
        payment_name = "Inne"

    return [payment_name, payment_cash]
