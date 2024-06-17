from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from pdf2image import convert_from_path
from pytesseract import image_to_string


class OCR(viewsets.ModelViewSet):
	"""
	OCR API
	"""

	def pdf2text(self, request, pdf_path, language="eng", pages_count=1):
		"""
		Convert pdf to text
		"""
		def convert_pdf_to_img(pdf_file):
			"""
			this function converts a PDF into Image
			
			Args:
				pdf_file: the file to be converted
			
			returns:
				an interable containing image format of all the pages of the PDF
			"""
			return convert_from_path(pdf_file, first_page=0, last_page=pages_count)


		def convert_image_to_text(file):
			"""
			this function extracts text from image
			
			Args:
				file: the image file to extract the content
			
			returns:
				the textual content of single image
			"""
			
			text = image_to_string(file, lang=language)
			return text


		def get_text_from_any_pdf(pdf_file):
			"""
			this function is our final system combining the previous functions
			
			Args:
				file: the original PDF File
			
			returns:
				the textual content of ALL the pages
			"""
			images = convert_pdf_to_img(pdf_file)
			final_text = ""
			for pg, img in enumerate(images):
				
				final_text += convert_image_to_text(img)
			
			return final_text


		Text = get_text_from_any_pdf(pdf_path)

		return Response(Text, status=status.HTTP_200_OK)
