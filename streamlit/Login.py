import streamlit as st
from db_utils import login_user, register_user
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# Postavite svoje Google OAuth 2.0 parametre ovdje
GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"
GOOGLE_CLIENT_SECRET = "YOUR_GOOGLE_CLIENT_SECRET"


def login_page():
    st.title("Login / Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.header("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input(
            "Password", type="password", key="login_password"
        )
        login_button = st.button("Login")

        if login_button:
            if login_username and login_password:
                user = login_user(login_username, login_password)
                if user:
                    st.session_state.user = user
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid login credentials. Please try again.")
            else:
                st.warning("Please enter both username and password.")

        st.markdown("---")
        st.subheader("Or login with Google")
        if st.button("Login with Google"):
            google_login()

    with tab2:
        st.header("Register")
        register_username = st.text_input("Username", key="register_username")
        register_password = st.text_input(
            "Password", type="password", key="register_password"
        )
        register_email = st.text_input("Email", key="register_email")
        register_button = st.button("Register")

        if register_button:
            if register_username and register_password and register_email:
                if register_user(register_username, register_password, register_email):
                    st.success("Registration successful! You can now log in.")
                else:
                    st.error("Registration failed. Username may already exist.")
            else:
                st.warning("Please fill in all fields.")


def google_login():
    # Ovo je pojednostavljena implementacija. U stvarnoj aplikaciji, trebali biste
    # implementirati potpuni OAuth 2.0 tok s odgovarajućim preusmjeravanjima.
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri=YOUR_REDIRECT_URI&scope=openid%20email%20profile"
    st.markdown(f"[Login with Google]({auth_url})")

    # Nakon što korisnik odobri pristup, Google će preusmjeriti na vašu aplikaciju s kodom.
    # Ovdje biste trebali obraditi taj kod i dobiti token.

    # Ovo je primjer kako biste mogli obraditi token:
    # code = st.experimental_get_query_params().get("code")
    # if code:
    #     token = exchange_code_for_token(code)
    #     user_info = get_user_info(token)
    #     # Prijavite korisnika u vašu aplikaciju koristeći dobivene informacije


def exchange_code_for_token(code):
    # Implementirajte razmjenu koda za token
    pass


def get_user_info(token):
    # Implementirajte dohvaćanje korisničkih informacija s tokenom
    pass
