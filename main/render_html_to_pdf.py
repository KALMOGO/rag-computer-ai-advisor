from io import BytesIO
import os
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import qrcode
from django.core.files.storage import default_storage
from computerWebsite import settings
from django.utils import timezone

def render_html_to_pdf(template_src, context_dict={}):
    """
    Converts an HTML template into a PDF file and returns it as an HttpResponse.
    
    This function takes a Django template and a context dictionary, renders the template
    with the given context, and then converts the rendered HTML into a PDF file using
    xhtml2pdf. The resulting PDF is returned as an HttpResponse with the content type
    set to 'application/pdf'.
    
    Args:
        template_src (str): The path to the Django template to be rendered.
        context_dict (dict, optional): A dictionary containing context variables to be
            used in the template rendering. Defaults to an empty dictionary.
    
    Returns:
        HttpResponse: An HTTP response containing the generated PDF file. If an error
        occurs during PDF generation, an HTTP response with status code 400 and a message
        "Invalid PDF" is returned.
    """
    # Contenu  du qrcode
    if len(context_dict['time']) != 0:
            qr_data = f"http://192.168.1.97:8000/bright.cbuy/detail/{context_dict['computer_id']}/{context_dict['time']}"
    else:
        qr_data = f"http://192.168.1.97:8000/bright.cbuy/"

    qr = qrcode.make(qr_data)

    # Save QR code image to a BytesIO object
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)  # Move to the beginning of the BytesIO buffer

    # Save QR code to default storage
    qr_path = default_storage.save("qr_code.png", qr_buffer)

    # Add QR code path to context dictionary for rendering in template
    context_dict['qr_code_path'] = qr_path
    context_dict['currentDate'] = timezone.now()
    context_dict['page_number'] = "1"

    # Render HTML template with context data
    template = get_template(template_src)
    html = template.render(context_dict)

    # Create PDF from HTML
    result = BytesIO()

    # Define link callback for resolving media URLs
    links = lambda uri, rel: os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))

    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), dest=result, link_callback=links)

    # Delete the QR image regardless of PDF generation success or failure
    if default_storage.exists(qr_path):
        default_storage.delete(qr_path)

    if pdf.err:
        return HttpResponse("Invalid PDF", status=400, content_type='text/plain')

    return HttpResponse(result.getvalue(), content_type='application/pdf')