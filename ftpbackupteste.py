import os
from ftplib import FTP
from datetime import datetime
import time
import threading
from config import directory, ftpserver, username, password, max_file_retention_ftp_server, deleted_file_log
from check_file import get_large_files, get_newest_file, check_file_function, check_result_file
from progress_bar import simple_progress_bar, retrieve_parameters
from send_mail import send_mail_based_on_ftp_check

# @echo off
# "C:\Users\Administrador\AppData\Local\Programs\Python\Python312\python.exe" "C:\BackupFTP-PABX-Python\FTPBACKUP_02\FIX MODULAR IMPORT\ftpbackupteste.py"
# pause
#create batch file ftpbackupteste.bat and use task scheduler
#remember to change in bat file, where your python exe and python script is at

print("FTPBACKUPTESTE.PY")

# Get large files in config.directory
print("Get large files in config.directory")
large_files = get_large_files(directory)
print("Done large files in config.directory")
print("Large_files: ", large_files)
print("Directory: ", directory)

# Get the newest file
print("Get the newest file")
newest_large_file = get_newest_file(large_files)
print("Done the newest file")
print("newest_large_file: ", newest_large_file)

# Function to check if the file exists on FTP and compare names and file sizes
print("Get the ftp file check")
ftp_check_result = check_file_function(newest_large_file)
print("Done the ftp file check")
print("ftp_check_result: ", ftp_check_result)

if ftp_check_result != "skip_transfer":
    print("Get parameters for progress bar calc")
    total_iterations = retrieve_parameters()

#no error handling
def retry_upload_to_ftp(file_path, max_attempts=3, delay=5):
    attempt = 0
    while attempt < max_attempts:
        try:
            with FTP(ftpserver) as ftp:
                ftp.login(user=username, passwd=password)
                print("file_path inside retry_ftp: ", file_path)

                # Start the progress bar in a separate thread
                print("Call progress bar inside retry")
                progress_thread = threading.Thread(target=simple_progress_bar, args=(total_iterations,))
                progress_thread.start()
                print("FTP Start")
                with open(file_path, 'rb') as file:
                    ftp.storbinary(f'STOR {os.path.basename(file_path)}', file)
                    print("\nTask completed!")
                    progress_thread.join()

            return True
        except Exception as e:
            print("FTP Reattempting: ", attempt)
            print("FTP Error: ", e)
            attempt += 1
            if attempt < max_attempts:
                time.sleep(delay)  # Delay before the next attempt
            else:
                return False, str(e)


# Function to delete oldest files on FTP if more than 3 files exist
def delete_oldest_files():
    oldest_file = None
    try:
        with FTP(ftpserver) as ftp:
            ftp.login(user=username, passwd=password)
            ftp.cwd('/')  # Change to the appropriate config.directory
            files = ftp.nlst()
            files_info = [(f, ftp.sendcmd(f"MDTM {f}")) for f in files]
            files_info.sort(key=lambda x: x[1])
            if len(files_info) > max_file_retention_ftp_server: #default is three, so there won't be more than 03 files in the ftp server
                oldest_file = files_info[0][0]
                print("delete oldest file in ftp server: ",oldest_file)
                ftp.delete(oldest_file)
                with open(os.path.join(directory, deleted_file_log), 'a') as file:
                   file.write(oldest_file + '\n')
            else:
                print("Oldest file threshold not reached")
                oldest_file = 0
    except Exception as e:
        oldest_file = 1
        print("error deleting: ", e)
        pass  # Handle exception
    return oldest_file


# Try FTP transfer multiple times before failing
print("Call ftp retry")
#ftp_check_result = "skip_transfer"
validate_ftp_need_to_transfer = check_result_file(ftp_check_result)
print("validate_ftp_need_to_transfer: ", validate_ftp_need_to_transfer)
if validate_ftp_need_to_transfer == 2:
    ftp_attempt = retry_upload_to_ftp(ftp_check_result)
    send_mail_based_on_ftp_check(ftp_check_result)
else:
    send_mail_based_on_ftp_check(ftp_check_result)

print("Mail sent")

# Delete oldest files on FTP if more than 3 files exist
print("Delete old files in FTP server")
responseOldFile = delete_oldest_files()
if responseOldFile == 0:
    print("Nothing to delete yet in ftp server")
elif responseOldFile == 1:
    print("Error deleting old files in FTP server")
else:
    print("Done delete old files in FTP server")
# Call send_mail.send_mail_based_on_ftp_check with the obtained result
