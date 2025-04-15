from decimal import Decimal

from amper_api.product import Stock, StockLocation
from app.trawers_commons import get_records_trawers

def import_stock_locations(backend):
    fields = ['ident', 'symbol', 'nazwa']
    records = get_records_trawers(system='MG', table_id='245', fields=fields)
    stock_locations = []

    for record in records:
        if record['IDENT'] == 'M':
            stock_location = StockLocation()
            stock_location.external_id = record['SYMBOL']
            stock_location.name = record['NAZWA']
            stock_locations.append(stock_location)

    backend.send_stock_locations(stock_locations)

def import_stocks(backend):
    fields = ['INDEKS', 'MAG', 'MILOSC', 'MREZER', 'FREZER', 'WREZER', 'REZMAG', 'PPRZMAG', 'PREZER']
    records = get_records_trawers(system='MG', table_id='224', fields=fields)
    stocks = []

    for record in records:
        milosc = Decimal(record['MILOSC']) if record['MILOSC'] else 0
        mrezer = Decimal(record['MREZER']) if record['MREZER'] else 0
        frezer = Decimal(record['FREZER']) if record['FREZER'] else 0
        wrezer = Decimal(record['WREZER']) if record['WREZER'] else 0
        rezmag = Decimal(record['REZMAG']) if record['REZMAG'] else 0
        pprzmag = Decimal(record['PPRZMAG']) if record['PPRZMAG'] else 0
        prezer = Decimal(record['PREZER']) if record['PREZER'] else 0
        stock_quantity = milosc - mrezer - frezer - wrezer - rezmag - pprzmag - prezer

        stock = Stock()
        stock.external_id = f"{record['INDEKS']}_{record['MAG']}"
        stock.product_external_id = record['INDEKS']
        stock.stock_level_external_id = record['MAG']
        stock.quantity = stock_quantity
        stock.quantity_allocated = Decimal(0)
        stocks.append(stock)

    backend.send_stocks(stocks)
