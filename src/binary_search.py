from manim import *
import numpy as np
import os

# ====================================================
# CONFIGURATION & COLOR PALETTE
# Output: 1080x1920 (9:16 Vertical), 60fps, 8000 KBPS
# ====================================================
COLOR_BG          = "#F4ECE1"   # Warm Cream Paper
COLOR_INK         = "#1C1917"   # Dark Charcoal Ink
COLOR_MUTED       = "#57534E"   # Warm Stone Gray
COLOR_GRID        = "#D6CBB8"   # Soft Parchment Grid
COLOR_CARD_BG     = "#EFE6D8"   # Warm Container Fill
COLOR_CARD_BORDER = "#B8A995"   # Warm Card Border

# Soft Pastel Card Colors
COLOR_ACTIVE      = "#A0C4FF"   # Soft Pastel Blue (Search space)
COLOR_MID         = "#FFD185"   # Soft Pastel Peach (Mid index candidate)
COLOR_SUCCESS     = "#73E6D0"   # Soft Pastel Mint / Green (Found target)
COLOR_MUTED_CARD  = "#D6CBB8"   # Eliminated card color

config.pixel_width      = 1080
config.pixel_height     = 1920
config.frame_width      = 9.0
config.frame_height     = 16.0
config.frame_rate       = 60
config.bitrate          = "8000k"
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

class TargetCard(VGroup):
    """Small upper box indicating target value to be found."""
    def __init__(self, target_val: int, pos=np.array([0.0, 2.4, 0])):
        super().__init__()
        text_group = VGroup(
            Text("TARGET: ", font="Consolas", font_size=11, weight=BOLD, color=COLOR_MUTED),
            Text(str(target_val), font="Segoe UI", font_size=18, weight=BOLD, color=COLOR_INK)
        ).arrange(RIGHT, buff=0.1)
        
        self.box = RoundedRectangle(
            corner_radius=0.12,
            width=text_group.width + 0.5,
            height=0.55,
            color=COLOR_CARD_BORDER,
            stroke_width=1.5,
            fill_color=COLOR_CARD_BG,
            fill_opacity=0.95
        ).move_to(pos)
        text_group.move_to(self.box.get_center())
        self.add(self.box, text_group)
        self.set_z_index(5)

class StatusCard(VGroup):
    """Compact status card displaying Phase and search details."""
    def __init__(self, pos=np.array([0.0, -3.10, 0])):
        super().__init__()
        self.box = RoundedRectangle(
            corner_radius=0.14,
            width=6.0,
            height=0.72,
            color=COLOR_CARD_BORDER,
            stroke_width=1.5,
            fill_color=COLOR_CARD_BG,
            fill_opacity=0.95
        ).move_to(pos)
        
        self.title_label = Text("BINARY SEARCH STATUS", font="Consolas", font_size=10, weight=BOLD, color=COLOR_MUTED)
        self.title_label.move_to(pos + UP * 0.16)
        
        self.value_text = Text("Initialize Search Space", font="Consolas", font_size=13, weight=BOLD, color=COLOR_INK)
        self.value_text.move_to(pos + DOWN * 0.12)
        
        self.add(self.box, self.title_label, self.value_text)
        self.set_z_index(10)

    def update_status(self, text: str, color=COLOR_INK):
        new_text = Text(text, font="Consolas", font_size=13, weight=BOLD, color=color)
        new_text.move_to(self.value_text.get_center())
        self.value_text.become(new_text)

class Pointer(VGroup):
    """Arrow pointer pointing to an index with a text label."""
    def __init__(self, label: str, color: str, length: float, **kwargs):
        super().__init__(**kwargs)
        self.arrow = Arrow(
            start=DOWN * length,
            end=ORIGIN,
            buff=0.0,
            color=color,
            stroke_width=3.5,
            max_tip_length_to_length_ratio=0.35
        )
        self.text = Text(label, font="Consolas", font_size=15, color=color, weight=BOLD)
        self.text.next_to(self.arrow, DOWN, buff=0.08)
        self.add(self.arrow, self.text)
        self.set_z_index(8)

# ====================================================
# MAIN SCENE
# ====================================================

