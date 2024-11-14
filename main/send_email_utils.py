from io import BytesIO
import os
from django.template.loader import get_template
from xhtml2pdf import pisa
import qrcode
from django.core.files.storage import default_storage
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from pathlib import Path
from computerWebsite import settings
from django.conf import settings as django_settings

def generate_pdf(template_src, commande_instance, time):
    """
    Converts an HTML template into a PDF file and returns the PDF content.
    """
    context_dict = {
        "computer_id": commande_instance.computer.id,
        "user_name": f"{commande_instance.first_name} {commande_instance.last_name}",
        "computer_brand": commande_instance.computer.brand,
        "computer_processeur": commande_instance.computer.processor.model,
        "computer_ram": commande_instance.computer.memory.capacity,
        "computer_storage": commande_instance.computer.storages.first().capacity,
        "computer_color": commande_instance.computer.color.color,
        "user_phone": commande_instance.phone,
        "time": time,
        "computer_quantite": commande_instance.number
    }
    
    try:
        # Generate QR code
        if time:
            qr_data = f"http://192.168.1.97:8000/bright.cbuy/detail/{context_dict['computer_id']}/{time}"
        else:
            qr_data = f"http://192.168.1.97:8000/bright.cbuy/"

        qr = qrcode.make(qr_data)

        # Save QR code to BytesIO
        qr_buffer = BytesIO()
        qr.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)

        # Save temporary QR code
        qr_path = default_storage.save("qr_code.png", qr_buffer)

        # Update context
        context_dict.update({
            'qr_code_path': qr_path,
            'currentDate': timezone.now(),
            'page_number': "1"
        })

        # Render template
        template = get_template(template_src)
        html = template.render(context_dict)

        # Create PDF
        result = BytesIO()
        
        # Define link callback
        def link_callback(uri, rel):
            return os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))

        # Generate PDF
        pdf = pisa.pisaDocument(
            BytesIO(html.encode("UTF-8")), 
            dest=result,
            link_callback=link_callback
        )

        # Clean up QR code
        if default_storage.exists(qr_path):
            default_storage.delete(qr_path)

        if not pdf.err:
            return result.getvalue(), True
        
        return None, False

    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return None, False

def send_pdf_email(
    to_email: str,
    subject: str,
    template_src: str,
    commande_instance,
    time: str,
    logo_path: str = None,
    email_context: dict = None
) -> bool:
    """
    Generate PDF and send email with PDF attachment.
    """
    try:
        # Generate PDF
        pdf_content, success = generate_pdf(template_src, commande_instance, time)
        if not success:
            print("Failed to generate PDF")
            return False

        # Generate email body
        email_body = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    color: #333;
                    background-color: #f4f4f4;
                }}
                .email-container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    text-align: center;
                    background-color: #050A44;
                    color: #ffffff;
                    padding: 10px 0;
                    border-radius: 8px 8px 0 0;
                }}
                .content {{
                    padding: 20px;
                    line-height: 1.6;
                }}
                .button {{
                    display: inline-block;
                    background-color: #0A21C0;
                    color: #ffffff;
                    padding: 10px 20px;
                    border-radius: 5px;
                    text-decoration: none;
                    margin-top: 20px;
                    text-align: center;
                }}
                .footer {{
                    text-align: center;
                    font-size: 0.9em;
                    color: #777;
                    margin-top: 20px;
                }}
            </style>
            </head>
            <body>
            <div class="email-container">
                <div class="header">
                    <h2>Confirmation de Commande</h2>
                </div>
                <div class="content">
                    <p>Bonjour {commande_instance.first_name} {commande_instance.last_name},</p>
                    <p>Merci pour votre commande. Nous confirmons que votre commande a bien été prise en compte.</p>
                    <p>Vous trouverez les détails de votre commande dans le fichier ci-joint.</p>
                    <p>Si vous avez des questions, n'hésitez pas à nous contacter.</p>
                    <a href="mailto:{django_settings.EMAIL_HOST_USER}" class="button" style="color:#fff">Contacter le Support</a>
                </div>
                <div class="footer">
                    <p>Merci de faire confiance à notre entreprise.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Créer l'e-mail
        email = EmailMessage(
            subject=subject,
            body=email_body,
            from_email=django_settings.EMAIL_HOST_USER,
            to=[to_email]
        )
        
            # Set email to use HTML
        email.content_subtype = 'html'
            
        # Attach generated PDF with a meaningful name
        pdf_filename = f"order_zoodo_Computer_{time}.pdf"
        email.attach(
            pdf_filename,
            pdf_content,
            'application/pdf'
        )
            
        # Send email
        email.send(fail_silently=False)
        return True
    
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
