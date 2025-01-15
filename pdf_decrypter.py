'''pdf_decrypter.py'''

import os, sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter, errors
os.chdir(Path(sys.argv[0]).parent) # Changes directory to script location.

# TODO: Implement command line functionality (make it optional this time).

# Prompts user for directory to be crawled.
while True:
    pdf_folder = Path(input("Folder path where PDF's are to be decrypted:\n")).resolve()
    if pdf_folder.is_dir():
        os.chdir(pdf_folder)
        break
    else:
        print('\nERROR - INVALID DIRECTORY PATH!\n')

# User prompt for decryption password.
while True:
    password = input('\nEnter a decryption password: ')
    confirm_pass = input('\nPlease confirm the password: ')
    
    if confirm_pass == password:
        break
    
    else:
        print("\nERROR - PASSWORDS DO NOT MATCH!")

# Crawls through directory
for folder, subfolders, files in os.walk(pdf_folder):
    
    # Crawls through pdf files
    for pdf in Path(folder).glob('*.pdf'):

        # Decryptes pdf and creates writer.
        with open(Path(pdf), 'rb') as fhandle:
            reader = PdfReader(fhandle)

            # Checks file is encrypted and decrypts.
            if reader.is_encrypted:
                
                # Checks decryption password is correct.
                try:
                    reader.decrypt(password)
                    writer = PdfWriter(clone_from=reader)
                except errors.FileNotDecryptedError:
                    print(f'\nERROR - {pdf} DECRYPTION FAILED! WRONG PASSWORD!')
                    continue
            else:
                print(f'\nERROR - {pdf} ALREADY DECRYPTED!')
                continue            
        
        # Adds _decrypted tag to filename.
        filename = pdf.stem

        # Replaces tag created by pdf_encrypter.py.
        if filename.endswith('_encrypted'):
            filename = filename.replace('_encrypted', '_decrypted')
        else:
            filename += '_decrypted'

        # Replaces original file with decrypted copy
        with open(Path(f'./{filename}.pdf'), 'wb') as fhandle:
            print(f'\nDecrypting {pdf}...')
            writer.write(fhandle)
            os.remove(Path(pdf))

print(f'\nPDF decryption finished!')