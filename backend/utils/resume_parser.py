"""
Resume Parser Module
Handles PDF and DOCX file parsing to extract text content
"""

import PyPDF2
from docx import Document
import os
import tempfile

class ResumeParser:
    """
    A class to handle resume parsing from PDF and DOCX files
    """
    
    @staticmethod
    def extract_text_from_pdf(file_path):
        """
        Extract text from PDF file
        
        Args:
            file_path (str): Path to PDF file
            
        Returns:
            str: Extracted text content
        """
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract text from all pages
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                    
            return text.strip()
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            return ""
    
    @staticmethod
    def extract_text_from_docx(file_path):
        """
        Extract text from DOCX file
        
        Args:
            file_path (str): Path to DOCX file
            
        Returns:
            str: Extracted text content
        """
        try:
            doc = Document(file_path)
            text = ""
            
            # Extract text from all paragraphs
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
                
            return text.strip()
        except Exception as e:
            print(f"Error extracting DOCX: {e}")
            return ""
    
    @staticmethod
    def extract_text_from_txt(file_path):
        """
        Extract text from TXT file
        
        Args:
            file_path (str): Path to TXT file
            
        Returns:
            str: Extracted text content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            return text.strip()
        except Exception as e:
            print(f"Error extracting TXT: {e}")
            return ""
    
    @staticmethod
    def parse_resume(file_path, file_extension):
        """
        Main method to parse resume based on file extension
        
        Args:
            file_path (str): Path to resume file
            file_extension (str): File extension (.pdf or .docx)
            
        Returns:
            str: Extracted text content
        """
        if file_extension.lower() == '.pdf':
            return ResumeParser.extract_text_from_pdf(file_path)
        elif file_extension.lower() in ['.docx', '.doc']:
            return ResumeParser.extract_text_from_docx(file_path)
        elif file_extension.lower() == '.txt':
            return ResumeParser.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    @staticmethod
    def save_uploaded_file(uploaded_file):
        """
        Save uploaded file temporarily and return path
        
        Args:
            uploaded_file: Flask uploaded file object
            
        Returns:
            tuple: (file_path, file_extension)
        """
        try:
            # Get file extension
            filename = uploaded_file.filename
            file_extension = os.path.splitext(filename)[1]
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_extension)
            uploaded_file.save(temp_file.name)
            
            return temp_file.name, file_extension
        except Exception as e:
            print(f"Error saving file: {e}")
            return None, None