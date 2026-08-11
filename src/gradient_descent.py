from manim import *
import numpy as np
import os

# ====================================================
# FORMAT & USER PASTEL COLOR PALETTE (PRESERVED EXACTLY)
# Output: 1080x1920 (9:16 Vertical), 60fps, 8000 KBPS
# Target Video Duration: ~18.5 Seconds
# ====================================================
COLOR_BG = "#F4ECE1"               # Warm Cream Paper
COLOR_INK = "#1C1917"              # Dark Charcoal Ink Text
COLOR_MUTED = "#57534E"            # Warm Stone Gray (Subtitles/Author)
COLOR_GRID = "#D6CBB8"             # Soft Parchment Grid Lines
COLOR_CARD_BG = "#EFE6D8"          # Warm Container Fill
COLOR_CARD_BORDER = "#B8A995"      # Warm Card Border

COLOR_CURVE = "#386CFA"            # Royal Ink Blue Curve
COLOR_BALL = "#FC4747"             # Crimson Red Optimization Ball
COLOR_TANGENT = "#FF9F1C"          # Gold/Orange Gradient Tangent
COLOR_SUCCESS = "#36E470"          # Emerald Green Minimum

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
    """Subtle technical background grid styled for warm paper aesthetic."""
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

class MetricsCard(VGroup):
    """Card displaying live parameter values (w, gradient, loss) during optimization."""
    def __init__(self, pos=np.array([0.0, -2.85, 0])):
        super().__init__()
        self.pos = pos
        self.box = RoundedRectangle(
            corner_radius=0.14,
            width=6.8,
            height=1.15,
            color=COLOR_CARD_BORDER,
            stroke_width=1.5,
            fill_color=COLOR_CARD_BG,
            fill_opacity=0.95
        ).move_to(pos)

        self.title_text = Text(
            "LIVE PARAMETER METRICS",
            font="Consolas",
            font_size=11,
            weight=BOLD,
            color=COLOR_MUTED
        ).move_to(pos + UP * 0.34)

        self.add(self.box, self.title_text)
        self.set_z_index(10)

