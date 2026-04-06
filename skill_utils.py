import re
from role_data import job_roles


# -----------------------------
# CLEAN TEXT
# -----------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# -----------------------------
# NORMALIZE SKILL
# -----------------------------
def normalize_skill(skill):
    return skill.lower().replace(".", " ").replace("-", " ").strip()


# -----------------------------
# CALCULATE SKILL SCORE
# -----------------------------
def calculate_skill_score(role, user_input):
    if role not in job_roles:
        return 0, []

    required = job_roles[role]["skills_required"]

    text = clean_text(user_input)
    words = set(text.split())

    matched = []
    score_count = 0

    for skill in required:
        norm = normalize_skill(skill)
        tokens = norm.split()

        # ✅ Exact match (best case)
        if norm in text:
            matched.append(skill)
            score_count += 1

        # ✅ Token match (ALL tokens must exist)
        elif all(token in words for token in tokens):
            matched.append(skill)
            score_count += 0.5

        # ✅ Compact match (handles "machinelearning")
        elif norm.replace(" ", "") in text.replace(" ", ""):
            matched.append(skill)
            score_count += 1

    total = len(required)
    score = (score_count / total) * 100 if total else 0

    return round(min(score, 100), 2), list(set(matched))


# -----------------------------
# SKILL GAP
# -----------------------------
def get_skill_gap(role, user_input):
    if role not in job_roles:
        return [], []

    required = job_roles[role]["skills_required"]

    text = clean_text(user_input)
    words = set(text.split())

    missing = []

    for skill in required:
        norm = normalize_skill(skill)
        tokens = norm.split()

        if (
            norm in text
            or all(token in words for token in tokens)
            or norm.replace(" ", "") in text.replace(" ", "")
        ):
            continue
        else:
            missing.append(skill)

    return required, missing