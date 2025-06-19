from cryptography.fernet import Fernet
import os


def encryptedMethod():
    file_name ="secret.key"
    file_exists = os.path.isfile("secret.key")
    csv_file_name = "student_data.csv"

    if not file_exists:
        key = Fernet.generate_key() # Generate a new key

        
        # Save the key to a file so you can use it later
        with open(file_name,"wb") as key_file:
            key_file.write(key)


    # Load the key from the file
    with open(file_name,"rb") as key_file:
        key = key_file.read()

    # Create a Fernet object with the key
    fernet = Fernet(key)

    # Read the CSV file as bytes
    with open(csv_file_name,"rb") as csv_file:
        original = csv_file.read()

    # Encrypt the file content
    encripted = fernet.encrypt(original)

    # Save the encrypted data to a new file
    with open("student_data.csv","wb") as encrypted_data_file:
        encrypted_data_file.write(encripted)


# encryptedMethod()
