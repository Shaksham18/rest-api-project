
import os
from flask.cli import load_dotenv
import jinja2
import requests

load_dotenv()
template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader)

def render_template(tempate_filename, **context):
    return template_env.get_template(tempate_filename).render(**context)

def send_simple_message(to, subject, text, html):
    domain = os.getenv('MAILGUN_DOMAIN', '')
    return requests.post(
            f"https://api.mailgun.net/v3/{domain}/messages",
            auth=("api", os.getenv('API_KEY', 'API_KEY')),
            data={"from": f"Mailgun Sandbox <postmaster@{domain}>",
                "to": [to],
                "subject": subject,
                "text": text,
                "html":html
            })

def send_user_registration_email(username, email):
    subject = "Welcome to StoreAPI!"
    text = f"Hello {username}, thank you for registering at StoreAPI."
    html = render_template("email/action.html", username=username)

    return send_simple_message(
        to=email, 
        subject=subject, 
        text=text, 
        html=html
    )