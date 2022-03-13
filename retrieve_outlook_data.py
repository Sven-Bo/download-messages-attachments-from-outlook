from pathlib import Path  #core python module
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

    # Create separate folder for each message
    target_folder = output_dir / str(subject)
    target_folder.mkdir(parents=True, exist_ok=True)

    # Write body to text file
    Path(target_folder / "EMAIL_BODY.txt").write_text(str(body))

    # Save attachments
    for attachment in attachments:
        attachment.SaveAsFile(target_folder / str(attachment))