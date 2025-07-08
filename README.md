# 🏆 Tournamento – Tournament Management System

Tournamento is a full-featured, user-friendly tournament management web application built with **Django**. It allows users to create, manage, and view tournaments with automatic group-stage fixture generation, knockout stage progression, and match score updates.

---

## 🚀 Features

- ✅ Create new tournaments with custom number of teams and groups  
- 🛠️ Automatically assign teams to groups and generate fixtures  
- 🔄 Record match scores and track standings  
- 📈 View group stage tables and knockout stages (Quarterfinals, Semifinals, Final)  
- 🏅 Automatically determine and display the tournament winner  
- ✏️ Edit tournament info  
- 🗑️ Delete tournaments  
- 🎨 Clean, modern, and responsive UI using pure HTML + CSS

---



## 📂 Project Structure

tournamento/
│
├── core/ # Main app
│ ├── models.py # Database models
│ ├── views.py # Business logic and rendering
│ ├── urls.py # App-level routing
│ ├── templates/core/ # HTML templates
│ └── ...
│
├── tournamento/ # Project settings
│ ├── settings.py
│ ├── urls.py
│ └── ...
│
├── db.sqlite3 # Database
├── manage.py
└── README.md # You are here!


---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/tournamento.git
   cd tournamento
2. **Create a virtual environment and activate it**
   ```bash
      python -m venv venv
      source venv/bin/activate  # on Windows: venv\Scripts\activate
3. **Install dependencies**
   ```bash
      pip install django
4. **Run migrations**
   ```bash
    python manage.py migrate
5. **Start the development server**
    ```bash
      python manage.py runserver
6. **Open in your browser**
   Visit http://127.0.0.1:8000/ to access the app.

## 🧠 Tech Stack

- **Framework:** Django 5.2+
- **Language:** Python 3.10+
- **Database:** SQLite (default)
- **Frontend:** HTML5, CSS3, Google Fonts
- **Version Control:** Git

---

## 📌 To Do (Optional Enhancements)

- Add user authentication for multi-user support  
- Export fixtures and results as PDF  
- REST API support using Django REST Framework  
- Deploy online (Render / PythonAnywhere / Heroku)  
- Add flash messages for better UX  

---

## 📃 License

This project is open-source and free to use for educational and non-commercial purposes.  
Customize it to fit your needs!

## 🙌 Acknowledgements
Built with ❤️ by RK Tushar

Feel free to fork this project, contribute, and share your feedback!
