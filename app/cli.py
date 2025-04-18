import os

from amper_api.auth import AmplifierJWTAuth
from amper_api.backend import Backend

from app.products import import_products
from app.accounts import import_accounts
from app.stocks import import_stock_locations, import_stocks
from app.settlements import import_settlements

AMPER_USERNAME = os.environ.get('AMPER_USERNAME', None)
AMPER_PASS = os.environ.get('AMPER_PASS', None)
AMPER_WS_URL = os.environ.get('AMPER_WS_URL', None)
TRAWERS_SOA_URL = os.environ.get('TRAWERS_SOA_URL', None)

def main(args):
    if not args:
        print('You need to provide an parameter.')
        return

    if not AMPER_USERNAME or not AMPER_PASS or not AMPER_WS_URL:
        print('You need to provide environment variables.')
        return

    amper_api = AmplifierJWTAuth(
        username=AMPER_USERNAME, password=AMPER_PASS, auth_url=AMPER_WS_URL
    )
    amper_token = amper_api.get_token()
    if not amper_token:
        print('Could not authenticate with provided credentials.')
        return
    amper_ws = Backend(amper_token, AMPER_WS_URL, log_source='amper-trawers-translator')
    if args.i and args.i == 'products':
        import_products(amper_ws)
    if args.i and args.i == 'accounts':
        import_accounts(amper_ws)
    if args.i and args.i == 'stocks':
        import_stock_locations(amper_ws)
        import_stocks(amper_ws)
    if args.i and args.i == 'settlements':
        import_settlements(amper_ws)
