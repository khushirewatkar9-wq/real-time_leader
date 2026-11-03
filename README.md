# 🏆 PulseBoard — Real-Time Leaderboard System

An ultra-responsive, Python-powered **Real-Time Leaderboard System** designed to track, rank, and spotlight participants or students as scores dynamically shift. Features instant descending re-ranking, live displacement tracking, a 3D Hall of Fame podium, and a custom **Pink & Light Blue Theme**.

Ready for **one-click deployment to Vercel**.

---

## ✨ Key Features

- **⚡ Instant Real-Time Sorting & Displacement Tracking**:
  - Automatically sorts participants in descending order by score with secondary tie-break logic.
  - Computes rank movement (`▲ +2`, `▼ -1`, `➖ 0`) relative to previous position.
- **🥇 3D Podium & Top Performers Spotlight**:
  - Highlights top 3 contenders with Gold 👑, Silver, and Bronze pedestals, crowns, and animated glowing borders.
  - Automatically triggers festive confetti celebrations whenever someone claims the #1 Champion position.
- **🎨 Pink & Light Blue Theme**:
  - Modern pastel cotton-candy aesthetic with subtle glowing mesh orbs, glassmorphic cards, and neon badges.
  - Includes a Dark Mode toggle (Cyber Synthwave) with neon pink (`#EC4899`) and cyan (`#38BDF8`).
- **💾 Dual Persistence (File Handling & SQLite)**:
  - Supports persistent file handling (`data/leaderboard.json`) or SQLite database (`data/leaderboard.db`).
  - Seamlessly adapts to serverless environments (e.g. Vercel) using `/tmp` and in-memory caches to prevent crashes on read-only filesystems.
- **🎵 Synthesized Web Audio Chimes**:
  - Built-in Web Audio API tone synthesizer (uplifting chimes on score boosts and triumphant fanfare on reaching #1) with zero external MP3 dependencies.
- **🎲 Live Competition Simulator**:
  - Built-in live simulation bot (`Live Sim` button) that triggers real-time score boosts and activity alerts to demonstrate live ranking updates during demos.
- **🖥️ Standalone Python CLI Tool**:
  - Includes `cli.py` to add participants, update scores, and view leaderboards straight from your command line.

---

## 📁 Project Architecture

```
realtime-leaderboard/
├── api/
│   └── index.py            # FastAPI main app & Vercel serverless entrypoint
├── core/
│   ├── __init__.py
│   ├── models.py           # Pydantic data schemas
│   ├── storage.py          # Storage manager (JSON file handling & SQLite)
│   └── leaderboard.py      # Core ranking engine, statistics, tie-breaks
├── data/
│   └── leaderboard.json    # Initial seed data for competition roster
├── public/
│   ├── index.html          # Web UI with Pink & Light Blue Theme
│   ├── style.css           # Glassmorphism, neon glows, responsive layouts
│   └── app.js              # Real-time state synchronization, audio, confetti
├── cli.py                  # Standalone Python CLI for terminal management
├── run.py                  # Local FastAPI server launcher
├── requirements.txt        # Python dependencies
├── vercel.json             # Vercel serverless deployment config
└── README.md
```

---

## 🚀 Quickstart: Running Locally

### 1. Prerequisites
Ensure you have Python 3.9+ installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Web Server
```bash
python run.py
```
Open your browser and navigate to:
- **Web Application**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 💻 Terminal CLI Usage

You can manage the leaderboard directly from the terminal using `cli.py`:

```bash
# 1. View current rankings
python cli.py list

# 2. Add a new participant
python cli.py add "Sarah Connor" 890 --category "AI & Robotics" --avatar "🤖"

# 3. Boost score with delta
python cli.py update p-101 --delta 50 --reason "Hackathon Champion"

# 4. View top 3 podium
python cli.py top 3

# 5. View leaderboard statistics
python cli.py stats

# 6. Reset to initial roster
python cli.py reset
```

---

## 🌐 Deploying to Vercel

This repository is pre-configured with `vercel.json` and `@vercel/python` for instantaneous deployment.

### Method 1: Deploy via GitHub (Recommended)
1. Push this folder to a GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of Real-Time Leaderboard System"
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git branch -M main
   git push -u origin main
   ```
2. Go to [vercel.com](https://vercel.com) and log in.
3. Click **Add New Project** &rarr; **Import Git Repository**.
4. Select your repository.
5. Vercel automatically detects `vercel.json` and `api/index.py`. Click **Deploy**!
6. Your live website URL will be ready in under 60 seconds (e.g. `https://your-leaderboard.vercel.app`).

### Method 2: Deploy via Vercel CLI
1. Install Vercel CLI globally (if not already installed):
   ```bash
   npm install -g vercel
   ```
2. In the `realtime-leaderboard` directory, run:
   ```bash
   vercel
   ```
3. Follow the on-screen prompts (accept defaults). When complete, deploy to production:
   ```bash
   vercel --prod
   ```

---

## 📡 RESTful API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/leaderboard` | Get sorted participants, top 3, metrics, and live events |
| `POST` | `/api/participants` | Register a new participant (`name`, `score`, `category`, `avatar`) |
| `PATCH` | `/api/participants/{id}/score` | Adjust score by `delta` (+10, -5) or set absolute `score` |
| `DELETE` | `/api/participants/{id}` | Remove a participant from the competition |
| `GET` | `/api/stats` | Retrieve aggregated score metrics (mean, median, top score) |
| `POST` | `/api/reset` | Reset leaderboard back to default tournament roster |
| `POST` | `/api/simulate` | Simulate a random competition event (for live demos) |

---

## 🎨 Theme Palette (Pink & Light Blue)

| Element | Color Hex | Role |
|---|---|---|
| **Primary Pink** | `#EC4899` / `#F472B6` | Accents, Champion Pedestal, Active Pills, Glows |
| **Sky Blue** | `#0EA5E9` / `#38BDF8` | Badges, Track Tags, Secondary Buttons |
| **Pastel Background** | `#F8FAFC` &rarr; `#FDF2F8` | Light Theme Ambient Mesh Background |
| **Dark Theme Slate** | `#090D16` &rarr; `#130F1E` | Cyber Neon Dark Mode Background |
| **Gold / Crown** | `#F59E0B` / `#FBBF24` | 1st Place Podium & Laurel |
