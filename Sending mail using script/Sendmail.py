import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, message, from_email, password, to_emails):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ', '.join(to_emails)
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, to_emails, msg.as_string())
    server.quit()

# Email configuration
your_email = 'your_email@gmail.com'  # Replace with your email address
your_password = 'your_password'  # Replace with your email password
to_emails = ['recipient1@example.com', 'recipient2@example.com']  # Replace with recipient email addresses

# Email content
email_subject = 'Subject of the email'
email_message = 'Body of the email'

# Send email
send_email(email_subject, email_message, your_email, your_password, to_emails)
