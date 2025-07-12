# Attendance System

## Overview  
This update covers the progress made on Task 3 of the Attendance System project. The focus was on building features that let students and admins record attendance, view reports, and enjoy a smooth website experience.

## What Has Been Done  
- Set up login for students and admins with different access levels.  
- Students can mark their own attendance via a simple form.  
- Admins can mark attendance for multiple students at once (bulk attendance).  
- Created reports that admins can view online or download as spreadsheets (CSV).  
- Designed a user-friendly and mobile-friendly website with clear navigation and smooth transitions.  
- Added notifications to inform users when actions succeed or fail.

## How It Works  
- Students log in and submit attendance for a given date and time.  
- Admins log in and can submit attendance for groups, as well as view detailed attendance reports.  
- All attendance data is saved securely in the system.  
- Reports are accessible through the website and can be downloaded for offline use.  
- The website guides users with helpful messages and smooth page changes.

## What Needs Improvement / Next Steps  
- Ensure all attendance data is reliably saved and shows up correctly in reports.  
- Add better checks to prevent missing or incorrect data during submission.  
- Improve admin reports with more filtering options to easily find specific attendance records.  
- Move sensitive settings to secure places to protect user data.  
- Continue refining the website’s design and usability based on user feedback.  
- Develop automatic tests to catch issues early and maintain quality.

---

## How to Install and Run the System  

1. **Clone the project:**  
   ```bash
   git clone [your-repo-url]
   cd attendance-app
Set up a Python environment:
Create a virtual environment to keep things tidy:

 
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
Install required packages:

 
pip install -r requirements.txt
Set up the database:
The system uses SQLite by default. The database file will be created automatically when you run the app.

Run the app:

 
flask run
Access the system:
Open your browser and go to http://127.0.0.1:5000 to start using the attendance system.

Feel free to reach out if you need help with setup or have questions!
