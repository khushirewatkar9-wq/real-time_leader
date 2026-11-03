#!/usr/bin/env python3
"""
Real-Time Leaderboard System - Terminal CLI
A command-line interface to manage participants, update scores, and view rankings.
"""

import argparse
import sys
from tabulate import tabulate if False else None
from core.leaderboard import LeaderboardEngine

def format_table(rows, headers):
    """Simple ASCII table formatter without external dependencies."""
    if not rows:
        return "No records found."
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    sep_line = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    data_lines = [
        " | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row))
        for row in rows
    ]
    return f"\n{header_line}\n{sep_line}\n" + "\n".join(data_lines) + "\n"

def main():
    parser = argparse.ArgumentParser(
        description="Real-Time Leaderboard System CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py list
  python cli.py add "Sarah Connor" 920 --category "Cybersecurity"
  python cli.py update p-101 --delta 25 --reason "Bonus Quiz"
  python cli.py top 3
  python cli.py stats
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # List command
    list_parser = subparsers.add_parser("list", help="Display full sorted leaderboard")
    list_parser.add_argument("--category", "-c", help="Filter by category")
    list_parser.add_argument("--search", "-s", help="Search name or category")
    list_parser.add_argument("--limit", "-l", type=int, help="Limit number of rows")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new participant")
    add_parser.add_argument("name", help="Participant name")
    add_parser.add_argument("score", type=float, default=0.0, nargs="?", help="Initial score")
    add_parser.add_argument("--category", "-c", default="General", help="Category/Track")
    add_parser.add_argument("--avatar", "-a", default="🎯", help="Avatar emoji")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update participant score")
    update_parser.add_argument("id", help="Participant ID (e.g. p-101)")
    update_parser.add_argument("--score", type=float, help="Set absolute score")
    update_parser.add_argument("--delta", "-d", type=float, help="Score adjustment (+25, -10)")
    update_parser.add_argument("--reason", "-r", help="Reason for score change")

    # Top command
    top_parser = subparsers.add_parser("top", help="View top performers")
    top_parser.add_argument("count", type=int, default=3, nargs="?", help="Number of performers (default: 3)")

    # Stats command
    subparsers.add_parser("stats", help="View leaderboard analytics & statistics")

    # Reset command
    subparsers.add_parser("reset", help="Reset leaderboard to initial demo records")

    args = parser.parse_args()
    engine = LeaderboardEngine()

    if args.command == "list" or not args.command:
        data = engine.get_leaderboard(
            category=getattr(args, "category", None),
            search=getattr(args, "search", None),
            limit=getattr(args, "limit", None)
        )
        headers = ["Rank", "Trend", "Avatar", "Name", "Score", "Category", "ID"]
        rows = []
        for p in data:
            trend = "➖"
            if p.get("rank_change", 0) > 0:
                trend = f"▲ +{p['rank_change']}"
            elif p.get("rank_change", 0) < 0:
                trend = f"▼ {p['rank_change']}"
            rows.append([
                f"#{p['rank']}",
                trend,
                p.get("avatar", "⭐"),
                p["name"],
                f"{p['score']:.1f}",
                p.get("category", "General"),
                p["id"]
            ])
        print(f"\n🏆 REAL-TIME LEADERBOARD ({len(data)} Participants)")
        print(format_table(rows, headers))

    elif args.command == "add":
        new_p = engine.add_participant(
            name=args.name,
            score=args.score,
            category=args.category,
            avatar=args.avatar
        )
        print(f"✅ Successfully added {new_p['name']} (ID: {new_p['id']}) at Rank #{new_p['rank']} with {new_p['score']} pts.")

    elif args.command == "update":
        if args.score is None and args.delta is None:
            print("❌ Please specify either --score <val> or --delta <val>")
            sys.exit(1)
        res = engine.update_score(
            participant_id=args.id,
            score=args.score,
            delta=args.delta,
            reason=args.reason
        )
        if res:
            print(f"✅ Updated {res['name']}: New Score = {res['score']:.1f} (Rank #{res['rank']})")
        else:
            print(f"❌ Participant with ID '{args.id}' not found.")

    elif args.command == "top":
        top = engine.get_top_performers(count=args.count)
        print(f"\n🌟 TOP {len(top)} PERFORMERS")
        headers = ["Podium", "Avatar", "Name", "Score", "Category"]
        rows = [
            [p["badge"], p["avatar"], p["name"], f"{p['score']:.1f}", p["category"]]
            for p in top
        ]
        print(format_table(rows, headers))

    elif args.command == "stats":
        stats = engine.get_stats()
        print("\n📊 LEADERBOARD ANALYTICS")
        print(f"• Total Participants : {stats['total_participants']}")
        print(f"• Highest Score      : {stats['top_score']}")
        print(f"• Average Score      : {stats['average_score']}")
        print(f"• Median Score       : {stats['median_score']}")
        print(f"• Lowest Score       : {stats['lowest_score']}")
        print(f"• Categories         : {', '.join(stats['categories'])}")

    elif args.command == "reset":
        engine.reset_leaderboard()
        print("🔄 Leaderboard has been reset to default tournament roster.")

if __name__ == "__main__":
    main()
