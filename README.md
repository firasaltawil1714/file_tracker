# File Status Tracker & Processor

A lightweight Python automation script that scans an inbox folder, tracks the status of each file in a JSON file, and moves processed files to a separate folder, with full logging and safe error handling.

Built for managing batches of documents (for example, translation files) where you need to know what has been processed, what is still pending, and what failed.

## Features

- Scans the `inbox/` folder for supported files (`.txt`, `.pdf`, `.docx`)
- Registers each new file in `tracker.json` with the status `pending`
- Moves pending files to `processed/` and marks them `done`
- Never overwrites an existing file in the destination folder
- Records problems instead of crashing: `missing`, `conflict`, `error`
- Saves progress even if the script stops unexpectedly
- Writes a timestamped log to `processor.log`
- Supports Arabic and other Unicode file names

## How It Works

1. **Scan**: new files in `inbox/` are added to the tracker as `pending`.
2. **Process**: each pending file is moved to `processed/`.
3. **Save**: the updated statuses are written to `tracker.json`.

## File Statuses

| Status     | Meaning                                              |
|------------|------------------------------------------------------|
| `pending`  | Registered, waiting to be processed                  |
| `done`     | Successfully moved to `processed/`                   |
| `missing`  | Listed in the tracker but not found in `inbox/`      |
| `conflict` | A file with the same name already exists in `processed/` |
| `error`    | The move failed (details are in the log)             |

## Requirements

- Python 3.8 or newer
- No external libraries (standard library only)

## Usage

1. Put your files in the `inbox/` folder (it is created automatically on first run).
2. Run:

```bash
python file_tracker.py
```

3. Check the summary in the terminal, the details in `processor.log`, and the statuses in `tracker.json`.

Example output:

```
processed 3 files, 0 errors, added 3 new files
```

Example `tracker.json`:

```json
{
  "invoice1.docx": "done",
  "api_reference.pdf": "done",
  "notes.txt": "conflict"
}
```

## Project Structure

```
.
├── file_tracker.py
├── tracker.json      # created automatically
├── processor.log     # created automatically
├── inbox/            # put new files here
└── processed/        # processed files are moved here
```

## Libraries Used

`json`, `shutil`, `logging`, `pathlib` (all from the Python standard library)

## Author
GitHub: https://github.com/firasaltawil1714
