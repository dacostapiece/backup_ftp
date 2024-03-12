import os
from ftplib import FTP
from config import directory, ftpserver, username, password

# Function to retrieve list files from FTP SERVER
def retrieve_list_ftp_server():
    with FTP(ftpserver) as ftp:
        ftp.login(user=username, passwd=password)
        ftp.cwd('/')
        files = ftp.nlst()
        print("files ftp list - rearrange.py: ", files)
    return files

def rename_ftp_filename(test_ftp_files):
    # Connect to the FTP server
    with FTP(ftpserver, username, password) as ftp:
        # Create a tuple for each element with its ASCII sum value
        print("test_ftp_files - rearrange.py: ", test_ftp_files)

        tuple_list = [(s, sum(ord(char) for char in s)) for s in test_ftp_files]
        print("tuple_list - rearrange.py: ", tuple_list)


        # Sort the list of tuples based on ASCII sum values
        sorted_tuple_list = sorted(tuple_list, key=lambda x: x[1])
        print("sorted_tuple_list - rearrange.py: ", sorted_tuple_list)

        ftp_files = [tup[0] for tup in sorted_tuple_list]
        print("ftp_files - rearrange.py: ", ftp_files)
        new_ftp_files = list(ftp_files)

        tmpextension = ".tmp"
        suffix = 1

        for i in range(len(ftp_files)):
            base_name, extension = os.path.splitext(ftp_files[i])
            partes = ftp_files[i].split('.')
            print("partes - rearrange.py: ", partes)

            if len(partes) <= 2:
                new_ftp_files[i] = f"{base_name}.{suffix}{extension}{tmpextension}"
                print("IF new_ftp_files - rearrange.py: ", new_ftp_files[i])
                old_file_name = ftp_files[i]
                print("IF old_file_name[i] - rearrange.py: ", old_file_name)
                new_file_name = new_ftp_files[i]
                print("IF new_file_name[i] - rearrange.py: ", new_file_name)
                print(f"Change file name on FTP server: {old_file_name} -> {new_file_name}")
                ftp.rename(old_file_name, new_file_name)
                suffix += 1
            else:
                new_ftp_files[i] = f"{base_name}{extension}{tmpextension}"
                print("ELSE new_ftp_files - rearrange.py: ", new_ftp_files[i])
                partes2 = new_ftp_files[i].split('.')
                number_suffix = partes2[1]
                new_ftp_files[i] = new_ftp_files[i].replace(number_suffix, str(int(number_suffix) + 1))
                print("ELSE EDITED new_ftp_files - rearrange.py: ", new_ftp_files[i])
                suffix += 1

                # Rename the files on FTP server
                old_file_name = ftp_files[i]
                print("old_file_name[i] - rearrange.py: ", old_file_name)
                new_file_name = new_ftp_files[i]
                print("new_file_name[i] - rearrange.py: ", new_file_name)
                print(f"Change file name on FTP server: {old_file_name} -> {new_file_name}")
                ftp.rename(old_file_name, new_file_name)

    return new_ftp_files


# new_list = rename_ftp_filename(test_ftp_files)
# #print("")
# print("RECAP starting ftp_files: ", test_ftp_files)

# print("finishing ftp_files: ", new_list)

def remove_tmp_extension_ftp(file_list):
    # Connect to the FTP server
    with FTP(ftpserver, username, password) as ftp:
        for i in range(len(file_list)):
            old_file_name = file_list[i]
            print("REMOVE TMP old_file_name - rearrange.py: ", old_file_name)
            new_file_name = old_file_name.replace(".tmp", "")
            print("REMOVE TMP new_file_name - rearrange.py: ", new_file_name)
            
            # Rename the files on FTP server
            print(f"Removing '.tmp' extension on FTP server: {old_file_name} -> {new_file_name}")
            ftp.rename(old_file_name, new_file_name)

            # Update the file list with the new names
            file_list[i] = new_file_name
            print("REMOVE TMP file_list[i] - rearrange.py: ", file_list[i])

    return file_list
