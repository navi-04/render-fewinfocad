from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import random

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


# ==================== ATTENDANCE DATA ====================

def generate_comprehensive_attendance_data():
    """Generate attendance data matching the old frontend structure exactly"""
    
    attendance_records = [
        # January 2026 data
        {
            "id": 1,
            "date": "2026-01-15",
            "period": "Period 1",
            "subject": "Data Structures",
            "faculty": "Dr. Smith",
            "status": "Present",
            "timeIn": "09:00",
            "timeOut": "09:50"
        },
        {
            "id": 2,
            "date": "2026-01-15",
            "period": "Period 2",
            "subject": "Database Systems",
            "faculty": "Dr. Johnson",
            "status": "Present",
            "timeIn": "10:00",
            "timeOut": "10:50"
        },
        {
            "id": 3,
            "date": "2026-01-15",
            "period": "Period 3",
            "subject": "Software Engineering",
            "faculty": "Dr. Williams",
            "status": "Late",
            "timeIn": "11:15",
            "timeOut": "11:50"
        },
        {
            "id": 4,
            "date": "2026-01-14",
            "period": "Period 1",
            "subject": "Data Structures",
            "faculty": "Dr. Smith",
            "status": "Present",
            "timeIn": "09:00",
            "timeOut": "09:50"
        },
        {
            "id": 5,
            "date": "2026-01-14",
            "period": "Period 2",
            "subject": "Database Systems",
            "faculty": "Dr. Johnson",
            "status": "Absent",
            "timeIn": "",
            "timeOut": ""
        },
        {
            "id": 6,
            "date": "2026-01-13",
            "period": "Period 1",
            "subject": "Data Structures",
            "faculty": "Dr. Smith",
            "status": "Present",
            "timeIn": "09:00",
            "timeOut": "09:50"
        },
        {
            "id": 7,
            "date": "2026-01-13",
            "period": "Period 2",
            "subject": "Web Development",
            "faculty": "Ms. Brown",
            "status": "Present",
            "timeIn": "10:00",
            "timeOut": "10:50"
        },
        {
            "id": 8,
            "date": "2026-01-12",
            "period": "Period 1",
            "subject": "Operating Systems",
            "faculty": "Dr. Wilson",
            "status": "Late",
            "timeIn": "09:20",
            "timeOut": "09:50"
        },
        {
            "id": 9,
            "date": "2026-01-11",
            "period": "Period 1",
            "subject": "Computer Networks",
            "faculty": "Prof. Davis",
            "status": "Present",
            "timeIn": "09:00",
            "timeOut": "09:50"
        },
        {
            "id": 10,
            "date": "2026-01-10",
            "period": "Period 2",
            "subject": "Software Engineering",
            "faculty": "Dr. Williams",
            "status": "Present",
            "timeIn": "10:00",
            "timeOut": "10:50"
        },
        # December 2025 data
        {
            "id": 11,
            "date": "2025-12-20",
            "period": "Period 1",
            "subject": "Data Structures",
            "faculty": "Dr. Smith",
            "status": "Present",
            "timeIn": "09:00",
            "timeOut": "09:50"
        },
        {
            "id": 12,
            "date": "2025-12-19",
            "period": "Period 2",
            "subject": "Database Systems",
            "faculty": "Dr. Johnson",
            "status": "Absent",
            "timeIn": "",
            "timeOut": ""
        },
        {
            "id": 13,
            "date": "2025-12-18",
            "period": "Period 1",
            "subject": "Web Development",
            "faculty": "Ms. Brown",
            "status": "Present",
            "timeIn": "09:00",
            "timeOut": "09:50"
        },
        {
            "id": 14,
            "date": "2025-12-17",
            "period": "Period 3",
            "subject": "Operating Systems",
            "faculty": "Dr. Wilson",
            "status": "Late",
            "timeIn": "11:25",
            "timeOut": "11:50"
        },
        {
            "id": 15,
            "date": "2025-12-16",
            "period": "Period 1",
            "subject": "Computer Networks",
            "faculty": "Prof. Davis",
            "status": "Present",
            "timeIn": "09:00",
            "timeOut": "09:50"
        },
        # November 2025 data
        {
            "id": 16,
            "date": "2025-11-25",
            "period": "Period 2",
            "subject": "Software Engineering",
            "faculty": "Dr. Williams",
            "status": "Present",
            "timeIn": "10:00",
            "timeOut": "10:50"
        },
        {
            "id": 17,
            "date": "2025-11-24",
            "period": "Period 1",
            "subject": "Data Structures",
            "faculty": "Dr. Smith",
            "status": "Absent",
            "timeIn": "",
            "timeOut": ""
        },
        {
            "id": 18,
            "date": "2025-11-23",
            "period": "Period 3",
            "subject": "Database Systems",
            "faculty": "Dr. Johnson",
            "status": "Present",
            "timeIn": "11:00",
            "timeOut": "11:50"
        },
        {
            "id": 19,
            "date": "2025-11-22",
            "period": "Period 1",
            "subject": "Web Development",
            "faculty": "Ms. Brown",
            "status": "Present",
            "timeIn": "09:00",
            "timeOut": "09:50"
        },
        {
            "id": 20,
            "date": "2025-11-21",
            "period": "Period 2",
            "subject": "Operating Systems",
            "faculty": "Dr. Wilson",
            "status": "Present",
            "timeIn": "10:00",
            "timeOut": "10:50"
        }
    ]
    
    # Generate more records dynamically for the past 60 days
    subjects = ["Data Structures", "Database Systems", "Software Engineering", 
                "Web Development", "Operating Systems", "Computer Networks"]
    faculties = ["Dr. Smith", "Dr. Johnson", "Dr. Williams", "Ms. Brown", "Dr. Wilson", "Prof. Davis"]
    periods = ["Period 1", "Period 2", "Period 3"]
    statuses = ["Present", "Present", "Present", "Present", "Late", "Absent"]  # Weighted towards Present
    
    current_id = len(attendance_records) + 1
    today = datetime.now()
    
    for days_ago in range(21, 60):
        date = today - timedelta(days=days_ago)
        if date.weekday() < 5:  # Weekdays only
            for _ in range(random.randint(2, 3)):  # 2-3 classes per day
                subject = random.choice(subjects)
                faculty = random.choice(faculties)
                period = random.choice(periods)
                status = random.choice(statuses)
                
                attendance_records.append({
                    "id": current_id,
                    "date": date.strftime("%Y-%m-%d"),
                    "period": period,
                    "subject": subject,
                    "faculty": faculty,
                    "status": status,
                    "timeIn": "" if status == "Absent" else f"{random.randint(9, 16)}:{random.choice(['00', '15', '20'])}",
                    "timeOut": "" if status == "Absent" else f"{random.randint(9, 16)}:50"
                })
                current_id += 1
    
    return attendance_records

