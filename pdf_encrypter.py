'''pdf_encrypter.py'''

import os, sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter
os.chdir(Path(sys.argv[0]).parent) # Changes directory to script location.

# TODO: Implement command line functionality (make it optional this time).
# TODO: Deal with errors when files are already encrypted.

# Prompts user for directory to be crawled.
while True:
    pdf_folder = Path(input("Folder path where PDF's are to be encrypted:\n"))
    if pdf_folder.is_dir():
        os.chdir(pdf_folder)
        break
    else:
        print('\nERROR - Invalid directory path.\n')

# User prompt for decryption password.
while True:
    password = input('\nEnter an encryption password: ')
    confirm_pass = input('\nPlease confirm the password: ')
    
    if confirm_pass == password:
        break
    
    else:
        print("\nERROR - Password's don't match. Try again.")

# Crawls through directory
for folder, subfolders, files in os.walk(pdf_folder):
    
    # Crawls through pdf files
    for pdf in Path(folder).glob('*.pdf'):
        
        # Creates writer and encrypts pdf.
        with open(Path(pdf), 'rb') as fhandle: 
            reader = PdfReader(fhandle)
            writer = PdfWriter(clone_from=reader)
            writer.encrypt(password)

        # Remove _decrypted tag line from filename.
        filename = pdf.stem
        if pdf.stem.endswith('_decrypted'):
            filename = pdf.stem.replace('_decrypted', '_encrypted')

        # Replaces original file with encrypted copy.
        with open(Path(f'./{filename}.pdf'), 'wb') as fhandle:
            print(f'\nEncrypting {pdf}...')
            writer.write(fhandle)
            os.remove(Path(pdf))

print('PDF encryption successful!')