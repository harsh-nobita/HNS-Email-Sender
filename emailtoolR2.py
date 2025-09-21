import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from tkinter import Tk, Label, Entry, Button, scrolledtext, filedialog, messagebox
import os

# ----- Global Variables -----
images_to_attach = []

# ----- Function to select images -----
def add_images():
    global images_to_attach
    file_paths = filedialog.askopenfilenames(title="Select images", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])
    images_to_attach = list(file_paths)
    lbl_images.config(text=f"{len(images_to_attach)} image(s) selected")

# ----- Send Email Function -----
def send_email():
    sender = entry_sender.get().strip()
    password = entry_password.get().strip()
    recipients = [email.strip() for email in entry_recipients.get().split(",") if email.strip()]
    subject = entry_subject.get().strip()
    body_html = text_body.get("1.0", "end").strip()

    if not sender or not password or not recipients or not subject or not body_html:
        messagebox.showerror("Error", "Please fill in all fields")
        return

    try:
        # Build email
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject

        # Attach HTML body
        msg.attach(MIMEText(body_html, "html"))

        # Attach images
        for img_path in images_to_attach:
            with open(img_path, "rb") as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', f"<{os.path.basename(img_path)}>")
                img.add_header('Content-Disposition', 'inline', filename=os.path.basename(img_path))
                msg.attach(img)

        # Send email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipients, msg.as_string())
        server.quit()

        messagebox.showinfo("Success", f"Email sent to {len(recipients)} recipient(s)!")
    except smtplib.SMTPAuthenticationError:
        messagebox.showerror("Authentication Error", "Login failed! Check Gmail and App Password.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email:\n{e}")

# ----- GUI Setup -----
root = Tk()
root.title("📧 HNS Email Sender")
root.geometry("600x700")

# Sender Gmail
Label(root, text="Sender Gmail:").pack(anchor="w", padx=10, pady=5)
entry_sender = Entry(root, width=50)
entry_sender.pack(padx=10, pady=5)

# App password
Label(root, text="App Password:").pack(anchor="w", padx=10, pady=5)
entry_password = Entry(root, width=50, show="*")
entry_password.pack(padx=10, pady=5)

# Recipients
Label(root, text="Recipients (comma separated):").pack(anchor="w", padx=10, pady=5)
entry_recipients = Entry(root, width=50)
entry_recipients.pack(padx=10, pady=5)

# Subject
Label(root, text="Subject:").pack(anchor="w", padx=10, pady=5)
entry_subject = Entry(root, width=50)
entry_subject.pack(padx=10, pady=5)

# Body (HTML)
Label(root, text="Message (HTML supported):").pack(anchor="w", padx=10, pady=5)
text_body = scrolledtext.ScrolledText(root, width=70, height=15)
text_body.pack(padx=10, pady=5)

# Attach images
Button(root, text="Add Images", command=add_images, bg="blue", fg="white").pack(pady=5)
lbl_images = Label(root, text="No images selected")
lbl_images.pack(pady=5)

# Send button
Button(root, text="Send Email", command=send_email, bg="green", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

root.mainloop()