# ==================== ATTENDANCE ROUTES ====================

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    """Get all attendance records - exactly matching old frontend structure"""
    try:
        attendance_records = generate_comprehensive_attendance_data()
        
        return jsonify({
            "result": True,
            "message": "Attendance data fetched successfully",
            "data": attendance_records
        }), 200
    except Exception as e:
        return jsonify({
            "result": False,
            "message": f"Error fetching attendance data: {str(e)}",
            "data": None
        }), 500

@app.route('/api/attendance/stats', methods=['GET'])
def get_attendance_statistics():
    """Get attendance statistics"""
    try:
        records = generate_comprehensive_attendance_data()
        
        total = len(records)
        present = sum(1 for r in records if r["status"] == "Present")
        absent = sum(1 for r in records if r["status"] == "Absent")
        late = sum(1 for r in records if r["status"] == "Late")
        percentage = round((present + late) / total * 100, 1) if total > 0 else 0
        
        return jsonify({
            "result": True,
            "message": "Attendance statistics fetched successfully",
            "data": {
                "total": total,
                "present": present,
                "absent": absent,
                "late": late,
                "percentage": percentage
            }
        }), 200
    except Exception as e:
        return jsonify({
            "result": False,
            "message": f"Error fetching statistics: {str(e)}",
            "data": None
        }), 500


