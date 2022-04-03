# GmailNoSubject
A tool to apply a label to all emails without a subject (no subject) in GMAIL.

GMAIL does not allow us to filter all emails without a subject. This can be annoying at times. Say, I keep receiving emails with large attachments without any subject and I want to quickly delete them to clear Inbox space.
This tool will apply a label "NOSUBJECT" to all emails without any subject 

Usage:
This project uses the Python GMAIL API as described here:
https://developers.google.com/gmail/api/quickstart/python

Follow the instructions in the above link to achieve below:
In Google Cloud Console, Create a Project named "LabelGmail" and enable GMAIL API.
Next create "OAuth client ID" credentials for "Desktop App" with "https://mail.google.com/" scope to download client.json file using above steps and change the path to the downloaded client.json file in the code here

Client_File = r'C:\Users\yaman\Downloads\client_secret.json'

Also you'll need to add your email id to the "Test users" section of OAuth consent screen, else you will get error.
And you need to Create a label called NOSUBJECT in your GMAIL account.

You can change the below string to any GMAIL filter just like you would in actual GMAIL search. You can customize which emails you want to select as NOSUBJECT.
query_string = 'has:attachment After:2016/12/31 Before:2021/01/01'

Change below List object in Python code to search only emails with a particular label, by default it only searches the INBOX.
search_label_ids = ['INBOX']
