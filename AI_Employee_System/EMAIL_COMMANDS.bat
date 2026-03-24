# EMAIL.BAT - Quick Email Commands
# Run these from AI_Employee_System folder

# Test email connection
email.bat test

# Send an email
email.bat send --to recipient@example.com --subject "Hello" --body "This is a test email"

# Receive emails
email.bat receive

# Show inbox
email.bat inbox

# Compose new email (interactive)
email.bat compose

# Send with CC and attachments
email.bat send --to user@example.com --cc boss@example.com --subject "Report" --body "Please find attached" --attachments report.pdf summary.xlsx

# Send HTML email
email.bat send --to client@example.com --subject "Newsletter" --body "<h1>Hello</h1><p>This is HTML</p>" --html

# Receive all emails (including read)
email.bat receive --all --limit 20
