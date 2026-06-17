"""
Music Playlist Analyzer & Visualizer
=====================================
Reads a playlist CSV, cleans the data, analyzes it,
and generates visual charts as PNG files.

Usage:
    python analyzer.py
    python analyzer.py --file my_playlist.csv
"""

import argparse
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend (no display needed)
import matplotlib.pyplot as plt


# ─────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────

def load_data(filepath: str) -> pd.DataFrame:
    """
    Reads the CSV file and returns a Pandas DataFrame.
    Raises a clear error if the file is not found or columns are missing.
    """
    required_columns = {"Track Name", "Artist", "Album", "Duration (sec)", "Tempo (BPM)"}

    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"[ERROR] File not found: '{filepath}'")
        sys.exit(1)

    # Check that all required columns exist
    missing = required_columns - set(df.columns)
    if missing:
        print(f"[ERROR] CSV is missing column(s): {missing}")
        sys.exit(1)

    print(f"[OK] Loaded {len(df)} tracks from '{filepath}'")
    return df


# ─────────────────────────────────────────────
# 2. CLEAN DATA
# ─────────────────────────────────────────────

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handles missing values and ensures correct data types.
    - Drops rows where Artist or Track Name is missing (can't analyze without them).
    - Fills missing numeric values with column median.
    - Coerces Duration and Tempo to numeric types.
    """
    initial_count = len(df)

    # Drop rows missing critical text fields
    df = df.dropna(subset=["Track Name", "Artist"])

    # Coerce numeric columns (non-parseable values become NaN)
    df["Duration (sec)"] = pd.to_numeric(df["Duration (sec)"], errors="coerce")
    df["Tempo (BPM)"]    = pd.to_numeric(df["Tempo (BPM)"],    errors="coerce")

    # Fill remaining NaN numerics with median of that column
    df["Duration (sec)"] = df["Duration (sec)"].fillna(df["Duration (sec)"].median())
    df["Tempo (BPM)"]    = df["Tempo (BPM)"].fillna(df["Tempo (BPM)"].median())

    # Strip extra whitespace from text columns
    df["Track Name"] = df["Track Name"].str.strip()
    df["Artist"]     = df["Artist"].str.strip()

    dropped = initial_count - len(df)
    if dropped:
        print(f"[CLEAN] Dropped {dropped} row(s) with missing Track Name or Artist.")

    print(f"[CLEAN] Data cleaned. {len(df)} valid tracks remaining.")
    return df


# ─────────────────────────────────────────────
# 3. ANALYZE DATA
# ─────────────────────────────────────────────

def analyze_data(df: pd.DataFrame) -> dict:
    """
    Computes key statistics from the cleaned playlist.

    Returns a dict with:
      - top_artists    : Pandas Series of top 5 artists by track count
      - avg_bpm        : Average tempo across all tracks
      - avg_duration   : Average track duration in seconds
      - total_duration : Total playlist duration in seconds
    """
    # Count how many tracks each artist has, pick top 5
    top_artists = df["Artist"].value_counts().head(5)

    avg_bpm       = df["Tempo (BPM)"].mean()
    avg_duration  = df["Duration (sec)"].mean()
    total_duration = df["Duration (sec)"].sum()

    return {
        "top_artists":     top_artists,
        "avg_bpm":         avg_bpm,
        "avg_duration":    avg_duration,
        "total_duration":  total_duration,
    }


# ─────────────────────────────────────────────
# 4. PRINT SUMMARY
# ─────────────────────────────────────────────

def print_summary(df: pd.DataFrame, stats: dict) -> None:
    """
    Prints a clean, terminal-friendly summary of the playlist analysis.
    """
    total_min = int(stats["total_duration"] // 60)
    total_sec = int(stats["total_duration"] % 60)
    avg_min   = int(stats["avg_duration"] // 60)
    avg_sec   = int(stats["avg_duration"] % 60)

    print()
    print("=" * 45)
    print("       🎵 PLAYLIST ANALYSIS SUMMARY")
    print("=" * 45)
    print(f"  Total Tracks       : {len(df)}")
    print(f"  Total Duration     : {total_min}m {total_sec}s")
    print(f"  Avg Track Duration : {avg_min}m {avg_sec}s")
    print(f"  Avg Tempo          : {stats['avg_bpm']:.1f} BPM")
    print()
    print("  Top Artists by Track Count:")
    for rank, (artist, count) in enumerate(stats["top_artists"].items(), start=1):
        print(f"    {rank}. {artist} — {count} track(s)")
    print("=" * 45)
    print()


# ─────────────────────────────────────────────
# 5. VISUALIZE DATA
# ─────────────────────────────────────────────

def visualize_data(df: pd.DataFrame, stats: dict) -> None:
    """
    Generates and saves two charts as PNG files:
      1. bar_chart_top_artists.png  — Top 5 artists by track count
      2. histogram_tempo.png        — Distribution of Tempo (BPM)
    """

    # ── Chart 1: Bar Chart — Top 5 Artists ──
    fig1, ax1 = plt.subplots(figsize=(8, 5))

    artists = stats["top_artists"].index.tolist()
    counts  = stats["top_artists"].values.tolist()
    colors  = plt.cm.Set2(np.linspace(0, 1, len(artists)))

    bars = ax1.bar(artists, counts, color=colors, edgecolor="black", linewidth=0.7)

    # Add count labels on top of each bar
    for bar, count in zip(bars, counts):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.05,
            str(count),
            ha="center", va="bottom", fontsize=11, fontweight="bold"
        )

    ax1.set_title("Top 5 Artists by Track Count", fontsize=14, fontweight="bold", pad=12)
    ax1.set_xlabel("Artist", fontsize=11)
    ax1.set_ylabel("Number of Tracks", fontsize=11)
    ax1.set_ylim(0, max(counts) + 1)
    ax1.tick_params(axis="x", rotation=15)
    ax1.grid(axis="y", linestyle="--", alpha=0.5)
    fig1.tight_layout()

    output1 = "bar_chart_top_artists.png"
    fig1.savefig(output1, dpi=150)
    plt.close(fig1)
    print(f"[SAVED] {output1}")

    # ── Chart 2: Histogram — Tempo Distribution ──
    fig2, ax2 = plt.subplots(figsize=(8, 5))

    bpm_values = df["Tempo (BPM)"].dropna()

    # Number of bins: at least 5, scales with data size
    n_bins = max(5, len(bpm_values) // 2)

    ax2.hist(bpm_values, bins=n_bins, color="#5B9BD5", edgecolor="black",
             linewidth=0.7, alpha=0.85)

    # Mark the average BPM with a dashed vertical line
    avg_bpm = stats["avg_bpm"]
    ax2.axvline(avg_bpm, color="red", linestyle="--", linewidth=1.5,
                label=f"Avg BPM: {avg_bpm:.1f}")

    # Highlight a "target BPM zone" around 149 BPM (example from brief)
    ax2.axvspan(144, 154, alpha=0.15, color="orange", label="Target zone ~149 BPM")

    ax2.set_title("Tempo (BPM) Distribution", fontsize=14, fontweight="bold", pad=12)
    ax2.set_xlabel("Tempo (BPM)", fontsize=11)
    ax2.set_ylabel("Number of Tracks", fontsize=11)
    ax2.legend(fontsize=10)
    ax2.grid(axis="y", linestyle="--", alpha=0.5)
    fig2.tight_layout()

    output2 = "histogram_tempo.png"
    fig2.savefig(output2, dpi=150)
    plt.close(fig2)
    print(f"[SAVED] {output2}")


# ─────────────────────────────────────────────
# 6. MAIN ENTRY POINT
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Music Playlist Analyzer & Visualizer"
    )
    parser.add_argument(
        "--file", "-f",
        default="playlist.csv",
        help="Path to the playlist CSV file (default: playlist.csv)"
    )
    args = parser.parse_args()

    # Run the pipeline step by step
    df    = load_data(args.file)
    df    = clean_data(df)
    stats = analyze_data(df)
    print_summary(df, stats)
    visualize_data(df, stats)

    print("[DONE] Analysis complete.")


if __name__ == "__main__":
    main()
