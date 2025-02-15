import decimal

from amper_api.product import Product, UnitOfMeasure
from app.trawers_commons import get_records_trawers

def import_products(backend):
    fields = ['indeks', 'inazwa', 'nrptu', 'jm', 'jmz', 'opilosc', 'waga', 'ean13', 'opakowan']
    records = get_records_trawers(system='MG', table_id='229', fields=fields)
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
        #todo ustalić skąd ma być pobierana cena katalogowa (cena 100) i cena minimalna (jeżeli taka jest)
        cena = 0
        min_price = 0
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
        product.weight = record['WAGA']
        product.default_unit_of_measure = record['JM']
        product.external_id = record['INDEKS']
        product.cumulative_unit_of_measure = 'Op.zb.'
        product.cumulative_converter = record['OPILOSC']
        product.can_be_split = False
        product.cumulative_unit_ratio_splitter = 1
        product.unit_roundup = False
        product.ean = record['EAN13']
        product.default_price = cena
        product.minimal_price = min_price

        products.append(product)

        if record['OPILOSC'] and decimal.Decimal(record['OPILOSC']) > 0 and record['OPAKOWAN'] is not None:
            unit_of_measure = UnitOfMeasure()
            unit_of_measure.external_id = f'opzb_{record["INDEKS"]}'
            unit_of_measure.product_external_id = record['INDEKS']
            unit_of_measure.can_be_split = False
            unit_of_measure.converter = record['OPILOSC']
            unit_of_measure.cumulative_unit_ratio_splitter = 1
            unit_of_measure.name = record['OPAKOWAN']
            unit_of_measure.weight = 0
            unit_of_measure.unit_roundup = False
            unit_of_measures.append(unit_of_measure)

    backend.send_products(products)
    backend.send_unit_of_measures(unit_of_measures)