# Bright Guide — AI-Powered Computer Advisor

> A full-stack web application that recommends the best computer matching a user's needs, budget, and preferences — powered by a RAG (Retrieval-Augmented Generation) pipeline with OpenAI GPT.

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-Full--Stack-green)](https://djangoproject.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT-orange)](https://openai.com)
[![RAG](https://img.shields.io/badge/RAG-Pipeline-purple)]()

---

## Problem Statement

Choosing the right computer is overwhelming — hundreds of models, specs, and price points. Users often don't know which machine truly fits their professional needs, budget, and preferences.

**Bright Guide** solves this by combining a structured product database with an AI layer that understands natural language requirements and recommends the most suitable options.

---

## How It Works

```
User connects and describes their needs :
"I need a laptop for video editing, budget 800€,
 I prefer lightweight machines with long battery life"
        │
        ▼
1. RETRIEVAL — Query the computer database
   → Filter by price range, category, specs
   → Retrieve candidate products

        │
        ▼
2. AUGMENTATION — Build a structured context
   → Format retrieved products as structured context
   → Combine with user requirements

        │
        ▼
3. GENERATION — OpenAI GPT analyzes and recommends
   → LLM validates candidates against user needs
   → Generates a personalized recommendation with explanation

        │
        ▼
User receives the best-matched computer + justification 
```

---

## Features

-  **User authentication** — registration, login, personalized session
-  **Product catalog** — structured database of computers with specs, price, category
- **AI recommendation engine** — RAG pipeline (database retrieval + GPT validation)
- **Dashboard** — overview of products and user activity
-  **Full-stack interface** — responsive HTML/CSS/JS templates

---

##  Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django (Python) |
| **AI Module** | OpenAI GPT API + RAG pipeline |
| **Database** | SQLite / PostgreSQL |
| **Frontend** | HTML · CSS · JavaScript |
| **Auth** | Django built-in authentication |
| **Media** | Django media files (product images) |

---

##  Repository Structure

```
computerWebsite/
├── accounts/           ← User authentication (register, login, logout)
├── article/            ← Product management (computers catalog)
├── zoodoAI/            ← RAG pipeline : retrieval + OpenAI GPT validation
├── dashbord/           ← User dashboard
├── main/               ← Main app (home, search, recommendations)
├── templates/          ← HTML templates
├── static/             ← CSS, JavaScript, images
├── media/              ← Product images
├── manage.py
└── requirements.txt
```

---






---

## AI Usage

The `zoodoAI` module uses **OpenAI GPT** as the language model for the recommendation engine. The RAG pipeline retrieves candidate products from the database and passes them as context to GPT, which generates a personalized recommendation based on the user's stated needs.

> This README was written with the assistance of Claude (Anthropic) for structure and English phrasing. The application code and AI pipeline were developed by the author.

---

##  Author

**KALMOGO Lucien** — Freelance project for PowerTech
-  M2 AI for Public Health — Aix-Marseille University
-  Research Intern — IRIT/CNRS (MELODI Team, Toulouse)
-  [LinkedIn](https://linkedin.com/in/kalmogozakir9)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
