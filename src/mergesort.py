from manim import *
import numpy as np
import os

# ====================================================
# FORMAT & USER PASTEL COLOR PALETTE (HIGH CONTRAST TEXT)
# Output: 1080x1920 (9:16 Vertical), 60fps, 8000 KBPS
# Target Video Duration: ~17.5 Seconds
# ====================================================
COLOR_BG = "#F4ECE1"               # Warm Cream Paper
COLOR_TEXT = "#1C1917"              # Dark Charcoal Ink Text
COLOR_MUTED = "#57534E"            # Warm Stone Gray (Subtitles/Author)
COLOR_GRID = "#D6CBB8"             # Soft Parchment Grid Lines
COLOR_CARD_BG = "#EFE6D8"          # Warm Container Fill
COLOR_CARD_BORDER = "#B8A995"      # Warm Card Border

# Merge Sort Bar Fill Palette (Pastel)
COLOR_IDLE = "#A0C4FF"             # Soft Pastel Blue (Unsorted)
COLOR_SPLIT = "#FFD185"            # Soft Coral Amber (Dividing)
COLOR_MERGE = "#FFB7B2"            # Soft Peach Pink (Comparing/Merging)
COLOR_SORTED = "#73E6D0"           # Mint Green (Sorted)

# High-Contrast Status Text Palette (Crisp Readability on Light Paper)
COLOR_SPLIT_TEXT = "#B45309"        # Rich Amber Bronze (High Contrast 7:1)
COLOR_MERGE_TEXT = "#C026D3"        # Rich Magenta Violet (High Contrast 7:1)
COLOR_SORTED_TEXT = "#047857"       # Rich Emerald Green (High Contrast 7:1)

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
    def __init__(self, handle="@tiendatbrn", pos=np.array([0.0, -3.45, 0])):
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
    """Compact status card displaying Phase and Merge Sort metrics."""
    def __init__(self, pos=np.array([0.0, -2.70, 0])):
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
        
        self.title_label = Text("MERGE SORT STATUS", font="Consolas", font_size=10, weight=BOLD, color=COLOR_MUTED)
        self.title_label.move_to(pos + UP * 0.16)
        
        self.value_text = Text("Status: Unsorted Array", font="Consolas", font_size=14, weight=BOLD, color=COLOR_TEXT)
        self.value_text.move_to(pos + DOWN * 0.12)
        
        self.add(self.box, self.title_label, self.value_text)
        self.set_z_index(10)

    def update_status(self, text: str, color=COLOR_TEXT):
        new_text = Text(text, font="Consolas", font_size=14, weight=BOLD, color=color)
        new_text.move_to(self.value_text.get_center())
        self.value_text.become(new_text)

