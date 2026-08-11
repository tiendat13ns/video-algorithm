# Algorithm Motion Graphics Generator

Production-quality 9:16 vertical animation generators (Instagram Reels, TikTok, YouTube Shorts) visualizing computer science algorithms, machine learning concepts, and software architecture using **Python** & **Manim Community Edition**.

---

## ✨ Features

- **9:16 Vertical Video Native**: Optimized for mobile short-form video (1080×1920 resolution, 60 FPS).
- **Instagram Reels Safe-Zone Compliant**: Carefully calibrated UI placement avoiding camera notches, player overlays, caption areas, and side action buttons.
- **Synchronized Audio SFX**: Custom audio pipeline generating and embedding precise sound effects (`click`, `compare`, `swap`, `success`).
- **Paper Pastel Design System**: Modern aesthetic with high-contrast text readability (7:1 contrast ratio) and fixed-camera procedural animations.

---

## 📁 Repository Structure

```text
├── src/                          # Python source code for algorithm animations
│   ├── bubblesort.py             # Bubble Sort visualization
│   ├── mergesort.py              # Merge Sort visualization (Divide & Conquer)
│   ├── heapsort.py               # Max-Heap & Array dual representation
│   ├── insertion_sort.py         # Insertion Sort visualization
│   ├── selection_sort.py         # Selection Sort visualization
│   ├── quicksort.py              # Quick Sort visualization
│   ├── hashmap.py                # Hash Table collision & lookup
│   ├── SemanticSearch.py         # Vector embeddings & cosine similarity
│   ├── kmeans_clustering.py      # K-Means clustering algorithm
│   ├── knn.py                    # K-Nearest Neighbors classifier
│   ├── linear_regression.py     # Linear Regression & loss optimization
│   ├── logistic_regression.py   # Logistic Regression & sigmoid curve
│   ├── gradient_descent.py       # Gradient Descent optimization
│   ├── make_sfx.py               # Procedural audio SFX generator (.wav)
│   └── render_with_sound.py      # Video & audio track merger (ffmpeg)
├── instagram/                    # Rendered output MP4 videos (git-ignored)
├── sfx/                          # Generated sound effects (git-ignored)
├── manim.cfg                     # Global Manim configuration (1080x1920 60fps)
└── README.md
```

---

## 🚀 Quick Start

### 1. Prerequisites & Environment Setup

Ensure Python 3.10+ and FFmpeg are installed.

```bash
# Create and activate virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate

# Install required dependencies
pip install manim imageio-ffmpeg
```

### 2. Generate Audio SFX

Generate the required `.wav` sound effect assets:

```bash
python src/make_sfx.py
```

### 3. Render Video

Render high-quality HD 1080×1920 (60 FPS) animation:

```bash
# Example: Render Merge Sort
manim -qh src/mergesort.py MergeSort

# Example: Render Heap Sort
manim -qh src/heapsort.py HeapSort
```

### 4. Merge Audio SFX

Combine the rendered video with synchronized audio:

```bash
python src/render_with_sound.py instagram/MergeSort.mp4
```

The final video with audio track will be saved at `instagram/MergeSort.mp4`.

---

## 📩 Contact & Commercial Inquiries

> **AI Skill & Motion Automation Pipeline**
>
> The automated AI skill engine, prompt engineering rulesets, anti-kerning typography systems, Reels safe-zone calculators, and visual QA review pipelines used to generate these scenes are maintained separately.
>
> If you are interested in acquiring the **AI Skill Pipeline**, custom algorithm animations, or technical collaboration, please contact:
>
> 📧 **Email:** [dat96133@gmail.com](mailto:dat96133@gmail.com)
