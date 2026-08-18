# Resume Screening & Candidate Recommendation System

## 📌 Project Overview

The Resume Screening & Candidate Recommendation System is an AI-based recruitment application developed using Python and Flask.

The system helps recruiters analyze multiple resumes, extract candidate skills, compare them with a given job description, calculate a match score, rank candidates, and recommend suitable candidates.

## 🎯 Objectives

- Automate the resume screening process
- Extract useful information from PDF resumes
- Identify candidate skills
- Compare resumes with job requirements
- Calculate resume-job similarity
- Rank multiple candidates
- Recommend suitable candidates

## ✨ Key Features

### 1. Resume Parsing
The system reads PDF resumes and extracts their text using the PyPDF library.

### 2. NLP-Based Skill Extraction
The system analyzes resume text and identifies relevant technical and soft skills.

### 3. Job Description Analysis
Recruiters can enter a job title and job description with required skills.

### 4. Similarity Analysis
The system compares the resume and job description using TF-IDF and cosine similarity.

### 5. Skill Matching
Required job skills are compared with the candidate's extracted skills.

### 6. Candidate Ranking
Multiple resumes can be uploaded and candidates are ranked according to their match scores.

### 7. Recommendation Engine
Candidates are classified as:

- Highly Recommended
- Recommended
- Consider
- Not Recommended

## 🛠️ Technologies Used

- Python
- Flask
- Natural Language Processing (NLP)
- TF-IDF
- Cosine Similarity
- PyPDF
- Scikit-learn
- HTML
- CSS

## 📂 Project Structure

```text
Resume-Screening-Candidate-Recommendation/
│
├── app.py
├── skill_extractor.py
├── similarity.py
├── ranking.py
├── requirements.txt
│
└── templates/
    └── index.html
