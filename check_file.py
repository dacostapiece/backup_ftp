import os
from ftplib import FTP
from config import directory, ftpserver, username, password, min_file_size
from rearrange import rename_ftp_filename, remove_tmp_extension_ftp, retrieve_list_ftp_server

print("CHECK_FILE.PY")

# Function to get files larger than 10GB in a config.directory
def get_large_files(directory):
    print("function get_large_files")
    large_files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.getsize(filepath) > min_file_size:  # Check if file is > 10MB
                large_files.append(filepath)
    return large_files

# Function to get the newest file in a config.directory
def get_newest_file(file_paths):
    print("function get_newest_file")
    if file_paths:
        # Sort by modification time to get the newest file
        file_paths.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return file_paths[0]
    return None

# Function to check if the file exists on FTP and compare names and file sizes
def check_file_function(file_path):
    with FTP(ftpserver) as ftp:
        ftp.login(user=username, passwd=password)
        ftp.cwd('/')
        files = ftp.nlst()
        files.sort(key=lambda x: ftp.voidcmd(f"MDTM {x}")[4:], reverse=True)  # Sort files by modification time

        local_file_name = os.path.basename(file_path)
        print("local_file_name: ", local_file_name)
        local_file_size = os.path.getsize(file_path)
        print("local_file_size: ", local_file_size)

        #Function local_file_size.txt with the local_file_size information for timespeed and progress files
        def Write_file_size(local_file_size):
            print("Write file size: ", local_file_size)
            with open('local_file_size.txt', 'w') as size_file:
                size_file.write(str(local_file_size))

        print("ftp files: ", files)

        for file_ftp in files:
            if local_file_name == file_ftp:
                # Get file size on FTP
                print("Same file name in ftp server")
                print("file_ftp: ", file_ftp)
                try:
                    ftp_file_size = ftp.size(file_ftp)
                except Exception as e:
                    print(f"Error getting file size on FTP: {e}")
                    continue

                if local_file_size == ftp_file_size:
                    print("Same file size in ftp server")
                    print("file_ftp: ", file_ftp)
                    # Same filename and file size, skip FTP transfer
                    return "skip_transfer"
                else:
                    # Different file sizes, find the next available suffix
                    print("loop: ", files.index(file_ftp))
                    print("file_ftp: ", file_ftp)
                    
                    #RETRIEVE FTP FILE LIST
                    retrieve_list = retrieve_list_ftp_server()
                    print("retrieve_list ftp: ", retrieve_list)

                    #RENAME FUNCTION
                    renamed_ftp_list = rename_ftp_filename(retrieve_list)
                    #new_file_name = rename_ftp_filename(files)
                    print("renamed_ftp_list: ", renamed_ftp_list)

                    #RENAME FUNCTION 2
                    remove_tmp = remove_tmp_extension_ftp(renamed_ftp_list)
                    print("remove_tmp: ", remove_tmp)

                    #Create local_file_size.txt with the local_file_size information for timespeed and progress files
                    print("file name to write: ", file_ftp)
                    print("file size  to write: ", local_file_size)
                    Write_file_size(local_file_size)
                    
                    # Restart FTP checking for new file transfers
                    #return check_file_function(file_path)
                    #return file_ftp
            else:
                print("FTP Server file name NOT equal to local file name: ",file_ftp)
        
        #Create local_file_size.txt with the local_file_size information for timespeed and progress files
        print("different name local and FTP")
        print("file name to write: ", local_file_name)
        print("file size  to write: ", local_file_size)
        Write_file_size(local_file_size)

                
    return file_path  # No matching file found

print("whole check filed runned")

# #TESTE ISOLATED FILE
# sample_file_path = r'F:\teste\teste.zip'
# print("start sample_file_path")

# file_to_copy = check_file_function(sample_file_path)
# print("file to copy: ", file_to_copy)

#file should be transfer? 0 = no, 1 = no with error code, 2 = yes
def check_result_file(result_file):
    if result_file == "skip_transfer":
        exit_code = 0
        return exit_code
    elif isinstance(result_file, bool):
        exit_code = 1
        error_code = result_file[0]
        return exit_code, error_code
    else:
        exit_code = 2
        return exit_code
    
# def rename_ftp_filename(files, file_ftp):
#     base_name, extension = os.path.splitext(file_ftp)
#     suffix = 1
#     while True:
#         new_file_name = f"{base_name}.{suffix}{extension}"
#         if new_file_name not in files:
#             break
#         suffix += 1

#     print("files: ", files)
#     print("file_ftp: ", file_ftp)
#     print("new_file_name: ", new_file_name)

#     return new_file_name
