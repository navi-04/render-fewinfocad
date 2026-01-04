from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/')
def home():
    return "Hello, this Flask app is running on Render"

USERS = {
    "swathi@fewinfocad.com": "swathi123",
    "john@fewinfocad.com": "john456",
    "priya@fewinfocad.com": "priya789"
}

# User-specific dashboard data
USER_DATA = {
    "swathi@fewinfocad.com": {
        "profile": {
            "name": "Swathi",
            "role": "Design Manager",
            "initials": "S",
            "avatarSrc": None,
            "progress": 78,
            "projects": 11,
            "tasks": 56,
            "teams": 12,
        },
        "metrics": {
            "cgpa": "8.290",
            "credits": "42",
        },
        "mentor": {
            "mentorName": "Dr.B.Padmini Devi",
            "mentorTitle": "Professor",
            "advisorName": "Mrs.A.Selvanayagi",
            "advisorTitle": "Assistant Professor",
        },
        "syllabus": [
            {"id": 1, "title": "Disaster Management", "progress": 100},
            {"id": 2, "title": "Computer Networks", "progress": 75},
            {"id": 3, "title": "Explainable AI Programming", "progress": 40},
        ],
        "attendance": {
            "range": "Last month",
            "avgConcentration": 41,
        },
        "notices": [
            {"id": 1, "title": "Assignment Due", "message": "React Project submission by Nov 5", "time": "2 hours ago", "type": "urgent"},
            {"id": 2, "title": "New Material", "message": "Chapter 5 notes uploaded", "time": "5 hours ago", "type": "info"},
            {"id": 3, "title": "Event Reminder", "message": "Tech talk tomorrow at 3 PM", "time": "1 day ago", "type": "event"},
        ],
        "activities": [
            "Uploaded new course material — Design Patterns",
            "Commented on 'React Deep Dive' discussion",
            "New collaboration: UI Redesign project",
        ],
        "stats": {
            "pattern": 41,
            "copyrights": 103,
            "conference": 15,
        },
        "rankings": [
            {"id": 1, "name": "Swathi", "rank": 1, "score": 98, "avatar": "S"},
            {"id": 2, "name": "Priya", "rank": 2, "score": 95, "avatar": "P"},
            {"id": 3, "name": "John", "rank": 3, "score": 92, "avatar": "J"},
        ],
    },
    "john@fewinfocad.com": {
        "profile": {
            "name": "John Doe",
            "role": "Software Engineer",
            "initials": "J",
            "avatarSrc": None,
            "progress": 65,
            "projects": 8,
            "tasks": 42,
            "teams": 5,
        },
        "metrics": {
            "cgpa": "7.850",
            "credits": "38",
        },
        "mentor": {
            "mentorName": "Dr.R.Kumar",
            "mentorTitle": "Associate Professor",
            "advisorName": "Mr.S.Ravi",
            "advisorTitle": "Assistant Professor",
        },
        "syllabus": [
            {"id": 1, "title": "Data Structures", "progress": 85},
            {"id": 2, "title": "Web Development", "progress": 60},
            {"id": 3, "title": "Machine Learning", "progress": 30},
        ],
        "attendance": {
            "range": "Last month",
            "avgConcentration": 35,
        },
        "notices": [
            {"id": 1, "title": "Lab Schedule", "message": "Software lab on Monday 2 PM", "time": "1 hour ago", "type": "info"},
            {"id": 2, "title": "Project Review", "message": "Final year project review next week", "time": "3 hours ago", "type": "urgent"},
            {"id": 3, "title": "Workshop", "message": "React workshop this Saturday", "time": "1 day ago", "type": "event"},
        ],
        "activities": [
            "Submitted assignment for Web Development",
            "Participated in coding competition",
            "Completed Machine Learning quiz",
        ],
        "stats": {
            "pattern": 28,
            "copyrights": 52,
            "conference": 8,
        },
        "rankings": [
            {"id": 1, "name": "Swathi", "rank": 1, "score": 98, "avatar": "S"},
            {"id": 2, "name": "Priya", "rank": 2, "score": 95, "avatar": "P"},
            {"id": 3, "name": "John", "rank": 3, "score": 92, "avatar": "J"},
        ],
    },
    "priya@fewinfocad.com": {
        "profile": {
            "name": "Priya Sharma",
            "role": "Data Analyst",
            "initials": "P",
            "avatarSrc": None,
            "progress": 92,
            "projects": 15,
            "tasks": 68,
            "teams": 8,
        },
        "metrics": {
            "cgpa": "9.100",
            "credits": "48",
        },
        "mentor": {
            "mentorName": "Dr.M.Lakshmi",
            "mentorTitle": "Professor",
            "advisorName": "Mrs.K.Priya",
            "advisorTitle": "Senior Lecturer",
        },
        "syllabus": [
            {"id": 1, "title": "Advanced Python", "progress": 100},
            {"id": 2, "title": "Big Data Analytics", "progress": 90},
            {"id": 3, "title": "Cloud Computing", "progress": 80},
        ],
        "attendance": {
            "range": "Last month",
            "avgConcentration": 48,
        },
        "notices": [
            {"id": 1, "title": "Internship", "message": "Summer internship applications open", "time": "30 mins ago", "type": "urgent"},
            {"id": 2, "title": "Achievement", "message": "Congratulations on winning hackathon!", "time": "2 hours ago", "type": "success"},
            {"id": 3, "title": "Seminar", "message": "Data Science seminar on Friday", "time": "5 hours ago", "type": "event"},
        ],
        "activities": [
            "Published research paper on AI",
            "Led team presentation on Data Analytics",
            "Mentored junior students",
        ],
        "stats": {
            "pattern": 56,
            "copyrights": 145,
            "conference": 22,
        },
        "rankings": [
            {"id": 1, "name": "Swathi", "rank": 1, "score": 98, "avatar": "S"},
            {"id": 2, "name": "Priya", "rank": 2, "score": 95, "avatar": "P"},
            {"id": 3, "name": "John", "rank": 3, "score": 92, "avatar": "J"},
        ],
    }
}

