#!/usr/bin/env python3
"""
Enhanced Scanner Processor for Glacier Care
Handles OCR, image processing, and document extraction
"""

import os
import io
import logging
from typing import Optional, Dict, Any
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
import fitz  # PyMuPDF
from pdf2image import convert_from_bytes
import easyocr
import pytesseract
from PyPDF2 import PdfReader
from docx import Document

logger = logging.getLogger(__name__)

class EnhancedScannerProcessor:
    def __init__(self):
        """Initialize the enhanced scanner processor"""
        self.easyocr_reader = None
        self._init_ocr()
    
    def _init_ocr(self):
        """Initialize OCR engines"""
        try:
            # Initialize EasyOCR (supports 80+ languages)
            self.easyocr_reader = easyocr.Reader(['en'], gpu=False)
            logger.info("EasyOCR initialized successfully")
        except Exception as e:
            logger.warning(f"EasyOCR initialization failed: {e}")
            self.easyocr_reader = None
        
        # Set Tesseract path if needed (Windows)
        if os.name == 'nt':
            # Common Tesseract installation paths on Windows
            possible_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                r'C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'.format(os.getenv('USERNAME', ''))
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    break
    
    def process_image(self, image_data: bytes, filename: str) -> str:
        """
        Process image files with OCR and image enhancement
        
        Args:
            image_data: Raw image bytes
            filename: Original filename
            
        Returns:
            Extracted text from the image
        """
        try:
            # Load image with PIL
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Enhance image for better OCR
            enhanced_image = self._enhance_image_for_ocr(image)
            
            # Try multiple OCR methods
            text = self._extract_text_from_image(enhanced_image)
            
            if not text.strip():
                # If no text found, try with original image
                text = self._extract_text_from_image(image)
            
            return text.strip() or f"[IMAGE] {filename} - No text detected"
            
        except Exception as e:
            logger.error(f"Error processing image {filename}: {e}")
            return f"[IMAGE] {filename} - Processing failed: {str(e)}"
    
    def process_pdf(self, pdf_data: bytes, filename: str) -> str:
        """
        Process PDF files with multiple extraction methods
        
        Args:
            pdf_data: Raw PDF bytes
            filename: Original filename
            
        Returns:
            Extracted text from the PDF
        """
        try:
            text_content = []
            
            # Method 1: Try PyMuPDF (fitz) - better for complex PDFs
            try:
                pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
                for page_num in range(pdf_document.page_count):
                    page = pdf_document[page_num]
                    text = page.get_text()
                    if text.strip():
                        text_content.append(f"Page {page_num + 1}:\n{text}")
                pdf_document.close()
                
                if text_content:
                    return "\n\n".join(text_content)
            except Exception as e:
                logger.warning(f"PyMuPDF extraction failed: {e}")
            
            # Method 2: Try PDF2Image + OCR for scanned PDFs
            try:
                images = convert_from_bytes(pdf_data, dpi=300)
                for i, image in enumerate(images):
                    enhanced_image = self._enhance_image_for_ocr(image)
                    text = self._extract_text_from_image(enhanced_image)
                    if text.strip():
                        text_content.append(f"Page {i + 1}:\n{text}")
                
                if text_content:
                    return "\n\n".join(text_content)
            except Exception as e:
                logger.warning(f"PDF2Image extraction failed: {e}")
            
            # Method 3: Try PyPDF2 as fallback
            try:
                pdf_reader = PdfReader(io.BytesIO(pdf_data))
                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    if text.strip():
                        text_content.append(f"Page {page_num + 1}:\n{text}")
                
                if text_content:
                    return "\n\n".join(text_content)
            except Exception as e:
                logger.warning(f"PyPDF2 extraction failed: {e}")
            
            return f"[PDF] {filename} - No text could be extracted"
            
        except Exception as e:
            logger.error(f"Error processing PDF {filename}: {e}")
            return f"[PDF] {filename} - Processing failed: {str(e)}"
    
    def process_docx(self, docx_data: bytes, filename: str) -> str:
        """
        Process DOCX files
        
        Args:
            docx_data: Raw DOCX bytes
            filename: Original filename
            
        Returns:
            Extracted text from the DOCX
        """
        try:
            doc = Document(io.BytesIO(docx_data))
            text_content = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_content.append(paragraph.text)
            
            return "\n".join(text_content) or f"[DOCX] {filename} - No text found"
            
        except Exception as e:
            logger.error(f"Error processing DOCX {filename}: {e}")
            return f"[DOCX] {filename} - Processing failed: {str(e)}"
    
    def _enhance_image_for_ocr(self, image: Image.Image) -> Image.Image:
        """
        Enhance image for better OCR results
        
        Args:
            image: PIL Image object
            
        Returns:
            Enhanced PIL Image object
        """
        try:
            # Convert to numpy array for OpenCV processing
            img_array = np.array(image)
            
            # Convert RGB to BGR for OpenCV
            if len(img_array.shape) == 3:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # Apply image preprocessing
            # 1. Convert to grayscale
            gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
            
            # 2. Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # 3. Apply adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            # 4. Morphological operations to clean up
            kernel = np.ones((1, 1), np.uint8)
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            # Convert back to PIL Image
            enhanced_image = Image.fromarray(cleaned)
            
            # Additional PIL enhancements
            # Increase contrast
            enhancer = ImageEnhance.Contrast(enhanced_image)
            enhanced_image = enhancer.enhance(1.5)
            
            # Increase sharpness
            enhancer = ImageEnhance.Sharpness(enhanced_image)
            enhanced_image = enhancer.enhance(2.0)
            
            return enhanced_image
            
        except Exception as e:
            logger.warning(f"Image enhancement failed: {e}")
            return image
    
    def _extract_text_from_image(self, image: Image.Image) -> str:
        """
        Extract text from image using multiple OCR methods
        
        Args:
            image: PIL Image object
            
        Returns:
            Extracted text
        """
        text_results = []
        
        # Method 1: Try EasyOCR first (usually more accurate)
        if self.easyocr_reader:
            try:
                # Convert PIL image to numpy array
                img_array = np.array(image)
                
                # EasyOCR expects RGB images
                if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
                
                results = self.easyocr_reader.readtext(img_array)
                text = " ".join([result[1] for result in results if result[2] > 0.5])
                if text.strip():
                    text_results.append(text)
            except Exception as e:
                logger.warning(f"EasyOCR failed: {e}")
        
        # Method 2: Try Tesseract as fallback
        try:
            # Convert to RGB for Tesseract
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Configure Tesseract for better medical text recognition
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,:;()[]{}%+-=<>/\\|"\'`~!@#$^&*_'
            text = pytesseract.image_to_string(image, config=custom_config)
            if text.strip():
                text_results.append(text)
        except Exception as e:
            logger.warning(f"Tesseract failed: {e}")
        
        # Return the best result (longest text)
        if text_results:
            return max(text_results, key=len)
        
        return ""
    
    def process_file(self, file_data: bytes, filename: str, content_type: str) -> str:
        """
        Main method to process any file type
        
        Args:
            file_data: Raw file bytes
            filename: Original filename
            content_type: MIME type of the file
            
        Returns:
            Extracted text content
        """
        try:
            # Determine file type and process accordingly
            if content_type.startswith('image/'):
                return self.process_image(file_data, filename)
            elif content_type == 'application/pdf':
                return self.process_pdf(file_data, filename)
            elif content_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                return self.process_docx(file_data, filename)
            elif content_type == 'text/plain':
                return file_data.decode('utf-8', errors='ignore')
            else:
                return f"[UNSUPPORTED] {filename} - File type not supported for processing"
                
        except Exception as e:
            logger.error(f"Error processing file {filename}: {e}")
            return f"[ERROR] {filename} - Processing failed: {str(e)}"

# Global instance
scanner_processor = EnhancedScannerProcessor()
