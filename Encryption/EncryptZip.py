import pyzipper
import os

def encrypt_zip(file_path, output_zip, password):
    if not os.path.exists(file_path):
        print(f"Error: File or directory '{file_path}' not found.")
        return

    with pyzipper.AESZipFile(output_zip,
                              'w',
                              compression=pyzipper.ZIP_DEFLATED,
                              encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(password.encode('utf-8'))
        zf.setencryption(pyzipper.WZ_AES, nbits=256)

        if os.path.isfile(file_path):
            zf.write(file_path, arcname=os.path.basename(file_path))
                    
    print(f"Encrypted ZIP created: {output_zip}")

# Example usage
encrypt_zip('ZIPFILE.zip', 'encrypted_FILE.zip', 'YOUR_PASSWORD_HERE')
