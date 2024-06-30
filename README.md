# Thamarat API
## Description
This project provides the backend API for a social media platform specifically designed for readers. Users can create accounts, connect with other readers, share book recommendations, write reviews, participate in discussions, and more.
## Technologies
Django: A high-level Python web framework for rapid development (https://www.djangoproject.com/)
Django REST Framework (DRF): An extension for Django that simplifies building RESTful APIs (https://www.django-rest-framework.org/)
## Installation for Linux
1-Prerequisites:
Python (version 3.x recommended) - Check with python --version
pip (Python package manager) - Usually included with Python installation
2-Clone the Repository:
git clone https://github.com/A-social-media-platform-for-readers/Thamarat-Backend.git
cd Thamarat-Backend
3-Create a Virtual Environment (Recommended):
python -m venv venv
source venv/bin/activate
4-Install Dependencies:
pip install -r requirements.txt
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-ara
## Running the Application
1-Start the Development Server:
python3 manage.py runserver
2-SWAGGER Interactive API Documentation:
https://backend-9s26.onrender.com/api/schema/swagger-ui/
