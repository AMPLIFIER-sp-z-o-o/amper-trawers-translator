from datetime import datetime
from decimal import Decimal

from amper_api.settlement import Settlement
from app.trawers_commons import get_records_trawers, get_liabilities_request

def import_settlements(backend):
    records = get_liabilities_request()
    settlements = []

    for record in records:
        # if not record['name'].startswith('Faktura sprzedaży nr'): continue
        settlement_number = f"{record['name'].split('Faktura sprzedaży nr: ')[1]}/{record['create'][5:7]}/{record['create'][2:4]}"
        settlement = Settlement()
        settlement.customer = record['customerKey']
        settlement.account = record['customerKey']
        settlement.number = settlement_number
        settlement.external_id = settlement_number
        settlement.value = record['value']
        settlement.value_to_pay = record['remainder']
        settlement.date = record['create']
        settlement.due_date = record['maturity']
        settlements.append(settlement)

    fields = ['NUMER', 'ODBDOST', 'DATA', 'TERMIN']
    for year in range(2022, datetime.now().year + 1):
        records = get_records_trawers(system='NA', table_id='313', fields=fields, query=f"<year>{year}</year><where><RODZAJD>FK</RODZAJD></where>")
        for record in records:
            value = Decimal(0)
            fields_pos = ['OWARTOSC', 'PWARTOSC']
            records_pos = get_records_trawers(system='NA', table_id='188', fields=fields_pos, query=f"<year>{year}</year><where><numer>{record['NUMER']}</numer></where>")
            for record_pos in records_pos:
                value += Decimal(record_pos['OWARTOSC']) + Decimal(record_pos['PWARTOSC'])

            settlement = Settlement()
            settlement.customer = record['ODBDOST']
            settlement.account = record['ODBDOST']
            settlement.number = record['NUMER']
            settlement.value = str(value)
            settlement.value_to_pay = str(value)
            settlement.date = record['DATA']
            settlement.due_date = record['TERMIN']
            settlement.external_id = record['NUMER']
            settlements.append(settlement)

    backend.send_settlements(settlements)
