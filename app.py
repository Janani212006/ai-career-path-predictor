import streamlit as st
import matplotlib.pyplot as plt
import PyPDF2

st.title("AI Career Path Predictor")

st.write("Enter skills manually OR upload your resume")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

skills_input = st.text_input("Enter your skills (comma separated)")

skill_keywords = [
    "python","machine learning","deep learning","sql","statistics",
    "html","css","javascript","excel","nlp","data visualization"
]

career_db = {
    "Data Scientist": {
        "skills": ["python","machine learning","statistics","sql"],
        "description": "Works on data analysis and predictive models.",
        "learn": ["deep learning","data visualization","pandas"]
    },
    "Machine Learning Engineer": {
        "skills": ["python","machine learning","deep learning"],
        "description": "Builds and deploys ML models in real systems.",
        "learn": ["pytorch","tensorflow","mlops"]
    },
    "Web Developer": {
        "skills": ["html","css","javascript"],
        "description": "Builds websites and web applications.",
        "learn": ["react","nodejs","ui design"]
    },
    "Data Analyst": {
        "skills": ["excel","sql","python","data visualization"],
        "description": "Analyzes data to find business insights.",
        "learn": ["power bi","tableau","statistics"]
    },
    "AI Engineer": {
        "skills": ["python","deep learning","nlp"],
        "description": "Develops AI systems and intelligent applications.",
        "learn": ["transformers","computer vision","mlops"]
    }
}

career_roadmap = {
    "Data Scientist": [
        "Learn Python",
        "Learn Statistics",
        "Learn Machine Learning",
        "Learn Data Visualization",
        "Build ML Projects"
    ],
    
    "Machine Learning Engineer": [
        "Learn Python",
        "Learn Machine Learning",
        "Learn Deep Learning",
        "Learn TensorFlow/PyTorch",
        "Deploy ML Models"
    ],
    
    "Web Developer": [
        "Learn HTML",
        "Learn CSS",
        "Learn JavaScript",
        "Learn React",
        "Build Web Applications"
    ],
    
    "Data Analyst": [
        "Learn Excel",
        "Learn SQL",
        "Learn Python",
        "Learn Data Visualization",
        "Use Power BI or Tableau"
    ],
    
    "AI Engineer": [
        "Learn Python",
        "Learn Machine Learning",
        "Learn Deep Learning",
        "Learn NLP/Computer Vision",
        "Build AI Applications"
    ]
}

resume_text = ""

if uploaded_file is not None:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    for page in pdf_reader.pages:
        resume_text += page.extract_text().lower()

    detected_skills = []

    for skill in skill_keywords:
        if skill in resume_text:
            detected_skills.append(skill)

    st.subheader("Detected Skills From Resume")
    st.write(detected_skills)

    skills_input = ",".join(detected_skills)

if st.button("Predict Career Path"):

    user_skills = [s.strip().lower() for s in skills_input.split(",")]

    st.subheader("Career Recommendations")

    scores = []
    careers = []

    for career, data in career_db.items():

        required_skills = data["skills"]

        matched = set(user_skills) & set(required_skills)
        missing = set(required_skills) - set(user_skills)

        score = (len(matched) / len(required_skills)) * 100

        scores.append(score)
        careers.append(career)

        if score > 0:
            st.write(f"## {career}")
            st.write(f"Match Score: {score:.1f}%")
            st.write(data["description"])

            st.markdown("### ✅ Skills you have")
            if matched:
                for skill in matched:
                    st.write(f"- {skill}")
            else:
                st.write("None")

            st.markdown("### ❌ Skills you need to learn")
            if missing:
                for skill in missing:
                    st.write(f"- {skill}")
            else:
                st.write("None")

            st.markdown("### 📚 Suggested skills to explore")
            for skill in data["learn"]:
                st.write(f"- {skill}")

            st.markdown("### 🚀 Career Roadmap")

            steps = career_roadmap[career]

            for i, step in enumerate(steps, 1):
                st.write(f"{i}. {step}")

            st.write("---")

    fig, ax = plt.subplots()

    ax.bar(careers, scores)

    ax.set_ylabel("Match Percentage")
    ax.set_title("Career Match Scores")

    plt.xticks(rotation=45)

    st.subheader("Career Match Visualization")
    st.pyplot(fig)