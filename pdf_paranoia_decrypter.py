'''PDF Paranoia

Using the os.walk() function from Chapter 10, write a script that will go through every PDF in a
folder (and its subfolders) and encrypt the PDFs using a password provided on the command line.
Save each encrypted PDF with an _encrypted.pdf suffix added to the original filename. Before
deleting the original file, have the program attempt to read and decrypt the file to ensure that it
was encrypted correctly.

Then, write a program that finds all encrypted PDFs in a folder (and its subfolders) and creates a
decrypted copy of the PDF using a provided password. If the password is incorrect, the program
should print a message to the user and continue to the next PDF.'''

# Module imports
import sys, os
from pypdf import PdfReader, PdfWriter
from pathlib import Path

# Test file path
pdf_folder = r'''C:\Users\Manka\Documents\Programming\Automate the Boring Stuff with Python\Chapter 15 - Working with PDF and Word documents\pdf_paranoia'''

# Crawls through folder and subfolders
for folder, subfolders, files in os.walk(pdf_folder):
    
    # Isolates pdfs in crawled folder
    for pdf in Path(folder).glob('*.pdf'):

        # Creates reader object
        with open(pdf, 'rb') as fhandle:
            reader = PdfReader(fhandle)

        # Ignores already encrypted files
        if reader.is_encrypted:
            try:
                reader.decrypt('hideokojima')
                writer = PdfWriter(clone_from=reader)
                file_name = pdf.stem
                file_name.replace('_encrypted', '_decrypted')
                with open(Path(folder) / f'{file_name}.pdf', 'wb') as fhandle:
                    writer.write(fhandle)
                    os.remove(pdf)
                    print(f'{pdf} SUCCESSFULLY DECRYPTED.\n')
            
            except:
                print(f'ERROR - {pdf} DECRYPTION FAILED.\nTry different password.\n')


        # Encrypts and saves pdf file.
        else:
            print(f'{pdf}\nis already decrypted.\n')
            continue