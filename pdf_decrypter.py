'''pdf_decrypter.py'''

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
    
    # Explains command line usage to user.
    else:
        print("\nERROR - INSUFFICIENT COMMAND LINE ARGUMENTS")
        print("\nARG 1: File path to crawl for PDF's to decrypt")
        print("ARG 2: Password to decrypt PDF's with (INCLUDES SPACES)")
        quit()

# User prompt for folder path and password.
else:
    pdf_folder = Path(input("File path to crawl for PDF's to decrypt:\n")).resolve()
    password = input('\nEnter a decryption password: ')

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

            # Attempts decryption of encrypted pdf file.
            reader = PdfReader(fhandle)
            if reader.is_encrypted:
                try:
                    reader.decrypt(password)
                    writer = PdfWriter(clone_from=reader)
                except errors.FileNotDecryptedError:
                    print(f'\nERROR - {pdf} DECRYPTION FAILED! WRONG PASSWORD!')
                    continue

            # Skips file if already decrypted.
            else:
                print(f'\nERROR - {pdf} ALREADY DECRYPTED!')
                continue            
        
        # Adds _decrypted tag to filename.
        filename = pdf.stem
        if filename.endswith('_encrypted'): filename = filename.replace('_encrypted', '_decrypted')
        else: filename += '_decrypted'

        # Replaces original file with decrypted copy
        with open(Path(f'./{filename}.pdf'), 'wb') as fhandle:
            print(f'\nDecrypting {pdf}...')
            writer.write(fhandle)
            os.remove(Path(pdf))

print(f'\nPDF decryption finished!')