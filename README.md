# Abhyaas — UPSC Prep Tool

A beginner-friendly full-stack app for UPSC aspirants. It does two things:

1. **Learn** — read subject-wise notes (Polity, Economy to start).
2. **Evaluate** — write a Mains-style answer and get examiner-style AI feedback
   (scores out of 40, strengths, improvements, and points you missed).

Built with **Python (Flask)** + **HTML/CSS/JavaScript** + **Google Gemini**.

---

## How to run it (about 5 minutes)

You only need Python installed. Then, in a terminal, from inside this folder:

### 1. Install the requirements
```bash
pip install -r requirements.txt
```

### 2. Get your free AI key
- Go to https://aistudio.google.com/apikey
- Sign in with a Google account and click **Create API key**
- Copy the key

### 3. Add the key to the project
- Make a copy of `.env.example` and rename the copy to **`.env`**
- Open `.env` and paste your key after `GEMINI_API_KEY=`

### 4. Start the app
```bash
python app.py
```

### 5. Open it
Go to **http://127.0.0.1:5000** in your browser. Done!

The **Learn** tab works even without a key. The **Evaluate** tab needs the key.

---

## The multi-agent system (the "Ask" tab)

Instead of one giant prompt, the app uses several focused **agents**, each the
same Gemini model given a specific job. A **router** reads the aspirant's input
and picks the right one automatically.

```
User types anything
        │
        ▼
   Router agent  ──► decides: evaluator? tutor? mcq? current_affairs?
        │
        ▼
  The chosen specialist answers
        │
        ▼
  UI shows the answer + which agent handled it
```

Everything lives in the `agents/` folder:

| File | Agent's job |
|------|-------------|
| `router.py` | Reads the input, picks the right specialist. |
| `evaluator.py` | Grades Mains-style answers. |
| `tutor.py` | Explains concepts and clears doubts. |
| `mcq.py` | Generates Prelims MCQs on a topic. |
| `current_affairs.py` | Links news/events to the syllabus. |
| `orchestrator.py` | Runs the router, then calls the chosen agent. |
| `gemini_client.py` | The one place that talks to Gemini. |

**To add a new agent** (e.g. an Essay agent): create `agents/essay.py` with a
`handle()` function, then add it to the `AGENTS` map in `orchestrator.py` and
the list in `router.py`. That's it.

## What each file does

| File | What it's for |
|------|---------------|
| `app.py` | The server. Runs the website and talks to the AI. |
| `data/subjects.json` | Your notes and practice questions. **Edit this to add content.** |
| `templates/index.html` | The page layout. |
| `static/style.css` | How it looks. |
| `static/script.js` | The buttons, tabs, and calling the AI. |
| `.env` | Your secret key (you create this — never share it). |

**Tip:** To add a new subject or topic, just edit `data/subjects.json` and
refresh the page. No code changes needed.

---

## Roadmap — what to build next (in order)

You've got the two core features. Add these one at a time as you learn:

1. **User login** — so each aspirant's progress is saved.
2. **Save past evaluations** — a history page showing score trends over time.
3. **Prelims MCQ practice** — topic-wise multiple-choice questions.
4. **Previous Year Questions (PYQs)** — hugely valued by aspirants.
5. **Daily current affairs** — the make-or-break area for UPSC.
6. **Progress dashboard** — weak-area detection and revision reminders.

When you're ready for any of these, just ask and we'll build it together.

---

## Note on the AI model

The app uses the `gemini-2.0-flash` model (free-tier friendly). If Google ever
renames it, open `app.py`, find `MODEL_NAME`, and update the string. Current
model names are listed at https://ai.google.dev.
