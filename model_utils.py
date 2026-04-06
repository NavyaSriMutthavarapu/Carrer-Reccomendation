import joblib
import numpy as np

model = joblib.load("career_pipeline.pkl")
label_encoder = joblib.load("label_encoder.pkl")


def predict_top_roles_with_scores(text):
    scores_raw = model.decision_function([text])[0]

    # Softmax
    scores = np.exp(scores_raw) / np.sum(np.exp(scores_raw))

    top_indices = np.argsort(scores)[::-1][:3]

    roles = label_encoder.inverse_transform(top_indices)
    scores = scores[top_indices]

    text_lower = text.lower()

    # -----------------------------
    # BOOST LOGIC (FIXED)
    # -----------------------------
    for i, role in enumerate(roles):

        # DATA ANALYST
        if role == "Data Analyst":
            if any(skill in text_lower for skill in [
                "sql", "excel", "power bi", "tableau",
                "dashboard", "reporting"
            ]):
                scores[i] += 0.20

        # DATA SCIENTIST
        elif role == "Data Scientist":
            if any(skill in text_lower for skill in [
                "machine learning", "deep learning", "nlp",
                "tensorflow", "pytorch"
            ]):
                scores[i] += 0.20

        # DATA ENGINEER
        elif role == "Data Engineer":
            if any(skill in text_lower for skill in [
                "etl", "pipeline", "hadoop", "spark"
            ]):
                scores[i] += 0.20

        # WEB DEVELOPER (🔥 frontend fix)
        elif role == "Web Developer":
            if any(skill in text_lower for skill in [
                "frontend", "react", "angular",
                "html", "css", "javascript"
            ]):
                scores[i] += 0.25

        # SOFTWARE ENGINEER
        elif role == "Software Engineer":
            if any(skill in text_lower for skill in [
                "software engineer", "software development", "developer",
                "backend", "api", "flask", "django", "node",
                "microservices", "system design", "programming"
                ]):
                scores[i] += 0.30   

        # JAVA
        elif role == "Java Developer":
            if any(skill in text_lower for skill in [
                "java", "spring", "hibernate"
            ]):
                scores[i] += 0.20

        # QA
        elif role == "QA Engineer":
            if any(skill in text_lower for skill in [
                "testing", "selenium", "automation"
            ]):
                scores[i] += 0.15

        # DEVOPS
        elif role == "DevOps Engineer":
            if any(skill in text_lower for skill in [
                "docker", "kubernetes", "jenkins", "aws"
            ]):
                scores[i] += 0.20

        # SYSTEM ADMIN
        elif role == "System Administrator":
            if any(skill in text_lower for skill in [
                "linux", "server", "administration"
            ]):
                scores[i] += 0.20

        # NETWORK
        elif role == "Network Engineer":
            if any(skill in text_lower for skill in [
                "network", "routing", "tcp ip"
            ]):
                scores[i] += 0.20

        # BUSINESS ANALYST
        elif role == "Business Analyst":
            if any(skill in text_lower for skill in [
                "requirements", "stakeholders", "documentation"
            ]):
                scores[i] += 0.20

        # SAP (🔥 important)
        elif role == "SAP Consultant":
            if any(skill in text_lower for skill in [
                "sap", "sap fico", "sap mm", "sap sd"
            ]):
                scores[i] += 0.30

        # ARCHITECT (🔥 important)
        elif role == "Architect":
            if any(skill in text_lower for skill in [
                "architecture", "system design"
            ]):
                scores[i] += 0.30

    # -----------------------------
    # SORT AFTER BOOST
    # -----------------------------
    sorted_idx = np.argsort(scores)[::-1]

    roles = roles[sorted_idx]
    scores = scores[sorted_idx]

    return roles.tolist(), scores.tolist()


def get_confidence_label(score):
    if score > 0.75:
        return "High Confidence 🔥"
    elif score > 0.5:
        return "Moderate Confidence 👍"
    else:
        return "Low Confidence ⚠️"