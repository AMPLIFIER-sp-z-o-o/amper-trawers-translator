from decimal import Decimal

from amper_api.customer import Account, Customer, CustomerCategory, CustomerCategoryRelation, PaymentForm
from app.trawers_commons import get_records_trawers, get_payment_form

def import_accounts(backend):
    fields = ['odnazwa', 'odbdost', 'odmiasto', 'odulica', 'odkod', 'odgrupa', 'odnip', 'odtel1', 'odtlx', 'odlimit',
              'odsubdiv', 'remark01', 'odlimit', 'odrabat', 'odwaluta', 'grupa', 'odrcena', 'odkodpr', 'odwarpl',
              'odformap']
    records = get_records_trawers(system='NA', table_id='199', fields=fields)
    accounts = []
    customer_categories_relations = []
    payment_forms = []
    payment_form_ids = []
    for record in records:
        account = Account()
        account.name = record['ODNAZWA']
        account.city = record['ODMIASTO']
        account.street = record['ODULICA']
        account.postal_code = record['ODKOD']
        account.tax_id = record['ODNIP']
        account.short_name = record['ODBDOST']
        account.external_id = record['ODBDOST']
        account.customers = []
        customer = Customer()
        customer.name = record['ODNAZWA']
        customer.short_name = record['ODBDOST']
        customer.city = record['ODMIASTO']
        customer.street = record['ODULICA']
        customer.postal_code = record['ODKOD']
        customer.phone = record['ODTEL1']
        customer.tax_id = record['ODNIP']
        customer.external_id = record['ODBDOST']
        customer.primary_email = record['ODTLX']
        customer.discount = Decimal(0)
        customer.payment_form_external_id = f"{record['ODFORMAP']}{record['ODWARPL']}"
        account.customers.append(customer)
        accounts.append(account)

        customer_categories_relation = CustomerCategoryRelation()
        customer_categories_relation.external_id = f"all_customers_{record['ODBDOST']}"
        customer_categories_relation.category_external_id = "all_customers"
        customer_categories_relation.customer_external_id = f"{record['ODBDOST']}"
        customer_categories_relations.append(customer_categories_relation)

        if customer.payment_form_external_id not in payment_form_ids:
            payment_form_ids.append(f"{record['ODFORMAP']}{record['ODWARPL']}")
            payment_form = PaymentForm()
            payment_form.external_id = f"{record['ODFORMAP']}{record['ODWARPL']}"
            customer_payment_form = get_payment_form(record['ODFORMAP'])
            payment_form.name = customer_payment_form[0]
            payment_form.is_cash = customer_payment_form[1]
            payment_forms.append(payment_form)

    customer_categories = []
    customer_category = CustomerCategory()
    customer_category.external_id = "all_customers"
    customer_category.parent_external_id = None
    customer_category.name = "Wszyscy"
    customer_category.description = ""
    customer_category.seo_tags = None
    customer_category.order = 1
    customer_categories.append(customer_category)

    backend.send_payment_forms(payment_forms)
    backend.send_accounts(accounts)
    backend.send_customer_categories(customer_categories)
    backend.send_customer_categories_relation(customer_categories_relations)
