import streamlit as st


# Custom CSS for dark mode and pricing page
def pricing_page():
    st.markdown(
        """
        <style>
        :root {
            --bg-color: #121212;
            --text-color: #ffffff;
            --border-color: #f4c542;
            --button-bg: #f4c542;
            --button-text-color: #ffffff;
            --button-hover-bg: #e6b835;
            --header-font-size: 2rem;  /* 2x povećanje */
            --subheader-font-size: 1.5rem;  /* 1.5x povećanje */
            --description-font-size: 1.2rem;  /* 1.2x povećanje */
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-color);
        }

        .pricing-box {
            background-color: var(--bg-color);
            border: 4px solid var(--border-color);  /* Veći žuti border */
            border-radius: 15px;  /* Zaobljeni uglovi */
            padding: 30px;  /* Povećani padding */
            margin: 20px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .pricing-box:hover {
            transform: translateY(-10px);
            box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);  /* Veća sjena */
        }

        .pricing-header {
            font-size: var(--header-font-size);
            color: var(--text-color);
            margin-bottom: 15px;
            font-weight: bold;
        }

        .pricing-subheader {
            font-size: var(--subheader-font-size);
            color: var(--text-color);
            margin-bottom: 25px;
        }

        .pricing-description {
            font-size: var(--description-font-size);
            color: var(--text-color);
            margin-bottom: 30px;
        }

        .subscribe-button {
            background-color: var(--button-bg);
            color: var(--button-text-color);
            border: none;
            padding: 15px 25px;  /* Povećani padding za veći gumb */
            border-radius: 30px;
            font-size: 18px;  /* Povećana veličina fonta na gumbu */
            cursor: pointer;
            transition: background-color 0.3s ease;
            text-align: center;
            display: inline-block;
            width: 100%;
            text-decoration: none;
        }

        .subscribe-button:hover {
            background-color: var(--button-hover-bg);
        }

        .center-content {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
        }

        .pricing-container {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Choose Your Plan")

    st.write("Select the best plan that fits your needs:")

    # Pricing plans data
    plans = [
        {
            "name": "Basic",
            "price": 9,
            "description": "Up to 10 documents, Basic AI capabilities",
        },
        {
            "name": "Pro",
            "price": 29,
            "description": "Up to 100 documents, Advanced AI capabilities, Priority support",
        },
        {
            "name": "Enterprise",
            "price": 99,
            "description": "Unlimited documents, Premium AI capabilities, Dedicated support",
        },
    ]

    col1, col2, col3 = st.columns(3)

    # Display pricing plans
    for i, plan in enumerate(plans):
        with [col1, col2, col3][i]:
            st.write(
                f"""
                <div class='pricing-box'>
                    <div class='pricing-border-wrap'>
                        <div class='pricing-header'>{plan['name']}</div>
                        <div class='pricing-subheader'>${plan['price']}/month</div>
                        <p class='pricing-description'>{plan['description']}</p>
                        <button class="subscribe-button" onclick="window.location.href='/{plan['name']}';">Subscribe - {plan['name']}</button>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
