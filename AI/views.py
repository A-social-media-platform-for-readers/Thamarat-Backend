from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from users.views import UserView
from books.models import Book
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
        translated = GoogleTranslator(source='auto', target=language).translate(text)
        
        return Response(translated, status=status.HTTP_200_OK)


class OCR(viewsets.ModelViewSet):
    """
    OCR API
    """

    def pdf2text(self, request, book_id, start_page=0, end_page=1, language="eng"):
        """
        Convert pdf to text

        Parameters:
			book_id (int): the id of the book.
			start_page (int): the number of page to start with(eg: 13).
			end_page (int): the number of page to end with(eg: 15).
			language (str): the language of the PDF(eg: "eng" or "ara").

		Return:
			the textual content of all the pages.
		"""

        def convert_pdf_to_img(pdf_file):
            """
            this function converts a PDF into Image

            Parameters:
                pdf_file: the file path to be converted

            Return:
                an interable containing image format of all the pages of the PDF
            """
            return convert_from_path(pdf_file, first_page=start_page, last_page=end_page)

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

        book = get_object_or_404(Book, id=book_id)
        if book.pdf_file:
            book_path = book.pdf_file
            Text = get_text_from_any_pdf(book_path)
        else:
            return HttpResponseNotFound("The requested book does not have a PDF file.")

        return Response(Text, status=status.HTTP_200_OK)