# ==================== CLUBS DATA ====================

CLUBS_DATA = {
    "myClubs": [
        {
            "id": 1,
            "name": "Coding Club",
            "shortDescription": "Programming enthusiasts exploring new technologies",
            "description": "A community of passionate programmers and developers who collaborate on projects, organize hackathons, and explore cutting-edge technologies. Weekly workshops and coding sessions help members improve their skills.",
            "meetingSchedule": "Every Tuesday at 5:00 PM",
            "location": "Computer Science Building, Room 103",
            "memberCount": 42,
            "category": "Academic",
            "image": "https://images.unsplash.com/photo-1580894742597-87bc8789db3d?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "tags": ["Programming", "Technology", "Projects"],
            "contact": "codingclub@example.edu",
            "gallery": [
                {
                    "id": 1,
                    "title": "Hackathon 2023",
                    "image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                },
                {
                    "id": 2,
                    "title": "Workshop on AI",
                    "image": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                },
                {
                    "id": 3,
                    "title": "Team Coding Challenge",
                    "image": "https://images.unsplash.com/photo-1531482615713-2afd69097998?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                },
                {
                    "id": 4,
                    "title": "Web Development Session",
                    "image": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                }
            ],
            "upcomingEvents": [
                {
                    "id": 1,
                    "title": "Annual Hackathon",
                    "date": "December 10-12, 2026",
                    "time": "9:00 AM - 6:00 PM",
                    "location": "Computer Science Building",
                    "description": "A 48-hour coding marathon where teams compete to build innovative software solutions."
                },
                {
                    "id": 2,
                    "title": "Introduction to Machine Learning",
                    "date": "November 15, 2026",
                    "time": "4:00 PM - 6:00 PM",
                    "location": "Room 103, CS Building",
                    "description": "Workshop covering the basics of machine learning algorithms and their applications."
                }
            ]
        },
        {
            "id": 2,
            "name": "Photography Society",
            "shortDescription": "Capturing moments and sharing photographic techniques",
            "description": "A creative space for photography enthusiasts to share their work, learn new techniques, and participate in photo walks. The club organizes exhibitions and competitions throughout the academic year.",
            "meetingSchedule": "Every Saturday at 2:00 PM",
            "location": "Arts Building, Room 215",
            "memberCount": 38,
            "category": "Creative",
            "image": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "tags": ["Photography", "Creative", "Arts"],
            "contact": "photosociety@example.edu",
            "gallery": [
                {
                    "id": 1,
                    "title": "Campus Photowalk",
                    "image": "https://images.unsplash.com/photo-1554080353-a576cf803bda?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                },
                {
                    "id": 2,
                    "title": "Portrait Photography Session",
                    "image": "https://images.unsplash.com/photo-1597393353415-b3730f3940fe?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                },
                {
                    "id": 3,
                    "title": "Annual Exhibition",
                    "image": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                },
                {
                    "id": 4,
                    "title": "Nature Photography Workshop",
                    "image": "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                }
            ],
            "upcomingEvents": [
                {
                    "id": 1,
                    "title": "Campus Photography Contest",
                    "date": "November 20, 2026",
                    "time": "1:00 PM - 5:00 PM",
                    "location": "Arts Building Gallery",
                    "description": "Annual photography competition with categories for landscape, portrait, and abstract photography."
                },
                {
                    "id": 2,
                    "title": "Night Photography Workshop",
                    "date": "December 5, 2026",
                    "time": "7:00 PM - 10:00 PM",
                    "location": "Campus Garden",
                    "description": "Learn techniques for capturing stunning night-time photographs with various lighting conditions."
                }
            ]
        }
    ],
    "otherClubs": [
        {
            "id": 3,
            "name": "Debate Club",
            "shortDescription": "Fostering public speaking and critical thinking skills",
            "description": "A platform for students to develop their oratory and critical thinking skills through structured debates on current affairs and philosophical topics. Members participate in intercollegiate competitions.",
            "meetingSchedule": "Every Wednesday at 4:30 PM",
            "location": "Liberal Arts Building, Room 122",
            "memberCount": 25,
            "category": "Academic",
            "image": "https://images.unsplash.com/photo-1529390079861-591de354faf5?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "tags": ["Debate", "Public Speaking", "Current Affairs"],
            "contact": "debateclub@example.edu",
            "gallery": [
                {
                    "id": 1,
                    "title": "Intercollegiate Debate Finals",
                    "image": "https://images.unsplash.com/photo-1517048676732-d65bc937f952?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                },
                {
                    "id": 2,
                    "title": "Public Speaking Workshop",
                    "image": "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                },
                {
                    "id": 3,
                    "title": "Mock Parliament Session",
                    "image": "https://images.unsplash.com/photo-1560439514-4e9645039924?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                }
            ],
            "upcomingEvents": [
                {
                    "id": 1,
                    "title": "National Debate Championship",
                    "date": "November 25-26, 2026",
                    "time": "9:00 AM - 5:00 PM",
                    "location": "University Auditorium",
                    "description": "Two-day national level debate competition with teams from across the country."
                }
            ]
        },
        {
            "id": 4,
            "name": "Sports Club",
            "shortDescription": "Promoting physical fitness and sportsmanship",
            "description": "A club dedicated to promoting physical fitness, team spirit, and sportsmanship. Various sports teams operate under this club, participating in inter-university tournaments and organizing friendly matches.",
            "meetingSchedule": "Every Monday, Wednesday, Friday at 6:00 PM",
            "location": "University Sports Complex",
            "memberCount": 75,
            "category": "Sports",
            "image": "https://images.unsplash.com/photo-1517649763962-0c623066013b?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "tags": ["Sports", "Fitness", "Team Building"],
            "contact": "sportsclub@example.edu",
            "gallery": [
                {
                    "id": 1,
                    "title": "Inter-University Football Match",
                    "image": "https://images.unsplash.com/photo-1529626455594-4ff0831eab8c?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                },
                {
                    "id": 2,
                    "title": "Basketball Tournament",
                    "image": "https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                },
                {
                    "id": 3,
                    "title": "Annual Sports Day",
                    "image": "https://images.unsplash.com/photo-1514516872074-4b6f3e6f3e6f?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                }
            ],
            "upcomingEvents": [
                {
                    "id": 1,
                    "title": "Annual Sports Meet",
                    "date": "January 15-16, 2027",
                    "time": "8:00 AM - 5:00 PM",
                    "location": "University Sports Complex",
                    "description": "Join us for the annual sports meet featuring athletics, team games, and fun activities."
                },
                {
                    "id": 2,
                    "title": "Yoga and Meditation Workshop",
                    "date": "February 10, 2027",
                    "time": "7:00 AM - 9:00 AM",
                    "location": "Campus Quad",
                    "description": "A workshop focusing on yoga techniques and meditation practices for overall well-being."
                }
            ]
        },
        {
            "id": 5,
            "name": "Environmental Society",
            "shortDescription": "Working towards a greener and sustainable campus",
            "description": "An environmental advocacy group committed to raising awareness about ecological issues and implementing sustainable practices on campus. The club organizes tree plantation drives, clean-up initiatives, and awareness campaigns.",
            "meetingSchedule": "Every Friday at 3:00 PM",
            "location": "Science Block, Room 301",
            "memberCount": 32,
            "category": "Social",
            "image": "https://images.unsplash.com/photo-1496437792604-55ca7c5c3f6f?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "tags": ["Environment", "Sustainability", "Community Service"],
            "contact": "ecosociety@example.edu",
            "gallery": [
                {
                    "id": 1,
                    "title": "Tree Plantation Drive",
                    "image": "https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                },
                {
                    "id": 2,
                    "title": "Campus Clean-up",
                    "image": "https://images.unsplash.com/photo-1514516872074-4b6f3e6f3e6f?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                },
                {
                    "id": 3,
                    "title": "Recycling Awareness Campaign",
                    "image": "https://images.unsplash.com/photo-1529626455594-4ff0831eab8c?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                }
            ],
            "upcomingEvents": [
                {
                    "id": 1,
                    "title": "Sustainability Workshop",
                    "date": "March 5, 2027",
                    "time": "10:00 AM - 1:00 PM",
                    "location": "Room 301, Science Block",
                    "description": "Workshop on sustainable practices and how to reduce your carbon footprint."
                },
                {
                    "id": 2,
                    "title": "Earth Day Celebration",
                    "date": "April 22, 2027",
                    "time": "All day event",
                    "location": "Campus Wide",
                    "description": "Join us for a day of activities, workshops, and talks focused on environmental conservation."
                }
            ]
        },
        {
            "id": 6,
            "name": "Music Band",
            "shortDescription": "Creating melodies and performing at campus events",
            "description": "A group of musicians who come together to create, practice, and perform music at various campus events. The band covers various genres and encourages original compositions from its members.",
            "meetingSchedule": "Every Thursday at 5:30 PM",
            "location": "Fine Arts Building, Music Room",
            "memberCount": 18,
            "category": "Creative",
            "image": "https://images.unsplash.com/photo-1516280440614-37939bbacd81?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
            "tags": ["Music", "Performance", "Creative"],
            "contact": "musicband@example.edu",
            "gallery": [
                {
                    "id": 1,
                    "title": "Campus Concert",
                    "image": "https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                },
                {
                    "id": 2,
                    "title": "Music Workshop",
                    "image": "https://images.unsplash.com/photo-1514516872074-4b6f3e6f3e6f?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                },
                {
                    "id": 3,
                    "title": "Battle of the Bands",
                    "image": "https://images.unsplash.com/photo-1529626455594-4ff0831eab8c?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
                }
            ],
            "upcomingEvents": [
                {
                    "id": 1,
                    "title": "Spring Music Fest",
                    "date": "April 15, 2027",
                    "time": "2:00 PM - 10:00 PM",
                    "location": "Campus Amphitheater",
                    "description": "Annual music festival featuring performances by student bands and artists."
                },
                {
                    "id": 2,
                    "title": "Songwriting Workshop",
                    "date": "May 10, 2027",
                    "time": "3:00 PM - 6:00 PM",
                    "location": "Music Room, Fine Arts Building",
                    "description": "Workshop on songwriting techniques and music composition."
                }
            ]
        }
    ]
}

# ==================== CLUBS ROUTES ====================

@app.route('/clubs/<user_id>', methods=['GET'])
def get_clubs_data(user_id):
    """Get all clubs data - exactly matching old frontend structure"""
    try:
        return jsonify({
            "result": True,
            "message": "Clubs data fetched successfully",
            "myClubs": CLUBS_DATA["myClubs"],
            "otherClubs": CLUBS_DATA["otherClubs"]
        }), 200
    except Exception as e:
        return jsonify({
            "result": False,
            "message": f"Error fetching clubs data: {str(e)}"
        }), 500

@app.route('/clubs/my/<user_id>', methods=['GET'])
def get_my_clubs(user_id):
    """Get clubs that user is a member of"""
    try:
        return jsonify({
            "result": True,
            "message": "User clubs fetched successfully",
            "data": CLUBS_DATA["myClubs"]
        }), 200
    except Exception as e:
        return jsonify({
            "result": False,
            "message": f"Error fetching user clubs: {str(e)}"
        }), 500

@app.route('/clubs/all', methods=['GET'])
def get_all_clubs():
    """Get all available clubs"""
    try:
        all_clubs = CLUBS_DATA["myClubs"] + CLUBS_DATA["otherClubs"]
        return jsonify({
            "result": True,
            "message": "All clubs fetched successfully",
            "data": all_clubs
        }), 200
    except Exception as e:
        return jsonify({
            "result": False,
            "message": f"Error fetching clubs: {str(e)}"
        }), 500

@app.route('/clubs/details/<int:club_id>', methods=['GET'])
def get_club_details(club_id):
    """Get detailed information about a specific club"""
    try:
        all_clubs = CLUBS_DATA["myClubs"] + CLUBS_DATA["otherClubs"]
        club = next((c for c in all_clubs if c['id'] == club_id), None)
        
        if club:
            return jsonify({
                "result": True,
                "message": "Club details fetched successfully",
                "data": club
            }), 200
        else:
            return jsonify({
                "result": False,
                "message": "Club not found",
                "data": None
            }), 404
    except Exception as e:
        return jsonify({
            "result": False,
            "message": f"Error fetching club details: {str(e)}"
        }), 500

@app.route('/clubs/join', methods=['POST'])
def join_club():
    """Join a club"""
    try:
        data = request.get_json()
        user_id = data.get('userId')
        club_id = data.get('clubId')
        
        return jsonify({
            "result": True,
            "message": "Successfully joined the club",
            "data": {"userId": user_id, "clubId": club_id}
        }), 200
    except Exception as e:
        return jsonify({
            "result": False,
            "message": f"Error joining club: {str(e)}"
        }), 500

@app.route('/clubs/leave', methods=['POST'])
def leave_club():
    """Leave a club"""
    try:
        data = request.get_json()
        user_id = data.get('userId')
        club_id = data.get('clubId')
        
        return jsonify({
            "result": True,
            "message": "Successfully left the club",
            "data": {"userId": user_id, "clubId": club_id}
        }), 200
    except Exception as e:
        return jsonify({
            "result": False,
            "message": f"Error leaving club: {str(e)}"
        }), 500

@app.route('/clubs/search', methods=['GET'])
def search_clubs():
    """Search clubs"""
    try:
        query = request.args.get('q', '').lower()
        all_clubs = CLUBS_DATA["myClubs"] + CLUBS_DATA["otherClubs"]
        
        if not query:
            return jsonify({
                "result": True,
                "message": "All clubs returned",
                "data": all_clubs
            }), 200
        
        filtered = [c for c in all_clubs if query in c['name'].lower() or query in c['description'].lower()]
        
        return jsonify({
            "result": True,
            "message": f"Found {len(filtered)} clubs",
            "data": filtered
        }), 200
    except Exception as e:
        return jsonify({
            "result": False,
            "message": f"Error searching clubs: {str(e)}"
        }), 500


# ==================== LIVE STREAMS DATA ====================

LIVE_STREAMS_DATA = {
    "currentStreams": [
        {
            "id": 1,
            "title": "Annual College Cultural Fest - Day 1",
            "description": "Live coverage of the opening ceremony and performances from the Annual Cultural Festival.",
            "thumbnail": "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
            "viewerCount": 1250,
            "startTime": "10:00 AM",
            "date": "Today",
            "streamUrl": "#",
            "hostedBy": "Cultural Committee",
            "location": "Main Auditorium"
        },
        {
            "id": 2,
            "title": "Guest Lecture: Future of AI in Education",
            "description": "Distinguished Professor Dr. Emily Chen discusses how artificial intelligence is transforming education systems worldwide.",
            "thumbnail": "https://images.unsplash.com/photo-1531482615713-2afd69097998?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
            "viewerCount": 875,
            "startTime": "2:30 PM",
            "date": "Today",
            "streamUrl": "#",
            "hostedBy": "Computer Science Department",
            "location": "CS Lecture Hall"
        },
        {
            "id": 3,
            "title": "Inter-College Basketball Finals",
            "description": "Live stream of the championship match between our college team and State University.",
            "thumbnail": "https://images.unsplash.com/photo-1519861531473-9200262188bf?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
            "viewerCount": 2340,
            "startTime": "4:00 PM",
            "date": "Today",
            "streamUrl": "#",
            "hostedBy": "Sports Department",
            "location": "College Stadium"
        }
    ],
    "upcomingStreams": [
        {
            "id": 4,
            "title": "Placement Training Workshop",
            "description": "Career guidance experts share tips on resume building, interview skills, and placement preparation.",
            "thumbnail": "https://images.unsplash.com/photo-1552581234-26160f608093?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
            "scheduledDate": "Tomorrow",
            "scheduledTime": "11:00 AM",
            "hostedBy": "Placement Cell",
            "location": "Seminar Hall B",
            "remindMeEnabled": False
        },
        {
            "id": 5,
            "title": "Annual College Cultural Fest - Day 2",
            "description": "Day 2 of the cultural fest featuring music performances, dance competitions, and more.",
            "thumbnail": "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
            "scheduledDate": "Tomorrow",
            "scheduledTime": "10:00 AM",
            "hostedBy": "Cultural Committee",
            "location": "Main Auditorium",
            "remindMeEnabled": False
        },
        {
            "id": 6,
            "title": "Research Symposium: Renewable Energy",
            "description": "Students and faculty present their research findings on renewable energy solutions.",
            "thumbnail": "https://images.unsplash.com/photo-1497435334941-8c899ee9e8e9?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
            "scheduledDate": "Jan 15, 2026",
            "scheduledTime": "1:00 PM",
            "hostedBy": "Engineering Department",
            "location": "Engineering Block",
            "remindMeEnabled": False
        },
        {
            "id": 7,
            "title": "Alumni Connect: Entrepreneurship Journey",
            "description": "Successful alumni share their entrepreneurial journeys and insights with current students.",
            "thumbnail": "https://images.unsplash.com/photo-1556761175-b413da4baf72?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
            "scheduledDate": "Jan 18, 2026",
            "scheduledTime": "3:00 PM",
            "hostedBy": "Alumni Association",
            "location": "Business School",
            "remindMeEnabled": False
        },
        {
            "id": 8,
            "title": "Tech Talk: Cloud Computing Trends",
            "description": "Industry experts discuss the latest trends and innovations in cloud computing technology.",
            "thumbnail": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
            "scheduledDate": "Jan 20, 2026",
            "scheduledTime": "2:00 PM",
            "hostedBy": "IT Department",
            "location": "Tech Auditorium",
            "remindMeEnabled": False
        },
        {
            "id": 9,
            "title": "Annual Debate Championship",
            "description": "Inter-departmental debate competition on current affairs and social issues.",
            "thumbnail": "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60",
            "scheduledDate": "Jan 22, 2026",
            "scheduledTime": "4:30 PM",
            "hostedBy": "Debate Club",
            "location": "Liberal Arts Building",
            "remindMeEnabled": False
        }
    ]
}

# ==================== LIVE STREAMS ROUTES ====================

@app.route('/api/streams/all', methods=['GET'])
def get_all_streams():
    """Get all streams (both live and upcoming)"""
    try:
        return jsonify({
            "result": True,
            "message": "All streams fetched successfully",
            "data": {
                "currentStreams": LIVE_STREAMS_DATA["currentStreams"],
                "upcomingStreams": LIVE_STREAMS_DATA["upcomingStreams"]
            }
        }), 200
    except Exception as e:
        return jsonify({
            "result": False,
            "message": f"Error fetching streams: {str(e)}",
            "data": None
        }), 500

@app.route('/api/streams/live', methods=['GET'])
def get_live_streams():
    """Get currently live streams"""
    try:
        return jsonify({
            "result": True,
            "message": "Live streams fetched successfully",
            "data": LIVE_STREAMS_DATA["currentStreams"]
        }), 200
    except Exception as e:
        return jsonify({
            "result": False,
            "message": f"Error fetching live streams: {str(e)}",
            "data": None
        }), 500

@app.route('/api/streams/upcoming', methods=['GET'])
def get_upcoming_streams():
    """Get upcoming scheduled streams"""
    try:
        return jsonify({
            "result": True,
            "message": "Upcoming streams fetched successfully",
            "data": LIVE_STREAMS_DATA["upcomingStreams"]
        }), 200
    except Exception as e:
        return jsonify({
            "result": False,
            "message": f"Error fetching upcoming streams: {str(e)}",
            "data": None
        }), 500

@app.route('/api/streams/<int:stream_id>', methods=['GET'])
def get_stream_details(stream_id):
    """Get details of a specific stream"""
    try:
        # Search in both current and upcoming streams
        all_streams = LIVE_STREAMS_DATA["currentStreams"] + LIVE_STREAMS_DATA["upcomingStreams"]
        stream = next((s for s in all_streams if s['id'] == stream_id), None)
        
        if stream:
            return jsonify({
                "result": True,
                "message": "Stream details fetched successfully",
                "data": stream
            }), 200
        else:
            return jsonify({
                "result": False,
                "message": "Stream not found",
                "data": None
            }), 404
    except Exception as e:
        return jsonify({
            "result": False,
            "message": f"Error fetching stream details: {str(e)}",
            "data": None
        }), 500

@app.route('/api/streams/<int:stream_id>/viewers', methods=['GET'])
def get_viewer_count(stream_id):
    """Get current viewer count for a live stream"""
    try:
        stream = next((s for s in LIVE_STREAMS_DATA["currentStreams"] if s['id'] == stream_id), None)
        
        if stream:
            return jsonify({
                "result": True,
                "message": "Viewer count fetched successfully",
                "data": {
                    "streamId": stream_id,
                    "viewerCount": stream.get("viewerCount", 0)
                }
            }), 200
        else:
            return jsonify({
                "result": False,
                "message": "Live stream not found",
                "data": None
            }), 404
    except Exception as e:
        return jsonify({
            "result": False,
            "message": f"Error fetching viewer count: {str(e)}",
            "data": None
        }), 500

@app.route('/api/streams/reminder', methods=['POST'])
def set_stream_reminder():
    """Set a reminder for an upcoming stream"""
    try:
        data = request.get_json()
        stream_id = data.get('streamId')
        user_id = data.get('userId')
        
        if not stream_id or not user_id:
            return jsonify({
                "result": False,
                "message": "streamId and userId are required",
                "data": None
            }), 400
        
        # Find the stream in upcoming streams
        stream = next((s for s in LIVE_STREAMS_DATA["upcomingStreams"] if s['id'] == stream_id), None)
        
        if stream:
            # In a real application, you would save this to a database
            return jsonify({
                "result": True,
                "message": "Reminder set successfully",
                "data": {
                    "streamId": stream_id,
                    "userId": user_id,
                    "streamTitle": stream.get("title"),
                    "scheduledDate": stream.get("scheduledDate"),
                    "scheduledTime": stream.get("scheduledTime")
                }
            }), 200
        else:
            return jsonify({
                "result": False,
                "message": "Upcoming stream not found",
                "data": None
            }), 404
    except Exception as e:
        return jsonify({
            "result": False,
            "message": f"Error setting reminder: {str(e)}",
            "data": None
        }), 500

@app.route('/api/streams/search', methods=['GET'])
def search_streams():
    """Search streams by title or description"""
    try:
        query = request.args.get('q', '').lower()
        
        if not query:
            return jsonify({
                "result": False,
                "message": "Search query is required",
                "data": []
            }), 400
        
        all_streams = LIVE_STREAMS_DATA["currentStreams"] + LIVE_STREAMS_DATA["upcomingStreams"]
        filtered_streams = [
            stream for stream in all_streams 
            if query in stream['title'].lower() or query in stream['description'].lower()
        ]
        
        return jsonify({
            "result": True,
            "message": f"Found {len(filtered_streams)} streams",
            "data": filtered_streams
        }), 200
    except Exception as e:
        return jsonify({
            "result": False,
            "message": f"Error searching streams: {str(e)}",
            "data": None
        }), 500

@app.route('/api/streams/category/<category>', methods=['GET'])
def get_streams_by_category(category):
    """Get streams by category (e.g., education, sports, cultural)"""
    try:
        # This is a simple implementation - you can expand based on your needs
        all_streams = LIVE_STREAMS_DATA["currentStreams"] + LIVE_STREAMS_DATA["upcomingStreams"]
        filtered_streams = [
            stream for stream in all_streams 
            if category.lower() in stream.get('hostedBy', '').lower()
        ]
        
        return jsonify({
            "result": True,
            "message": f"Streams in {category} category fetched successfully",
            "data": filtered_streams
        }), 200
    except Exception as e:
        return jsonify({
            "result": False,
            "message": f"Error fetching streams by category: {str(e)}",
            "data": None
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=3001)