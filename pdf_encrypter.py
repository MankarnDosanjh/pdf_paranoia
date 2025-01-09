'''pdf_encrypter.py'''

import os, sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter


# Test file path
pdf_folder = Path(r'C:\Users\Manka\Documents\Programming\Automate the Boring Stuff with Python\Chapter 15 - Working with PDF and Word documents\pdf_paranoia\PDF files')
os.chdir(pdf_folder)

# Crawls through directory
for folder, subfolders, files in os.walk(pdf_folder):
    
    # Crawls through pdf files
    for pdf in Path(folder).glob('*.pdf'):
        
        # Creates reader object
        with open(Path(pdf), 'rb') as fhandle: 
            reader = PdfReader(fhandle)
            writer = PdfWriter(clone_from=reader)
            writer.encrypt('a')

        with open(Path(f'./{pdf.stem}_encrypted.pdf'), 'wb') as fhandle:
            writer.write(fhandle)
            os.remove(Path(pdf))