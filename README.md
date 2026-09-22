# Meeting-Intelligence
AI-powered meeting transcript analyzer for extracting decisions, action items, deadlines, dependencies, and project risks.


# 🧠 Meeting Intelligence

> **Turn conversations into clear execution plans.**

Meeting Intelligence is an AI-powered meeting analysis application that transforms unstructured meeting transcripts into actionable project insights.

It extracts important information such as decisions, action items, task owners, deadlines, dependencies, and potential risks, then presents them through a clean and interactive dashboard.

---

## 📸 Application Preview

<img width="1345" height="638" alt="image" src="https://github.com/user-attachments/assets/b53987fa-e97d-472c-9b84-27b75e2e37dc" />


---

## 📌 Project Overview

Important tasks and decisions are often discussed during meetings but can easily be forgotten or remain buried inside long conversations.

Meeting Intelligence helps teams convert meeting discussions into a structured execution plan by automatically identifying:

- Important project decisions
- Actionable tasks
- Responsible team members
- Task deadlines
- Task dependencies
- Potential project risks
- Project delivery blockers

This allows teams to understand **what needs to be done, who will do it, when it should be completed, and what tasks are blocking other tasks**.

---

## ✨ Key Features

### 📝 1. Meeting Transcript Analysis

Users can paste a meeting transcript into the application and analyze the conversation.

### 🎯 2. Decision Extraction

The system identifies important decisions and agreements made during meetings.

Examples include:

- Product launch decisions
- Release commitments
- Project milestones
- Team agreements

### ✅ 3. Action Item Extraction

The application extracts actionable tasks from meeting conversations and displays them in a structured format.

Each task may include:

- Task description
- Task owner
- Deadline
- Task status

### 👤 4. Owner Detection

The system identifies the team member responsible for completing a particular task.

Example:

```text
Task: Complete payment gateway integration
Owner: Amit
```
---

⏰ 5. Deadline Detection

The application identifies deadlines mentioned in the transcript, such as:

Monday

Tuesday evening

Wednesday

Friday

End of the week

---

🔗 6. Dependency Detection

The system identifies relationships between tasks and shows which task must be completed before another task can begin.

Example:

Product Catalog Approval
          ↓
Payment Gateway Integration
          ↓
Integration Testing
          ↓
Production Release

---

⚠️ 7. Risk Monitoring

The application highlights possible project risks, including:

Missing deadlines

Technical issues

Conditional releases

Complex dependency chains

Potential delivery delays

---

🕸️ 8. Dependency Map

The dependency map helps users understand task relationships and identify possible project bottlenecks.

---

📊 9. Interactive Dashboard

The dashboard provides a centralized view of:

Project overview

Extracted decisions

Action items

Task owners

Deadlines

Risk monitor

Dependency relationships

---

🔄 Application Workflow

Meeting Transcript
        ↓
Text Processing
        ↓
Sentence Analysis
        ↓
Decision Extraction
        ↓
Action Item Detection
        ↓
Owner and Deadline Detection
        ↓
Dependency Analysis
        ↓
Risk Identification
        ↓
Actionable Meeting Dashboard

---

🧪 Example Input

Weekly E-commerce Development Meeting

Sarah: We reviewed the current progress of the e-commerce platform.

Rahul: The product catalog module is 90% complete.
I will finish the remaining work by Monday.

Amit: The payment gateway integration depends on product catalog approval.
I will complete the integration by Tuesday.

Priya: Once the payment gateway is ready,
I will begin integration testing on Wednesday.

Sarah: The checkout module must be tested before the production release.

Amit: I will prepare the payment gateway test cases by Tuesday evening.

Rahul: If the API integration faces technical issues,
the delivery may be delayed.

Sarah: We agreed that the website launch will happen on Friday,
provided all testing is completed successfully.

---

---

## 📤 Example Output

### 🎯 Key Decision

