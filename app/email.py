import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import current_app, render_template


def send_mail(to_emails, subject, template, **kwargs):
    app = current_app._get_current_object()
    message = Mail(from_email=app.config['APP_MAIL_SENDER'],
                   to_emails=to_emails,
                   subject=subject,
                   html_content=render_template(template + '.html', **kwargs))

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code, response.body, response.headers)
