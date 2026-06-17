# 🎵 Music Playlist Analyzer & Visualizer

A lightweight Python script that reads a music playlist CSV, cleans the data, and generates visual insights — no web scraping, no APIs, just your own playlist data.

---

## Features

- **Data Cleaning** — handles missing values and inconsistent types automatically
- **Top 5 Artists** — bar chart of your most-played artists
- **Tempo Distribution** — histogram of BPM spread across your playlist
- **Terminal Summary** — quick stats printed right in your console
- **PNG Output** — charts saved locally, ready to share

---

## Requirements

- Python 3.8+
- Install dependencies:

```bash
pip install -r requirements.txt
```

---

## CSV Format

Your playlist CSV must have these columns:

| Column | Example |
|---|---|
| `Track Name` | Rockn Roll Morning Light Falls on You |
| `Artist` | ASIAN KUNG-FU GENERATION |
| `Album` | Sol-fa |
| `Duration (sec)` | 271 |
| `Tempo (BPM)` | 150 |

A sample file `playlist.csv` is included to get you started.

---

## Usage

```bash
# Use the default playlist.csv
python analyzer.py

# Use a custom file
python analyzer.py --file my_playlist.csv
python analyzer.py -f my_playlist.csv
```

---

## Output

**Terminal:**
```
[OK] Loaded 6 tracks from 'playlist.csv'
[CLEAN] Data cleaned. 6 valid tracks remaining.

=============================================
       🎵 PLAYLIST ANALYSIS SUMMARY
=============================================
  Total Tracks       : 6
  Total Duration     : 21m 46s
  Avg Track Duration : 3m 37s
  Avg Tempo          : 136.3 BPM

  Top Artists by Track Count:
    1. Yorushika — 3 track(s)
    2. ASIAN KUNG-FU GENERATION — 2 track(s)
    3. Gen Hoshino — 1 track(s)
=============================================

[SAVED] bar_chart_top_artists.png
[SAVED] histogram_tempo.png
[DONE] Analysis complete.
```

**Charts saved as:**
- `bar_chart_top_artists.png`
- `histogram_tempo.png`

---

## Tech Stack

| Library | Purpose |
|---|---|
| `pandas` | Data loading and cleaning |
| `numpy` | Numeric utilities |
| `matplotlib` | Chart generation |

---

## Project Structure

```
music-playlist-analyzer/
├── analyzer.py        # Main script
├── playlist.csv       # Sample playlist data
├── requirements.txt   # Python dependencies
└── README.md
```

---

## License

MIT
