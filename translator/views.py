from django.shortcuts import render
from django.http import HttpResponse
from translator.forms import TextInputForm
from translator.models import Input_text
# noinspection PyUnresolvedReferences
import re
# noinspection PyUnresolvedReferences
from googletrans import Translator
import qrcode
import qrcode
from io import BytesIO
import base64


# Create your views here.
def main_page(request):
    return render(request, 'translator/main_page.html')


def text_input_view(request):
    translator = Translator()
    sig_codes = {
        'qd': 'Once daily',
        'bid': 'twice daily', 'tid': 'three times daily', 'qid': 'four times daily', 'hs': 'at bedtime',
        'am': 'every morning', 'pm': 'every evening', 'po': 'by mouth',
        '1t': 'Take 1 tablet', '1c': 'Take 1 capsule', 'prn': 'as needed',
        'wf': 'with food',
        'f7d': 'for 7 days',
        'fxd': 'for 10 days'
    }
    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            user_text = form.cleaned_data['user_text']
            input_unispace = re.sub(r'(\s+;\s+|;\s+|\s+;|;)', ' ', user_text)
            input_split = input_unispace.split()
            converted_text = ''
            sig_keys = sig_codes.keys()
            for words in input_split:
                if words in sig_keys:
                    converted_text += sig_codes[words] + ' '

                else:
                    converted_text += words + ' '

            spanish_translation = translator.translate(converted_text, dest='es')
            # Create QR code instance
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)

            # Add data to the QR code
            data = spanish_translation.text
            qr.add_data(data)
            qr.make(fit=True)

            # Create an image from the QR code
            img = qr.make_image(fill_color="black", back_color="white")

            # Create a BytesIO buffer to hold the image data
            buffer = BytesIO()
            img.save(buffer)
            buffer.seek(0)

            # Encode the image in Base64
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            # Save the image
            # img.save("qr_code.png")

            # Open the image using default image viewer

            return render(request, 'translator/success.html', {'img_base64': img_base64})
    else:
        form = TextInputForm()

    return render(request, 'translator/main_page.html', {'form': form})


