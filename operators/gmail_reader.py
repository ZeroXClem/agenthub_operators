import email
import imaplib
import base64
import os
import tempfile
from google.cloud import storage

from .base_operator import BaseOperator
from ai_context import AiContext

class GmailReader(BaseOperator):
    @staticmethod
    def declare_name():
        return 'GmailReader'
    
    @staticmethod
    def declare_category():
        return BaseOperator.OperatorCategory.CONSUME_DATA.value

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
                "data_type": "string", 
            },
            {
                "name": "attached_file_name",
                "data_type": "string",
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
        
        email_data, uploaded_file_names = self.read_emails(email, password, mark_as_read, ai_context)
        ai_context.set_output('email_data', email_data, self)
        # TODO: switch to multi attachment support when looping functionality is added to operators
        ai_context.set_output('attached_file_names', uploaded_file_names[0], self)

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
        uploaded_files = []
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(user, password)

            mail.select("inbox")  # connect to inbox.

            result, data = mail.uid('search', None, "(UNSEEN)")  # search and return uids of all unread messages
            if result == 'OK':
                num = data[0].split()[0]
                result, data = mail.uid('fetch', num, '(BODY.PEEK[])')
                if result == 'OK':
                    raw_email = data[0][1]
                    email_message = email.message_from_bytes(raw_email)
                    body = ''
                    file_paths_to_save = []

                    with tempfile.TemporaryDirectory() as tempdir:
                        for part in email_message.walk():
                            if part.get_content_disposition() == 'attachment':
                                file_data = part.get_payload(decode=True)
                                file_name = part.get_filename()
                                if file_name:
                                    file_path = os.path.join(tempdir, file_name)
                                    with open(file_path, 'wb') as temp:
                                        temp.write(file_data)
                                    file_paths_to_save.append(file_path)

                            elif part.get_content_type() == 'text/plain':
                                text = part.get_payload(decode=True)
                                charset = part.get_content_charset()
                                if charset:
                                    text = text.decode(charset)
                                body += text
                        
                        # Upload attachments to Google Cloud Storage
                        uploaded_files = self.upload_attachments(file_paths_to_save, ai_context)

                    email_info = {
                        'name': email_message['Subject'],  # Use 'Subject' as 'name'
                        'content': {
                            'From': email_message['From'],
                            'Subject': email_message['Subject'],
                            'Date': email_message['Date'],
                            'Body': body,
                            'Attachments': uploaded_files
                        }
                    }

                    email_data = str(email_info)
                    ai_context.add_to_log(f"Read email: {email_info}")

                    if mark_as_read:
                        mail.uid('store', num, '+FLAGS', '\Seen')

                    ai_context.add_to_log(f"Emails read successfully", color='green')
                else:
                    ai_context.add_to_log("No new email.")
            else:
                ai_context.add_to_log("No new email.")

            mail.logout()
            return email_data, uploaded_files
        except Exception as error:
            ai_context.add_to_log(f"An error occurred: {str(error)}")
            return ''

        
    def upload_attachments(self, file_paths, ai_context):
        uploaded_files = []

        for file_path in file_paths:
            file_name = os.path.basename(file_path)

            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    ai_context.store_file(file, file_name, ai_context.get_run_id())
                uploaded_files.append(file_name)

        return uploaded_files
