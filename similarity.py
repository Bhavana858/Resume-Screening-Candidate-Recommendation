from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_final_score(resume_text, job_description, resume_skills, job_skills):

    # -----------------------------
    # TEXT SIMILARITY
    # -----------------------------

    documents = [
        resume_text,
        job_description
    ]

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )

    text_score = similarity[0][0] * 100


    # -----------------------------
    # SKILL MATCH SCORE
    # -----------------------------

    if len(job_skills) > 0:

        matched_count = 0

        for skill in job_skills:

            if skill in resume_skills:
                matched_count += 1

        skill_score = (
            matched_count / len(job_skills)
        ) * 100

    else:

        skill_score = 0


    # -----------------------------
    # FINAL SCORE
    # -----------------------------

    final_score = (
        (skill_score * 0.70)
        +
        (text_score * 0.30)
    )

    return round(final_score, 2)