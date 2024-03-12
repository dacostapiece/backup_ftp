from ftplib import FTP
import time
import os
from config import ftpserver, username, password, file_path, file_size_kb, time_file_path

print("timespeedy script ")


def create_test_file(file_path, size_kb):
    with open(file_path, 'wb') as f:
        f.write(b'0' * size_kb * 1024)

def upload_file_ftp(file_path, ftp_server, username, password):
    with FTP(ftp_server) as ftp:
        ftp.login(user=username, passwd=password)
        with open(file_path, 'rb') as file:
            start_time = time.time()
            ftp.storbinary('STOR testspeed.txt', file)
            end_time = time.time()
        ftp.delete('testspeed.txt')  # Delete the file from the FTP server
    return end_time - start_time

def write_upload_time_to_file(file_path, upload_time):
    with open(file_path, 'w') as f:
        f.write(str(upload_time))

print("timespeedy create file: ", file_path)
print("timespeedy create file size: ", file_size_kb)
create_test_file(file_path, file_size_kb)

print("timespeedy upload test file: ", file_path)
upload_time = upload_file_ftp(file_path, ftpserver, username, password)

print(f"File uploaded in {upload_time:.2f} seconds")

print("timespeedy write test file: ", time_file_path)    
write_upload_time_to_file(time_file_path, upload_time)

print("timespeedy local delete file: ", file_path)
os.remove(file_path)  # Remove the local file after uploading
