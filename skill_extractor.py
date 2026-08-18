# ---------------------------------------
# Skill Extraction
# ---------------------------------------

SKILLS = [

    # Programming Languages
    "Python",
    "Java",
    "C",
    "C++",
    "JavaScript",

    # Web Technologies
    "HTML",
    "CSS",
    "Flask",
    "Django",

    # Databases
    "SQL",
    "MySQL",
    "MongoDB",

    # AI / ML
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Natural Language Processing",
    "NLP",

    # Data
    "Data Science",
    "Data Analysis",

    # Other Technologies
    "Computer Networks",
    "Cyber Security",
    "Cloud Computing",

    # Tools
    "Git",
    "GitHub",

    # Soft Skills
    "Problem Solving",
    "Communication"

]


def extract_skills(text):

    # Convert text to lowercase
    text_lower = text.lower()

    found_skills = []


    # Check each skill
    for skill in SKILLS:

        if skill.lower() in text_lower:

            found_skills.append(skill)


    return found_skills