class GradientDescent(Scene):
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
            "GRADIENT DESCENT",
            font="Segoe UI",
            font_size=34,
            weight=BOLD,
            color=COLOR_INK
        ).move_to(np.array([0.0, 4.8, 0]))

        subtitle = Text(
            "Optimization Mechanism",
            font="Verdana",
            font_size=14,
            color=COLOR_MUTED
        ).next_to(title, DOWN, buff=0.15)
        
        title.set_z_index(10)
        subtitle.set_z_index(10)

        author_badge = AuthorBadge(handle="@tiendatbrn", pos=np.array([0.0, -4.15, 0]))

        # Central Loss Axes Setup
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 7, 2],
            x_length=5.6,
            y_length=4.5,
            axis_config={
                "color": COLOR_MUTED,
                "stroke_width": 1.5,
                "include_numbers": False,
            }
        ).move_to(np.array([0.0, 0.65, 0]))
        axes.set_z_index(1)

        x_label = Text("w (Weight)", font="Verdana", font_size=14, color=COLOR_INK, weight=BOLD).next_to(axes.x_axis, DOWN, buff=0.25)
        y_label = Text("J(w) (Loss)", font="Verdana", font_size=14, color=COLOR_INK, weight=BOLD).next_to(axes.y_axis, UP, buff=0.35).shift(LEFT * 0.35)
        x_label.set_z_index(1)
        y_label.set_z_index(1)

        # Loss function curve: J(w) = w^2 + 0.5
        func = lambda w: w**2 + 0.5
        curve = axes.plot(func, x_range=[-2.4, 2.4], color=COLOR_CURVE, stroke_width=3.5)
        curve.set_z_index(1)

        # Minimum indicator dot & label
        min_dot = Dot(axes.c2p(0, 0.5), radius=0.08, color=COLOR_SUCCESS)
        min_label = Text("Minimum (w=0)", font="Consolas", font_size=12, color=COLOR_SUCCESS, weight=BOLD).next_to(min_dot, UP + RIGHT, buff=0.18)
        min_dot.set_z_index(6)
        min_label.set_z_index(6)

        # Metrics Card Component
        metrics_card = MetricsCard(pos=np.array([0.0, -2.85, 0]))

        # Optimization sequence values (5 steps for ~18s total video length)
        w_start = 2.6
        learning_rate = 0.28
        w_vals = [w_start]
        curr_w = w_start
        for _ in range(5):
            grad = 2.0 * curr_w
            curr_w = curr_w - learning_rate * grad
            w_vals.append(curr_w)

        # Continuous ValueTracker for parameter w
        w_tracker = ValueTracker(w_vals[0])
        is_converged = [False]

        # Dynamic MObjects driven safely by always_redraw
        ball = always_redraw(lambda: Dot(
            axes.c2p(w_tracker.get_value(), func(w_tracker.get_value())),
            radius=0.16,
            color=COLOR_SUCCESS if is_converged[0] else COLOR_BALL
        ).set_z_index(5))

        def get_tangent_line():
            w = w_tracker.get_value()
            slope = 2.0 * w
            dx = 0.55
            dy = slope * dx
            p1 = axes.c2p(w - dx, func(w) - dy)
            p2 = axes.c2p(w + dx, func(w) + dy)
            line = Line(p1, p2, color=COLOR_TANGENT, stroke_width=3.0)
            line.set_z_index(2)
            return line

        tangent_line = always_redraw(get_tangent_line)

        def get_metrics_group():
            w = w_tracker.get_value()
            grad = 2.0 * w
            loss = func(w)
            sign = "+" if grad >= 0 else ""
            w_t = Text(f"w = {w:.3f}", font="Consolas", font_size=14, weight=BOLD, color=COLOR_INK)
            g_t = Text(f"dJ/dw = {sign}{grad:.3f}", font="Consolas", font_size=14, weight=BOLD, 
                       color=COLOR_TANGENT if abs(grad) > 0.15 else COLOR_SUCCESS)
            l_t = Text(f"Loss = {loss:.3f}", font="Consolas", font_size=14, weight=BOLD, 
                       color=COLOR_BALL if loss > 0.6 else COLOR_SUCCESS)
            group = VGroup(w_t, g_t, l_t).arrange(RIGHT, buff=0.40)
            group.move_to(metrics_card.box.get_center() + DOWN * 0.15)
            group.set_z_index(11)
            return group

        metrics_group = always_redraw(get_metrics_group)

        # ----------------------------------------------------
        # 2. ANIMATION TIMELINE
        # ----------------------------------------------------
        self.play_sfx("click")
        self.play(
            Write(title),
            FadeIn(subtitle, shift=DOWN * 0.1),
            FadeIn(author_badge, shift=UP * 0.1),
            run_time=1.2
        )

        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label),
            Create(curve),
            FadeIn(metrics_card),
            run_time=1.5
        )
        self.wait(0.5)

        # Add redrawn MObjects directly to scene
        self.add(ball, tangent_line, metrics_group)
        self.wait(0.6)

        # Continuous Gradient Descent Sliding Animations (5 steps x 1.9s = ~9.5s)
        for step in range(len(w_vals) - 1):
            w_next = w_vals[step + 1]

            # Play SFX at start of each descent step
            self.play_sfx("swap" if step > 0 else "compare")

            # Smoothly update w_tracker: ball, tangent line, and live metrics all slide continuously!
            self.play(
                w_tracker.animate.set_value(w_next),
                run_time=1.5,
                rate_func=smooth
            )
            self.wait(0.4)

        # Final Convergence to Minimum (w ≈ 0)
        is_converged[0] = True
        self.play_sfx("success")
        self.play(
            FadeIn(min_dot),
            FadeIn(min_label, shift=LEFT * 0.1),
            run_time=0.8
        )

        # Extended outro hold for final duration ~18.5s
        self.wait(3.5)
