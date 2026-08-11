# Manim Video Generator

Bộ công cụ tạo video hoạt hình ngắn (9:16 Dọc - Reels/Shorts/TikTok) minh họa thuật toán & hệ thống bằng Manim.

---

## 🚀 1. Chuẩn bị môi trường

Kích hoạt môi trường ảo Python và cài đặt các thư viện cần thiết:

```bash
# Kích hoạt venv (trên Windows)
.venv\Scripts\activate

# Cài đặt thư viện (nếu chưa có)
pip install manim imageio-ffmpeg
```

---

## 🔊 2. Tạo file âm thanh (SFX)

Tạo sẵn các hiệu ứng âm thanh `.wav` (click, compare, swap, success) vào thư mục `sfx/`:

```bash
python src/make_sfx.py
```

---

## 🎬 3. Render Video

Sử dụng câu lệnh Manim CLI để xuất video từ script Python:

* **Preview nhanh (Chất lượng thấp, render nhanh):**
  ```bash
  manim -ql src/bubblesort.py BubbleSort
  ```

* **Render bản đẹp (Chất lượng cao HD - 1080x1920, 60fps):**
  ```bash
  manim -qh src/bubblesort.py BubbleSort
  ```

> **Lưu ý:** Video render xong sẽ nằm trong thư mục `instagram/`.

---

## 🔊 4. Ghép âm thanh vào Video

Gộp track âm thanh `.wav` vào video `.mp4` đã render:

```bash
python src/render_with_sound.py instagram/BubbleSort.mp4
```

---

## 📁 5. Danh sách thuật toán có sẵn (trong `src/`)

* **Bubble Sort:** `src/bubblesort.py` (`BubbleSort`)
* **Heap Sort:** `src/heapsort.py` (`HeapSort`)
* **Insertion Sort:** `src/insertion_sort.py` (`InsertionSort`)
* **HashMap:** `src/hashmap.py` (`HashMap`)
* **Semantic Search:** `src/SemanticSearch.py` (`SemanticSearch`)
