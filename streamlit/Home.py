import streamlit as st
from db_utils import login_user, register_user


def home_page():
    # Initialize the session state for sidebar visibility and selected action
    if "show_sidebar" not in st.session_state:
        st.session_state.show_sidebar = False
        st.session_state.action = "none"

    # Function to toggle sidebar visibility
    def toggle_sidebar(action):
        st.session_state.show_sidebar = True
        st.session_state.action = action

    # Custom CSS for styling
    st.markdown(
        """
        <style>
        .css-18e3th9 { 
            background-color: #282c34; 
            color: #ffffff;
            font-family: 'Arial', sans-serif;
        }
        .css-18e3th9 .stText {
            color: #ffffff;
        }
        .css-18e3th9 .stButton {
            background-color: #61dafb;
            color: #282c34;
            border-radius: 5px;
            border: none;
            padding: 12px;
            margin-top: 10px;
            font-weight: bold;
        }
        .css-18e3th9 .stButton:hover {
            background-color: #21a1f1;
        }
        .main-content {
            color: #ffffff;  /* Ensure text color is white */
        }
        .main-content h1 {
            color: #61dafb;
            font-size: 2.5em;
        }
        .main-content h2 {
            color: #61dafb;
            font-size: 2em;
        }
        .main-content p {
            font-size: 1.2em;
            line-height: 1.6;
        }
        .section-divider {
            margin: 40px 0;
            border-top: 2px solid #61dafb;
        }
        .cta-button {
            background-color: #61dafb;
            color: #282c34;
            border-radius: 5px;
            border: none;
            padding: 12px 24px;
            font-weight: bold;
            font-size: 1.1em;
        }
        .cta-button:hover {
            background-color: #21a1f1;
        }
        /* Style for forms */
        .stForm {
            color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Main content for the home page
    st.markdown(
        '<div class="main-content"><h1>Dobrodošli na AI Chat s vašim dokumentima 🤖</h1>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="main-content">
        <p>Transformirajte način na koji komunicirate s vašim dokumentima koristeći naprednu AI tehnologiju. Naša aplikacija vam omogućava učinkovito upravljanje i analizu vaših dokumenata.</p>
        <h2>Značajke</h2>
        <ul>
            <li>📂 <strong>Učitajte dokumente:</strong> Dodajte različite vrste dokumenata poput CSV, PDF i Excel datoteka u vašu zbirku bez poteškoća.</li>
            <li>📁 <strong>Upravljačke zbirke:</strong> Organizirajte svoje dokumente u zbirke za lakši pristup i upravljanje.</li>
            <li>🤖 <strong>Razgovarajte s AI:</strong> Komunicirajte s AI kako biste dobili uvide i odgovore iz vaših dokumenata. Postavite pitanja i primite detaljne odgovore.</li>
        </ul>
        </div>
        <div class="section-divider"></div>
        <div class="main-content">
        <h2>Napredne AI tehnologije</h2>
        <p>Naša AI tehnologija podržava različite formate dokumenata kako bi pružila duboke uvide:</p>
        <ul>
            <li>📊 <strong>CSV datoteke:</strong> Analizirajte i sažimajte tablične podatke.</li>
            <li>📄 <strong>PDF datoteke:</strong> Izdvojite i razumijete složene informacije iz PDF-ova.</li>
            <li>📈 <strong>Excel datoteke:</strong> Procesirajte podatke iz tablica za detaljnu analizu.</li>
        </ul>
        <p>Na primjer, možete postaviti pitanja poput, <i>"Koji su ključni trendovi u podacima o prodaji?"</i>, i AI će pružiti precizne odgovore na temelju sadržaja vašeg dokumenta.</p>
        <button class="cta-button" onclick="location.href='#'">Započnite</button>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Show sidebar if toggle is activated
    if st.session_state.show_sidebar:
        st.sidebar.header("Login / Register")

        # Option to choose between login and registration
        option = st.sidebar.selectbox("Choose an option", ["Log In", "Register"])

        if option == "Log In":
            # Login Form
            with st.sidebar.form(key="login_form"):
                st.write("🔑 Log In")
                login_email = st.text_input("Email", key="login_email")
                login_password = st.text_input(
                    "Password", type="password", key="login_password"
                )
                login_button = st.form_submit_button("Log In")

                if login_button:
                    if login_email and login_password:
                        user = login_user(login_email, login_password)
                        if user:
                            st.session_state.user = user
                            st.success("You have logged in successfully!")
                            st.session_state.show_sidebar = False
                            st.rerun()
                        else:
                            st.error("Invalid credentials. Please try again.")
                    else:
                        st.warning("Please enter both email and password.")

        elif option == "Register":
            # Registration Form
            with st.sidebar.form(key="registration_form"):
                st.write("📝 Register")
                register_email = st.text_input("Email", key="register_email")
                register_password = st.text_input(
                    "Password", type="password", key="register_password"
                )
                register_button = st.form_submit_button("Register")

                if register_button:
                    if register_email and register_password:
                        user = register_user(register_email, register_password)
                        if user:
                            st.session_state.user = user
                            st.success(
                                "Registration successful! You are now logged in."
                            )
                            st.session_state.show_sidebar = False
                            st.rerun()
                        else:
                            st.error("Registration failed. Please try again.")
                    else:
                        st.warning("Please enter both email and password.")

    # Button to show sidebar
    if not st.session_state.show_sidebar:
        if st.button("Započnite"):
            toggle_sidebar(action="login_or_register")
