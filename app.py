import streamlit as st
import joblib

from model_utils import predict_top_roles_with_scores, get_confidence_label
from skill_utils import calculate_skill_score, get_skill_gap
from role_data import job_roles
from resume_utils import extract_text_from_pdf


# -----------------------------
# LOAD RELATED ROLES (FIXED)
# -----------------------------
role_to_titles = joblib.load("clean_role_to_titles.pkl")


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Career Advisor", layout="centered")

st.title("🚀 AI Career Advisor")
st.write("Upload your resume or enter your skills")


# -----------------------------
# INPUT
# -----------------------------
user_input = st.text_area("📝 Enter your skills or resume text", height=150)
uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])


# -----------------------------
# ANALYZE
# -----------------------------
if st.button("🚀 Analyze"):

    if uploaded_file is not None:
        user_input = extract_text_from_pdf(uploaded_file)

    if not user_input or not user_input.strip():
        st.warning("⚠️ Please enter valid input")
        st.stop()

    roles, scores = predict_top_roles_with_scores(user_input)
    best_role = roles[0]

    # CURRENT ROLE
    st.markdown("## 🧾 Current Role")
    st.success(best_role)
    st.write(f"Confidence: {get_confidence_label(scores[0])}")

    # TOP MATCHES
    st.markdown("### 🎯 Top Career Matches")
    for i in range(len(roles)):
        st.write(f"{roles[i]} → {round(scores[i]*100, 2)}%")
        st.progress(int(scores[i]*100))

    # WHY ROLE
    st.markdown("### 💡 Why this role?")
    skills = job_roles.get(best_role, {}).get("skills_required", [])
    user_text = user_input.lower()

    matched_skills = [s for s in skills if s.lower() in user_text]

    if matched_skills:
        st.write(f"Based on your skills: {', '.join(matched_skills[:5])}")
    else:
        st.write("Based on overall resume content")

    # RELATED ROLES
    st.markdown("### 💼 Related Job Titles")
    sub_roles = list(role_to_titles.get(best_role, []))

    if sub_roles:
        for role in sub_roles[:5]:
            st.write(f"👉 {role}")
    else:
        st.write("No related roles found")

    # SKILL MATCH
    score, matched = calculate_skill_score(best_role, user_input)

    st.markdown(f"### 🧠 Match Score: {score}%")

    if score >= 75:
        st.success("Excellent match 🔥")
    elif score >= 50:
        st.info("Good match 👍")
    else:
        st.warning("Needs improvement ⚠️")

    if matched:
        st.write("✔ Matched Skills:")
        for m in matched[:5]:
            st.write(f"✔ {m}")

    # SKILL GAP
    _, missing = get_skill_gap(best_role, user_input)

    st.markdown("### ⚠️ Skill Gap")

    if score >= 70:
        st.success("You are ready! 🎉")
    else:
        if missing:
            for skill in missing[:5]:
                st.write(f"❌ {skill}")

    # ACTION PLAN
    st.markdown("### 🚀 Action Plan")

    if score >= 70:
        st.success("🎉 Start applying!")
    elif missing:
        for skill in missing[:3]:
            st.write(f"👉 Learn {skill}")
    else:
        st.warning("⚠️ Add more skills")