from flask import Flask, render_template, request
import os
from pypdf import PdfReader

from skill_extractor import extract_skills
from similarity import calculate_final_score
from ranking import rank_candidates


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# --------------------------------
# CREATE UPLOAD FOLDER
# --------------------------------

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# --------------------------------
# HOME PAGE
# --------------------------------

@app.route("/")
def home():

    return render_template("index.html")


# --------------------------------
# UPLOAD MULTIPLE RESUMES
# --------------------------------

@app.route("/upload", methods=["POST"])
def upload():

    job_title = request.form.get(
        "job_title",
        ""
    )

    job_description = request.form.get(
        "job_description",
        ""
    )

    files = request.files.getlist(
        "resumes"
    )


    if not files:

        return "No resumes selected."


    # --------------------------------
    # EXTRACT JOB SKILLS
    # --------------------------------

    job_skills = extract_skills(
        job_description
    )


    candidates = []


    # --------------------------------
    # PROCESS RESUMES
    # --------------------------------

    for file in files:

        if not file or file.filename == "":
            continue


        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)


        # Read PDF
        reader = PdfReader(filepath)

        text = ""


        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"


        # Resume skills
        resume_skills = extract_skills(
            text
        )


        # Score
        score = calculate_final_score(

            text,

            job_description,

            resume_skills,

            job_skills

        )


        # Matched skills
        matched_skills = []

        for skill in job_skills:

            if skill in resume_skills:

                matched_skills.append(skill)


        # Missing skills
        missing_skills = []

        for skill in job_skills:

            if skill not in resume_skills:

                missing_skills.append(skill)


        # --------------------------------
        # RECOMMENDATION ENGINE
        # --------------------------------

        if score >= 75:

            recommendation = "Highly Recommended"

            reason = (
                "Strong match with the required "
                "skills and job description."
            )

        elif score >= 50:

            recommendation = "Recommended"

            reason = (
                "Good match with several "
                "required skills."
            )

        elif score >= 30:

            recommendation = "Consider"

            reason = (
                "Partial match. Some required "
                "skills are present."
            )

        else:

            recommendation = "Not Recommended"

            reason = (
                "Low match with the required "
                "skills."
            )


        # Candidate
        candidate = {

            "name": file.filename,

            "score": score,

            "skills": resume_skills,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "recommendation": recommendation,

            "reason": reason

        }


        candidates.append(
            candidate
        )


    # --------------------------------
    # RANK CANDIDATES
    # --------------------------------

    ranked_candidates = rank_candidates(
        candidates
    )


    if len(ranked_candidates) == 0:

        return "No valid resumes found."


    # --------------------------------
    # BEST CANDIDATE
    # --------------------------------

    best_candidate = ranked_candidates[0]


    # --------------------------------
    # CREATE RANKING HTML
    # --------------------------------

    ranking_html = ""


    for index, candidate in enumerate(

        ranked_candidates,

        start=1

    ):

        matched = ", ".join(
            candidate["matched_skills"]
        )

        missing = ", ".join(
            candidate["missing_skills"]
        )


        if not matched:

            matched = "None"


        if not missing:

            missing = "None"


        ranking_html += f"""

        <div class="candidate">

            <h3>

                #{index}

                {candidate["name"]}

            </h3>


            <p class="candidate-score">

                {candidate["score"]}%

            </p>


            <p>

                <strong>
                Recommendation:
                </strong>

                {candidate["recommendation"]}

            </p>


            <p>

                <strong>
                Matched Skills:
                </strong>

                {matched}

            </p>


            <p>

                <strong>
                Missing Skills:
                </strong>

                {missing}

            </p>


            <p>

                <strong>
                Reason:
                </strong>

                {candidate["reason"]}

            </p>

        </div>

        """


    # --------------------------------
    # BEST CANDIDATE SKILLS
    # --------------------------------

    best_matched = ", ".join(
        best_candidate["matched_skills"]
    )


    best_missing = ", ".join(
        best_candidate["missing_skills"]
    )


    if not best_matched:

        best_matched = "None"


    if not best_missing:

        best_missing = "None"


    # --------------------------------
    # RESULT PAGE
    # --------------------------------

    return f"""

<!DOCTYPE html>

<html>

<head>

<title>
Resume Screening & Candidate Ranking
</title>


<style>

body {{

    font-family: Arial, sans-serif;

    background-color: #f4f6f8;

    margin: 0;

    padding: 40px;

}}


.container {{

    max-width: 950px;

    margin: auto;

    background-color: white;

    padding: 40px;

    border-radius: 12px;

    box-shadow:
        0 4px 15px rgba(0,0,0,0.1);

}}


h1 {{

    text-align: center;

    color: #222;

}}


h2 {{

    margin-top: 30px;

    color: #333;

}}


.job-box {{

    background-color: #f4f4f4;

    padding: 20px;

    border-radius: 8px;

}}


.best {{

    background-color: #e8f5e9;

    padding: 25px;

    border-radius: 10px;

    border-left: 6px solid #4caf50;

}}


.best-score {{

    font-size: 40px;

    font-weight: bold;

}}


.candidate {{

    background-color: #f8f9fa;

    padding: 20px;

    margin-top: 15px;

    border-radius: 8px;

    border: 1px solid #ddd;

}}


.candidate-score {{

    font-size: 25px;

    font-weight: bold;

}}


.matched {{

    color: green;

}}


.missing {{

    color: #d32f2f;

}}


.reason {{

    background-color: #fff3cd;

    padding: 15px;

    border-radius: 6px;

}}


a {{

    display: block;

    text-align: center;

    margin-top: 30px;

    text-decoration: none;

    font-weight: bold;

}}

</style>

</head>


<body>


<div class="container">


<h1>

Resume Screening & Candidate Ranking

</h1>


<h2>

Job Details

</h2>


<div class="job-box">

<p>

<strong>
Job Title:
</strong>

{job_title}

</p>


<p>

<strong>
Job Description:
</strong>

{job_description}

</p>

</div>


<h2>

🏆 Best Candidate

</h2>


<div class="best">

<h3>

{best_candidate["name"]}

</h3>


<div class="best-score">

{best_candidate["score"]}%

</div>


<p>

<strong>
Recommendation:
</strong>

{best_candidate["recommendation"]}

</p>


<p class="matched">

<strong>
Matched Skills:
</strong>

{best_matched}

</p>


<p class="missing">

<strong>
Missing Skills:
</strong>

{best_missing}

</p>


<div class="reason">

<strong>
Why this candidate?
</strong>

<br><br>

{best_candidate["reason"]}

</div>


</div>


<h2>

Candidate Ranking

</h2>


{ranking_html}


<a href="/">

← Upload More Resumes

</a>


</div>


</body>

</html>

"""


# --------------------------------
# RUN APPLICATION
# --------------------------------

if __name__ == "__main__":

    app.run(debug=True)