class BinarySearch(Scene):
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

        title = Text(
            "BINARY SEARCH",
            font="Segoe UI",
            font_size=34,
            weight=BOLD,
            color=COLOR_INK
        ).move_to(np.array([0.0, 4.8, 0]))

        subtitle = Text(
            "O(log n) Divide & Conquer",
            font="Verdana",
            font_size=14,
            color=COLOR_MUTED
        ).next_to(title, DOWN, buff=0.15)
        
        title.set_z_index(10)
        subtitle.set_z_index(10)

        author_badge = AuthorBadge(handle="@tiendatbrn", pos=np.array([0.0, -4.15, 0]))
        target_card = TargetCard(target_val=23, pos=np.array([0.0, 2.4, 0]))
        status_card = StatusCard(pos=np.array([0.0, -3.10, 0]))

        # Data & Array sizing
        values = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
        target = 23
        card_w = 0.65
        card_h = 0.70
        spacing = 0.82
        
        start_x = -((len(values) - 1) * spacing) / 2
        baseline_y = 0.0

        cards = []
        labels = []

        for i, val in enumerate(values):
            card = RoundedRectangle(
                corner_radius=0.08,
                width=card_w,
                height=card_h,
                fill_color=COLOR_ACTIVE,
                fill_opacity=0.95,
                stroke_color=COLOR_INK,
                stroke_width=1.2,
            )
            card.set_z_index(2)
            card.move_to(RIGHT * (start_x + spacing * i) + UP * baseline_y)

            label = Text(str(val), font="Segoe UI", font_size=20, color=COLOR_INK, weight=BOLD)
            label.set_z_index(3)
            label.move_to(card.get_center())

            cards.append(card)
            labels.append(label)

        # ----------------------------------------------------
        # Helper Pointer calculation functions
        # ----------------------------------------------------
        def get_pointer_tip_pos(col_idx: int, p_type: str):
            card_x = start_x + spacing * col_idx
            card_bottom_y = baseline_y - card_h / 2
            if p_type == "L":
                return np.array([card_x - 0.16, card_bottom_y, 0])
            elif p_type == "H":
                return np.array([card_x + 0.16, card_bottom_y, 0])
            else: # Mid
                return np.array([card_x, card_bottom_y, 0])

        def move_pointer_to(pointer: Pointer, col_idx: int, p_type: str):
            tip_pos = get_pointer_tip_pos(col_idx, p_type)
            target_center = tip_pos + DOWN * (pointer.get_height() / 2)
            return pointer.animate.move_to(target_center)

        # ----------------------------------------------------
        # 2. ANIMATION TIMELINE — "Combine, Not Sequence"
        # ----------------------------------------------------

        # INTRO: Everything fades in at once
        self.play_sfx("click")
        self.play(
            Write(title),
            FadeIn(subtitle, shift=DOWN * 0.1),
            FadeIn(author_badge, shift=UP * 0.1),
            FadeIn(target_card, shift=DOWN * 0.1),
            FadeIn(status_card, shift=UP * 0.1),
            *[FadeIn(c, shift=UP * 0.2) for c in cards],
            *[FadeIn(l, shift=UP * 0.2) for l in labels],
            run_time=0.9
        )
        self.wait(0.3)

        # Initialize Pointer objects
        # Low pointer: shorter, Red
        low_ptr = Pointer("Low", "#E05A47", length=0.65)
        # High pointer: shorter, Blue
        high_ptr = Pointer("High", "#478BE0", length=0.65)
        # Mid pointer: longer to avoid collision, Orange
        mid_ptr = Pointer("Mid", "#FF9F1C", length=1.20)

        # Align pointers to initial state centers before fade-in
        low_ptr.move_to(get_pointer_tip_pos(0, "L") + DOWN * (low_ptr.get_height() / 2))
        high_ptr.move_to(get_pointer_tip_pos(9, "H") + DOWN * (high_ptr.get_height() / 2))
        
        # Calculate initial mid pointer
        low_idx = 0
        high_idx = 9
        mid_idx = (low_idx + high_idx) // 2 # 4
        mid_ptr.move_to(get_pointer_tip_pos(mid_idx, "M") + DOWN * (mid_ptr.get_height() / 2))

        # Show initial pointers
        status_card.update_status("Set Low=0, High=9", COLOR_ACTIVE)
        self.play_sfx("click")
        self.play(
            FadeIn(low_ptr, shift=UP * 0.1),
            FadeIn(high_ptr, shift=UP * 0.1),
            run_time=0.4
        )

        # ====================================================
        # ITERATION 1
        # ====================================================
        status_card.update_status(f"Mid = (0 + 9)//2 = {mid_idx} (Val: {values[mid_idx]})", "#FF9F1C")
        self.play_sfx("compare")
        self.play(
            FadeIn(mid_ptr, shift=UP * 0.1),
            cards[mid_idx].animate.set_fill(COLOR_MID),
            run_time=0.5
        )
        self.wait(0.4)

        # Compare target (23) > mid (16) -> Eliminate left (indices 0 to 4)
        status_card.update_status(f"Target (23) > Mid ({values[mid_idx]}) → Eliminate Left", "#E05A47")
        self.play_sfx("swap")
        
        # We fade left cards, shift Low pointer to mid_idx + 1 (5), and reset mid card fill to muted in one transition
        self.play(
            # Move Low pointer
            move_pointer_to(low_ptr, mid_idx + 1, "L"),
            # Fade mid pointer temporarily
            FadeOut(mid_ptr, shift=DOWN * 0.1),
            # Update left cards styling (mute color and opacity)
            *[cards[idx].animate.set_fill(COLOR_MUTED_CARD, opacity=0.3).set_stroke(COLOR_MUTED, opacity=0.3) for idx in range(mid_idx + 1)],
            *[labels[idx].animate.set_color(COLOR_MUTED).set_opacity(0.3) for idx in range(mid_idx + 1)],
            run_time=0.8
        )
        low_idx = mid_idx + 1 # 5

        # ====================================================
        # ITERATION 2
        # ====================================================
        mid_idx = (low_idx + high_idx) // 2 # (5+9)//2 = 7
        mid_ptr.move_to(get_pointer_tip_pos(mid_idx, "M") + DOWN * (mid_ptr.get_height() / 2))
        
        status_card.update_status(f"Mid = (5 + 9)//2 = {mid_idx} (Val: {values[mid_idx]})", "#FF9F1C")
        self.play_sfx("compare")
        self.play(
            FadeIn(mid_ptr, shift=UP * 0.1),
            cards[mid_idx].animate.set_fill(COLOR_MID),
            run_time=0.5
        )
        self.wait(0.4)

        # Compare target (23) < mid (56) -> Eliminate right (indices 7 to 9)
        status_card.update_status(f"Target (23) < Mid ({values[mid_idx]}) → Eliminate Right", "#478BE0")
        self.play_sfx("swap")
        
        # We fade right cards, shift High pointer to mid_idx - 1 (6), and reset mid card fill to muted in one transition
        self.play(
            # Move High pointer
            move_pointer_to(high_ptr, mid_idx - 1, "H"),
            # Fade mid pointer temporarily
            FadeOut(mid_ptr, shift=DOWN * 0.1),
            # Update right cards styling
            *[cards[idx].animate.set_fill(COLOR_MUTED_CARD, opacity=0.3).set_stroke(COLOR_MUTED, opacity=0.3) for idx in range(mid_idx, high_idx + 1)],
            *[labels[idx].animate.set_color(COLOR_MUTED).set_opacity(0.3) for idx in range(mid_idx, high_idx + 1)],
            run_time=0.8
        )
        high_idx = mid_idx - 1 # 6

        # ====================================================
        # ITERATION 3
        # ====================================================
        mid_idx = (low_idx + high_idx) // 2 # (5+6)//2 = 5 (Val: 23)
        mid_ptr.move_to(get_pointer_tip_pos(mid_idx, "M") + DOWN * (mid_ptr.get_height() / 2))
        
        status_card.update_status(f"Mid = (5 + 6)//2 = {mid_idx} (Val: {values[mid_idx]})", "#FF9F1C")
        self.play_sfx("compare")
        self.play(
            FadeIn(mid_ptr, shift=UP * 0.1),
            cards[mid_idx].animate.set_fill(COLOR_MID),
            run_time=0.5
        )
        self.wait(0.4)

        # Match! Success
        status_card.update_status(f"Target (23) == Mid (23) → Match Found!", COLOR_SUCCESS)
        self.play_sfx("success")
        
        # Grow card slightly and turn it Mint/Success color, clean up pointers
        self.play(
            cards[mid_idx].animate.set_fill(COLOR_SUCCESS).scale(1.15),
            labels[mid_idx].animate.scale(1.15),
            FadeOut(low_ptr),
            FadeOut(high_ptr),
            mid_ptr.animate.set_color(COLOR_SUCCESS),
            run_time=0.6
        )
        
        # Celebration hold
        self.play_sfx("success")
        self.wait(3.0)
