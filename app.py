import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

load_dotenv()

llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model="Gemma-7b-It")
prompt_template = """
Generate an email based on the following details. Ensure the email aligns with the specified tone, length, and style preferences.

- Title: "{title}"  c
- Context: "{context}"  
- Sender's Name: "{user_name}"  
- Recipient's Name: "{recipient_name}"  
- Email Type: "{email_type}"  
- Recipient's Gender: "{recipient_gender}"  
- Recipient's Level: "{recipient_level}"  
- Recipient's Category: "{recipient_category}"  
- Email Length: "{email_length}" (Choose from short, medium, or long)  
- Grammar and Tone: "{grammar_tone}"  

Please include these requirements: 
- Personalize the email for "{recipient_name}" considering their {recipient_level} status and {recipient_category} category.
- Use a {grammar_tone} tone and language.
- Make sure the email content follows a {email_length} length to suit the user's preference.
- Ensure the content is well-structured and clearly aligned with the purpose of a(n) {email_type} email.

Example Request (For Reference Only):

Title: "Invitation to Health & Wellness Webinar"  
Context: "Invitation for participation in a health & wellness event hosted by the Health First Foundation, targeting professionals in wellness and medical research."  
Sender's Name: "Alex Johnson"  
Recipient's Name: "Dr. Parker"  
Email Type: "Formal"  
Recipient's Gender: "Male"  
Recipient's Level: "Senior"  
Recipient's Category: "Individual"  
Email Length: "Medium"  
Grammar and Tone: "Professional and Polite"  
"""

prompt = PromptTemplate(template=prompt_template, input_variables=[
    "title", "context", "user_name", "recipient_name", "email_type", 
    "recipient_gender", "recipient_level", "recipient_category", 
    "email_length", "grammar_tone"
])

st.set_page_config(page_title="Email Generator", page_icon="📧", layout="centered")

with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

st.markdown(
    "<h3 style='font-size:32px;'>Email Generator - "
    "<a href='https://www.linkedin.com/in/prince-khunt-linked-in/' target='_blank'>Prince Khunt</a></h3>",
    unsafe_allow_html=True
)

st.write("Customize and generate emails easily based on different parameters.")

st.write("---")

email_title = st.text_input("Email Title", placeholder="Enter the title of your email", help="This will set the subject of your email.")

email_context = st.text_area("Context", placeholder="Enter the context of your email", help="This will set the context of your email.")

sender_name = st.text_input("Your Name", placeholder="Enter your name", help="This will appear as the sender's name.")

recipient_name = st.text_input("Recipient's Name", placeholder="Enter the recipient's name", help="This will appear as the recipient's name in the email.")

email_type = st.selectbox(
    "Email Type",
    [
        "Personal", "Formal", "Informal", "General Communication", "Promotional",
        "Seasonal Campaign", "Newsletter", "Order Confirmation", "Shipping Notification",
        "Account Statement", "Notification", "Invitation", "Survey or Feedback",
        "Apology", "Welcome", "Follow-up", "Reminder", "Cold", "Thank-You"
    ],
    help="Choose the tone and style of your email."
)

gender = st.radio("Recipient Gender", ["Male", "Female"], help="Specify the recipient's gender.")

recipient_level = st.selectbox(
    "Recipient Level",
    [
        "Default", "Junior", "Mid-level", "Senior", "Executive", "Student",
        "Manager", "Director", "C-Suite", "Founder/Owner"
    ],
    help="Select the level or role of the recipient."
)

recipient_category = st.selectbox(
    "Recipient Category",
    [
        "Individual", "Company", "Organization", "Team", "Educational Institution",
        "Government Agency", "Customer", "Partner", "Supplier", "Investor"
    ],
    help="Select the type of recipient."
)

email_length = st.selectbox(
    "Email Length",
    ["Short", "Medium", "Long"],
    help="Choose the length of the email content."
)

grammar_tone = st.selectbox(
    "Grammar and Tone",
    ["Simple", "Professional", "Friendly", "Persuasive", "Polite", "Concise", "Elaborate"],
    help="Select the grammar style and tone of your email."
)

st.write("")

if st.button("Generate Email"):
    if not all([email_title, email_context, sender_name, recipient_name, email_type, gender, recipient_level, recipient_category, email_length, grammar_tone]):
        st.warning("Please fill out all fields before generating the email.")
    else:
        st.write("")

        prompt_text = prompt.format(
            title=email_title,
            context=email_context,
            user_name=sender_name,
            recipient_name=recipient_name,
            email_type=email_type,
            recipient_gender=gender,
            recipient_level=recipient_level,
            recipient_category=recipient_category,
            email_length=email_length,
            grammar_tone=grammar_tone
        )

        try:
            result = llm.invoke(prompt_text)

            if result: 
                st.subheader("Generated Email")
                st.markdown(result.content, unsafe_allow_html=True)
            else:
                st.warning("No email content was generated. Please check the input values or the API connection.")
        except Exception as e:
            st.write(f"Error details: {e}")    