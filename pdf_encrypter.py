'''pdf_encrypter.py'''

import os, sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter

# TODO: Implement command line functionality (make it optional this time).
# TODO: Allow user to specify encryption/decryption password.
# TODO: Allow user to specify file path to be crawled.

# Test file path
pdf_folder = Path(r'C:\Users\Manka\Documents\Programming\Automate the Boring Stuff with Python\Chapter 15 - Working with PDF and Word documents\pdf_paranoia\PDF files')
os.chdir(pdf_folder)

# Crawls through directory
for folder, subfolders, files in os.walk(pdf_folder):
    
    # Crawls through pdf files
    for pdf in Path(folder).glob('*.pdf'):
        
        # Creates writer and encrypts pdf.
        with open(Path(pdf), 'rb') as fhandle: 
            reader = PdfReader(fhandle)
            writer = PdfWriter(clone_from=reader)
            writer.encrypt('a')

        # Remove _decrypted tag line from filename.
        filename = pdf.stem
        if pdf.stem.endswith('_decrypted'):
            filename = pdf.stem.replace('_decrypted', '_encrypted')

        # Replaces original file with encrypted copy.
        with open(Path(f'./{filename}.pdf'), 'wb') as fhandle:
            writer.write(fhandle)
            os.remove(Path(pdf))