import email
import imaplib
import base64

from .base_operator import BaseOperator
from ai_context import AiContext

class GmailReader(BaseOperator):
    @staticmethod
    def declare_name():
        return 'GmailReader'

    @staticmethod
    def declare_parameters():
        return [
            {
                "name": "email",
                "data_type": "string",
                "placeholder": "Enter the email address",
            },
            {
                "name": "password",
                "data_type": "string",
                "placeholder": "Enter the password",
            },
            {
                "name": "mark_as_read",
                "data_type": "string",
                "placeholder": "Mark email as read (default is False)",
            }
        ]

    @staticmethod
    def declare_inputs():
        return []

    @staticmethod
    def declare_outputs():
        return [
            {
                "name": "email_data",
                "data_type": "string",  # Changed from "{name,content}[]" to "string"
            }
        ]

    def run_step(self, step, ai_context: AiContext):
        params = step['parameters']
        email = params.get('email')
        password = params.get('password')
        mark_as_read_str = params.get('mark_as_read')

        mark_as_read = False  # Default to False
        if mark_as_read_str and mark_as_read_str.lower() == 'true':
            mark_as_read = True
        

        email_data = self.read_emails(email, password, mark_as_read, ai_context)
        ai_context.set_output('email_data', email_data, self)

    def get_body_from_part(self, part):
        if part.is_multipart():
            return ''.join(self.get_body_from_part(subpart) for subpart in part.get_payload())
        if part.get_content_type() == 'text/plain':
            text = part.get_payload(decode=True)
            charset = part.get_content_charset()
            if charset:
                text = text.decode(charset)

            # Clean up the text
            lines = text.split('\r\n')
            cleaned_lines = [line.strip() for line in lines if line.strip() != '']
            cleaned_text = '\n'.join(cleaned_lines)

            return cleaned_text
        return ''

    def read_emails(self, user: str, password: str, mark_as_read: bool, ai_context):
        email_data = ''
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(user, password)

            mail.select("inbox")  # connect to inbox.

            result, data = mail.uid('search', None, "(UNSEEN)")  # search and return uids of all unread messages
            if result == 'OK':
                # Get the first unread email
                num = data[0].split()[0]
                result, data = mail.uid('fetch', num, '(BODY.PEEK[])')
                if result == 'OK':
                    raw_email = data[0][1]
                    email_message = email.message_from_bytes(raw_email)
                    email_info = {
                        'name': email_message['Subject'],  # Use 'Subject' as 'name'
                        'content': {
                            'From': email_message['From'],
                            'Subject': email_message['Subject'],
                            'Date': email_message['Date'],
                            'Body': self.get_body_from_part(email_message) if email_message.is_multipart() else base64.b64decode(email_message.get_payload()).decode('utf-8')
                        }
                    }

                    email_data = str(email_info)
                    ai_context.add_to_log(f"Read email: {email_info}")

                    # Mark the email as read
                    if mark_as_read:
                        mail.uid('store', num, '+FLAGS', '\Seen')

                    ai_context.add_to_log(f"Emails read successfully", color='green')
                else:
                    ai_context.add_to_log("No new email.")
            else:
                ai_context.add_to_log("No new email.")

            mail.logout()
            return email_data
        except Exception as error:
            ai_context.add_to_log(f"An error occurred: {str(error)}")
            return ''
