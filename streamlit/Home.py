import streamlit as st
from db_utils import (
    add_collection_to_user,
    get_user_collections,
    login_user,
    register_user,
)


def home_page():
    # Initialize the session state for sidebar visibility and selected action
    if "show_sidebar" not in st.session_state:
        st.session_state.show_sidebar = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "collections" not in st.session_state:
        st.session_state.collections = []

    # Function to toggle sidebar visibility
    def toggle_sidebar():
        st.session_state.show_sidebar = not st.session_state.show_sidebar

    # Function to handle successful login
    # Function to handle successful login
    def handle_successful_login(user_id):
        st.session_state.user = user_id
        st.session_state.collections = get_user_collections(user_id)
        st.session_state.show_sidebar = False
        st.rerun()

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
                font-size: 1.3em; /* Increased font size by 1x */
                line-height: 1.6;
                text-align: justify; /* Align text for better readability */
                margin-top: 20px; /* Add top margin */
                margin-bottom: 20px; /* Add bottom margin */
            }
            ul {
                text-align: left; /* Align bullet points with text */
                list-style-type: disc; /* Ensure bullet points are discs */
                padding-left: 1.5em;
                margin-top: 20px; /* Add top margin */
                margin-bottom: 20px; /* Add bottom margin */
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
            /* Style for container boxes with yellow border and rounded corners */
            .container-box {
                border: 2px solid #FFA500; /* Yellow border */
                border-radius: 10px; /* Rounded corners */
                padding: 20px;
                margin: 20px; /* Add margin for spacing */
                width: 30%; /* Adjust width of each container */
                display: inline-block;
                vertical-align: top;
                transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out; /* Smooth animation for hover */
                position: relative;
            }
            .container-box::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                border: 2px solid #FFA500; /* Yellow border */
                border-radius: 10px; /* Rounded corners */
                box-shadow: 0 0 0 rgba(0, 0, 0, 0);
                transition: box-shadow 0.3s ease-in-out;
                z-index: -1;
            }
            .container-box:hover {
                transform: scale(1.05); /* Slightly enlarge box on hover */
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); /* Add shadow on hover */
            }
            .container-box:hover::before {
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.3); /* Intensify shadow on hover */
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
            /* Style for the yellow info box */
            .info-box {
                border: 2px solid #FFA500; /* Yellow border */
                border-radius: 10px; /* Rounded corners */
                padding: 20px;
                margin: 20px auto; /* Margin for spacing */
                width: 80%; /* Adjust width */
                background-color: rgba(128, 128, 128, 0.1); /* Transparent gray background */
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); /* Subtle shadow for better visibility */
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
            <div >
                <p>Transformirajte način na koji komunicirate s vašim dokumentima koristeći naprednu AI tehnologiju. Naša aplikacija vam omogućava učinkovito upravljanje i analizu vaših dokumenata. Evo što dobijate:</p>
                <ul>
                    <li><h3>🚀 <strong>Optimizacija:</strong> Naša aplikacija koristi napredne algoritme za brzu i preciznu analizu vaših dokumenata.</h3></li>
                    <li><h3>⚡ <strong>Brzina:</strong> Brza obrada podataka omogućava vam da dobijete rezultate u realnom vremenu.</h3></li>
                    <li><h3>🎯 <strong>Točnost:</strong> Visoka točnost u interpretaciji i analizi podataka pomoću napredne umjetne inteligencije.</h3></li>
                </ul>
            </div>
            <h2>Kako možete koristiti našu aplikaciju?</h2>
            <p>Naša aplikacija omogućava interaktivnu komunikaciju s različitim vrstama dokumenata. Evo nekoliko primjera:</p>
            <div class="container-wrapper">
                <div class="container-box">
                    <h3>📊 Word datoteke</h3>
                    <p>Postavite pitanja kao što su "<i>Daj mi sažetak ovog worda?</i>" ili "<i>Generiraj mi kviz na temelju poglavlja 5?</i>"</p>
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

    # Show sidebar if toggle is activated
    if st.session_state.show_sidebar:
        st.sidebar.header("Login / Register")

        option = st.sidebar.selectbox("Odaberite opciju", ["Prijava", "Registracija"])

        if option == "Prijava":
            with st.sidebar.form(key="login_form"):
                st.write("🔑 Prijava")
                login_username = st.text_input("Korisničko ime", key="login_username")
                login_password = st.text_input(
                    "Lozinka", type="password", key="login_password"
                )
                login_button = st.form_submit_button("Prijava")

                if login_button:
                    if login_username and login_password:
                        user = login_user(login_username, login_password)
                        if user:
                            handle_successful_login(user[0])  # Pass user_id
                        else:
                            st.error(
                                "Nevažeći podaci za prijavu. Molimo pokušajte ponovno."
                            )
                    else:
                        st.warning("Molimo unesite korisničko ime i lozinku.")

        elif option == "Registracija":
            with st.sidebar.form(key="registration_form"):
                st.write("📝 Registracija")
                register_username = st.text_input(
                    "Korisničko ime", key="register_username"
                )
                register_password = st.text_input(
                    "Lozinka", type="password", key="register_password"
                )
                register_button = st.form_submit_button("Registracija")

                if register_button:
                    if register_username and register_password:
                        if register_user(register_username, register_password):
                            st.sidebar.success(
                                "Registracija uspješna! Sada se možete prijaviti."
                            )
                        else:
                            st.error(
                                "Registracija nije uspjela. Korisničko ime možda već postoji."
                            )
                    else:
                        st.warning("Molimo unesite korisničko ime i lozinku.")
    # If user is logged in, show their collections
    if st.session_state.user:
        if st.sidebar.button("Odjava"):
            st.session_state.user = None
            st.session_state.collections = []
            st.rerun()
