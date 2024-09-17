import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from create_msg import create_msg_html


# Function to send an email with the API data
def send_email(recipient_emails):
    sender_email = "jobsearchtest2@outlook.com"
    sender_password = "noodleMayo"
    smtp_server = "smtp-mail.outlook.com"
    smtp_port = 587

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipient_emails)  # Send to multiple recipients
    msg['Subject'] = "API Data Collected"

    # Convert API data (JSON) to a formatted string

    # HTML version
    html_body = create_msg_html()
    msg.attach(MIMEText(html_body, 'html'))

    try:
        # Connect to the server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_emails, msg.as_string())
        server.quit()

        print(f"Email sent successfully to: {', '.join(recipient_emails)}")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Function to load email addresses from emails.txt
def load_emails_from_file():
    if os.path.exists('emails.txt'):
        with open('emails.txt', 'r') as f:
            emails = f.read().splitlines()
        return emails
    else:
        return []


# Function to add a new email to emails.txt
def add_email_to_file(new_email):
    with open('emails.txt', 'a') as f:
        f.write(new_email + '\n')
    print(f"Added {new_email} to emails.txt")
