# DevCheatHub - The Developer's Ultimate Reference Platform

<div align="center">
<img src="https://placehold.co/600x300/0a0e1a/00ff88?text=DevCheatHub&font=source-sans-pro" alt="DevCheatHub Banner">
</div>

**A modern, open-source platform that serves as a comprehensive, searchable repository of technical cheat sheets, code snippets, and quick references. Find any command, snippet, or concept in milliseconds.**

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/your-username/devcheathub)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/your-username/devcheathub/pulls)

## ✨ Key Features

* **Global Search:** A powerful, command-palette style (⌘K) search to find anything instantly.
* **Comprehensive Cheatsheets:** A growing collection of references for languages, frameworks, and tools.
* **Code Snippets:** A library of ready-to-use, copy-pasteable code blocks with syntax highlighting.
* **Community Driven:** Contribute your own cheatsheets and help the community grow.
* **Modern Aesthetic:** A beautiful, dark-themed UI focused on developer experience.
* **Interactive:** Interactive examples and a clean, two-column layout for easy reading.

## 🛠️ Tech Stack

* **Backend:** Django
* **Database:** MySQL
* **Frontend:** Django Templates, Tailwind CSS
* **Interactivity:** Alpine.js, HTMX
* **Animations:** Anime.js
* **Hosting:** Railway.app (or similar)

---

## 🚀 Getting Started

Follow these instructions to set up a local development environment.

### 1. Prerequisites

Make sure you have the following installed on your local machine:
* Python 3.8+
* Git
* A code editor (e.g., VS Code)

### 2. Clone the Repository

```bash
git clone [https://github.com/your-username/devcheathub.git](https://github.com/your-username/devcheathub.git)
cd devcheathub
```

### 3. Set Up the Environment

1.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python -m venv venv
    source venv/bin/activate
    ```
2.  **Install project dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 4. Configure Environment Variables

1.  Create a `.env` file in the project root. You can copy the example file:
    ```bash
    # For Windows
    copy .env.example .env

    # For macOS/Linux
    cp .env.example .env
    ```
2.  Open the `.env` file and fill in your database credentials. For local development, you can use a local MySQL server or connect to a cloud instance (like on Railway).
    ```ini
    # .env
    SECRET_KEY='your-strong-django-secret-key-here'
    DEBUG=True

    ```

### 5. Prepare the Database

Run the migrations to create the necessary database tables:
```bash
python manage.py migrate
```

### 6. Create the Default Admin User

To access the Django admin panel, create a superuser.
```bash
python manage.py createsuperuser
```
When prompted, use the following default credentials for consistency across the team:
* **Username:** `admin`
* **Email:** `admin@example.com` (or any email)
* **Password:** `admin`

You may get a warning that the password is too common. You can safely bypass this for local development.

### 7. Run the Development Server

You're all set! Start the Django server:
```bash
python manage.py runserver
```
Open your browser and navigate to `http://127.0.0.1:8000/` to see the application running. You can log into the admin panel at `http://127.0.0.1:8000/admin`.

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Please see our `CONTRIBUTING.md` file for details on our code of conduct and the process for submitting pull requests.

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.