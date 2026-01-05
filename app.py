"""
Clubs API Backend - FastAPI Implementation
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import motor.motor_asyncio
from bson import ObjectId
import os

app = FastAPI(title="Clubs API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.fewinfocad
clubs_collection = db.clubs
user_clubs_collection = db.user_clubs


# Pydantic models
class GalleryItem(BaseModel):
    id: int
    title: str
    image: str


class Event(BaseModel):
    id: int
    title: str
    date: str
    time: str
    location: str
    description: str


class Club(BaseModel):
    id: int
    name: str
    shortDescription: str
    description: str
    meetingSchedule: str
    location: str
    memberCount: int
    category: str
    image: str
    tags: List[str]
    contact: str
    gallery: Optional[List[GalleryItem]] = []
    upcomingEvents: Optional[List[Event]] = []


class JoinLeaveRequest(BaseModel):
    userId: str
    clubId: int


# Helper functions
def club_helper(club) -> dict:
    """Convert MongoDB document to dict"""
    return {
        "id": club["id"],
        "name": club["name"],
        "shortDescription": club["shortDescription"],
        "description": club["description"],
        "meetingSchedule": club["meetingSchedule"],
        "location": club["location"],
        "memberCount": club["memberCount"],
        "category": club["category"],
        "image": club["image"],
        "tags": club["tags"],
        "contact": club["contact"],
        "gallery": club.get("gallery", []),
        "upcomingEvents": club.get("upcomingEvents", [])
    }


async def is_member(user_id: str, club_id: int) -> bool:
    """Check if user is a member of a club"""
    member = await user_clubs_collection.find_one({
        "userId": user_id,
        "clubId": club_id
    })
    return member is not None


async def get_user_club_ids(user_id: str) -> List[int]:
    """Get list of club IDs user is a member of"""
    cursor = user_clubs_collection.find({"userId": user_id})
    memberships = await cursor.to_list(length=None)
    return [m["clubId"] for m in memberships]


# API Endpoints
@app.get("/")
async def home():
    """Root endpoint"""
    return {"message": "Clubs API is running", "version": "1.0.0"}


@app.get("/clubs/{user_id}")
async def get_clubs_data(user_id: str):
    """Fetch all clubs data for a user"""
    try:
        clubs_cursor = clubs_collection.find({})
        all_clubs = await clubs_cursor.to_list(length=None)
        
        if not all_clubs:
            return {
                "result": True,
                "myClubs": [],
                "otherClubs": [],
                "message": "No clubs found"
            }
        
        user_club_ids = await get_user_club_ids(user_id)
        
        my_clubs = []
        other_clubs = []
        
        for club in all_clubs:
            club_dict = club_helper(club)
            if club["id"] in user_club_ids:
                my_clubs.append(club_dict)
            else:
                other_clubs.append(club_dict)
        
        return {
            "result": True,
            "myClubs": my_clubs,
            "otherClubs": other_clubs,
            "message": "Clubs data retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching clubs data: {str(e)}"
        )


@app.get("/clubs/my/{user_id}")
async def get_my_clubs(user_id: str):
    """Fetch clubs that the user is a member of"""
    try:
        user_club_ids = await get_user_club_ids(user_id)
        
        if not user_club_ids:
            return {
                "result": True,
                "clubs": [],
                "message": "User is not a member of any clubs"
            }
        
        clubs_cursor = clubs_collection.find({"id": {"$in": user_club_ids}})
        clubs = await clubs_cursor.to_list(length=None)
        
        return {
            "result": True,
            "clubs": [club_helper(club) for club in clubs],
            "message": "User clubs retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user clubs: {str(e)}"
        )


@app.get("/clubs/all")
async def get_all_clubs():
    """Fetch all available clubs"""
    try:
        clubs_cursor = clubs_collection.find({})
        clubs = await clubs_cursor.to_list(length=None)
        
        return {
            "result": True,
            "clubs": [club_helper(club) for club in clubs],
            "message": "All clubs retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching all clubs: {str(e)}"
        )


@app.get("/clubs/details/{club_id}")
async def get_club_details(club_id: int, user_id: Optional[str] = None):
    """Fetch details of a specific club with optional membership status"""
    try:
        club = await clubs_collection.find_one({"id": club_id})
        
        if not club:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Club with ID {club_id} not found"
            )
        
        club_data = club_helper(club)
        
        # Add membership status if user_id is provided
        if user_id:
            club_data["isMember"] = await is_member(user_id, club_id)
        
        return {
            "result": True,
            "club": club_data,
            "message": "Club details retrieved successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching club details: {str(e)}"
        )


@app.post("/clubs/join")
async def join_club(request: JoinLeaveRequest):
    """Join a club"""
    try:
        club = await clubs_collection.find_one({"id": request.clubId})
        if not club:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Club with ID {request.clubId} not found"
            )
        
        if await is_member(request.userId, request.clubId):
            return {
                "result": False,
                "message": "User is already a member of this club"
            }
        
        membership = {
            "userId": request.userId,
            "clubId": request.clubId,
            "joinedAt": datetime.utcnow()
        }
        await user_clubs_collection.insert_one(membership)
        
        await clubs_collection.update_one(
            {"id": request.clubId},
            {"$inc": {"memberCount": 1}}
        )
        
        return {
            "result": True,
            "message": f"Successfully joined {club['name']}",
            "clubId": request.clubId
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error joining club: {str(e)}"
        )


@app.post("/clubs/leave")
async def leave_club(request: JoinLeaveRequest):
    """Leave a club"""
    try:
        club = await clubs_collection.find_one({"id": request.clubId})
        if not club:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Club with ID {request.clubId} not found"
            )
        
        if not await is_member(request.userId, request.clubId):
            return {
                "result": False,
                "message": "User is not a member of this club"
            }
        
        result = await user_clubs_collection.delete_one({
            "userId": request.userId,
            "clubId": request.clubId
        })
        
        if result.deleted_count == 0:
            return {
                "result": False,
                "message": "Failed to leave club"
            }
        
        await clubs_collection.update_one(
            {"id": request.clubId},
            {"$inc": {"memberCount": -1}}
        )
        
        return {
            "result": True,
            "message": f"Successfully left {club['name']}",
            "clubId": request.clubId
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error leaving club: {str(e)}"
        )


@app.get("/clubs/search")
async def search_clubs(q: str):
    """Search clubs by name, category, or tags"""
    try:
        if not q or len(q.strip()) == 0:
            return {
                "result": True,
                "clubs": [],
                "message": "Please provide a search term"
            }
        
        search_pattern = {"$regex": q, "$options": "i"}
        query = {
            "$or": [
                {"name": search_pattern},
                {"shortDescription": search_pattern},
                {"description": search_pattern},
                {"category": search_pattern},
                {"tags": search_pattern}
            ]
        }
        
        clubs_cursor = clubs_collection.find(query)
        clubs = await clubs_cursor.to_list(length=None)
        
        return {
            "result": True,
            "clubs": [club_helper(club) for club in clubs],
            "message": f"Found {len(clubs)} clubs matching '{q}'"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching clubs: {str(e)}"
        )


@app.get("/clubs/events/{club_id}")
async def get_club_events(club_id: int):
    """Fetch upcoming events for a club"""
    try:
        club = await clubs_collection.find_one({"id": club_id})
        
        if not club:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Club with ID {club_id} not found"
            )
        
        return {
            "result": True,
            "events": club.get("upcomingEvents", []),
            "message": "Club events retrieved successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching club events: {str(e)}"
        )


@app.get("/clubs/gallery/{club_id}")
async def get_club_gallery(club_id: int):
    """Fetch gallery images for a club"""
    try:
        club = await clubs_collection.find_one({"id": club_id})
        
        if not club:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Club with ID {club_id} not found"
            )
        
        return {
            "result": True,
            "gallery": club.get("gallery", []),
            "message": "Club gallery retrieved successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching club gallery: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}


# Keep Flask routes below for backward compatibility
from flask import Flask as FlaskApp, request, jsonify
from flask_cors import CORS

flask_app = FlaskApp(__name__)
CORS(flask_app)

@flask_app.route('/')
def flask_home():
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