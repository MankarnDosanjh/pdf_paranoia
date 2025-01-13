'''pdf_encrypter.py'''

import os, sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter, errors
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
        print('\nERROR - INVALID DIRECTORY PATH.\n')

# User prompt for decryption password.
while True:
    password = input('\nEnter an encryption password: ')
    confirm_pass = input('\nPlease confirm the password: ')
    
    if confirm_pass == password:
        break
    
    else:
        print("\nERROR - PASSWORDS DO NOT MATCH!")

# Crawls through directory
for folder, subfolders, files in os.walk(pdf_folder):
    
    # Crawls through pdf files
    for pdf in Path(folder).glob('*.pdf'):
        
        # Creates writer and encrypts pdf.
        with open(Path(pdf), 'rb') as fhandle: 
            
            # Checks if file is already encrypted.
            try:
                reader = PdfReader(fhandle)
                writer = PdfWriter(clone_from=reader)
                writer.encrypt(password)
            except errors.FileNotDecryptedError:
                print(f'\nERROR - {pdf} ALREADY ENCRYPTED!')
                continue

        # Adds _encrypted tag line to filename.
        filename = pdf.stem

        # Replaces tag created by pdf_decrypter.py.
        if filename.endswith('_decrypted'):
            filename = filename.replace('_decrypted', '_encrypted')
        else:
            filename += '_encrypted'

        # Replaces original file with encrypted copy.
        with open(Path(f'./{filename}.pdf'), 'wb') as fhandle:
            print(f'\nEncrypting {pdf}...')
            writer.write(fhandle)
            os.remove(Path(pdf))
        
print('\nPDF encryption finished!')