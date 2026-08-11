from manim import *
import numpy as np
import os

# ====================================================
# FORMAT & USER PASTEL COLOR PALETTE (HIGH CONTRAST TEXT)
# Output: 1080x1920 (9:16 Vertical), 60fps, 8000 KBPS
# Target Video Duration: ~18.5 Seconds
# ====================================================
COLOR_BG = "#F4ECE1"               # Warm Cream Paper
COLOR_TEXT = "#1C1917"              # Dark Charcoal Ink Text
COLOR_MUTED = "#57534E"            # Warm Stone Gray (Subtitles/Author)
COLOR_GRID = "#D6CBB8"             # Soft Parchment Grid Lines
COLOR_CARD_BG = "#EFE6D8"          # Warm Container Fill
COLOR_CARD_BORDER = "#B8A995"      # Warm Card Border

# Quick Sort State Palette
COLOR_IDLE = "#A0C4FF"             # Soft Pastel Blue (Unsorted)
COLOR_PIVOT = "#FF9F1C"            # Gold / Orange (Active Pivot)
COLOR_COMPARE = "#FFD185"          # Soft Coral Amber (Scanning)
COLOR_SWAP = "#FFB7B2"             # Soft Peach Pink (Swapping)
COLOR_SORTED = "#73E6D0"           # Mint Green (Sorted / Fixed)

# High-Contrast Status Text Palette (Crisp Readability on Light Paper)
COLOR_STATUS_PIVOT = "#B45309"      # Rich Amber Bronze (High Contrast 7:1)
COLOR_STATUS_SWAP = "#C026D3"       # Rich Magenta Violet (High Contrast 7:1)
COLOR_STATUS_SORTED = "#047857"      # Rich Emerald Green (High Contrast 7:1)

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9.0
config.frame_height = 16.0
config.frame_rate = 60
config.bitrate = "8000k"
config.background_color = COLOR_BG

# ====================================================
# PROCEDURAL UI COMPONENTS
# ====================================================

