from cryptography.fernet import Fernet
import os 

def decryptMethod():
    key_file_name = "secret.key"
    encrypt_data_file_name = "student_data.csv"
    file_exists = os.path.isfile(key_file_name)

    if not file_exists:
        raise Exception("key file not exists")

    with open(key_file_name,"rb") as key_file:
        key = key_file.read()

    fernet = Fernet(key)

    with open(encrypt_data_file_name,"rb") as encrypt_file:
        encrypted_data = encrypt_file.read()

    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    

    except Exception as e:
        print("error during decryption :", e)
        exit()
    
    with open(encrypt_data_file_name, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)
    # return decrypted_data

# decryptMethod()