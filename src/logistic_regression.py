from manim import *
import numpy as np
import os

# ====================================================
# FORMAT & USER PASTEL COLOR PALETTE (HIGH CONTRAST TEXT)
# Output: 1080x1920 (9:16 Vertical), 60fps, 8000 KBPS
# Target Video Duration: ~21.0 Seconds (2 Query Examples)
# ====================================================
COLOR_BG = "#F4ECE1"               # Warm Cream Paper
COLOR_TEXT = "#1C1917"              # Dark Charcoal Ink Text
COLOR_MUTED = "#57534E"            # Warm Stone Gray (Subtitles/Author)
COLOR_GRID = "#D6CBB8"             # Soft Parchment Grid Lines
COLOR_CARD_BG = "#EFE6D8"          # Warm Container Fill
COLOR_CARD_BORDER = "#B8A995"      # Warm Card Border

# Binary Class & Sigmoid Curve Palette
COLOR_CLASS_0 = "#FC4747"          # Crimson / Coral Red (Class 0: Fail)
COLOR_CLASS_1 = "#386CFA"          # Royal Ink Blue (Class 1: Pass)
COLOR_SIGMOID = "#7C3AED"          # Vibrant Deep Violet (Sigmoid S-Curve)
COLOR_THRESHOLD = "#D97706"        # Gold / Amber (P = 0.5 Threshold)
COLOR_QUERY = "#FF9F1C"            # Gold / Orange (Sample Query)

# High-Contrast Status Text Palette (Crisp Readability on Light Paper)
COLOR_STATUS_INIT = "#B45309"       # Rich Amber Bronze (High Contrast 7:1)
COLOR_STATUS_FIT = "#C026D3"        # Rich Magenta Violet (High Contrast 7:1)
COLOR_STATUS_RED = "#B91C1C"        # Rich Crimson Red (Class 0)
COLOR_STATUS_BLUE = "#1D4ED8"       # Rich Royal Blue (Class 1)

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
    """Compact status card displaying Phase and Logistic Regression metrics."""
    def __init__(self, pos=np.array([0.0, -3.10, 0])):
        super().__init__()
        self.pos = pos
        self.box = RoundedRectangle(
            corner_radius=0.14,
            width=6.2,
            height=0.72,
            color=COLOR_CARD_BORDER,
            stroke_width=1.5,
            fill_color=COLOR_CARD_BG,
            fill_opacity=0.95
        ).move_to(pos)
        
        self.title_label = Text("LOGISTIC REGRESSION STATUS", font="Consolas", font_size=10, weight=BOLD, color=COLOR_MUTED)
        self.title_label.move_to(pos + UP * 0.16)
        
        self.value_text = Text("Status: Binary Dataset (0 & 1)", font="Consolas", font_size=13, weight=BOLD, color=COLOR_TEXT)
        self.value_text.move_to(pos + DOWN * 0.12)
        
        self.add(self.box, self.title_label, self.value_text)
        self.set_z_index(10)

    def update_status(self, text: str, color=COLOR_TEXT):
        new_text = Text(text, font="Consolas", font_size=13, weight=BOLD, color=color)
        new_text.move_to(self.value_text.get_center())
        self.value_text.become(new_text)

