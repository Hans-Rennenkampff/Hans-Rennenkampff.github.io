import imaplib
import email
import os

# Connect to your email account
mail_pass = "zsmjvcufsboisjvk"
username = "rsk-rasp@yandex.com"
imap_server = "imap.yandex.com"
imap = imaplib.IMAP4_SSL(imap_server)
imap.login(username, mail_pass)


# Select the inbox
imap.select("inbox")

# Search for messages with an attachment ending in ".xlsx"
status, messages = imap.search(None, 'ALL')
messages = messages[0].split(b' ')
for email_id in messages:
    status, msg = imap.fetch(email_id, "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                file_name = part.get_filename()
                if not file_name.endswith(".xlsx"):
                    continue

                # Download the attachment as "raspisanie.xlsx"
                os.chdir(r".\resourses\xl")
                open("raspisanie.xlsx", "wb").write(part.get_payload(decode=True))

# Close the connection to your email account
imap.close()
imap.logout()
