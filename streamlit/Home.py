import streamlit as st
from db_utils import login_user, register_user


def home_page():
    # Initialize the session state for sidebar visibility and selected action
    if "show_sidebar" not in st.session_state:
        st.session_state.show_sidebar = False
        st.session_state.action = "none"

    # Function to toggle sidebar visibility
    def toggle_sidebar():
        st.session_state.show_sidebar = not st.session_state.show_sidebar
        if st.session_state.show_sidebar:
            st.session_state.action = "login_or_register"

    # Function to handle successful login
    def handle_successful_login():
        st.session_state.show_sidebar = False
        st.rerun()  # Automatically rerun to load the new page

    # Custom CSS for styling
    st.markdown(
        """
        <style>
        /* Custom styling for the sidebar */
        .css-1l02m7d { 
            width: 400px; /* Increase the width of the sidebar */
        }
        .css-1l02m7d .css-1v3fvcr { /* Adjust this class if necessary */
            font-size: 16px; /* Decrease font size of text in the sidebar */
        }
        .css-1v3fvcr i { /* Increase size of icons in the sidebar */
            font-size: 18px;
        }
        .css-1v3fvcr .st-bd { /* Increase padding for sidebar items */
            padding: 12px;
        }
        .main-content {
            color: #ffffff;
            text-align: center; /* Center all text */
        }
        .main-content h1 {
            color: #61dafb;
            font-size: 4em; /* Increased font size by 1x */
            font-weight: bold;
        }
        .main-content h2 {
            color: #61dafb;
            font-size: 2.5em; /* Increased font size by 1x */
            font-weight: bold;
        }
        .main-content p {
            font-size: 1.2em; /* Font size for paragraphs */
            line-height: 1.6;
            text-align: justify; /* Align text for better readability */
        }
        ul {
            text-align: left; /* Align bullet points with text */
            list-style-type: disc; /* Ensure bullet points are discs */
            padding-left: 1.5em;
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
            padding: 16px 32px; /* Increase padding */
            font-weight: bold;
            font-size: 1.2em; /* Increase font size */
            display: block;
            margin: 40px auto 20px auto; /* Center the button with margin */
            animation: pulse 2s infinite; /* Animation effect */
            text-align: center;
        }
        .cta-button:hover {
            background-color: #21a1f1;
        }
        @keyframes pulse {
            0% {
                transform: scale(1);
                box-shadow: 0 0 0 rgba(0, 0, 0, 0);
            }
            50% {
                transform: scale(1.05);
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            }
            100% {
                transform: scale(1);
                box-shadow: 0 0 0 rgba(0, 0, 0, 0);
            }
        }
        /* Style for container boxes */
        .container-box {
            border: 2px solid #FFA500; /* Orange border */
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            width: 30%; /* Adjust width of each container */
            display: inline-block;
            vertical-align: top;
            transition: transform 0.3s ease-in-out; /* Smooth animation for hover */
        }
        .container-box:hover {
            transform: scale(1.05); /* Slightly enlarge box on hover */
        }
        /* Style for responsive layout */
        .container-wrapper {
            text-align: center; /* Center the containers */
        }
        @media (max-width: 800px) {
            .container-box {
                width: 90%; /* Full width on smaller screens */
                display: block;
                margin: 10px auto;
            }
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
        <p>Transformirajte način na koji komunicirate s vašim dokumentima koristeći naprednu AI tehnologiju. Naša aplikacija vam omogućava učinkovito upravljanje i analizu vaših dokumenata. Evo što dobijate:</p>
        <ul>
            <li>🚀 <strong>Optimizacija:</strong> Naša aplikacija koristi napredne algoritme za brzu i preciznu analizu vaših dokumenata.</li>
            <li>⚡ <strong>Brzina:</strong> Brza obrada podataka omogućava vam da dobijete rezultate u realnom vremenu.</li>
            <li>🎯 <strong>Točnost:</strong> Visoka točnost u interpretaciji i analizi podataka pomoću napredne umjetne inteligencije.</li>
        </ul>
        <h2>Kako možete koristiti našu aplikaciju?</h2>
        <p>Naša aplikacija omogućava interaktivnu komunikaciju s različitim vrstama dokumenata. Evo nekoliko primjera:</p>
        <div class="container-wrapper">
            <div class="container-box">
                <h3>📊 CSV datoteke</h3>
                <p>Postavite pitanja kao što su "<i>Koji su glavni trendovi u prodaji prema CSV datoteci?</i>"</p>
            </div>
            <div class="container-box">
                <h3>📄 PDF datoteke</h3>
                <p>Pitanja poput "<i>Koliko je ukupno stavki na fakturi?</i>" ili "<i>Što je navedeno kao datum dospjela?</i>"</p>
            </div>
            <div class="container-box">
                <h3>📈 Excel datoteke</h3>
                <p>Upit kao što je "<i>Koliko ima faktura s iznosom većim od 1000 kn?</i>" ili "<i>Koje su prosječne plaće po odjelima?</i>"</p>
            </div>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Adding the video section below the boxes
    st.markdown(
        "<h2 style='text-align:center;'>Pogledajte naš vodič</h2>",
        unsafe_allow_html=True,
    )
    video_path = "C:/Users/pvukovic/Videos/Screen Recordings/Screen Recording 2024-08-27 185352.mp4"

    # Display the video
    try:
        with open(video_path, "rb") as video_file:
            st.video(video_file.read())
    except Exception as e:
        st.error(f"Could not load the video. Error: {e}")

    # Button to toggle sidebar visibility
    if st.sidebar.button("Zapocni"):
        toggle_sidebar()

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
                            handle_successful_login()  # Redirect to collections.py
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
                            handle_successful_login()  # Redirect to collections.py
                        else:
                            st.error("Registration failed. Please try again.")
                    else:
                        st.warning("Please enter both email and password.")
