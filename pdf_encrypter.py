'''pdf_encrypter.py'''

# Module imports.
import os, sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter, errors

# Changes directory to script location.
os.chdir(Path(sys.argv[0]).parent)

# Optional command line functionality.
if len(sys.argv) > 1:

    # Stores folder and password from command line arguments
    if len(sys.argv) >= 3:
        pdf_folder = Path(sys.argv[1]).resolve()
        password = " ".join(sys.argv[2:])
    
    # Explains command line usage to user if insufficient arguments provided.
    else:
        print("\nERROR - INSUFFICIENT COMMAND LINE ARGUMENTS")
        print("\nARG 1: File path to crawl for PDF's to encrypt")
        print("ARG 2: Password to encrypt PDF's with (INCLUDES SPACES)")
        quit()

# User prompt for folder path and password.
else:
    pdf_folder = Path(input("File path to crawl for PDF's to encrypt:\n")).resolve()
    password = input('\nEnter an encryption password: ')
    
# Validates that path is a directory.
if pdf_folder.is_dir():
    os.chdir(pdf_folder)
else:
    print('\nERROR - INVALID DIRECTORY PATH.\n')
    quit()

# Crawls through pdf files in directory.
for folder, subfolders, files in os.walk(pdf_folder):
    for pdf in Path(folder).glob('*.pdf'):
        with open(Path(pdf), 'rb') as fhandle:
            
            # Checks if file is already encrypted.  
            try:
                reader = PdfReader(fhandle)
                writer = PdfWriter(clone_from=reader)
                writer.encrypt(password)
            except errors.FileNotDecryptedError:
                print(f'\nERROR - {pdf} ALREADY ENCRYPTED!')
                continue
        
        # Adds _encrypted tag to filename.
        filename = pdf.stem
        if filename.endswith('_decrypted'): filename = filename.replace('_decrypted', '_encrypted')
        else: filename += '_encrypted'

        # Replaces original file with encrypted copy.
        with open(Path(f'./{filename}.pdf'), 'wb') as fhandle:
            print(f'\nEncrypting {pdf}...')
            writer.write(fhandle)
            os.remove(Path(pdf))
        
print('\nPDF encryption finished!')