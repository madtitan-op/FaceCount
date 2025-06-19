import requests

# === Configuration ===
BASE_URL = "http://localhost:8080"
UPLOAD_ENDPOINT = "/api/encodings/upload"
DOWNLOAD_ENDPOINT = "/api/encodings/download-encrypted"
FILE_PATH = "student_data_copy.csv"  # Your encrypted CSV file path
DOWNLOAD_DEST = "student_data_copy.csv"
JWT_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMDMiLCJpYXQiOjE3NDk2MzAxMDksImV4cCI6MTc0OTY0ODEwOX0.JrEX7fn9QyWXSm6UxFuw5f1W5N4Az5XtQ3-uuxx2h7k"  # Replace with a valid JWT

# === Headers ===
headers = {
    "Authorization": f"Bearer {JWT_TOKEN}"
}

# === 1. Upload Encrypted File ===
def upload_file():
    with open(FILE_PATH, 'rb') as f:
        files = {'file': (FILE_PATH, f)}
        response = requests.post(BASE_URL + UPLOAD_ENDPOINT, files=files, headers=headers)
        print(f"[UPLOAD] Status Code: {response.status_code}")
        print(f"[UPLOAD] Response: {response.text}")

# === 2. Download Encrypted File ===
def download_file():
    response = requests.get(BASE_URL + DOWNLOAD_ENDPOINT, headers=headers)
    print(f"[DOWNLOAD] Status Code: {response.status_code}")
    
    if response.status_code == 200:
        with open(DOWNLOAD_DEST, 'wb') as f:
            f.write(response.content)
        print(f"[DOWNLOAD] File saved to: {DOWNLOAD_DEST}")
    else:
        print(f"[DOWNLOAD] Error: {response.text}")

# === Run both ===
upload_file()
# download_file()
