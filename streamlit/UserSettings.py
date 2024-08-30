import streamlit as st
from db_utils import update_user_settings


def user_settings_page():
    st.title("User Settings")

    if not st.session_state.user:
        st.warning("Please log in to access settings.")
        return

    user = st.session_state.user

    st.header(f"Settings for {user['username']}")

    # User information
    st.subheader("User Information")
    new_username = st.text_input("Username", value=user["username"])
    new_email = st.text_input("Email", value=user.get("email", ""))

    # Notification preferences
    st.subheader("Notification Preferences")
    email_notifications = st.checkbox(
        "Receive email notifications", value=user.get("email_notifications", False)
    )

    # Theme preferences
    st.subheader("Theme Preferences")
    theme_options = ["Light", "Dark", "System Default"]
    selected_theme = st.selectbox(
        "Theme",
        options=theme_options,
        index=theme_options.index(user.get("theme", "System Default")),
    )

    # Save changes button
    if st.button("Save Changes"):
        updated_settings = {
            "username": new_username,
            "email": new_email,
            "email_notifications": email_notifications,
            "theme": selected_theme,
        }

        # Update user settings in the database
        success = update_user_settings(user["id"], updated_settings)

        if success:
            st.success("Settings updated successfully!")
            # Update the session state with new settings
            st.session_state.user.update(updated_settings)
        else:
            st.error("Failed to update settings. Please try again.")

    # Add more settings as needed
