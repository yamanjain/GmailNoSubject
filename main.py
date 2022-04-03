from Google import create_service
import json
import time


#return subject of given message. This is no longer used since we are doing batch API calls
def retsubject(message):
    # print(message['id'])
    #messageResource = sevice.users().messages().get(userId="me", id=message['id']).execute()
    messageResource = sevice.users().messages().get(userId="me", id=message['id'], fields="payload/headers", format= "metadata", metadataHeaders="Subject").execute()
    headers = messageResource["payload"]["headers"]
    subject = [j['value'] for j in headers if j["name"] == "Subject"]
    # print(subject)
    return subject


# def printsubjects(results):
#     messages = results.get('messages', [])
#     if not messages:
#         print('No messages found.')
#     else:
#         print('Messages:')
#         for message in messages:
#             subject = retsubject(message)
#             print(subject)

#Function to search for emails based on query string
def search_messages(service, query, apply_label_ids, search_label_ids):
    result = service.users().messages().list(userId='me', q=query, labelIds=search_label_ids).execute()
    messages = []
    processed = 0
    if 'messages' in result:
        messages.extend(result['messages'])
    if messages:
        processed += len(messages)
        mark_as_label(service, apply_label_ids, messages)
    messages = []
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me', q=query, labelIds=search_label_ids,
                                                 pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
            if messages:
                processed += len(messages)
                mark_as_label(service, apply_label_ids, messages)
                print("Processed :" , processed)
            messages = []

#Function to find all emails with no subject and apply label using batch API calls
def mark_as_label(service, apply_label_ids, messages_to_mark):
    nosubmessages = []

    # New Method using batch commands
    batch = service.new_batch_http_request()
    for msg in messages_to_mark:
        batch.add(service.users().messages().get(userId="me", id=msg['id'], fields="id, payload/headers", format= "metadata", metadataHeaders="Subject"))
        #batch.add(service.users().messages().get(userId="me", id=msg['id']))
    batch.execute()
    for request_id in batch._order:
        resp, content = batch._responses[request_id]
        messageResource = json.loads(content)
        headers = messageResource.get('payload', {}).get('headers', '')
        #headers = messageResource["payload"]["headers"]
        subject = [j['value'] for j in headers if j["name"] == "Subject"]
        if (len(subject)==0):
            nosubmessages.append(messageResource['id'])
        elif (subject[0] == ""):
            nosubmessages.append(messageResource['id'])

    # #Old method of doing one by one instead of batch
    # for msg in messages_to_mark:
    #     subject = retsubject(msg)
    #     if (subject[0] == ""):
    #         print(subject)
    #         nosubmessages.append(msg['id'])

    # add the label UNREAD to each of the search results
    if nosubmessages:
        return service.users().messages().batchModify(
            userId='me',
            body={
                'ids': nosubmessages,
                'addLabelIds': apply_label_ids
            }
        ).execute()
    # 'ids': [msg['id'] for msg in messages_to_mark],


#Return label code for label_id string
def label_id(service, label_id_string):
    results = sevice.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    if not labels:
        print('No labels found.')
    else:
        for label in labels:
            if (label['name'] == label_id_string):
                return label['id']


#Main code begins here
#Change the path to downloaded client_secret.json file path
Client_File = r'C:\Users\yaman\Downloads\client_secret.json'
Api_Name = 'gmail'
Api_Version = 'v1'
SCOPES = ['https://mail.google.com/']

# Call the Gmail API
start_time = time.time()

sevice = create_service(Client_File, Api_Name, Api_Version, SCOPES)
xyz = sevice.users().getProfile(userId='me').execute()
print(xyz)
#Change query string to select only emails between dates or any other GMAIL filter query string
query_string = 'has:attachment After:2016/12/31 Before:2021/01/01'
label_id_string = 'NOSUBJECT'
mylabelid = label_id(sevice, label_id_string)
apply_label_ids = [mylabelid]
search_label_ids = ['INBOX']

# mark_as_label(sevice, query_string, apply_label_ids, search_label_ids)
search_messages(sevice, query_string, apply_label_ids, search_label_ids)
print("Success")
print("--- %s seconds ---" % (time.time() - start_time))
