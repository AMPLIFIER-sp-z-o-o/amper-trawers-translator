from amper_api.order import Order
from amper_api.log import LogSeverity
from amper_api.backend import Backend
from app.trawers_commons import trawers_soa_request, trawers_process_response


def export_orders(backend: Backend):
    orders = backend.get_list_of_orders({"status": "Pending"})
    for order in orders:
        try:
            content = create_order(order, backend)
            if content is None:
                return
            response = trawers_soa_request(content, "orderNew")
            trawers_order_number = trawers_process_response(response)
            if trawers_order_number[0]:
                backend.change_order_status(
                    {"status": "Exported",
                     "token": order.token}
                )
                backend.create_log_entry_async(LogSeverity.Info, f"Exported order {str(order.token)}: {trawers_order_number[1]}")
            else:
                backend.create_log_entry_async(LogSeverity.Error, f"Failure while sending order {str(order.token)}: {trawers_order_number[1]}")

        except Exception as ex:
            backend.create_log_entry_async(LogSeverity.Error, f"Error while in function export_orders() while processing document {str(order.token)}.", ex)


def create_order(order: Order, backend: Backend):
    try:
        customer = order.customer_external_id if order.customer_external_id else 'GOSC00'
        if '_' in customer:
            customer = customer.split('_')[0]

        items = ""
        for line in order.lines:
            item = f"""
                        <item>
                            <productKey>{line.product_external_id}</productKey>
                            <quantity>{str(line.quantity).replace('.', ',')}</quantity>
                            <price>{line.unit_price_net}</price>
                            <depot>{line.source_stock_location_name}</depot> 
                            <note></note>
                            <memo></memo>
                        </item>
                        """
            items = items + item

        description = f'{order.customer_note}; Nr: {order.order_number}'.replace('<', '').replace('>', '')

        content = f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                    <soapenv:Header/>
                    <soapenv:Body>
                        <orderNew>                    
                            <customerKey>{customer}</customerKey>
                            {items}
                            <description>{description}</description>
                            <note></note>
                        </orderNew>
                    </soapenv:Body>
                    </soapenv:Envelope> 
            """
        content = content.replace('&', '&amp;').encode('utf-8')
        return content
    except Exception as ex:
        backend.create_log_entry_async(LogSeverity.Error, f"Error while in function export_orders() while processing document {str(order.token)}.", ex)
        return None
