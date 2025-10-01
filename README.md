# AI Quiz App
![developer](https://img.shields.io/badge/Developed%20By%20%3A-Prashant%20Sharma-red)

An **AI-powered quiz application** built with **Django**, where quizzes are generated automatically using the **OpenRouter API** (free LLM API gateway).  
Users can register, take quizzes, track results, and view leaderboards.  

---

## Features

-  User authentication & registration
-  AI-generated quiz questions (via OpenRouter API)
-  Supports **Class-based** quiz
-  Real-time progress tracking during quiz
-  Leaderboard (rankings by score)
-  Session history (view past quizzes & results)
-  Question storage in database for future review

---

## screenshots

### Homepage

<img width="1919" height="1016" alt="Screenshot 2025-09-30 215746" src="https://github.com/user-attachments/assets/37c42a61-80f7-49a6-9c17-4035d1ded15b" />

### Login

<img width="1919" height="1015" alt="Screenshot 2025-09-30 215844" src="https://github.com/user-attachments/assets/754edfec-6c00-4fa6-b34e-8e54132305c8" />

### Register

<img width="1919" height="1015" alt="Screenshot 2025-09-30 215910" src="https://github.com/user-attachments/assets/17acbdb2-f552-45d1-a511-37692ff809bb" />

### User Dashboard

<img width="1919" height="1015" alt="Screenshot 2025-09-30 220135" src="https://github.com/user-attachments/assets/db58a31f-d901-4543-a807-e9d36292721e" />

### Generate Quiz View

<img width="1918" height="1017" alt="Screenshot 2025-09-30 220331" src="https://github.com/user-attachments/assets/7d16f5be-ff7e-4d70-933f-c17587f217fc" />

### Result View

<img width="1919" height="1015" alt="Screenshot 2025-09-30 220800" src="https://github.com/user-attachments/assets/3e832452-628e-41ac-b23a-919de2f69057" />

---

### User

- Create account (No Approval Required By Admin, Can Login After Signup)
- After Login, you can see your dashboard.
- Can see your given test with detailed view of your each test.
- You can see your leaderboard.
- Question Pattern Is MCQ With 4 Options And 1 Correct Answer.
> **_NOTE:_**  You can not delete your given test

---

### Guest User
- No need to login.
- Can see your given test with detailed view of your each test.
- You can not see your leaderboard you need to login for that.
- Click **Try Without Login** button.
- After that select all necessary fields and click generate button.
- Can see your given test with detailed view of your current test.
- Question Pattern Is MCQ With 4 Options And 1 Correct Answer.
- After refresh can not see any test result of yours

---

## ⚙️ Installation Guide

### 1️⃣ Clone Repository
```
git clone https://github.com/YOUR_USERNAME/quiz-ai-django.git
cd quiz-ai-django
```

### 2️⃣ Create Virtual Environment
```
#For Linux / Mac
python3 -m venv venv
source venv/bin/activate
```
```
## For Windows
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```pip install -r requirements.txt```

### 4️⃣ Database Setup

```
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create Superuser

```python manage.py createsuperuser```

### 6️⃣ Run Server

```python manage.py runserver```

---

## 🤖 OpenRouter API Setup

We use OpenRouter to generate quiz questions.
OpenRouter is free to start and provides access to models like gpt-3.5, llama-3, etc.

Steps:
- Go to https://openrouter.ai/
- Sign up with Google / GitHub.
- Navigate to API Keys → Generate a free API key.
- Copy the API key.

---

### Environment Variables

- Create a .env file inside your project root:

```OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx```

- In ai_client.py, the client automatically picks the API key from .env:
  
```
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

class OpenRouterClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.url = "https://openrouter.ai/api/v1/chat/completions"
```

---

## Future Improvements
- Add quiz timer
- Add detailed solution of each question 
- Make mobile-friendly UI
- Add analytics dashboard for users
- Improve styling with TailwindCSS / Bootstrap

