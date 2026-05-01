Event Management System (Django)

📌 Project Overview
This is a web-based Event Management System developed using Python and Django. The application is designed to manage and book non-technical events such as weddings, naming ceremonies, birthday parties, baby showers, and other personal functions.
It allows users to explore event categories, view images, and book events based on their preferences like indoor or outdoor arrangements.

🚀 Features
User Registration & Login (Accounts Module)
Browse different event types
Book events such as:
Wedding
Naming Ceremony
Birthday Party
Baby Shower
Indoor & Outdoor event selection
Event image display (media handling)
Booking and enquiry system
Organized event management

🛠️ Tech Stack
Backend: Python, Django
Frontend: HTML, CSS
Database: MySQL (Configured)
Version Control: Git & GitHub

📂 Project Structure
btrpy/
│
├── accounts/        # Handles user authentication (login, register)
├── events/          # Handles event booking and management
│
├── btrpy/           # Main project settings and configuration
│
├── media/           # Stores uploaded images (event, indoor, outdoor)
│   ├── event/
│   ├── indoorming/
│   ├── outdoorming/
│   └── userimg/
│
├── static/          # Static files (CSS, images)
├── templates/       # HTML templates
│
├── manage.py        # Django project entry point
├── db.sqlite3       # Default DB (MySQL configured separately)
⚙️ Installation & Setup
Clone the repository:
git clone https://github.com/rohittt18-git/Event-Management-System.git
Navigate to the project:
cd Event-Management-System
Create virtual environment:
python -m venv venv
venv\Scripts\activate
Install dependencies:
pip install -r requirements.txt
Configure MySQL database in settings.py
Apply migrations:
python manage.py migrate
Run the server:
python manage.py runserver
📸 Screenshots

(Add screenshots of your project UI here)

🎯 Future Enhancements
Online payment integration
Admin dashboard improvements
Email/SMS notifications
Advanced event customization

This project is developed for learning and academic purposes using Django framework.
