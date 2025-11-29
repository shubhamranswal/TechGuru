<div align="center">

<h1 align="center">TechGuru</h1>
<p align="center"><strong>Your AI Pair-Programmer That Actually Teaches You</strong> <br> Built with ❤️ by <a href="https://github.com/shubhamranswal">Shubham Singh Ranswal</a>
</p>

<hr>

<p align="center">
  <img src="https://raw.githubusercontent.com/shubhamranswal/TechGuru/main/Images/banner_1.png" width="70%" />
</p>


<br>

<a href="https://kaggle.com/competitions/agents-intensive-capstone-project/writeups/techguru">
<img src="https://img.shields.io/badge/Kaggle-Submission-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white" />
</a>

<img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />
<img src="https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/Gemini%20API-2.0%20Flash%20Lite-5A45FF?style=for-the-badge&logo=google" />
<img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" />
<br>
<img src="https://img.shields.io/github/license/shubhamranswal/TechGuru?style=flat-square" />

<br><br>

<img src="https://raw.githubusercontent.com/shubhamranswal/TechGuru/main/Images/screenshots/api_demo.png" width="75%" />

<br><br>

</div>

---

# 🧠 **What is TechGuru?**

TechGuru is an interactive **AI code-teaching agent** built for software students who need:

* A *teacher*
* A *mentor*
* A *tech lead*
* A *code reviewer*
* A *bug fixer*
* A *test writer*
* A *project generator*

Instead of just answering questions, TechGuru **teaches you how to think like a real software engineer**.

It’s powered by:

* **FastAPI backend**
* **Gemini 2.0 Flash Lite** (affordable, fast, highly capable)
* **Fully custom ChatGPT-style UI with streaming**
* **Multiple intelligent agents** (`explain`, `generate-tests`, `bughunt`, `scaffold`)
* **Local project generation & auto-pytest execution**

> 📌 This project is submitted to the **Kaggle Agents Capstone** competition.
> Check the writeup here:
> **[https://kaggle.com/competitions/agents-intensive-capstone-project/writeups/techguru](https://kaggle.com/competitions/agents-intensive-capstone-project/writeups/techguru)**

---

# 🧩 **Core Features**

### ✅ Explain Code (line-by-line with micro-exercises)

### ✅ Generate Pytest Tests

### ✅ Bughunt (finds issues + returns patch diff)

### ✅ Scaffold Complete Python Projects

### ✅ ChatGPT-style UI with token-by-token streaming

### ✅ Syntax highlighting via Prism.js

### ✅ Export chat as Markdown

### ✅ User avatar uploading

### ✅ Works offline with fallback logic

### ✅ Clean FastAPI endpoints (`/stream`, `/explain`, `/generate-tests`, `/bughunt`, `/scaffold`)

---

# 🏗️ **Architecture Overview**

```
┌────────────────────┐
│      Web UI        │
│ (streaming + Prism │
└─────────┬──────────┘
          │ /stream
┌─────────▼──────────┐
│   FastAPI Backend   │
│  - explain          │
│  - generate-tests   │
│  - bughunt          │
│  - scaffold         │
│  - run-tests        │
└─────────┬──────────┘
          │
┌─────────▼──────────┐
│   Agent Layer       │
│ ExplainAgent        │
│ TestGenAgent        │
│ BughuntAgent        │
│ ScaffoldAgent       │
└─────────┬──────────┘
          │
┌─────────▼──────────┐
│ Gemini API 2.0 Lite │
└─────────────────────┘
```

---

# 🎨 **UI Screenshots**

Below are actual screenshots from your `Images/screenshots/` folder.
Replace filenames if needed.

### 💬 Chat Interface

<img src="https://raw.githubusercontent.com/shubhamranswal/TechGuru/main/Images/screenshots/chat_empty.png" width="750px" />

### 🔍 Explain Mode

<img src="https://raw.githubusercontent.com/shubhamranswal/TechGuru/main/Images/screenshots/chat.mp4" width="750px" />

### 🧪 Test Generation

<img src="https://raw.githubusercontent.com/shubhamranswal/TechGuru/main/Images/screenshots/chat_test_generate.mp4" width="750px" />

### 🏗️ Scaffolding

<img src="https://raw.githubusercontent.com/shubhamranswal/TechGuru/main/Images/screenshots/chat_scaffold.mp4" width="750px" />

---

# 🚀 **Running Locally**

### 1. Clone repo

```bash
git clone https://github.com/shubhamranswal/TechGuru
cd TechGuru
```

### 2. Create virtual env

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your API key

Windows:

```powershell
setx GOOGLE_API_KEY "your_key_here"
```

Mac/Linux:

```bash
export GOOGLE_API_KEY="your_key_here"
```

### 5. Start server

```bash
uvicorn demo.demo_fastapi:app --reload
```

### 6. Open UI

```
http://127.0.0.1:8000/chat
```

---

# 🔌 **API Endpoints**

```
POST /explain
POST /generate-tests
POST /bughunt
POST /scaffold
GET  /run-tests
POST /stream   <-- streaming UI endpoint
```

Example:

```bash
curl -X POST "http://127.0.0.1:8000/explain" \
-H "Content-Type: application/json" \
-d "{\"code\":\"def add(a,b): return a+b\"}"
```

---

# 📦 **Project Scaffolding Example**

Generated automatically:

```
myproject/
  ├── README.md
  ├── src/
  │     └── main.py
  ├── tests/
  │     └── test_main.py
  └── .github/workflows/ci.yml
```

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

# 🧪 Running Tests

```bash
python -m pytest
```

Scaffold-generated projects also include their own tests.

---

# 🏆 **Kaggle Submission Link**

**👉 [https://kaggle.com/competitions/agents-intensive-capstone-project/writeups/techguru](https://kaggle.com/competitions/agents-intensive-capstone-project/writeups/techguru)**

---

# 📝 **Roadmap**

* VS Code extension
* More languages (JS, Java, C++)
* Better patch viewer
* Multi-file understanding
* Real-time tutoring mode
* Deploy live demo server
* Student progress tracking

---

# 🧑‍💻 **Author**

[**Shubham Singh Ranswal**](github.com/shubhamranswal)
Software Engineer

---

# 🤝 **Contributing**

Pull requests are welcome!
If you want to add test templates, fix prompts, or extend to new languages - feel free to contribute.

---

# 📄 **License**

This project is licensed under the [**MIT License**](/LICENSE).

---

# 🎉 Final Words

TechGuru started as a simple agent…
and became a friendly, powerful personal tech lead for students everywhere.

If you like the project, ⭐ star the repo and share it!