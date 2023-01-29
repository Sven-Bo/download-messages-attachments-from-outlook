from pathlib import Path
import datetime
import re

import win32com.client  #pip install pywin32


# Create output folder
output_dir = Path.cwd() / "Output"
output_dir.mkdir(parents=True, exist_ok=True)

# Connect to outlook
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

# Connect to folder
#inbox = outlook.Folders("youremail@provider.com").Folders("Inbox")
inbox = outlook.GetDefaultFolder(6)
# https://docs.microsoft.com/en-us/office/vba/api/outlook.oldefaultfolders
# DeletedItems=3, Outbox=4, SentMail=5, Inbox=6, Drafts=16, FolderJunk=23

# Get messages
messages = inbox.Items

for message in messages:
    subject = message.Subject
    body = message.body
    attachments = message.Attachments

    # Create separate folder for each message, exclude special characters and timestampe
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    target_folder = output_dir / re.sub('[^0-9a-zA-Z]+', '', subject) / current_time
    target_folder.mkdir(parents=True, exist_ok=True)

    # Write body to text file
    Path(target_folder / "EMAIL_BODY.txt").write_text(str(body))

    # Save attachments and exclude special
    for attachment in attachments:
        filename = re.sub('[^0-9a-zA-Z\.]+', '', attachment.FileName)
        attachment.SaveAsFile(target_folder / filename)