class BackgroundGrid(VGroup):
    """Subtle technical grid styled for warm paper aesthetic."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        dots = VGroup()
        for x in np.arange(-4.0, 4.5, 0.8):
            for y in np.arange(-7.5, 8.0, 0.8):
                dot = Dot(point=[x, y, 0], radius=0.025, color=COLOR_GRID)
                dot.set_opacity(0.65)
                dots.add(dot)
        self.add(dots)

class AuthorBadge(VGroup):
    """Sleek modern author watermark badge with clean kerning."""
    def __init__(self, handle="@tiendatbrn", pos=np.array([0.0, -4.15, 0])):
        super().__init__()
        self.handle_text = Text(handle, font="Consolas", font_size=13, weight=BOLD, color=COLOR_MUTED)
        
        self.box = RoundedRectangle(
            corner_radius=0.16,
            width=self.handle_text.width + 0.45,
            height=0.40,
            color=COLOR_CARD_BORDER,
            stroke_width=1.5,
            fill_color=COLOR_CARD_BG,
            fill_opacity=0.95
        )
        self.handle_text.move_to(self.box.get_center())
        self.add(self.box, self.handle_text)
        self.move_to(pos)
        self.set_z_index(10)

class StatusCard(VGroup):
    """Compact status card displaying Phase and Quick Sort metrics."""
    def __init__(self, pos=np.array([0.0, -3.10, 0])):
        super().__init__()
        self.pos = pos
        self.box = RoundedRectangle(
            corner_radius=0.14,
            width=6.0,
            height=0.72,
            color=COLOR_CARD_BORDER,
            stroke_width=1.5,
            fill_color=COLOR_CARD_BG,
            fill_opacity=0.95
        ).move_to(pos)
        
        self.title_label = Text("QUICK SORT STATUS", font="Consolas", font_size=10, weight=BOLD, color=COLOR_MUTED)
        self.title_label.move_to(pos + UP * 0.16)
        
        self.value_text = Text("Status: Unsorted Array", font="Consolas", font_size=14, weight=BOLD, color=COLOR_TEXT)
        self.value_text.move_to(pos + DOWN * 0.12)
        
        self.add(self.box, self.title_label, self.value_text)
        self.set_z_index(10)

    def update_status(self, text: str, color=COLOR_TEXT):
        new_text = Text(text, font="Consolas", font_size=14, weight=BOLD, color=color)
        new_text.move_to(self.value_text.get_center())
        self.value_text.become(new_text)

class QuickSort(Scene):
    def play_sfx(self, sfx_name: str):
        """Helper to play SFX safely from sfx/ directory."""
        path = os.path.join("sfx", f"{sfx_name}.wav")
        if os.path.exists(path):
            self.add_sound(path)

    def construct(self):
        # ----------------------------------------------------
        # 1. SETUP STATIC SYSTEM DIAGRAM
        # ----------------------------------------------------
        grid = BackgroundGrid()
        grid.set_z_index(0)
        self.add(grid)

        # Header Titles (Instagram Reels Safe Zone: Y = 4.8)
        title = Text(
            "QUICK SORT",
            font="Segoe UI",
            font_size=36,
            weight=BOLD,
            color=COLOR_TEXT
        ).move_to(np.array([0.0, 4.8, 0])).set_z_index(10)

        subtitle = Text(
            "Lomuto Partitioning Mechanism",
            font="Verdana",
            font_size=14,
            color=COLOR_MUTED
        ).next_to(title, DOWN, buff=0.15).set_z_index(10)

        author_badge = AuthorBadge(handle="@tiendatbrn", pos=np.array([0.0, -4.15, 0]))
        status_card = StatusCard(pos=np.array([0.0, -3.10, 0]))

        self.play_sfx("click")
        self.play(
            Write(title),
            FadeIn(subtitle, shift=DOWN * 0.1),
            FadeIn(author_badge, shift=UP * 0.1),
            FadeIn(status_card, shift=UP * 0.1),
            run_time=1.0
        )

        # ----------------------------------------------------
        # 2. INITIAL ARRAY CREATION (7 Elements)
        # ----------------------------------------------------
        initial_vals = [4, 2, 7, 1, 6, 3, 5]
        n = len(initial_vals)
        xs = np.linspace(-2.4, 2.4, n)
        y_pos = 0.8

        bars = []
        labels = []
        
        # Track active bar objects in current array slots (slots 0..6)
        slot_bars = [None] * n

        for i, val in enumerate(initial_vals):
            h = val * 0.40 + 0.4
            w = 0.58
            
            b = RoundedRectangle(
                corner_radius=0.08,
                width=w,
                height=h,
                color=COLOR_CARD_BORDER,
                stroke_width=1.5,
                fill_color=COLOR_IDLE,
                fill_opacity=0.95
            ).move_to(np.array([xs[i], y_pos, 0]))
            
            lbl = Text(str(val), font="Consolas", font_size=16, weight=BOLD, color=COLOR_TEXT)
            # Decoupled updater pinning text to bar's bottom edge with fixed 0.28 offset
            lbl.add_updater(lambda l, bar_ref=b: l.move_to(bar_ref.get_bottom() + DOWN * 0.28))
            
            b.set_z_index(4)
            lbl.set_z_index(5)
            
            bars.append(b)
            labels.append(lbl)
            slot_bars[i] = b

        self.play_sfx("click")
        self.play(
            LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in bars], lag_ratio=0.06),
            LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.06),
            run_time=1.2
        )
        self.wait(0.5)

        # Helper function to swap two slots in the array visually
        def swap_slots(idx1, idx2, run_time=0.9):
            if idx1 == idx2:
                return
            b1 = slot_bars[idx1]
            b2 = slot_bars[idx2]
            p1 = np.array([xs[idx1], y_pos, 0])
            p2 = np.array([xs[idx2], y_pos, 0])

            # Arc motion for smooth swap
            self.play_sfx("swap")
            self.play(
                b1.animate.move_to(p2),
                b2.animate.move_to(p1),
                run_time=run_time,
                rate_func=smooth
            )
            # Update tracking array
            slot_bars[idx1], slot_bars[idx2] = slot_bars[idx2], slot_bars[idx1]

        # ----------------------------------------------------
        # 3. PARTITION 1: Pivot = 5 (slot 6)
        # ----------------------------------------------------
        status_card.update_status("Select Pivot = 5", COLOR_STATUS_PIVOT)
        self.play_sfx("compare")
        self.play(
            slot_bars[6].animate.set_fill(COLOR_PIVOT),
            run_time=0.6
        )
        self.wait(0.4)

        # Partitioning step 1: swap slot 3 (val 1) and slot 2 (val 7)
        status_card.update_status("Partition: 1 < 5 -> Swap with 7", COLOR_STATUS_SWAP)
        self.play(
            slot_bars[3].animate.set_fill(COLOR_SWAP),
            slot_bars[2].animate.set_fill(COLOR_SWAP),
            run_time=0.5
        )
        swap_slots(2, 3)
        self.play(
            slot_bars[2].animate.set_fill(COLOR_IDLE),
            slot_bars[3].animate.set_fill(COLOR_IDLE),
            run_time=0.3
        )
        self.wait(0.4)

        # Partitioning step 2: swap slot 5 (val 3) and slot 3 (val 7)
        status_card.update_status("Partition: 3 < 5 -> Swap with 7", COLOR_STATUS_SWAP)
        self.play(
            slot_bars[5].animate.set_fill(COLOR_SWAP),
            slot_bars[3].animate.set_fill(COLOR_SWAP),
            run_time=0.5
        )
        swap_slots(3, 5)
        self.play(
            slot_bars[3].animate.set_fill(COLOR_IDLE),
            slot_bars[5].animate.set_fill(COLOR_IDLE),
            run_time=0.3
        )
        self.wait(0.4)

        # Place Pivot 5 in final position: swap slot 6 (pivot 5) with slot 4 (val 6)
        status_card.update_status("Place Pivot 5 in Position [4]", COLOR_STATUS_PIVOT)
        swap_slots(4, 6)
        
        # Lock Pivot 5 in Mint Green!
        self.play_sfx("click")
        self.play(
            slot_bars[4].animate.set_fill(COLOR_SORTED),
            run_time=0.6
        )
        self.wait(0.5)

        # ----------------------------------------------------
        # 4. PARTITION LEFT SUBARRAY [4, 2, 1, 3] (slots 0..3)
        # ----------------------------------------------------
        status_card.update_status("Left Subarray: Pivot = 3", COLOR_STATUS_PIVOT)
        self.play_sfx("compare")
        self.play(
            slot_bars[3].animate.set_fill(COLOR_PIVOT),
            run_time=0.6
        )
        self.wait(0.4)

        # Swap slot 1 (val 2) and slot 0 (val 4)
        status_card.update_status("Partition: 2 < 3 -> Swap with 4", COLOR_STATUS_SWAP)
        swap_slots(0, 1)
        self.wait(0.3)

        # Swap slot 2 (val 1) and slot 1 (val 4)
        status_card.update_status("Partition: 1 < 3 -> Swap with 4", COLOR_STATUS_SWAP)
        swap_slots(1, 2)
        self.wait(0.3)

        # Place Pivot 3 in final position: swap slot 3 (pivot 3) with slot 2 (val 4)
        status_card.update_status("Place Pivot 3 in Position [2]", COLOR_STATUS_PIVOT)
        swap_slots(2, 3)
        
        # Lock Pivot 3 & Single Element 4 in Mint Green!
        self.play_sfx("click")
        self.play(
            slot_bars[2].animate.set_fill(COLOR_SORTED),
            slot_bars[3].animate.set_fill(COLOR_SORTED),
            run_time=0.6
        )
        self.wait(0.5)

        # ----------------------------------------------------
        # 5. PARTITION SUBARRAY [2, 1] (slots 0..1)
        # ----------------------------------------------------
        status_card.update_status("Subarray [2, 1]: Pivot = 1", COLOR_STATUS_PIVOT)
        self.play_sfx("compare")
        self.play(
            slot_bars[1].animate.set_fill(COLOR_PIVOT),
            run_time=0.5
        )
        self.wait(0.3)

        # Place Pivot 1: swap slot 1 (pivot 1) with slot 0 (val 2)
        status_card.update_status("Swap 1 & 2 -> Lock Positions", COLOR_STATUS_SWAP)
        swap_slots(0, 1)
        
        self.play_sfx("click")
        self.play(
            slot_bars[0].animate.set_fill(COLOR_SORTED),
            slot_bars[1].animate.set_fill(COLOR_SORTED),
            run_time=0.6
        )
        self.wait(0.5)

        # ----------------------------------------------------
        # 6. PARTITION RIGHT SUBARRAY [7, 6] (slots 5..6)
        # ----------------------------------------------------
        status_card.update_status("Right Subarray [7, 6]: Swap", COLOR_STATUS_PIVOT)
        self.play_sfx("compare")
        self.play(
            slot_bars[6].animate.set_fill(COLOR_PIVOT),
            run_time=0.5
        )
        self.wait(0.3)

        swap_slots(5, 6)
        
        self.play_sfx("click")
        self.play(
            slot_bars[5].animate.set_fill(COLOR_SORTED),
            slot_bars[6].animate.set_fill(COLOR_SORTED),
            run_time=0.6
        )
        self.wait(0.5)

        # ----------------------------------------------------
        # 7. FINAL CELEBRATION
        # ----------------------------------------------------
        self.play_sfx("success")
        status_card.update_status("SORTED! Quick Sort Complete", COLOR_STATUS_SORTED)
        
        self.play(
            *[b.animate.set_stroke(color=COLOR_SORTED, width=3.0) for b in bars],
            run_time=0.8
        )

        self.wait(3.0)
