<div align="center">

# 🚀 QuizApp

**Next-Generation AI-Powered Trivia.**

![Features](https://img.shields.io/badge/Features-AI%20Generation-purple?style=for-the-badge&logo=google)
![Django](https://img.shields.io/badge/Backend-Django_5.x-092E20?style=for-the-badge&logo=django)
![UI](https://img.shields.io/badge/UI-Glassmorphism-blue?style=for-the-badge&logo=css3)
![Status](https://img.shields.io/badge/Status-In_Development-FFD700?style=for-the-badge)

A fully-featured, rich-UI Quiz Web Application built with Python (Django) and a gorgeous modern glassmorphism frontend. Featuring seamless user authentication, automated question generation using Google Gemini AI, and native local tracking.

[View Demo](#) · [Report Bug](#) · [Request Feature](#)

</div>

---

## 📖 Overview
QuizApp redefines the trivia experience. Gone are the days of sterile, clunky testing interfaces. We've married cutting-edge AI—powered by Google Gemini—with an Apple-inspired, premium glassmorphic UI to create an immersive, endlessly replayable platform. Whether you're a trivia aficionado or an educator seeking dynamic assessments, QuizApp scales with unparalleled elegance.

---

## 🎯 Problem ➔ 💡 Solution

**The Problem:** Traditional quiz platforms are static. They suffer from limited question banks, uninspired flat designs, and manual upkeep that quickly renders them stale. 

**The Solution (QuizApp):**
- **Infinite Generation:** Leveraging `gemini-1.5-flash`, QuizApp autonomously generates fresh, context-aware trivia on the fly.
- **Premium Aesthetics:** A fluid, hardware-accelerated interface featuring dynamic 3D tilts, dark-mode toggles, and ambient animations that transform rote answering into a delightful experience.
- **Automated Lifecycle:** From zero-config dataloaders to real-time AJAX saves, the system manages everything under the hood.

---

## ✨ Key Features

- **🧠 Gemini AI Auto-Generation:** Click "Generate" and watch the app seamlessly weave 5 fresh, topic-specific questions into your active quiz.
- **🎨 Premium Apple & Framer-Inspired UI:** True-black Dark Mode, liquid glassmorphism, dynamic 3D CSS tilts triggered via JS cursor tracking, and ambient electric SVG blobs.
- **⚡ Zero-Touch Onboarding:** Natively auto-loads 12 complete, meticulously categorized quizzes (from *Cricket Mastery* to *Geopolitics*) the moment the server boots utilizing custom middlewares.
- **🎮 Real-Time Gameplay Engine:** Answer choices highlight instantly via Vanilla JS, backed by a `save_answer` AJAX API to preserve state perfectly. 
- **⏱️ Sticky Time Manager:** A gorgeousSVG circular progress ring that fluidly drains and alerts users as their time depletes.
- **🔐 Secure Authentication & Dashboards:** Glass-themed Login/SignUp interfaces with a dedicated "My Attempts" dashboard tracking precision metrics and historic accuracy.

---

## 🧠 Architecture & Workflow

1. **Client Layer:** User interacts with the fluid Glassmorphism UI. Interactions (clicks, scrolls) trigger Vanilla JavaScript micro-animations and AJAX event listeners.
2. **API & Routing:** Django intercepts secure AJAX requests (like `save_answer`), validating session tokens and CSRF parameters.
3. **AI Logic Engine:** If the user requests new questions, `generator.py` constructs a secure prompt payload and queries Google's Gemini API, parsing the JSON response into native ORM objects.
4. **Data Persistence:** SQLite3 securely stores user profiles, encrypted passwords, generated questions, and granular score metrics.
5. **Dynamic Fallbacks:** If the AI service is unavailable, `loaders.py` seamlessly injects questions from a massively structured offline JSON bank.

---

## 🛠️ Tech Stack

**Frontend**
- HTML5 (Semantic Structure)
- CSS3 (Custom Properties, Backdrop Filters, Keyframe Animations)
- Vanilla JavaScript (Intersection Observers, DOM coords, AJAX)

**Backend**
- Python 3.11+
- Django 5.x Framework
- Google Generative AI (`google-generativeai`)

**Database & DevOps**
- SQLite3 (Local Dev) / Django ORM
- Pip & Virtualenv for Dependency Management

---

## 🧩 Module Breakdown

- **`generator.py`:** The AI nervous system. Packages context, talks to Gemini, handles rate limits, and safely unmarshals new questions into the database.
- **`loaders.py`:** The silent bootstrapping engine. Listens for Django signals to gracefully inject the curated starter quizzes and offline question banks into empty environments.
- **UI Components:** Reusable, componentized HTML templates utilizing Django template tags for consistent layout inheritance (e.g., `signup.html`, `login.html`, `quiz_result.html`).
- **`views.py`:** The core orchestrator managing authentication flows, session state, and the complex quiz scoring algorithms.

---

## ⚙️ Installation & Setup

Execute these steps chronologically to spin up QuizApp locally in seconds.

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/quizapp.git
cd quizapp
```

**2. Initialize Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Environment Variables**
Create a `.env` file in the root directory (or inject directly into your shell) to unlock AI capabilities:
```env
GEMINI_API_KEY=your_google_gemini_key_here
```

**5. Migrate & Launch**
```bash
python manage.py migrate
python manage.py runserver
```
*Note: Our custom auto-loaders will populate the database with premium quizzes the moment you hit the `runserver` command.*

---

## ▶️ Usage

1. **Sign Up:** Create a new account via the glassmorphic registration portal.
2. **Select a Quiz:** Choose from 12 pre-loaded categories (e.g., *Technology Today*, *Cinema & Entertainment*).
3. **Engage:** Answer questions under the ticking SVG timer. Click "Generate More Questions" to dynamically infinitely scale the current quiz using Gemini.
4. **Review:** Assess your personalized dashboard and check the global leaderboard to see how you stack up.

---

## 🔌 API Documentation

QuizApp exposes a sleek internal REST-like API for data extraction:

| Endpoint | Method | Description |
|---|---|---|
| `/api/quizzes/` | `GET` | Dumps all active quiz metadata (IDs, limits, titles, score metrics). |
| `/api/quiz/<id>/` | `GET` | Retrieves the complete choice array natively for a specific question block. |
| `/api/save_answer/` | `POST` | Internal endpoint to AJAX-save user choices securely mid-quiz. |

---

## 📁 Folder Structure

```text
quizapp/
│
├── quizproject/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── quizapp/
│   ├── Templates/
│   │   └── quizapp/       # Premium HTML views
│   ├── static/
│   │   └── quizapp/       # Vanilla JS & styling logic
│   ├── generator.py       # Gemini AI Logic
│   ├── loaders.py         # Offline bootstrapper
│   ├── models.py          # ORM Schema
│   └── views.py           # Core business logic
│
└── README.md
```

---

## 📸 UI & Aesthetics

While images speak louder than words, QuizApp's UI is defined by:
- **Depth:** Hovering over a quiz card tilts it smoothly towards your cursor, complete with a dynamic internal glare effect.
- **Vibrancy:** Deep blacks contrasted by Electric Violet (`#8B5CF6`) and Cyan (`#06B6D4`) blurred background artifacts.
- **Motion:** Confetti bursts on high scores and a visually draining, color-shifting SVG timer ring that keeps the adrenaline pumping.

---

## 🚀 Deployment

1. **Update `ALLOWED_HOSTS`:** Add your domain in `settings.py`.
2. **Static Files:** Run `python manage.py collectstatic` to bundle the premium CSS/JS.
3. **Database Migration:** Swap SQLite3 for PostgreSQL if deploying to production (e.g., via Railway, Render, or Heroku).
4. **Start Server:** Use Gunicorn or Waitress to launch.

---

## 🔒 Security

- **Authentication Handling:** Secure password hashing natively via Django `auth.models.User`.
- **CSRF Protection:** All internal API calls and form submissions mandate encrypted CSRF tokens.
- **Rate Limiting:** (In Progress) Throttling AI requests to prevent API abuse and cost overruns.

---

## ⚡ Performance Optimizations

- **FOUC Prevention:** LocalStorage parsing occurs synchronously in the `<head>` to prevent the dreaded "Flash of Unstyled Content" during dark/light mode flips.
- **Hardware Acceleration:** All floating background blobs rely on `transform` and `opacity` to push rendering to the GPU, keeping the main thread free.
- **Lazy AJAX States:** Instead of reloading pages, `save_answer` pings quietly in the background, making gameplay feel instantaneous.

---

## 🧱 Challenges & Learnings

- **Challenge:** Creating an Apple-like smooth dark mode without utilizing heavy CSS frameworks.
- **Solution:** Mastered nested CSS Custom Properties (variables) and vanilla JS intersection observers to keep the DOM light but visually stunning.
- **Challenge:** Managing state when the Gemini API occasionally hallucinates malformed JSON.
- **Solution:** Implemented aggressive RegEx parsers and fallback data strategies in `generator.py` to ensure the user never experiences a broken quiz state.

---

## 🔮 Future Scope

- **Multiplayer Live Lobbies:** Challenge friends via WebSockets / Django Channels.
- **Detailed Analytics:** Heatmaps on which questions players struggle with the most.
- **Markdown Support:** Rendering math equations and code blocks within the questions themselves.

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👨‍💻 Author

**Sai Sidharth**
- Complete Stack Engineer
- GitHub: [@saisidharth](https://github.com/saisidharth)
- LinkedIn: [in/saisidharth](https://linkedin.com/in/saisidharth)

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
