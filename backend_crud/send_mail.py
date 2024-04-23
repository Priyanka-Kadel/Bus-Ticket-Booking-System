import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage


def get_html(sent_to, id):
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Animeta Brandstar Inquiry</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }
                
                .container {
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                
                h1 {
                    color: #333;
                }
                
                p {
                    color: #666;
                    line-height: 1.6;
                }
                
                .contact-details {
                    margin-top: 20px;
                }
                
                .thank-you {
                    margin-top: 30px;
                    font-weight: bold;
                    color: #4CAF50;
                }
            </style>
        </head>
        <body>

        <div class="container">
            <h1>Hi %s,</h1>
            
            <p>
                This is a ticket you recently booked. You can click the below link to view your ticket.
            </p>
            
            <p>
                <a href="http://127.0.0.1:8000/backend/ticket/%s/">View Ticket</a>
            </p>
        </div>
        </body>
        </html>
    '''%(sent_to, id)


def send_html_mail(recipients, user_id, receiver_name):
    msg = EmailMessage()
    msg['Subject'] = 'Bus Ticket'
    msg['From'] = 'pandeybibe098k@gmail.com'
    msg['To'] = ','.join(recipients)
    msg.set_content(get_html(receiver_name, user_id), subtype='html')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        try:
            smtp_server.login('pandeybibe098k@gmail.com', 'bzqs edgz xbjr nspd')
            smtp_server.send_message(msg)
        except smtplib.SMTPAuthenticationError:
            return
        except BaseException as e:
            return
