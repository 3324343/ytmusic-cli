import subprocess
import json
import sys
from rich.console import Console
from rich.table import Table

console = Console()

def search_music(query, limit=10):
    cmd = [
        "yt-dlp",
        f"ytsearch{limit}:{query}",
        "--dump-json",
        "--flat-playlist",
        "--skip-download"
    ]

    results = []
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)

    for line in process.stdout:
        data = json.loads(line)
        results.append({
            "title": data.get("title"),
            "id": data.get("id"),
            "duration": data.get("duration"),
            "channel": data.get("uploader")
        })

    return results

def show_results(results):
    table = Table(title="YouTube Music Search")

    table.add_column("No", justify="right")
    table.add_column("Title", style="cyan")
    table.add_column("Channel", style="magenta")
    table.add_column("Duration", justify="right")

    for i, r in enumerate(results, 1):
        dur = str(r["duration"]) if r["duration"] else "-"
        table.add_row(str(i), r["title"], r["channel"], dur)

    console.print(table)

def play_video(video_id):
    url = f"https://music.youtube.com/watch?v={video_id}"
    console.print(f"[green]▶ Playing:[/] {url}\nPress Q to quit player")

    subprocess.run([
        "mpv",
        "--no-video",
        "--quiet",
        url
    ])

def main():
    console.print("[bold red]YouTube Music Terminal Player[/bold red]\n")

    query = console.input("[bold yellow]Search:[/] ")
    if not query.strip():
        sys.exit()

    results = search_music(query)
    if not results:
        console.print("[red]No results found[/red]")
        return

    show_results(results)

    choice = console.input("\n[bold green]Choose number:[/] ")
    if not choice.isdigit():
        return

    idx = int(choice) - 1
    if idx < 0 or idx >= len(results):
        return

    play_video(results[idx]["id"])

if __name__ == "__main__":
    main()
