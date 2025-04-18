from decimal import Decimal

from amper_api.product import Product, UnitOfMeasure
from amper_api.log import LogSeverity
from app.trawers_commons import get_records_trawers


def import_products(backend):
    try:
        fields = ['indeks', 'inazwa', 'nrptu', 'jm', 'jmz', 'opilosc', 'waga', 'ean13', 'opakowan']
        records = get_records_trawers(system='MG', table_id='229', fields=fields)
        fields = ['indeks', 'typ', 'spcena1', 'spcena3']
        prices = get_records_trawers(system='MI', table_id='211', fields=fields)
        prices_table = []
        for price in prices:
            if price['INDEKS'] and price['TYP'] == '60':
                prices_table.append(
                    {"INDEX": price['INDEKS'],
                     "PRICE": price['SPCENA1'],
                     "MINIMAL_PRICE": price['SPCENA3']}
                )
        vat = {'00': 0,
               '01': 23,
               '02': 8,
               '03': 3,
               '04': 5,
               '05': 22,
               '06': 23,
               '98': 0,
               '99': 0}

        products = []
        unit_of_measures = []
        for record in records:
            price = "0"
            min_price = "0"
            for price in prices_table:
                if price['INDEX'] == record['INDEKS']:
                    price = price['PRICE']
                    min_price = price['MINIMAL_PRICE']
                    break

            product = Product()
            product.updatable_fields = 'short_code,ean,sku,default_price,minimal_price,default_unit_of_measure,vat,piggy_bank_budget,weight'
            product.attributes = []
            product.name = record['INAZWA']
            product.friendly_name = ''
            product.short_description = record['INDEKS']
            product.description = ''
            product.short_code = record['INDEKS']
            product.sku = record['INDEKS']
            product.vat = vat[record['NRPTU']]
            product.available_on = '2000-01-01'
            product.is_published = True
            product.is_featured = False
            product.weight = Decimal(record['WAGA'])
            product.default_unit_of_measure = record['JM']
            product.external_id = record['INDEKS']
            product.cumulative_unit_of_measure = 'Op.zb.'
            product.cumulative_converter = Decimal(record['OPILOSC'])
            product.can_be_split = False
            product.cumulative_unit_ratio_splitter = Decimal("1")
            product.unit_roundup = False
            product.ean = record['EAN13']
            product.default_price = Decimal(price)
            product.minimal_price = Decimal(min_price)

            products.append(product)

            if record['OPILOSC'] and Decimal(record['OPILOSC']) > 0 and record['OPAKOWAN'] is not None:
                unit_of_measure = UnitOfMeasure()
                unit_of_measure.external_id = f'opzb_{record["INDEKS"]}'
                unit_of_measure.product_external_id = record['INDEKS']
                unit_of_measure.can_be_split = False
                unit_of_measure.converter = Decimal(record['OPILOSC'])
                unit_of_measure.cumulative_unit_ratio_splitter = Decimal("1")
                unit_of_measure.name = record['OPAKOWAN']
                unit_of_measure.weight = Decimal("0")
                unit_of_measure.unit_roundup = False
                unit_of_measures.append(unit_of_measure)

        backend.send_products(products)
        backend.send_unit_of_measures(unit_of_measures)
    except Exception as ex:
        backend.create_log_entry_async(LogSeverity.Error, f"Error while in function import_products()", ex)
