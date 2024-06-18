from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from users.views import UserView
from pdf2image import convert_from_path
from pytesseract import image_to_string
from deep_translator import GoogleTranslator


class Translate(viewsets.ModelViewSet):
    """
    Translation API
    """

    def translate(self, request, text, language="en"):
        """
        Translate text

        Parameters:
            text (str): the text to be translated.
            language (str): the destination language(eg: "en" or "ar").

        Return:
            translated text.
        """
        UserView.check_auth(self, request)
        translated = GoogleTranslator(source='auto', target=language).translate(text)
        
        return Response(translated, status=status.HTTP_200_OK)


class OCR(viewsets.ModelViewSet):
    """
    OCR API
    """

    def pdf2text(self, request, pdf_path, language="eng", pages_count=1):
        """
        Convert pdf to text

        Parameters:
			pdf_path (str): the path of the PDF file.
			language (str): the language of the PDF(eg: "eng" or "ara").
			pages_count (int): the number of pages to be converted to text.

		Return:
			the textual content of all the pages.
		"""

        UserView.check_auth(self, request)
        def convert_pdf_to_img(pdf_file):
            """
            this function converts a PDF into Image

            Parameters:
                pdf_file: the file path to be converted

            Return:
                an interable containing image format of all the pages of the PDF
            """
            return convert_from_path(pdf_file, first_page=0, last_page=pages_count)

        def convert_image_to_text(file):
            """
            this function extracts text from image

            Parameters:
                file: the image file to extract the content

            Return:
                the textual content of single image
            """

            text = image_to_string(file, lang=language)
            return text

        def get_text_from_any_pdf(pdf_file):
            """
            this function is our final system combining the previous functions

            Parameters:
                pdf_file: the original PDF file path

            Return:
                the textual content of ALL the pages
            """
            images = convert_pdf_to_img(pdf_file)
            final_text = ""
            for pg, img in enumerate(images):

                final_text += convert_image_to_text(img)

            return final_text

        Text = get_text_from_any_pdf(pdf_path)

        return Response(Text, status=status.HTTP_200_OK)
