from amper_api.document import Document
from amper_api.log import LogSeverity
from amper_api.backend import Backend
from app.trawers_commons import trawers_soa_request, trawers_process_response


def export_documents(backend: Backend):
    documents = backend.get_list_of_documents("APPROVED")
    for document in documents:
        try:
            content = create_document(document)
            response = trawers_soa_request(content, "SalesInvoice")
            trawers_document_number = trawers_process_response(response)
            if trawers_document_number[0]:
                backend.change_document_status(
                    {"status": "EXPORTED",
                     "id": document.id}
                )
                backend.create_log_entry_async(LogSeverity.info,
                                               f"Exported document {str(document.id)}: {trawers_document_number[1]}")
            else:
                backend.create_log_entry_async(LogSeverity.Error, f"Failure while sending document {str(document.id)}: {trawers_document_number[1]}")
        except Exception as ex:
            backend.create_log_entry_async(LogSeverity.Error, f"Error while in function export_documents() while processing document {str(document.id)}.", ex)


def create_document(document: Document):
    customer = document.customer_external_id if document.customer_external_id else 'GOSC00'
    if '_' in customer:
        customer = customer.split('_')[0]

    items = ""
    for line in document.document_lines:
        item = f"""
                <item>
                    <productKey>{line.product_external_id}</productKey>
                    <quantity>{line.quantity.replace('.' , ',')}</quantity>
                    <price>{line.price_net}</price>
                    <depot>{document.stock_location['external_id']}</depot> 
                    <note></note>
                    <memo></memo>
                </item>
                """
        items = items + item

    short_number = document.number
    description = f'{document.description}; Numer:{document.number}'.replace('<', '').replace('>', '')

    content = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                <soapenv:Header/>
                <soapenv:Body>
                    <orderNew>                    
                        <customerKey>{customer}</customerKey>
                        {items}
                        <description>{description}</description>
                        <note>{short_number}</note>
                    </orderNew>
                </soapenv:Body>
                </soapenv:Envelope> 
        """
    content = content.replace('&', '&amp;').encode('utf-8')
    return content
