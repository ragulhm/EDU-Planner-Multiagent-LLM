# 🎓 EduPlanner – LLM-Based Multi-Agent Learning System

EduPlanner is an **AI-driven personalized learning system** that uses a **multi-agent LLM architecture** to generate, evaluate, and refine lesson plans dynamically. It adapts learning paths based on student skill levels using a **skill tree-based personalization model**, combining **offline and cloud-based LLMs** for scalability and performance.

---

## 🚀 Features

- 🤖 **Multi-Agent LLM Architecture**
  - **Evaluator Agent** – Validates lesson quality and correctness
  - **Optimizer Agent** – Refines lesson structure, clarity, and difficulty
  - **Analyst Agent** – Analyzes learner progress and skill gaps

- 🌳 **Skill Tree-Based Personalization**
  - Tracks student competencies
  - Dynamically adjusts lesson difficulty and sequencing
  - Generates personalized learning paths

- ⚡ **Hybrid LLM Integration**
  - Offline LLM inference using **Ollama**
  - Cloud-based models via **OpenRouter** and **DeepSeek API**
  - Optimized for speed, accuracy, and scalability

- 🌐 **Full-Stack Application**
  - Interactive frontend for lesson visualization
  - REST APIs for lesson generation and evaluation

---

## 🛠️ Tech Stack

**Frontend**
- React

**Backend**
- Python
- FastAPI

**AI / LLM**
- Ollama
- DeepSeek API
- OpenRouter

**Architecture**
- Multi-Agent LLM System
- Skill Tree-Based Learning Model

---

## 🧠 System Architecture (High-Level)

User Input
↓
Analyst Agent → Skill Tree Evaluation
↓
Evaluator Agent → Lesson Validation
↓
Optimizer Agent → Content Refinement
↓
Personalized Lesson Output


---

## 📦 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/eduplanner.git
cd eduplanner

2️⃣ Backend Setup
pip install -r requirements.txt
uvicorn main:app --reload

3️⃣ Frontend Setup
cd frontend
npm install
npm run dev

4️⃣ Run Ollama (Offline LLM)
ollama run llama3


Ensure Ollama is installed and running locally before starting the backend.

📌 Use Cases

Personalized learning platforms

AI-powered tutoring systems

Adaptive learning management systems (LMS)

Self-paced education applications

🔮 Future Enhancements

Performance analytics dashboard

Student memory & progress tracking

Quiz and assessment generation

Multi-language lesson support

Hugging Face model integration

👨‍💻 Author

Ragul M
B.Tech Information Technology
📧 Email: ragul.mr3391@gmail.com

🔗 LinkedIn | GitHub | Portfolio
