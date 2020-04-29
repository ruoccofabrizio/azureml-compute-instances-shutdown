import datetime
import logging
import os

import azure.functions as func
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Send an email to avoid compute instance shutdown for a the current day
def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    # using SendGrid's Python Library
    # https://github.com/sendgrid/sendgrid-python
    
    message = Mail(
        from_email  = os.environ["from_email"],
        to_emails   = os.environ["to_emails"],
        subject     = os.environ["subject"] + os.environ["aml_compute_instance"],
        html_content= f'<a href="{os.environ["func_cancel_shutdown"]}?aml_compute_instance={os.environ["aml_compute_instance"]}">Click here to cancel Compute Instance shutdown</a>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


