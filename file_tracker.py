import json
import shutil
import logging
from pathlib import Path

logging.basicConfig(
    filename="processor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

tracker_file = Path("tracker.json")
inbox = Path("inbox")
processed = Path("processed")
allowed_extensions = [".txt", ".pdf", ".docx"]
inbox.mkdir(exist_ok=True)
processed.mkdir(exist_ok=True)


def load_data():
    if not tracker_file.exists():
        return {}
    try:
        with open(tracker_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        logging.error("tracker.json is corrupted")
        raise


def save_data(data):
    with open(tracker_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def scan(data):
    new_count = 0
    for file in inbox.iterdir():
        if not file.is_file():
            continue
        if file.suffix.lower() not in allowed_extensions:
            continue
        if file.name not in data:
            data[file.name] = "pending"
            new_count += 1
    return new_count


def process(data):
    done_count = 0
    error_count = 0

    for name, status in data.items():
        if status != "pending":
            continue

        source = inbox / name
        destination = processed / name

        if not source.is_file():
            data[name] = "missing"
            logging.error(f"file {name} not found in inbox")
            error_count += 1
            continue

        if destination.exists():
            data[name] = "conflict"
            logging.error(f"destination already exists: {name}")
            error_count += 1
            continue

        try:
            shutil.move(str(source), str(destination))
            data[name] = "done"
            logging.info(f"file {name} moved to processed")
            done_count += 1
        except Exception as e:
            data[name] = "error"
            logging.error(f"error moving file {name}: {e}")
            error_count += 1

    return done_count, error_count


def main():
    logging.info("starting scanner")
    data = load_data()
    try:
        new_count = scan(data)
        done_count, error_count = process(data)
    finally:
        save_data(data)

    logging.info(
        f"processed {done_count} files, {error_count} errors, added {new_count} new files"
    )
    print(
        f"processed {done_count} files, {error_count} errors, added {new_count} new files"
    )

if __name__ == "__main__":
    main()