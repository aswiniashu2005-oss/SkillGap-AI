from flask import Flask, render_template, request

app = Flask(__name__)

career_skills = {
    "Data Analyst": [
        "Python",
        "SQL",
        "Power BI",
        "Excel",
        "Statistics"
    ],

    "Full Stack Developer": [
        "HTML & CSS",
        "JavaScript",
        "Python",
        "SQL",
        "Java"
    ],

    "Data Scientist": [
        "Python",
        "SQL",
        "Statistics",
        "Machine Learning",
        "Excel"
    ],

    "AI / ML Engineer": [
        "Python",
        "Machine Learning",
        "SQL",
        "Java",
        "Statistics"
    ],

    "UI/UX Designer": [
        "HTML & CSS",
        "JavaScript",
        "Figma",
        "Design",
        "Research"
    ]
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/skills")
def skills():
    return render_template("skills.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    username = request.form.get("username")
    career = request.form.get("career")
    experience = request.form.get("experience")

    current_skills = request.form.getlist("skills")

    required_skills = career_skills.get(career, [])

    # Missing skills
    missing_skills = [
        skill for skill in required_skills
        if skill not in current_skills
    ]

    # Strengths
    strengths = [
        skill for skill in required_skills
        if skill in current_skills
    ]

    # Priority skill gaps
    priority_gaps = []

    for skill in missing_skills:
        priority_gaps.append({
            "skill": skill,
            "priority": "High"
        })

    # Career readiness
    if len(required_skills) > 0:
        readiness = round(
            (len(required_skills) - len(missing_skills))
            / len(required_skills) * 100
        )
    else:
        readiness = 0

    # 4-Week Personalized Roadmap
    roadmap = []

    for i, skill in enumerate(missing_skills[:4]):
        roadmap.append({
            "week": f"Week {i + 1}",
            "skill": skill,
            "task": f"Learn {skill} fundamentals and practice basic exercises"
        })

    # If no missing skills
    if len(roadmap)<4:
        roadmap = [
            {
                "week": "Week 1",
                "skill": "Advanced Skills",
                "task": "Practice advanced concepts"
            },
            {
                "week": "Week 2",
                "skill": "Projects",
                "task": "Build a real-world project"
            },
            {
                "week": "Week 3",
                "skill": "Portfolio",
                "task": "Improve your portfolio"
            },
            {
                "week": "Week 4",
                "skill": "Interview",
                "task": "Prepare for technical interviews"
            }
        ]

    return render_template(
        "result.html",
        username=username,
        career=career,
        strengths=strengths,
        priority_gaps=priority_gaps,
        experience=experience,
        current_skills=current_skills,
        required_skills=required_skills,
        missing_skills=missing_skills,
        readiness=readiness,
        roadmap=roadmap
    )


if __name__ == "__main__":
    app.run(debug=True)