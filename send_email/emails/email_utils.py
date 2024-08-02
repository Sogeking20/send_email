# email_utils.py
import imaplib
import email
from email.header import decode_header
from datetime import datetime
from .models import EmailMessage, EmailAccount

def fetch_emails(account):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(account.email, account.password)
    mail.select("inbox")

    result, data = mail.search(None, "ALL")
    email_ids = data[0].split()
    
    messages = []

    for email_id in email_ids:
        result, msg_data = mail.fetch(email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        sent_date = email.utils.parsedate_to_datetime(msg["Date"])
        
        body = ""
        attachments = []

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_maintype() == "multipart":
                    continue
                if part.get("Content-Disposition") is None:
                    continue
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                else:
                    attachment = part.get_filename()
                    if attachment:
                        attachments.append(attachment)
        else:
            body = msg.get_payload(decode=True).decode()
        
        email_message = EmailMessage(
            subject=subject,
            sent_date=sent_date,
            received_date=sent_date,
            body=body,
            attachments=attachments,
        )
        email_message.save()
        messages.append(email_message)
    
    mail.logout()
    return messages