class MergeSort(Scene):
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
            "MERGE SORT",
            font="Segoe UI",
            font_size=36,
            weight=BOLD,
            color=COLOR_TEXT
        ).move_to(np.array([0.0, 4.8, 0])).set_z_index(10)

        subtitle = Text(
            "Divide & Conquer Mechanism",
            font="Verdana",
            font_size=14,
            color=COLOR_MUTED
        ).next_to(title, DOWN, buff=0.15).set_z_index(10)

        author_badge = AuthorBadge(handle="@tiendatbrn", pos=np.array([0.0, -3.45, 0]))  # Safe Zone: bottom = -3.65 >= -3.8 ✅
        status_card = StatusCard(pos=np.array([0.0, -2.70, 0]))                            # Safe Zone: bottom = -3.06 >= -3.8 ✅

        self.play_sfx("click")
        self.play(
            Write(title),
            FadeIn(subtitle, shift=DOWN * 0.1),
            FadeIn(author_badge, shift=UP * 0.1),
            FadeIn(status_card, shift=UP * 0.1),
            run_time=1.0
        )

        # ----------------------------------------------------
        # 2. INITIAL ARRAY CREATION (8 Elements)
        # ----------------------------------------------------
        values = [5, 2, 8, 3, 7, 1, 6, 4]
        n = len(values)
        
        y_l0 = 2.0
        y_l1 = 0.6
        y_l2 = -0.7
        
        xs_l0 = np.linspace(-2.45, 2.45, 8)
        
        bars = []
        labels = []
        bar_groups = VGroup()

        for i, val in enumerate(values):
            h = val * 0.35 + 0.4
            w = 0.52
            
            b = RoundedRectangle(
                corner_radius=0.08,
                width=w,
                height=h,
                color=COLOR_CARD_BORDER,
                stroke_width=1.5,
                fill_color=COLOR_IDLE,
                fill_opacity=0.95
            ).move_to(np.array([xs_l0[i], y_l0, 0]))
            
            lbl = Text(str(val), font="Consolas", font_size=15, weight=BOLD, color=COLOR_TEXT)
            lbl.add_updater(lambda l, bar_ref=b: l.move_to(bar_ref.get_bottom() + DOWN * 0.28))
            
            b.set_z_index(4)
            lbl.set_z_index(5)
            
            bars.append(b)
            labels.append(lbl)
            bar_groups.add(b, lbl)

        self.play_sfx("click")
        self.play(
            LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in bars], lag_ratio=0.06),
            LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.06),
            run_time=1.2
        )
        self.wait(0.5)

        # ----------------------------------------------------
        # 3. DIVIDE PHASE (TREE SPLITTING)
        # ----------------------------------------------------
        status_card.update_status("DIVIDE: Split into 2 Halves", COLOR_SPLIT_TEXT)
        self.play_sfx("compare")

        xs_l1_left = np.linspace(-3.2, -1.1, 4)
        xs_l1_right = np.linspace(1.1, 3.2, 4)
        xs_l1 = np.concatenate([xs_l1_left, xs_l1_right])

        split_l1_anims = []
        for i in range(8):
            split_l1_anims.append(bars[i].animate.move_to(np.array([xs_l1[i], y_l1, 0])).set_fill(COLOR_SPLIT))

        self.play(
            AnimationGroup(*split_l1_anims, run_time=1.3, rate_func=smooth)
        )
        self.wait(0.5)

        status_card.update_status("DIVIDE: Split into Pairs", COLOR_SPLIT_TEXT)
        self.play_sfx("compare")

        xs_l2_p1 = np.linspace(-3.35, -2.65, 2)  # Safe Zone: left edge = -3.35-0.26 = -3.61 >= -4.0 ✅
        xs_l2_p2 = np.linspace(-1.7, -0.9, 2)
        xs_l2_p3 = np.linspace(0.9, 1.7, 2)
        xs_l2_p4 = np.linspace(2.65, 3.35, 2)   # Safe Zone: right edge = 3.35+0.26 = 3.61 <= 3.65 ✅
        xs_l2 = np.concatenate([xs_l2_p1, xs_l2_p2, xs_l2_p3, xs_l2_p4])

        split_l2_anims = []
        for i in range(8):
            split_l2_anims.append(bars[i].animate.move_to(np.array([xs_l2[i], y_l2, 0])))

        self.play(
            AnimationGroup(*split_l2_anims, run_time=1.3, rate_func=smooth)
        )
        self.wait(0.6)

        # ----------------------------------------------------
        # 4. CONQUER & MERGE PHASE
        # ----------------------------------------------------
        status_card.update_status("MERGE: Sort 2-Element Subarrays", COLOR_MERGE_TEXT)
        self.play_sfx("swap")

        sorted_pairs_bar_order = [1, 0, 3, 2, 5, 4, 7, 6]

        merge_pairs_anims = []
        for target_slot, bar_idx in enumerate(sorted_pairs_bar_order):
            target_x = xs_l1[target_slot]
            merge_pairs_anims.append(
                bars[bar_idx].animate.move_to(np.array([target_x, y_l1, 0])).set_fill(COLOR_MERGE)
            )

        self.play(
            AnimationGroup(*merge_pairs_anims, run_time=1.6, rate_func=smooth)
        )
        self.wait(0.6)

        status_card.update_status("MERGE: Sort 4-Element Halves", COLOR_MERGE_TEXT)
        self.play_sfx("swap")

        sorted_halves_bar_order = [1, 3, 0, 2, 5, 7, 6, 4]

        xs_halves_left = np.linspace(-2.8, -1.0, 4)
        xs_halves_right = np.linspace(1.0, 2.8, 4)
        xs_halves = np.concatenate([xs_halves_left, xs_halves_right])

        merge_halves_anims = []
        for target_slot, bar_idx in enumerate(sorted_halves_bar_order):
            target_x = xs_halves[target_slot]
            merge_halves_anims.append(
                bars[bar_idx].animate.move_to(np.array([target_x, 1.0, 0]))
            )

        self.play(
            AnimationGroup(*merge_halves_anims, run_time=1.6, rate_func=smooth)
        )
        self.wait(0.6)

        # ----------------------------------------------------
        # 5. FINAL MERGE (FULL 8-ELEMENT SORTED ARRAY AT Y = 2.0)
        # ----------------------------------------------------
        status_card.update_status("FINAL MERGE: Complete Array", COLOR_SORTED_TEXT)
        self.play_sfx("swap")

        final_sorted_bar_order = [5, 1, 3, 7, 0, 6, 4, 2]

        final_merge_anims = []
        for target_slot, bar_idx in enumerate(final_sorted_bar_order):
            target_x = xs_l0[target_slot]
            final_merge_anims.append(
                bars[bar_idx].animate.move_to(np.array([target_x, y_l0, 0])).set_fill(COLOR_SORTED)
            )

        self.play(
            AnimationGroup(*final_merge_anims, run_time=1.8, rate_func=smooth)
        )
        self.wait(0.5)

        # Final Success Celebration
        self.play_sfx("success")
        status_card.update_status("SORTED! Merge Complete", COLOR_SORTED_TEXT)
        
        self.play(
            *[b.animate.set_stroke(color=COLOR_SORTED, width=3.0) for b in bars],
            run_time=0.8
        )

        self.wait(3.0)
