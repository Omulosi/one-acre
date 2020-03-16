import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_mail(from_email, to_emails, subject, content):
    print(os.environ.get('SENDGRID_API_KEY'))
    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=content)

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code, response.body, response.headers)

if __name__ == '__main__':
    send_mail('one-acre@example.com', 'mulongojohnpaul@gmail.com', 'Sign Up',
            'successfully signed up!')
