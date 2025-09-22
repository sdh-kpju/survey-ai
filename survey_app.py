import streamlit as st
import pandas as pd
import os
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Digital Awareness & AI Literacy Survey (GenAI tools)", layout="wide")

# CSV file to save survey data
CSV_FILE = "survey_results.csv"

# ---------------- TAB MENU ---------------- #
tab1, tab2 = st.tabs(["📝 Survey Form", "📊 Data Analysis"])


# ---------------- TAB 1: SURVEY ---------------- #
with tab1:
    st.title("📋 Digital Awareness & AI Literacy Survey")
    st.write("""
    Dear Colleagues,

    We are from School of Digital health (SDH) planning to organise a *Bootcamp on AI Literacy & Tools* for academic staff at KPJU.  
    To ensure the training is relevant and beneficial, we would like to understand your current level of awareness, usage, and expectations regarding digital technologies and AI.  

    This survey will take **5–7 minutes**. All responses are confidential.  
    """)

    st.subheader("Section A: Background Information")

    email = st.text_input("0. Email Address (mandatory, will be kept confidential)")

    faculty = st.selectbox("1. Faculty/Department", [
        "Health Sciences", "Medicine", "Pharmacy", "Nursing",
        "Healthcare Management", "Digital Health", "Social Science", "CGPSD", "Other"
    ])
    if faculty == "Other":
        faculty_other = st.text_input("Please specify your Faculty/Department")
        faculty = faculty_other if faculty_other else faculty

    role = st.selectbox("2. Current Academic Role", [
        "Lecturer", "Senior Lecturer", "Associate Professor", "Professor", "Other"
    ])
    if role == "Other":
        role_other = st.text_input("Please specify your Academic Role")
        role = role_other if role_other else role

    experience = st.radio("3. Years of teaching experience", [
        "0–3 years", "4–7 years", "8–15 years", "More than 15 years"
    ])
    
    st.subheader("Section B: Digital Literacy & Technology Use")

    digital_literacy = st.radio("4. How would you rate your overall digital literacy?", [
        "Beginner", "Intermediate", "Advanced"
    ])
    tools = st.multiselect("5. Which digital tools do you currently use in teaching & research?", [
        "Learning Management Systems (Moodle, Blackboard, etc.)",
        "Microsoft 365 (Word, Excel, PowerPoint, Teams, SharePoint)",
        "Google Workspace (Docs, Slides, Drive, Forms)",
        "Data analysis tools (SPSS, R, Python, Matlab, Power BI)",
        "Online collaboration tools (Zoom, Webex, Miro, etc.)",
        "Other"
    ])
    if "Other" in tools:
        tools_other = st.text_input("Please specify other tools you use")
        if tools_other:
            tools = [t for t in tools if t != "Other"] + [tools_other]

    confidence = st.radio("6. How confident are you in integrating digital tools into your teaching/research?", [
        "Very confident", "Somewhat confident", "Neutral", "Not very confident", "Not confident at all"
    ])

    st.subheader("Section C: Awareness of AI & Emerging Tools")

    ai_familiarity = st.radio("7. How familiar are you with the concept of Artificial Intelligence (AI)?", [
        "Very familiar – I actively use AI tools",
        "Somewhat familiar – I know the basics but rarely use",
        "Heard of it – but not sure how it applies to me",
        "Not familiar at all"
    ])
    ai_tools = st.multiselect("8. Which AI tools have you used before?", [
        "ChatGPT or similar AI assistants",
        "AI-based plagiarism checkers (Turnitin AI detector, etc.)",
        "AI in research tools (Elicit, Scite, ResearchRabbit)",
        "AI in teaching tools (Quiz generators, lesson planners, adaptive learning systems)",
        "AI in data analysis (Machine learning tools, predictive models)",
        "None"
    ])
    ai_opportunities = st.text_area("9. In your opinion, what are the biggest opportunities for AI in education & research?")
    ai_concerns = st.multiselect("10. What are your main concerns about AI adoption in academia?", [
        "Academic integrity & plagiarism",
        "Data privacy & security",
        "Reliability of AI-generated content",
        "Lack of skills/training",
        "Fear of AI replacing academic roles",
        "Other"
    ])
    if "Other" in ai_concerns:
        ai_concerns_other = st.text_input("Please specify your other concerns")
        if ai_concerns_other:
            ai_concerns = [c for c in ai_concerns if c != "Other"] + [ai_concerns_other]

    st.subheader("Section D: Training Needs & Preferences")

    training_areas = st.multiselect("11. Which areas would you like the bootcamp to cover? (Select top 3)", [
        "Introduction to AI literacy – understanding AI concepts",
        "AI tools for teaching & learning (content creation, assessments, student engagement)",
        "AI tools for research (literature review, data analysis, manuscript writing)",
        "Ethical issues in AI usage (plagiarism, academic integrity, bias)",
        "Data management & digital tools for academics",
        "Hands-on practice with AI applications",
        "Other"
    ])
    if "Other" in training_areas:
        training_other = st.text_input("Please specify other training needs")
        if training_other:
            training_areas = [a for a in training_areas if a != "Other"] + [training_other]

    format_pref = st.radio("12. What is your preferred training format?", [
        "Workshop (face-to-face)", "Online webinar", "Hybrid (mix of online & in-person)", "Self-paced online modules"
    ])
    time_commitment = st.radio("13. How much time would you be willing to commit for the bootcamp?", [
        "Half-day", "1 full day", "2 days", "More than 2 days"
    ])

    st.subheader("Section E: Final Thoughts")
    final_comments = st.text_area("14. Please share any expectations, suggestions, or concerns:")

    # --- Email validation function ---
    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    # --- Submit button ---
    if st.button("✅ Submit Survey"):
        if not email:
            st.error("❌ Please enter your email address.")
        elif not is_valid_email(email):
            st.error("❌ Please enter a valid email address (e.g., name@domain.com).")
        else:
            new_response = pd.DataFrame([{
                "Email": email,
                "Faculty": faculty,
                "Role": role,
                "Experience": experience,
                "Digital Literacy": digital_literacy,
                "Tools": ", ".join(tools),
                "Confidence": confidence,
                "AI Familiarity": ai_familiarity,
                "AI Tools": ", ".join(ai_tools),
                "AI Opportunities": ai_opportunities,
                "AI Concerns": ", ".join(ai_concerns),
                "Training Areas": ", ".join(training_areas),
                "Format Preference": format_pref,
                "Time Commitment": time_commitment,
                "Final Comments": final_comments
            }])

            if os.path.exists(CSV_FILE):
                new_response.to_csv(CSV_FILE, mode='a', header=False, index=False)
            else:
                new_response.to_csv(CSV_FILE, index=False)

            st.success("✅ Thank you! Your response has been recorded.")