@app.route("/check-login", methods=["POST"])
def check_login():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    # Validate
    if username in USERS and USERS[username] == password:
        return jsonify({"result": True, "userId": username})
    else:
        return jsonify({"result": False})

# @app.route('/todos', methods=['GET', 'POST'])
# def todo_list():
#     global todos

#     task = None

#     if request.method == 'POST':
#         task = request.json.get('task')
#     elif request.method == 'GET' and 'task' in request.args:
#         task = request.args.get('task')
#     else:
#         task = None

#     if task:
#         todos.append(task)
#         return jsonify({"message": "Task added", "todos": todos})

#     return jsonify(todos)


# ==================== DASHBOARD ROUTES ====================

@app.route("/dashboard/<userId>", methods=["GET"])
def get_dashboard(userId):
    try:
        if userId not in USER_DATA:
            return jsonify({"result": False, "message": "User not found"})
        
        user_info = USER_DATA[userId]
        dashboard_data = {
            "result": True,
            "profile": user_info["profile"],
            "metrics": user_info["metrics"],
            "mentor": user_info["mentor"],
            "syllabus": user_info["syllabus"],
            "attendance": user_info["attendance"],
            "notices": user_info["notices"],
            "activities": user_info["activities"],
            "stats": user_info["stats"],
            "rankings": user_info["rankings"],
        }
        return jsonify(dashboard_data)
    except Exception as error:
        print(f"Error: {error}")
        return jsonify({"result": False, "message": "Failed to fetch dashboard data"})


@app.route("/dashboard/profile/<userId>", methods=["GET"])
def get_profile(userId):
    try:
        if userId not in USER_DATA:
            return jsonify({"result": False, "message": "User not found"})
        return jsonify({"result": True, **USER_DATA[userId]["profile"]})
    except Exception as error:
        print(f"Error: {error}")
        return jsonify({"result": False, "message": "Failed to fetch profile data"})


@app.route("/dashboard/metrics/<userId>", methods=["GET"])
def get_metrics(userId):
    try:
        if userId not in USER_DATA:
            return jsonify({"result": False, "message": "User not found"})
        return jsonify({"result": True, **USER_DATA[userId]["metrics"]})
    except Exception as error:
        print(f"Error: {error}")
        return jsonify({"result": False, "message": "Failed to fetch metrics data"})


@app.route("/dashboard/mentor/<userId>", methods=["GET"])
def get_mentor(userId):
    try:
        if userId not in USER_DATA:
            return jsonify({"result": False, "message": "User not found"})
        return jsonify({"result": True, **USER_DATA[userId]["mentor"]})
    except Exception as error:
        print(f"Error: {error}")
        return jsonify({"result": False, "message": "Failed to fetch mentor data"})


@app.route("/dashboard/notices/<userId>", methods=["GET"])
def get_notices(userId):
    try:
        if userId not in USER_DATA:
            return jsonify({"result": False, "message": "User not found"})
        return jsonify({"result": True, "notices": USER_DATA[userId]["notices"]})
    except Exception as error:
        print(f"Error: {error}")
        return jsonify({"result": False, "message": "Failed to fetch notices"})


@app.route("/dashboard/syllabus/<userId>", methods=["GET"])
def get_syllabus(userId):
    try:
        if userId not in USER_DATA:
            return jsonify({"result": False, "message": "User not found"})
        return jsonify({"result": True, "topics": USER_DATA[userId]["syllabus"]})
    except Exception as error:
        print(f"Error: {error}")
        return jsonify({"result": False, "message": "Failed to fetch syllabus data"})


@app.route("/dashboard/attendance/<userId>", methods=["GET"])
def get_attendance(userId):
    try:
        if userId not in USER_DATA:
            return jsonify({"result": False, "message": "User not found"})
        return jsonify({"result": True, **USER_DATA[userId]["attendance"]})
    except Exception as error:
        print(f"Error: {error}")
        return jsonify({"result": False, "message": "Failed to fetch attendance data"})


@app.route("/dashboard/activities/<userId>", methods=["GET"])
def get_activities(userId):
    try:
        if userId not in USER_DATA:
            return jsonify({"result": False, "message": "User not found"})
        return jsonify({"result": True, "activities": USER_DATA[userId]["activities"]})
    except Exception as error:
        print(f"Error: {error}")
        return jsonify({"result": False, "message": "Failed to fetch activities"})


@app.route("/dashboard/stats/<userId>", methods=["GET"])
def get_stats(userId):
    try:
        if userId not in USER_DATA:
            return jsonify({"result": False, "message": "User not found"})
        return jsonify({"result": True, **USER_DATA[userId]["stats"]})
    except Exception as error:
        print(f"Error: {error}")
        return jsonify({"result": False, "message": "Failed to fetch stats data"})


@app.route("/dashboard/rankings/<userId>", methods=["GET"])
def get_rankings(userId):
    try:
        if userId not in USER_DATA:
            return jsonify({"result": False, "message": "User not found"})
        return jsonify({"result": True, "rankings": USER_DATA[userId]["rankings"]})
    except Exception as error:
        print(f"Error: {error}")
        return jsonify({"result": False, "message": "Failed to fetch rankings"})


if __name__ == '__main__':
    app.run(debug=True, port=3001)