import dns.resolver
import socket
import smtplib
import re

# Set of allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'csv'}


# Extract all email addresses from a string with a regular expression
def extract_emails_from_text(text):
    emails = re.findall(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", text)
    return emails


# Extract file extension from file and return boolean that indicates whether or not the extension is allowed or not
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Extract and validate emails from a string
def process_data(text, file_extension):
    if file_extension == 'txt' or file_extension == 'csv':
        emails_with_valid_format = extract_emails_from_text(text)
        verified_emails = verify_list_of_emails(emails_with_valid_format)
    else:
        verified_emails = 'Text and CSV Files only!'
        emails_with_valid_format = ''
    return verified_emails, emails_with_valid_format


# Check if email address has an mx record
def check_mx_record(email):
    domain = email.split('@')[1]
    try:
        dns.resolver.query(domain, 'MX')
        return True
    except dns.resolver.NXDOMAIN:
        return False


# Check if mail server of an email address responds
def check_mail_server(email):
    domain = email.split('@')[1]

    # get the MX record for the domain
    records = dns.resolver.query(domain, 'MX')
    mx_record = records[0].exchange
    mx_record = str(mx_record)

    host = socket.gethostname()
    server = smtplib.SMTP()

    # SMTP Conversation
    server.connect(mx_record)
    server.helo(host)
    server.mail(email)

    try:
        code, message = server.rcpt(str(email))
    except smtplib.SMTPServerDisconnected:
        return False

    server.quit()

    # Assume 250 as Success
    if code == 250:
        return True
    else:
        return False


# Input a list of email addresses and return a list of emails with mx records and responding mail servers
def verify_list_of_emails(emails):
    verified_emails = []
    for email in emails:
        if check_mx_record(email) and check_mail_server(email):
            verified_emails.append(email)
    return verified_emails
