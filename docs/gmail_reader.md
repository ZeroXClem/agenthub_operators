# GmailReader

**GmailReader** is a class that extends the **BaseOperator** and is used to read emails from a Gmail account. It connects to the IMAP server and fetches the emails based on the provided parameters.

## run_step

The function `run_step` is the main entry point for the class. 

1. It retrieves the email address, password, and mark_as_read flag from the parameters provided.
2. It calls the `read_emails` function with these parameters to fetch the email data.
3. The fetched email data is then set as the output of the AI context.

## read_emails

The `read_emails` function is responsible for connecting to the Gmail IMAP server, logging into the account, and fetching the email data.

1. It logs into the Gmail account using the provided email address and password.
2. It selects the "inbox" folder and searches for all unread messages.
3. If there are any unread messages, it fetches the first unread email.
4. It extracts the email information (From, Subject, Date, and Body) and stores it in a dictionary `email_info`.
5. The email data is then converted to a string and added to the AI context log.
6. If the `mark_as_read` flag is True, the email is marked as read.
7. It logs out of the Gmail account and returns the email data.

## get_body_from_part

The `get_body_from_part` function is a helper function that extracts the plain text body of an email.

1. It checks if the part contains a multipart email. If so, it recursively calls the `get_body_from_part` function again for each subpart.
2. If the content type is 'text/plain', it extracts the text, decodes it using the charset (if provided), and cleans it up by removing empty lines and unnecessary spaces.
3. The cleaned up text is then returned as the email body.

By using the **GmailReader** class, it becomes easy to fetch unread emails from a Gmail account while also providing options to mark them as read.