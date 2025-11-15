<h1 align="center">TechGuru</h1>
<p align="center"><strong>Your AI Pair-Programmer That Actually Teaches You</strong> <br> Built with ❤️ by <a href="https://github.com/shubhamranswal">Shubham Singh Ranswal</a> • 🌐<a href="https://shubhamranswal.github.io/PasPas" target="_blank">Visit Live Site</a>↗
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/shubhamranswal/TechGuru/Images/banner_1.png" width="70%" />
</p>

<p align="center">
  <a href="https://github.com/shubhamranswal/TechGuru"><img src="https://img.shields.io/badge/Repo-TechGuru-blue?style=flat-square"></a>
  <a href="https://github.com/shubhamranswal/TechGuru/actions"><img src="https://img.shields.io/github/actions/workflow/status/shubhamranswal/TechGuru/ci.yml?style=flat-square&label=CI"></a>
  <img src="https://img.shields.io/badge/Python-3.10+-yellow?style=flat-square">
  <img src="https://img.shields.io/badge/Model-Gemini%201.5%20Pro-green?style=flat-square">
  <img src="https://img.shields.io/badge/License-MIT-purple?style=flat-square">
</p>

---

# 🚀 Overview

**TechGuru** is an AI-powered engineering mentor designed for software students who want *real* guidance, not just quick answers.  
Powered by **Google Gemini**, TechGuru behaves like your personal:

- 👨‍🏫 *Mentor*  
- 🧠 *Tech Lead*  
- 🧪 *QA Engineer*  
- 🛠️ *Debugger*  
- 👥 *Pair Programmer*

It explains your logic, generates tests, hunts bugs, proposes patches, scaffolds projects, and helps you grow as a real engineer.

TechGuru is built for **learning by doing**, giving students the kind of hands-on guidance normally found only in great engineering teams.

---

# ✨ Features

## 🧠 1. Code Explanation (Mentor Mode)
- High-level summaries  
- Line-by-line explanations  
- Time & space complexity  
- Pitfall detection  
- Personalized micro-exercises  

## 🧪 2. Automated Test Generation
- pytest test suites  
- Edge-case tests  
- Property-based tests  
- Invalid input tests  
- Commented, readable structure  

## 🐞 3. Bug Detection & Patch Suggestions
TechGuru acts like a senior engineer performing a real code review:
- Identifies logical flaws  
- Flags unsafe patterns  
- Suggests improvements  
- Generates unified diff patches  

## 📦 4. Project Scaffolding
Auto-generates:
- Project folders  
- Starter code  
- Tests  
- CI workflow  
- README templates  

## 🎯 5. Interview & DSA Practice
- Problem generation  
- Hint chains  
- Code evaluation  
- Follow-up exercises  

## 🔁 6. Adaptive Learning Engine (SRS)
- Analyzes skill gaps  
- Generates spaced-repetition tasks  
- Reinforces weak areas over time  

## ⚡ 7. Smart Model Switching
- Gemini 1.5 Mini → fast, cost-efficient tasks  
- Gemini 1.5 Pro → deep reasoning, test generation, patching  

---

# 🧩 Architecture

```

┌──────────────────────────────────────────────┐
│                 User Input                   │
│  (Code, project, questions, review request)  │
└──────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│          Gemini Reasoning Layer              │
│  - Explanation Engine                        │
│  - Test Generator                            │
│  - Bug Hunter                                │
│  - Patch Creator                             │
│  - Learning Task Generator                   │
└──────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│                Tooling Layer                 │
│  code_tools.py  → apply patches, run tests   │
│  scaffolder.py  → generate projects          │
│  srs_scheduler.py → spaced repetition tasks  │
└──────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│               Interface Layer                │
│    - FastAPI demo (local UI)                 │
│    - Kaggle Notebook (demo)                  │
└──────────────────────────────────────────────┘

````

---

# 🧪 Demo

The Kaggle notebook demonstrates:

### ✔ Code ingestion & explanation  
### ✔ Test generation & real pytest execution  
### ✔ Bug detection & patch application  
### ✔ Project scaffolding  
### ✔ Adaptive learning tasks  
### ✔ Cost & latency comparison  

You can view or run the notebook locally or in Kaggle.

---

# 🔧 Tech Stack

- **Google Gemini 1.5 Pro (AI Studio)**  
- Python 3.10+  
- FastAPI  
- pytest  
- Faiss (optional)  
- GitHub Actions  
- Kaggle Notebook  

---

# 📥 Installation

```bash
git clone https://github.com/shubhamranswal/TechGuru
cd TechGuru
pip install -r requirements.txt
````

Add your **Google AI Studio API key**:

```bash
export GOOGLE_API_KEY="your_key_here"
```

Run the FastAPI demo:

```bash
uvicorn demo.demo_fastapi:app --reload
```

---

# 🧭 Usage

### **1️⃣ Code Explanation**

POST to `/explain`:

```json
{
  "code": "def add(a, b): return a + b"
}
```

### **2️⃣ Generate Tests**

POST to `/generate-tests`

### **3️⃣ Bug Hunting**

POST to `/bughunt`

### **4️⃣ Project Scaffolding**

POST to `/scaffold`

Everything is available in the demo UI as well.

---

# 📂 Folder Structure

```
TechGuru/
├── app/
│   ├── agent_core.py
│   ├── code_tools.py
│   ├── srs_scheduler.py
│   └── scaffolder.py
├── demo/
│   ├── demo_fastapi.py
│   └── sample_project/
├── notebooks/
│   └── techguru_demo.ipynb
├── data/
│   └── sample_projects/
├── tests/
│   └── test_agent_core.py
├── requirements.txt
├── README.md
└── .github/workflows/ci.yml
```

---

# 🏗 The Build

TechGuru was built through:

* Modular prompt engineering
* A structured multi-agent architecture
* Custom tooling (patch applier, test runner)
* A reproducible Kaggle notebook
* A FastAPI-based demo interface

Google Gemini powers all deep reasoning:

* test generation
* bug hunting
* patch diff creation
* explanation logic
* SRS-learning tasks

---

# 🔭 If I Had More Time

* VS Code extension
* Cross-language support (Java, C++, JS)
* Real-time "Teaching Debugger"
* Student learning analytics dashboard
* Gamified XP system
* Open-source project onboarding assistant

---

# 🤝 Contributing

Pull requests are welcome!
If you want to add test templates, fix prompts, or extend to new languages — feel free to contribute.

---

# 📄 License

This project is licensed under the [**MIT License**](/LICENSE).

---
