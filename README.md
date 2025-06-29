# 🗣️ SpeakQL

**Conversational SQL Interface for Enterprise Data Teams**

SpeakQL is a Streamlit-powered AI app that lets users query structured databases like SQLite using natural language — via text or voice — and receive intelligent SQL-generated answers. Whether you're a data analyst or a business leader, SpeakQL lets you skip SQL and just ask.

---

## 🌟 Features

### 🔹 SpeakQL (Fast Mode)
> Lightweight querying for simple, fast interactions.

- Ask basic natural language questions.
- Optimized for speed (non-agentic execution).
- Example queries:
  - _"How many customers are there?"_
  - _"What are the different artist names?"_

### 🔸 SpeakQL Pro (Agentic Mode)
> Uses SQL agents for deep, multi-step reasoning.

- Handles complex queries using LangGraph agents.
- Dynamically generates SQL with joins, grouping, filters.
- Ideal for in-depth questions like:
  - _"Which artist had the most album sales in 2009?"_
  - _"What’s the revenue per genre sorted descending?"_

---

## 🧠 Enterprise-Ready Enhancements

The `SpeakQL for Enterprise` page includes powerful capabilities tailored for organizational use:

| Feature                        | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| 🎨 **ER Diagram Generation**   | Auto-generates Entity-Relationship diagrams for your database.              |
| 🧠 **SQL Agent Integration**   | Uses agents to reason across complex database schemas.                      |
| 🎙️ **Voice-to-Text Input**    | Direct voice recording translated into SQL prompts.                         |
| 🔒 **Runs Locally**            | No user data is ever stored — stays fully local for privacy and compliance. |

---

## 🔮 Future Enhancements

| Feature                      | Description                                                              |
|-----------------------------|--------------------------------------------------------------------------|
| ✅ **Data Validation**       | Custom logic to validate and sanitize generated SQL before execution.    |
| 👤 **Human-in-the-Loop**     | Manually approve SQL before it executes.                                 |
| 🔌 **API + Plugin Ready**    | Plug SpeakQL into BI tools, Slack, dashboards.                           |
| 🏢 **Role-Based Access**     | Enforce RBAC policies based on enterprise auth layers.                   |

---

## 🎤 Tech Stack

- 🐍 [Python](https://www.python.org)
- 🦜 [Langchain](https://www.langchain.com)
- 🎈 [Streamlit](https://streamlit.io)
- 🗄️ SQLite (via [Chinook Database](https://github.com/lerocha/chinook-database))

---

## 🚀 Getting Started

```bash
# Clone the repo
git clone https://github.com/your-username/speakql.git
cd speakql

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your API keys to .streamlit/secrets.toml
