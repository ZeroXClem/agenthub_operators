from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText

from .base_operator import BaseOperator
from ai_context import AiContext

class GmailSender(BaseOperator):
    @staticmethod
    def declare_name():
        return 'GmailSender'
    
    @staticmethod
    def declare_category():
        return BaseOperator.OperatorCategory.ACT.value

    @staticmethod
    def declare_parameters():
        return [
            {
                "name": "recipient_email",
                "data_type": "string",
                "placeholder": "Enter the recipient's email address"
            },
            {
                "name": "send_as_html",
                "data_type": "boolean",
                "placeholder": "Send email as HTML (default is False)",
            }
        ]

    @staticmethod
    def declare_inputs():
        return [
            {
                "name": "email_body",
                "data_type": "string",
            }
        ]

    @staticmethod
    def declare_outputs():
        return [
            {
                "name": "email_status",
                "data_type": "string",
            }
        ]
        
    def run_step(
        self,
        step,
        ai_context: AiContext
    ):
        params = step['parameters']
        recipient_email = params.get('recipient_email')
        send_as_html_str = params.get('send_as_html')
        send_as_html = False  # Default to False
        if send_as_html_str and send_as_html_str.lower() == 'true':
            send_as_html = True
        
        email_subject = "AgentHub Run Notification"
        email_body = ai_context.get_input('email_body', self)
        sender = ai_context.get_secret('gmail_sender')
        password = ai_context.get_secret('gmail_password')
        print(f"sender: {sender}, password: {password}")

        email_status = self.send_email(email_subject, email_body, sender, [recipient_email], password, send_as_html, ai_context)
        ai_context.set_output('email_status', email_status, self)

    def send_email(self, subject, body, sender, recipients, password, send_as_html, ai_context):
        try:
            if send_as_html:
                msg = MIMEMultipart()
                msg.attach(MIMEText(body, 'html'))
            else:
                msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = ', '.join(recipients)
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
            smtp_server.quit()
            ai_context.add_to_log(f"Email sent successfully", color='green')
            return "Email sent successfully"

        except Exception as error:
            ai_context.add_to_log(f"An error occurred: {str(error)}")
            return "Email sending failed"
