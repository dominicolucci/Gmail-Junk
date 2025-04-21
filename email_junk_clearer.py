import imaplib
import email

# === Your Configuration ===
EMAIL = "dominic.s.colucci@gmail.com"
APP_PASSWORD = "bqpwmbocpgkpqfdh"  # No spaces
IMAP_SERVER = "imap.gmail.com"

NEWSLETTER_SENDERS = ["noreply@", "newsletter@", "updates@", "info@", "promotions@"]

def connect_to_gmail():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, APP_PASSWORD)
    return mail

def find_candidates(mail):
    mail.select("inbox")
    status, data = mail.search(None, 'SEEN')

    candidates = []

    for num in data[0].split():
        status, msg_data = mail.fetch(num, "(RFC822)")
        raw_email = msg_data[0][1]
        message = email.message_from_bytes(raw_email)

        sender = message.get("From", "").lower()
        subject = message.get("Subject", "(No Subject)")

        if any(keyword in sender for keyword in NEWSLETTER_SENDERS):
            candidates.append({
                "uid": num,
                "sender": sender,
                "subject": subject
            })

    return candidates

def confirm_and_archive(mail, candidates):
    print(f"\nFound {len(candidates)} email(s) matching your filter.")
    print("-" * 50)

    for email_info in candidates[:10]:  # Preview first 10
        print(f"From: {email_info['sender']}")
        print(f"Subject: {email_info['subject']}\n")

    if len(candidates) > 10:
        print(f"...and {len(candidates) - 10} more.\n")

    confirm = input("Would you like to archive all of these emails? (yes/no): ").strip().lower()

    if confirm == "yes":
        for email_info in candidates:
            mail.copy(email_info["uid"], "[Gmail]/All Mail")
            mail.store(email_info["uid"], "+FLAGS", "\\Deleted")

        mail.expunge()
        print(f"\n✅ Archived {len(candidates)} email(s) successfully.")
    else:
        print("\n❌ No changes were made.")

def main():
    mail = connect_to_gmail()
    candidates = find_candidates(mail)
    confirm_and_archive(mail, candidates)
    mail.logout()

if __name__ == "__main__":
    main()
