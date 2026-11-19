
# 🧠 NEXUS AI – Intelligent Research Assistant

NEXUS AI is an AI-powered research assistant built using Python, Streamlit, LangChain, and Groq.

It helps users research topics, generate answers, search the web, and view source links through a simple interface.

## 📸 Application Screenshot

![NEXUS AI Application](assets/nexus-ai-screenshot.png)

## ✨ Features

- AI-powered research answers
- Web search integration
- Source URL accessibility checks
- Prioritization of selected domains
- Conversation history and memory
- Quick, Detailed, and Technical Research modes
- Interactive Streamlit interface
- Error handling for unclear questions

## 🛠️ Technologies Used

- Python
- Streamlit
- LangChain
- Groq API
- DuckDuckGo Search (DDGS)
- Requests

## 📁 Project Structure

```text
NEXUS_AI/
│
├── app.py
├── agent.py
├── tools.py
├── requirements.txt
├── .gitignore
│
└── assets/
    ├── style.css
    └── nexus-ai-screenshot.png
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/palyamindhu111/NEXUS_AI.git
```

### 2. Open the project folder

```bash
cd NEXUS_AI
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure your API key

Create a `.env` file in the project folder:

```text
GROQ_API_KEY=your_groq_api_key
```

**Important:** Never upload your API key to GitHub.

### 7. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal.

## 🧪 Testing

The following features have been manually tested:

- Research question answering
- Web search
- Source accessibility checking
- Follow-up questions using conversation history
- Python and Java comparison
- Unclear-question handling

## 🎯 Project Objective

The objective of NEXUS AI is to demonstrate how AI agents can use external tools, retrieve information, process results, and generate useful research responses.

## 👩‍💻 Author

**Indhu**

## 📌 Future Improvements

- Better source quality verification
- More research tools
- Improved conversation memory
- Export research reports
- Enhanced user interface

## 🔗 GitHub Repository

https://github.com/palyamindhu111/NEXUS_AI

