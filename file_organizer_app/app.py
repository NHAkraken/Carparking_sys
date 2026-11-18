import os
import sys
from pathlib import Path
import shutil
from flask import Flask, render_template, request, redirect, url_for
import webview

def get_template_dir():
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, "templates")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

app = Flask(__name__, template_folder=get_template_dir())

# Define extension categories
EXTENSIONS_MAP = {
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv", ".odt"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico"],
    "Code": [".py", ".js", ".html", ".css", ".json", ".cpp", ".c", ".java", ".sql"],
    "Installers": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Media": [".mp4", ".mkv", ".avi", ".mov", ".mp3", ".wav", ".flac"],
}

last_report = None
alert_msg = None


@app.route("/", methods=["GET"])
def index():
    # Default to the user's Downloads folder as a helpful default suggestion
    default_downloads = str(Path.home() / "Downloads")
    return render_template(
        "index.html",
        target_path=default_downloads,
        last_report=last_report,
        alert_msg=alert_msg,
    )


@app.route("/organize", methods=["POST"])
def organize_folder():
    global last_report, alert_msg
    folder_path_str = request.form.get("folder_path", "").strip()

    if not folder_path_str:
        alert_msg = ("error", "Please provide a valid folder path.")
        return redirect(url_for("index"))

    target_dir = Path(folder_path_str)

    if not target_dir.exists() or not target_dir.is_dir():
        alert_msg = ("error", f"The directory '{folder_path_str}' does not exist.")
        return redirect(url_for("index"))

    moved_count = 0
    category_breakdown = {cat: 0 for cat in EXTENSIONS_MAP.keys()}
    category_breakdown["Others"] = 0
    skipped_count = 0

    # Scan the folder (non-recursive, top-level files only)
    for item in target_dir.iterdir():
        if item.is_file():
            # Skip hidden files like .DS_Store or desktop.ini
            if item.name.startswith("."):
                continue

            file_ext = item.suffix.lower()
            assigned_category = "Others"

            # Find matching category
            for cat, exts in EXTENSIONS_MAP.items():
                if file_ext in exts:
                    assigned_category = cat
                    break

            # Create destination subfolder if it doesn't exist
            dest_folder = target_dir / assigned_category
            dest_folder.mkdir(exist_ok=True)

            dest_path = dest_folder / item.name

            # Handle duplicate filenames safely
            if dest_path.exists():
                # Append a suffix like _1, _2 to prevent overwriting
                base = item.stem
                counter = 1
                while (dest_folder / f"{base}_{counter}{file_ext}").exists():
                    counter += 1
                dest_path = dest_folder / f"{base}_{counter}{file_ext}"

            try:
                shutil.move(str(item), str(dest_path))
                category_breakdown[assigned_category] += 1
                moved_count += 1
            except Exception as e:
                skipped_count += 1

    last_report = {
        "path": str(target_dir),
        "total": moved_count,
        "breakdown": {k: v for k, v in category_breakdown.items() if v > 0},
        "skipped": skipped_count,
    }
    alert_msg = ("success", f"Successfully organized {moved_count} files!")
    return redirect(url_for("index"))


if __name__ == "__main__":
    webview.create_window(
        title="FileFlow — Smart File & Document Organizer",
        url=app,
        width=1050,
        height=750,
        min_size=(850, 600),
    )
    webview.start()