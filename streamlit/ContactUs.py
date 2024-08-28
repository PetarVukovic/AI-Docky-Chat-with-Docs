import streamlit as st
import smtplib


def contact_us_page():
    st.title("Contact Us")

    with st.form("email_form"):
        st.write("Send us an email with your query or feedback:")
        user_email = st.text_input("Your Email")
        subject = st.text_input("Subject")
        message = st.text_area("Message")

        submit = st.form_submit_button("Send")

        if submit:
            if user_email and subject and message:
                try:
                    smtp_server = "smtp.gmail.com"
                    smtp_port = 587
                    sender_email = "your_email@example.com"
                    password = "your_password"

                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        server.login(sender_email, password)
                        server.sendmail(
                            from_addr=sender_email,
                            to_addrs=user_email,
                            msg=f"Subject: {subject}\n\n{message}",
                        )
                    st.success("Email sent successfully!")
                except Exception as e:
                    st.error(f"Error sending email: {e}")
            else:
                st.error("Please fill in all fields.")