> The website launch will happen on Friday, provided all testing is completed successfully.

---

### ✅ Action Items

| Task | Owner | Deadline | Status |
|---|---|---|---|
| Complete product catalog module | Rahul | Monday | Pending |
| Complete payment gateway integration | Amit | Tuesday | Pending |
| Begin integration testing | Priya | Wednesday | Pending |
| Test checkout module | Sarah | Not specified | Pending |
| Prepare payment gateway test cases | Amit | Tuesday evening | Pending |
| Website launch | Sarah | Friday | Pending |

---

### 🔗 Dependency Map

```text
Product Catalog Approval
        ↓
Payment Gateway Integration
```

```text
Payment Gateway
        ↓
Integration Testing
```

```text
Checkout Module Testing
        ↓
Production Release
```

---

### ⚠️ Risk Monitor

Potential risks identified from the meeting:

- Missing deadline for checkout module testing
- Technical issues affecting delivery
- Multiple dependencies creating schedule delays
- Website launch depending on successful testing

---

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend processing and text analysis |
| FastAPI | Backend API development |
| HTML | Frontend structure |
| CSS | Styling and responsive design |
| JavaScript | Frontend interaction and API communication |
| Regular Expressions | Pattern-based information extraction |
| JSON | Structured data exchange |
| Uvicorn | FastAPI application server |

---


## 📂 Project Structure

```text
Meeting-Intelligence/
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── templates/
│   └── index.html
│
├── docs/
│   └── ui-preview.png
│
├── app.py
├── requirements.txt
└── README.md
```

> Update the project structure according to your actual files.

---

⚙️ Installation and Setup

1. Clone the Repository
git clone https://github.com/prajapatishubham336/meeting-intelligence.git

3. Navigate to the Project Directory
cd meeting-intelligence

5. Create a Virtual Environment
python -m venv venv

7. Activate the Virtual Environment
Windows
venv\Scripts\activate

8. macOS/Linux
source venv/bin/activate

9. Install Dependencies
pip install -r requirements.txt

11. Run the Application

For a standard Python application:

python app.py

For a FastAPI application using Uvicorn:

uvicorn app:app --reload

7. Open in Browser
http://127.0.0.1:8000

---

💡 Use Cases

Meeting Intelligence can be useful for:

Software development meetings

Sprint planning

Project review meetings

Product management discussions

Client meetings

Business operations meetings

Release planning

Technical coordination meetings

Startup team meetings

Team progress tracking

---

🚀 Benefits

Reduces manual meeting documentation

Improves task visibility

Makes task ownership clear

Helps teams track deadlines

Identifies task dependencies

Highlights potential project blockers

Converts conversations into actionable plans

Improves project coordination

Supports better accountability

---

🔮 Future Enhancements

Planned or possible future improvements include:

Audio-to-text meeting transcription

Zoom integration

Google Meet integration

Microsoft Teams integration

PDF and Excel report export

Slack and email notifications

Calendar integration

Automatic task reminders

Multi-language transcript analysis

Advanced NLP and LLM-based extraction

Historical meeting search

User authentication

Team-based workspaces

Integration with project-management tools

---

⚠️ Limitations

The accuracy of extracted information depends on:

Transcript quality

Clarity of the conversation

Correct speaker identification

Explicitly mentioned deadlines

Complexity of sentence structures

Important project decisions and extracted tasks should be reviewed by the responsible team members before execution.

---

🎓 Learning Outcomes

This project demonstrates practical implementation of:

Natural Language Processing concepts

Text classification and extraction

Rule-based information extraction

Backend API development

Frontend and backend integration

Project management automation

Dependency and risk analysis

Dashboard-based data visualization

---

👨‍💻 Author

**Shubham Prajapati**

AI/ML and Generative AI

Meeting Intelligence — AI-powered meeting analysis for actionable project execution.

📄 License

This project is developed for educational, portfolio, and demonstration purposes.
