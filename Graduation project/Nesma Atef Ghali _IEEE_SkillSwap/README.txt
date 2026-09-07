SkillSwap
=========

A simple skill-exchange platform built with HTML, CSS, JavaScript, Flask, and SQLite.

Project structure
-----------------
app.py                 Flask backend and routes
skillswap.db           SQLite database (created/updated by the app)
README.txt             Project notes and run instructions
static/css/style.css  Main CSS file
static/js/script.js    JavaScript interactions
static/images/         Demo and local images
static/uploads/        User-uploaded profile pictures
templates/             Independent HTML pages (no base.html)

Main pages
----------
index.html             Home
signup.html             Create account
login.html              Login
explore.html            Explore people and skills
matches.html            Reciprocal skill matches
requests.html           Accept/reject swap requests
chat.html               Chat after acceptance
profile.html            My profile
edit_profile.html       Edit profile

How to run
----------
1. Open a terminal in this folder.
2. Install Flask:
   python -m pip install Flask
3. Start the app:
   python app.py
4. Open:
   http://127.0.0.1:5000

Notes
-----
- The demo profile images are placeholders. Replace them in static/images/profiles/ if needed.
- User-uploaded profile pictures are saved in static/uploads/.
- Matches are based on a two-way skill exchange: I can teach what they want to learn, and they can teach what I want to learn.
