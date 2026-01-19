from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Hello, this Flask app is running on Render"


@app.route('/api/info', methods=['GET'])
def get_info():
    """Return centralized data for all info pages"""
    return jsonify({
        "contactInfo": {
            "email": {
                "general": "info@fewinfocad.edu",
                "support": "support@fewinfocad.edu",
                "privacy": "privacy@fewinfocad.edu",
                "legal": "legal@fewinfocad.edu"
            },
            "phone": {
                "main": "+123-4567",
                "support": "+1 (555) 123-4567",
                "formatted": "(555) 123-4567"
            },
            "address": {
                "full": "FewInfoCAD, 123 College Avenue, University City, ST 12345",
                "street": "123 College Avenue",
                "city": "University City",
                "state": "ST",
                "zip": "12345",
                "office": "FewInfoCAD Privacy Office, 123 College Avenue, University City, ST 12345",
                "legal": "FewInfoCAD Legal Department, 123 College Avenue, University City, ST 12345"
            },
            "officeHours": "Monday - Friday, 9:00 AM - 5:00 PM"
        },
        "institutionInfo": {
            "name": "FewInfoCAD",
            "fullName": "FewInfoCAD College Academic Information Portal",
            "description": "Your trusted college academic information portal for seamless campus life.",
            "established": "2020",
            "lastUpdated": "January 19, 2026"
        },
        "helpTopics": {
            "gettingStarted": [
                {
                    "question": "How do I log in?",
                    "answer": "Click the \"Login\" button on the homepage and enter your college email and password. If you're a new student, your credentials will be provided by the administration office."
                },
                {
                    "question": "What if I forgot my password?",
                    "answer": "Click on \"Forgot Password?\" in the login modal. You'll receive a password reset link via your registered email address."
                },
                {
                    "question": "How do I update my profile information?",
                    "answer": "After logging in, navigate to your dashboard and click on \"Profile Settings\" to update your personal information, contact details, and preferences."
                }
            ],
            "academicInfo": [
                {
                    "question": "Where can I view my grades?",
                    "answer": "Your grades are available in the Academic Dashboard section. Click on \"Grades\" to see subject-wise marks, semester results, and overall performance."
                },
                {
                    "question": "How do I check my attendance?",
                    "answer": "Navigate to the Attendance section from your dashboard. You can view daily, weekly, and monthly attendance records for all subjects."
                },
                {
                    "question": "Where can I find course materials?",
                    "answer": "Course materials, lecture notes, and assignments are available in the Course Materials section. Materials are organized by subject and semester."
                }
            ],
            "technicalSupport": [
                {
                    "question": "The portal is not loading properly",
                    "answer": "Try clearing your browser cache and cookies. Make sure you're using an updated version of Chrome, Firefox, Safari, or Edge. If the issue persists, contact technical support."
                },
                {
                    "question": "I'm having trouble uploading files",
                    "answer": "Ensure your file size doesn't exceed 10MB and is in a supported format (PDF, DOC, DOCX, JPG, PNG). Check your internet connection and try again."
                },
                {
                    "question": "Mobile app not working",
                    "answer": "Make sure you have the latest version of the app installed. Check your device's operating system compatibility and ensure you have a stable internet connection."
                }
            ]
        },
        "faqCategories": [
            {
                "category": "Account & Login",
                "questions": [
                    {
                        "question": "How do I create an account?",
                        "answer": "Accounts are automatically created for all enrolled students. You'll receive your login credentials via email from the administration office within 48 hours of enrollment."
                    },
                    {
                        "question": "Can I change my password?",
                        "answer": "Yes, you can change your password from the Profile Settings section after logging in. We recommend using a strong password with at least 8 characters, including numbers and special characters."
                    },
                    {
                        "question": "Why can't I log in?",
                        "answer": "Common reasons include incorrect credentials, expired password, or account not yet activated. Try resetting your password or contact the IT helpdesk if the problem persists."
                    }
                ]
            },
            {
                "category": "Academic Records",
                "questions": [
                    {
                        "question": "When are grades updated?",
                        "answer": "Grades are typically updated within 7-10 business days after exams. You'll receive an email notification once your results are available."
                    },
                    {
                        "question": "How can I download my mark sheets?",
                        "answer": "Navigate to Academic Dashboard > Grades > Download. Select the semester and click 'Download Mark Sheet'. The document will be in PDF format."
                    },
                    {
                        "question": "Is my attendance automatically tracked?",
                        "answer": "Yes, faculty members mark attendance digitally, and it's automatically reflected in your portal within 24 hours."
                    }
                ]
            },
            {
                "category": "Fees & Payments",
                "questions": [
                    {
                        "question": "What payment methods are accepted?",
                        "answer": "We accept credit/debit cards, net banking, UPI, and digital wallets. International students can use international cards or bank transfers."
                    },
                    {
                        "question": "How do I download fee receipts?",
                        "answer": "Go to Fee Management > Payment History > Select transaction > Download Receipt. All receipts are digitally signed and valid for official purposes."
                    },
                    {
                        "question": "Can I pay fees in installments?",
                        "answer": "Yes, installment options are available. Contact the accounts department to set up a payment plan based on your needs."
                    }
                ]
            },
            {
                "category": "Technical Issues",
                "questions": [
                    {
                        "question": "Which browsers are supported?",
                        "answer": "The portal works best on the latest versions of Chrome, Firefox, Safari, and Edge. We recommend keeping your browser updated for optimal performance."
                    },
                    {
                        "question": "Is there a mobile app?",
                        "answer": "Yes, FewInfoCAD is available on both iOS and Android. Download it from the App Store or Google Play Store. The mobile app offers most desktop features."
                    },
                    {
                        "question": "What should I do if I encounter an error?",
                        "answer": "Take a screenshot of the error, note what you were doing, and contact support at support@fewinfocad.edu. Include your student ID for faster resolution."
                    }
                ]
            }
        ],
        "technicalSpecs": {
            "maxFileSize": "10MB",
            "supportedFileFormats": ["PDF", "DOC", "DOCX", "JPG", "PNG"],
            "supportedBrowsers": ["Chrome", "Firefox", "Safari", "Edge"],
            "mobileApps": ["iOS", "Android"],
            "dataRetentionPeriod": "7 years",
            "passwordMinLength": 8
        },
        "legalInfo": {
            "lastUpdated": "January 19, 2026",
            "governingLaw": "the jurisdiction in which the institution is located",
            "minimumAge": 16,
            "dataRetention": "7 years after graduation or withdrawal"
        }
    })


if __name__ == '__main__':
    app.run(debug=True, port=3001)
