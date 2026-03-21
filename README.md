# 🚀 Django Quiz App - Modern AI-Powered Trivia

A fully-featured, rich-UI Quiz Web Application built with Python (Django) and a gorgeous modern glassmorphism frontend. It features seamless user authentication, automated question generation using Google Gemini AI, and extensive tracking of your past attempt scores natively out of the box!

---

## ✨ Key Features

### 🎨 Premium Framer & Apple-Inspired UI
*   **Intelligent Theme Engine:** Features a pristine Light Mode default alongside a stunning, true-black Dark Mode tailored with `prefers-color-scheme` media checks, `localStorage` persistence, and an animated, Apple-style navbar toggle pill that bypasses FOUC.
*   **Liquid Glassmorphism & Depth:** Incorporates beautifully frosted glass cards utilizing `saturate` and `backdrop-filter` bounds alongside dynamic 3D CSS perspective tilts triggered via Javascript mouse coordinate tracking.
*   **Ambient Global Animations:** Enjoy immersive `<svg>` noise overlays paired with fluid Electric Violet and Cyan blurred blobs that drift seamlessly via hardware-accelerated `@keyframes`.
*   **Advanced Micro-Interactions:** Custom vanilla JS cursor that dynamically scales out on hover, smooth intersection observer stagger-fades on scrolling interfaces, and integrated Confetti API bursts upon achieving >80% accuracy!
*   **Custom Typography:** Beautiful integration with Google's *Outfit* sans-serif font family, tightened letter tracking, and robust typography hierarchy.

### 🧠 Gemini AI Auto-Generation & Fallback Banks
*   **Unlimited Infinite Quizzes:** A "Generate More Questions" button on quiz dashboards uses Google's `gemini-1.5-flash` language model to automatically write 5 fresh, topic-specific trivia questions right onto the end of your quiz on the spot!
*   **Smart Offline Mode:** Even if your Gemini system API key isn't set (or fails), the system natively falls back to a massive, beautifully structured internal offline question bank perfectly formatted to each target category so you never stop playing.

### ⚡ Built-In Automated Quiz Library
*   No empty databases here! The app utilizes built-in signal listeners and custom middlewares to **automatically load 12 fully complete quizzes** perfectly formatted the moment you launch the application:
    *   *Cricket Mastery, Football Fundamentals, Technology Today, Current Affairs Challenge, Geopolitics & World Affairs, Natural Science, World History Highlights, Literature Classics, Cinema & Entertainment, Space & Astronomy, General Mathematics, Bollywood Magic*

### 🔐 User Registration & Profiles
*   **Seamless Authentication:** Clean Login and Sign Up interfaces specifically styled to directly mirror the glass themes. 
*   **Secure Routing:** Robust `POST` logout endpoints, redirect protection, and conditional session caching tools.
*   **My Attempts Dashboard:** Authenticated users get their own personal dashboard tracking total attempts, overall accuracy percentage, and a detailed list of every quiz ever submitted. 

### 🎮 Smooth Gameplay Experience
*   **Interactive Testing Interface:** Answer choices highlight automatically on click.
*   **Real-time Save:** Includes `save_answer` AJAX API hooks to preserve user choices securely directly to the database exactly at the moment they click—no more lost progress!
*   **Sticky Time Manager:** A gorgeous SVG circular progress ring that fluidly drains and shifts colors from Blue to Orange to Red as your time depletes using native `stroke-dashoffset` animations.
*   **Detailed Results Page:** After submitting, you get a sprawling summary showcasing your total score, your percentage logic, and a full question-by-question breakdown showing exactly what you got right and wrong!

### 🏆 Leaderboards & Competition
*   Every quiz page has an embedded `View Leaderboard` option to check up on the top 20 scorers worldwide on that exact test to spur competition.

### 🔌 RESTful API Access
*   Access your platform's raw JSON data anywhere!
*   `GET /api/quizzes/` - Lists all active quiz IDs, limits, titles, and score metrics.
*   `GET /api/quiz/<id>/` - Fully dumps out the complete text choices arrays natively.

---

## 🛠️ Tech Stack Foundational Architecture

*   **Backend Framework:** Python (Django 5.x)
*   **Frontend Technologies:** HTML5, CSS3 Variables, Vanilla JavaScript (DOM manipulation)
*   **Database:** SQLite3 / Django ORM ORM
*   **Integration Services:** `google-generativeai` package module

---

## 🚀 Getting Started

### Prerequisites

*   **Python 3.8+**
*   (Optional but Recommended) You can insert your gemini-1.5 API key in `generator.py` inside the `os.environ.get()` request to enable infinite automatic question generation online.

### Installation

1.  **Clone the Repository** and navigate inside the directory.
2.  **Activate your virtual environment**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # (Windows) or source venv/bin/activate (Mac/Linux)
    ```
3.  **Install dependencies**
    ```bash
    pip install django google-generativeai
    ```
4.  **Run Database Migrations**
    ```bash
    python manage.py migrate
    ```
5.  **Start the Local Server** *(The custom auto-loaders will take care of creating the quizzes as soon as you access it!)*
    ```bash
    python manage.py runserver
    ```
6.  Navigate to `http://127.0.0.1:8000` to interact with the application.

---

*Enjoy testing your knowledge!*
