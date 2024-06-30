# Thamarat API
## Description
This project provides the backend API for a social media platform specifically designed for readers. Users can create accounts, connect with other readers, read books, translate books by AI, convert books to audio by AI, share book summaries, write reviews, participate in discussions, send messages, follow authors or publishers, and more.
## Technologies
-Django: A high-level Python web framework for rapid development (https://www.djangoproject.com/)  
-Django REST Framework (DRF): An extension for Django that simplifies building RESTful APIs (https://www.django-rest-framework.org/)  
## Installation for Linux
### Prerequisites:
-Python (version 3.x recommended) - Check with python --version  
-pip (Python package manager) - Usually included with Python installation  
### Clone the Repository:
-git clone https://github.com/A-social-media-platform-for-readers/Thamarat-Backend.git  
-cd Thamarat-Backend  
### Create a Virtual Environment (Recommended):
-python -m venv venv  
-source venv/bin/activate  
### Install Dependencies:
-pip install -r requirements.txt  
-sudo apt install tesseract-ocr  
-sudo apt install tesseract-ocr-ara  
## Running the Application
### Start the Development Server:
-python3 manage.py runserver  
### SWAGGER Interactive API Documentation:
-https://backend-9s26.onrender.com/api/schema/swagger-ui/  