# ---------------- TAB 2: DATA ANALYSIS (PASSWORD PROTECTED) ---------------- #
with tab2:
    st.title("📊 Survey Data Analysis (Restricted Access)")

    password = st.text_input("Enter passcode to view results:", type="password")

    if password == "KPJU2025":   # 🔑 change this to your desired passcode
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            st.write("### All Responses")
            st.dataframe(df)

            st.write("### Summary Insights")
            col1, col2 = st.columns(2)

            with col1:
                st.write("**Digital Literacy Levels**")
                st.bar_chart(df["Digital Literacy"].value_counts())

                st.write("**Confidence in Digital Tools**")
                st.bar_chart(df["Confidence"].value_counts())

            with col2:
                st.write("**AI Familiarity**")
                st.bar_chart(df["AI Familiarity"].value_counts())

                st.write("**Preferred Training Format**")
                st.bar_chart(df["Format Preference"].value_counts())

            # --- Word Cloud Function ---
            def plot_wordcloud(text_series, title):
                text = " ".join(str(t) for t in text_series.dropna())
                if text.strip():
                    wc = WordCloud(width=800, height=400, background_color="white").generate(text)
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.imshow(wc, interpolation="bilinear")
                    ax.axis("off")
                    st.write(f"**{title}**")
                    st.pyplot(fig)
                else:
                    st.info(f"No responses for {title} yet.")

            st.write("### Word Clouds (Open-ended Questions)")
            plot_wordcloud(df["AI Opportunities"], "AI Opportunities")
            plot_wordcloud(df["AI Concerns"], "AI Concerns")
            plot_wordcloud(df["Final Comments"], "Final Comments")

            # Download option
            st.download_button(
                label="⬇️ Download Full Survey Data (CSV)",
                data=df.to_csv(index=False),
                file_name="survey_results.csv",
                mime="text/csv"
            )

            # --- Delete Data Option with Confirmation ---
            st.write("---")
            st.subheader("⚠️ Danger Zone")
            confirm_delete = st.text_input("Type DELETE to confirm data deletion:")

            if st.button("🗑️ Delete All Survey Data"):
                if confirm_delete == "DELETE":
                    os.remove(CSV_FILE)
                    st.warning("⚠️ All survey data has been permanently deleted.")
                    st.experimental_rerun()
                else:
                    st.error("❌ Deletion not confirmed. Please type DELETE to proceed.")

        else:
            st.warning("No survey responses recorded yet. Please submit the form in the Survey tab.")
    elif password != "":
        st.error("❌ Incorrect passcode. Please try again.")
