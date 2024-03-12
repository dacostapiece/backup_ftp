import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from config import mailserver, mailusername, mailpassword, source_mailaddress, dest_mailaddress, mailsubject_success, mailsubject_failed, smtpport , ftpserver

# Function to format file size in human-readable format
def format_size(size):
    if size > 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024 * 1024):.2f} GB"
    elif size > 1024 * 1024:
        return f"{size / (1024 * 1024):.2f} MB"
    elif size > 1024:
        return f"{size / 1024:.2f} KB"
    else:
        return f"{size} bytes"

# send_mail.py
def send_mail_based_on_ftp_check(ftp_check_result):
    if ftp_check_result == "skip_transfer":
        # Email if FTP transfer is unnecessary
        print("Email if FTP transfer is unnecessary")
        mail_result = unnecessary_transfer_mail()
    elif ftp_check_result == False:
        # Email if FTP transfer failed after retries
        print("Email if FTP transfer is failed")
        mail_result = failed_transfer_mail(
        source_mailaddress, dest_mailaddress, mailsubject_failed, ftp_check_result
        )
    else:
# FTP operations with retries
        # Email if FTP transfer successful
        print("Email if FTP transfer is necessary")
        mail_result = necessary_transfer_mail(
            source_mailaddress, dest_mailaddress, mailsubject_success, ftp_check_result
        )
        print("tp_check_result: ", ftp_check_result)
        #print("mail_result: ", mail_result)

    #return mail_result

#UNNECESSARY TRANSFER FILE - SEND MAIL
def unnecessary_transfer_mail():
    # Create email message
    msg = MIMEMultipart()
    msg['From'] = source_mailaddress
    msg['To'] = dest_mailaddress
    msg['Subject'] = "Backup Python 3CX Unnecessary Altermedios"

    # Compose email body
    body = "FTP transfer canceled: File with the same name and size already exists on the FTP server.\n"

    # Attach body to the email
    msg.attach(MIMEText(body, 'plain'))

    print("Unnecessary mail content:")
    print("From: ", source_mailaddress)
    print("To: ", dest_mailaddress)
    print("Subject: ", msg)

    # Send email
    with smtplib.SMTP(mailserver, smtpport) as server:
        server.starttls()
        server.login(mailusername, mailpassword)
        server.sendmail(source_mailaddress, dest_mailaddress, msg.as_string())

#NECESSARY TRANSFER FILE - SEND MAIL
def necessary_transfer_mail(source_mailaddress, dest_mailaddress, mailsubject, ftp_check_result):
    msg = MIMEMultipart()
    msg['From'] = source_mailaddress
    msg['To'] = dest_mailaddress
    msg['Subject'] = mailsubject

    # Calculate the size difference and format it
    size_difference = os.path.getsize(ftp_check_result)
    readable_size = format_size(size_difference)

    body = f"Source full path: {ftp_check_result}\n"
    readable_size = format_size(size_difference)
    body += f"Source file name with size: {readable_size}\n"
    body += f"\n"
    body += f"Destination full path on FTP server: ftp://{ftpserver}/{os.path.basename(ftp_check_result)}\n"

    msg.attach(MIMEText(body, 'plain'))
    print("Necessary mail content:")
    print("From: ", source_mailaddress)
    print("To: ", dest_mailaddress)
    print("Subject: ", mailsubject)
    print("ftp_check_result: ", ftp_check_result)

    with smtplib.SMTP(mailserver, smtpport) as server:
        server.starttls()
        server.login(mailusername, mailpassword)
        server.sendmail(source_mailaddress, dest_mailaddress, msg.as_string())

#FAILED TRANSFER FILE - SEND MAIL
def failed_transfer_mail(source_mailaddress, dest_mailaddress, mailsubject, ftp_check_result):
    msg = MIMEMultipart()
    msg['From'] = source_mailaddress
    msg['To'] = dest_mailaddress
    msg['Subject'] = mailsubject

    body = f"FTP error code: {ftp_check_result}\n"
    msg.attach(MIMEText(body, 'plain'))

    print("Failed mail content:")
    print("From: ", source_mailaddress)
    print("To: ", dest_mailaddress)
    print("Subject: ", mailsubject)
    print("ftp_check_result: ", ftp_check_result)


    with smtplib.SMTP(mailserver, smtpport) as server:
        server.starttls()
        server.login(mailusername, mailpassword)
        server.sendmail(source_mailaddress, dest_mailaddress, msg.as_string())
