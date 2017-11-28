# Curated by Cary McEwan. Stay tuned. 
# Twitter   :: @Cary_MakinMoves
# Instagram :: @Cary_MakinMoves
# LinkedIn  :: https://www.linkedin.com/in/cary-mcewan-000b64140/

import smtplib
from smtplib import SMTPException

class EmailClient():
    def __init__(self, name, email, password):
        self.name = str(name)
        self.email = str(email)
        self.password = str(password)
        try:
            self.server = smtplib.SMTP('smtp.gmail.com:587')
            self.server.starttls()
            self.server.login(self.email, self.password)
        except:
            raise SMTPException

    def sendMail(self, recipientName, recipientEmail, subject, content):
        message = "From: {} <{}>\nTo: {} <{}>\nSubject: {}\n\n{}"
        message = message.format(self.name, self.email, recipientName, recipientEmail, subject, content)
        self.server.sendmail(self.email, [recipientEmail], message)

    def sendScanEmail(self, recipientName, recipientEmail, link):
        content = str.format("Hey {},\n\nYour scan is now complete and is ready for download here:\n{}\n\nEnjoy,\nGroup B CREOL", recipientName, link)
        return self.sendMail(recipientName, recipientEmail, "Scan Complete", content)
    
    def sendScanEmails(self, recipientName, recipientEmail, plyLink, stlLink):
        content = str.format("Hey {},\n\nYour scan is now complete and is ready for download here:\nPLY: {}\nSTL: {}\n\nEnjoy,\nGroup B CREOL", recipientName, plyLink, stlLink)
        return self.sendMail(recipientName, recipientEmail, "Scan Complete", content)

