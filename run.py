#!/usr/bin/env python3
"""
PulseBoard Local Server Launcher
Runs the FastAPI real-time leaderboard server locally on http://127.0.0.1:8000
"""

import sys
import os

if __name__ == "__main__":
    try:
        import uvicorn
    except ImportError:
        print("❌ 'uvicorn' is required to launch the server locally.")
        print("👉 Install dependencies with: pip install -r requirements.txt")
        sys.exit(1)

    print("=" * 60)
    print("🏆 PulseBoard - Real-Time Leaderboard System")
    print("🎨 Theme: Pastel Pink & Light Blue")
    print("⚡ Server running at: http://127.0.0.1:8000")
    print("📖 API Swagger docs: http://127.0.0.1:8000/docs")
    print("=" * 60)

    uvicorn.run("api.index:app", host="127.0.0.1", port=8000, reload=True)
