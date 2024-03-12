#FTP Settings
ftpserver = '0.0.0.0'
#set your FTP IP or FQDN adress
username = 'ftpupsername'
password = 'ftppass'
max_file_retention_ftp_server = 3
min_file_size = 100 * 1024 * 1024 * 1024
#100GB min file size for transfer - change as you please

#local repository
directory = r'C:\source_folder'
deleted_file_log = "deleted_ftp_file_log.txt"

# Mail settings
mailserver = 'example.smtp.com.br'
#set your smtp mail server for mail notification
smtpport = 587
mailusername = 'soc@example.com.br'
#set your smtp mail server username
mailpassword = 'pass@#'
#set your smtp mail server password
source_mailaddress = 'soc@example.com.br'
#set your smtp mail server source mail address
dest_mailaddress = 'infraestrutura@example.com.br'
#set your receiving mail address
mailsubject_success = "Backup Python Application Completo Company"
mailsubject_failed = "Backup Python Application Failed  Company"
#set your subject for mail notification

#Filesize for speed test
file_path = 'testspeed.txt'
file_size_kb = 10
time_file_path = 'timespeed.txt'