class LogisticRegression(Scene):
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
            "LOGISTIC REGRESSION",
            font="Segoe UI",
            font_size=34,
            weight=BOLD,
            color=COLOR_TEXT
        ).move_to(np.array([0.0, 4.8, 0])).set_z_index(10)

        subtitle = Text(
            "Binary Classification & Sigmoid Function",
            font="Verdana",
            font_size=13,
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
            run_time=0.9
        )

        # ----------------------------------------------------
        # 2. AXES & BINARY DATA POINTS SETUP
        # ----------------------------------------------------
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1.0, 0.2],
            x_length=5.2,
            y_length=5.2,
            axis_config={
                "color": COLOR_MUTED,
                "stroke_width": 1.5,
                "include_numbers": False,
            },
            tips=False
        ).move_to(np.array([0.15, 0.85, 0]))
        axes.set_z_index(1)

        axis_numbers = VGroup()
        for x_val in range(0, 11, 2):
            lbl = Text(str(x_val), font="Consolas", font_size=11, color=COLOR_MUTED)
            lbl.next_to(axes.c2p(x_val, 0), DOWN, buff=0.10)
            axis_numbers.add(lbl)
            
        for y_val in [0.0, 0.5, 1.0]:
            lbl = Text(f"{y_val:.1f}", font="Consolas", font_size=11, color=COLOR_MUTED)
            lbl.next_to(axes.c2p(0, y_val), LEFT, buff=0.10)
            axis_numbers.add(lbl)
        axis_numbers.set_z_index(1)

        x_label = Text("Feature X", font="Verdana", font_size=13, color=COLOR_MUTED, weight=BOLD).next_to(axis_numbers, DOWN, buff=0.18)
        y_label = Text("Probability P(Y=1)", font="Verdana", font_size=13, color=COLOR_MUTED, weight=BOLD).next_to(axes.y_axis, LEFT, buff=0.75).rotate(90 * DEGREES)
        x_label.set_z_index(1)
        y_label.set_z_index(1)

        self.play(
            Create(axes),
            FadeIn(axis_numbers),
            Write(x_label),
            Write(y_label),
            run_time=1.0
        )

        # Class 0 Points at Y=0.0 (6 Red points)
        c0_coords = [[1.0, 0.0], [1.8, 0.0], [2.5, 0.0], [3.2, 0.0], [3.8, 0.0], [4.4, 0.0]]
        # Class 1 Points at Y=1.0 (6 Blue points)
        c1_coords = [[5.2, 1.0], [5.8, 1.0], [6.5, 1.0], [7.2, 1.0], [8.0, 1.0], [8.8, 1.0]]

        mobs_c0 = VGroup()
        for x_v, y_v in c0_coords:
            pt = axes.c2p(x_v, y_v)
            glow = Dot(point=pt, radius=0.16, color=COLOR_CLASS_0, fill_opacity=0.25)
            dot = Dot(point=pt, radius=0.09, color=COLOR_CLASS_0)
            g = VGroup(glow, dot).set_z_index(3)
            mobs_c0.add(g)

        mobs_c1 = VGroup()
        for x_v, y_v in c1_coords:
            pt = axes.c2p(x_v, y_v)
            glow = Dot(point=pt, radius=0.16, color=COLOR_CLASS_1, fill_opacity=0.25)
            dot = Dot(point=pt, radius=0.09, color=COLOR_CLASS_1)
            g = VGroup(glow, dot).set_z_index(3)
            mobs_c1.add(g)

        self.play_sfx("click")
        self.play(
            LaggedStart(*[FadeIn(p, scale=0.5) for p in mobs_c0], lag_ratio=0.04),
            LaggedStart(*[FadeIn(p, scale=0.5) for p in mobs_c1], lag_ratio=0.04),
            run_time=1.1
        )
        self.wait(0.4)

        # ----------------------------------------------------
        # 3. SIGMOID CURVE TRANSFORMATION & THRESHOLD RULE
        # ----------------------------------------------------
        # Linear fit attempt line first
        linear_line = axes.plot(
            lambda x: 0.14 * x - 0.18,
            x_range=[0, 10],
            color=COLOR_MUTED,
            stroke_width=2.0
        ).set_z_index(2)

        status_card.update_status("Linear Fit (Exceeds [0,1])", COLOR_STATUS_INIT)
        self.play_sfx("compare")
        self.play(Create(linear_line), run_time=0.9)
        self.wait(0.4)

        # Sigmoid Function: P(x) = 1 / (1 + exp(-1.8*(x - 4.8)))
        sigmoid_curve = axes.plot(
            lambda x: 1.0 / (1.0 + np.exp(-1.8 * (x - 4.8))),
            x_range=[0, 10],
            color=COLOR_SIGMOID,
            stroke_width=3.5
        ).set_z_index(4)

        status_card.update_status("Sigmoid Curve: σ(w·x + b)", COLOR_STATUS_FIT)
        self.play_sfx("swap")
        self.play(
            Transform(linear_line, sigmoid_curve),
            run_time=1.4,
            rate_func=smooth
        )
        self.wait(0.4)

        # Decision Threshold (P = 0.5) and Decision Boundary (X = 4.8)
        p05_line = DashedLine(
            axes.c2p(0, 0.5),
            axes.c2p(10, 0.5),
            color=COLOR_THRESHOLD,
            stroke_width=2.0,
            dash_length=0.08
        ).set_z_index(2)

        boundary_x_line = DashedLine(
            axes.c2p(4.8, 0),
            axes.c2p(4.8, 1.0),
            color=COLOR_THRESHOLD,
            stroke_width=2.0,
            dash_length=0.08
        ).set_z_index(2)

        status_card.update_status("Threshold P = 0.5 | Boundary X=4.8", COLOR_STATUS_INIT)
        self.play_sfx("compare")
        self.play(
            Create(p05_line),
            Create(boundary_x_line),
            run_time=1.0
        )
        self.wait(0.5)

        # ====================================================
        # EXAMPLE 1: Low Probability Sample X1 = 2.8 -> Class 0 (Red)
        # ====================================================
        x1 = 2.8
        p1 = 1.0 / (1.0 + np.exp(-1.8 * (x1 - 4.8)))  # ~0.03
        
        q1_pos_bottom = axes.c2p(x1, 0.0)
        q1_pos_curve = axes.c2p(x1, p1)
        q1_pos_yaxis = axes.c2p(0.0, p1)

        q1_dot = Dot(point=q1_pos_bottom, radius=0.11, color=COLOR_QUERY).set_z_index(7)
        q1_ring = Circle(radius=0.18, color=COLOR_QUERY, stroke_width=2.5).move_to(q1_pos_bottom).set_z_index(7)
        q1_qmark = Text("?", font="Consolas", font_size=11, weight=BOLD, color=COLOR_TEXT).move_to(q1_pos_bottom).set_z_index(8)
        q1_group = VGroup(q1_ring, q1_dot, q1_qmark)

        status_card.update_status("Ex 1: Predict Sample X = 2.8 ?", COLOR_STATUS_FIT)
        self.play_sfx("compare")
        self.play(SpinInFromNothing(q1_group), run_time=0.7)

        trace1_v = DashedLine(q1_pos_bottom, q1_pos_curve, color=COLOR_QUERY, stroke_width=2.0, dash_length=0.06).set_z_index(5)
        trace1_h = DashedLine(q1_pos_curve, q1_pos_yaxis, color=COLOR_QUERY, stroke_width=2.0, dash_length=0.06).set_z_index(5)

        self.play(
            Create(trace1_v),
            q1_group.animate.move_to(q1_pos_curve),
            run_time=0.9
        )
        self.play(Create(trace1_h), run_time=0.6)
        self.wait(0.3)

        final_red_1 = VGroup(
            Dot(point=q1_pos_curve, radius=0.18, color=COLOR_CLASS_0, fill_opacity=0.35),
            Dot(point=q1_pos_curve, radius=0.10, color=COLOR_CLASS_0)
        ).set_z_index(8)

        self.play_sfx("success")
        status_card.update_status("P = 0.03 < 0.5 -> CLASS 0 (Red)", COLOR_STATUS_RED)
        self.play(
            Transform(q1_group, final_red_1),
            run_time=0.8
        )
        self.wait(0.6)

        # Fade out trace lines for Example 1 before showing Example 2
        self.play(
            FadeOut(trace1_v),
            FadeOut(trace1_h),
            run_time=0.4
        )

        # ====================================================
        # EXAMPLE 2: High Probability Sample X2 = 6.5 -> Class 1 (Blue)
        # ====================================================
        x2 = 6.5
        p2 = 1.0 / (1.0 + np.exp(-1.8 * (x2 - 4.8)))  # ~0.95
        
        q2_pos_bottom = axes.c2p(x2, 0.0)
        q2_pos_curve = axes.c2p(x2, p2)
        q2_pos_yaxis = axes.c2p(0.0, p2)

        q2_dot = Dot(point=q2_pos_bottom, radius=0.11, color=COLOR_QUERY).set_z_index(7)
        q2_ring = Circle(radius=0.18, color=COLOR_QUERY, stroke_width=2.5).move_to(q2_pos_bottom).set_z_index(7)
        q2_qmark = Text("?", font="Consolas", font_size=11, weight=BOLD, color=COLOR_TEXT).move_to(q2_pos_bottom).set_z_index(8)
        q2_group = VGroup(q2_ring, q2_dot, q2_qmark)

        status_card.update_status("Ex 2: Predict Sample X = 6.5 ?", COLOR_STATUS_FIT)
        self.play_sfx("compare")
        self.play(SpinInFromNothing(q2_group), run_time=0.7)

        trace2_v = DashedLine(q2_pos_bottom, q2_pos_curve, color=COLOR_QUERY, stroke_width=2.0, dash_length=0.06).set_z_index(5)
        trace2_h = DashedLine(q2_pos_curve, q2_pos_yaxis, color=COLOR_QUERY, stroke_width=2.0, dash_length=0.06).set_z_index(5)

        self.play(
            Create(trace2_v),
            q2_group.animate.move_to(q2_pos_curve),
            run_time=0.9
        )
        self.play(Create(trace2_h), run_time=0.6)
        self.wait(0.3)

        final_blue_2 = VGroup(
            Dot(point=q2_pos_curve, radius=0.18, color=COLOR_CLASS_1, fill_opacity=0.35),
            Dot(point=q2_pos_curve, radius=0.10, color=COLOR_CLASS_1)
        ).set_z_index(8)

        self.play_sfx("success")
        status_card.update_status("P = 0.95 ≥ 0.5 -> CLASS 1 (Blue)", COLOR_STATUS_BLUE)
        self.play(
            Transform(q2_group, final_blue_2),
            run_time=0.8
        )

        self.wait(3.0)
