from manim import *
import numpy as np
import os

# ====================================================
# CONFIGURATION & WARM PAPER THEME CONFIGURATION
# Output: 1080x1920 (9:16 Vertical), 60fps, 8000 KBPS
# ====================================================
COLOR_BG = "#F4ECE1"               # Warm Cream Paper
COLOR_TEXT = "#1C1917"              # Dark Charcoal Ink Text
COLOR_MUTED = "#57534E"            # Warm Stone Charcoal (High Contrast)
COLOR_GRID = "#D6CBB8"             # Soft Parchment Grid Lines
COLOR_CARD_BG = "#EFE6D8"          # Warm Paper Container Fill
COLOR_CARD_BORDER = "#B8A995"      # Warm Card Border
COLOR_PRIMARY = "#386CFA"          # Royal Ink Blue (Regression Line)
COLOR_SECONDARY = "#904DFD"        # Deep Violet Accent
COLOR_POINT = "#5E5EFF"            # Cobalt Blue Data Points
COLOR_RESIDUAL = "#FC4747"         # Vibrant Crimson Red for Loss/Residuals
COLOR_SUCCESS = "#36E470"          # Deep Emerald Green for Best Fit

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

class TechGrid(VGroup):
    """Subtle technical grid styled for dark mode aesthetic."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        dots = VGroup()
        for x in np.arange(-4.0, 4.5, 0.8):
            for y in np.arange(-7.5, 8.0, 0.8):
                dot = Dot(point=[x, y, 0], radius=0.02, color=COLOR_GRID)
                dot.set_opacity(0.5)
                dots.add(dot)
        self.add(dots)

class AuthorBadge(VGroup):
    """Sleek modern author watermark badge."""
    def __init__(self, handle="@tiendatbrn", pos=np.array([0.0, -4.15, 0])):
        super().__init__()
        self.handle_text = Text(handle, font="Consolas", font_size=12, weight=BOLD, color=COLOR_MUTED)
        self.box = RoundedRectangle(
            corner_radius=0.12,
            width=self.handle_text.width + 0.35,
            height=0.34,
            color=COLOR_CARD_BORDER,
            stroke_width=1.5,
            fill_color=COLOR_CARD_BG,
            fill_opacity=0.9
        )
        self.handle_text.move_to(self.box.get_center())
        self.add(self.box, self.handle_text)
        self.move_to(pos)

class LossCard(VGroup):
    """Card displaying current Mean Squared Error (MSE) loss value."""
    def __init__(self, pos=np.array([0.0, -3.5, 0])):
        super().__init__()
        self.box = RoundedRectangle(
            corner_radius=0.10,
            width=4.0,
            height=0.54,
            color=COLOR_CARD_BORDER,
            stroke_width=1.5,
            fill_color=COLOR_CARD_BG,
            fill_opacity=0.95
        ).move_to(pos)
        
        self.title_label = Text("MEAN SQUARED ERROR (MSE)", font="Consolas", font_size=10, weight=BOLD, color=COLOR_MUTED)
        self.title_label.move_to(pos + UP * 0.10)
        
        self.value_text = Text("Loss: 4.850", font="Consolas", font_size=15, weight=BOLD, color=COLOR_RESIDUAL)
        self.value_text.move_to(pos + DOWN * 0.10)
        
        self.add(self.box, self.title_label, self.value_text)

# ====================================================
# MAIN SCENE
# ====================================================

class LinearRegression(Scene):
    def play_sfx(self, sfx_name: str):
        """Helper to play SFX safely from sfx/ directory."""
        path = os.path.join("sfx", f"{sfx_name}.wav")
        if os.path.exists(path):
            self.add_sound(path)

    def construct(self):
        # 1. Background Grid & Watermark
        grid = TechGrid()
        badge = AuthorBadge()
        self.add(grid, badge)

        # Header Title (Safe Zone Top: Y = 4.8)
        title = Text("LINEAR REGRESSION", font="Segoe UI", font_size=32, weight=BOLD, color=COLOR_TEXT)
        title.move_to(np.array([0.0, 4.8, 0]))
        
        subtitle = Text("Optimizing Line of Best Fit via Gradient Descent", font="Consolas", font_size=11, color=COLOR_PRIMARY)
        subtitle.next_to(title, DOWN, buff=0.15)

        self.play_sfx("click")
        self.play(
            FadeIn(title, shift=DOWN * 0.3),
            FadeIn(subtitle, shift=DOWN * 0.2),
            run_time=0.8
        )

        # 2. Axes and Scatter Plot Setup
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=5.4,
            y_length=5.4,
            axis_config={
                "color": COLOR_MUTED,
                "stroke_width": 2,
                "include_numbers": False,
            },
            tips=False
        ).move_to(np.array([0.1, 0.8, 0]))

        # Add custom Text labels for numbers to avoid LaTeX requirement
        axis_numbers = VGroup()
        for x_val in range(0, 11, 2):
            lbl = Text(str(x_val), font="Consolas", font_size=11, color=COLOR_MUTED)
            lbl.next_to(axes.c2p(x_val, 0), DOWN, buff=0.12)
            axis_numbers.add(lbl)
            
        for y_val in range(2, 11, 2):
            lbl = Text(str(y_val), font="Consolas", font_size=11, color=COLOR_MUTED)
            lbl.next_to(axes.c2p(0, y_val), LEFT, buff=0.12)
            axis_numbers.add(lbl)

        x_label = Text("Feature (X)", font="Segoe UI", font_size=12, color=COLOR_MUTED).next_to(axis_numbers, DOWN, buff=0.12)
        y_label = Text("Target (Y)", font="Segoe UI", font_size=12, color=COLOR_MUTED).next_to(axes.y_axis, LEFT, buff=0.45).rotate(90 * DEGREES)

        self.play(
            Create(axes),
            FadeIn(axis_numbers),
            Write(x_label),
            Write(y_label),
            run_time=1.0
        )

        # Data points (x, y)
        raw_data = [
            (1.5, 2.2),
            (2.5, 3.8),
            (3.8, 4.2),
            (5.0, 6.1),
            (6.2, 6.7),
            (7.5, 8.4),
            (8.5, 8.0),
            (3.2, 4.9)
        ]

        data_dots = VGroup()
        for x_val, y_val in raw_data:
            pt = axes.c2p(x_val, y_val)
            dot = Dot(point=pt, radius=0.08, color=COLOR_POINT)
            glow = Dot(point=pt, radius=0.15, color=COLOR_POINT, fill_opacity=0.3)
            data_dots.add(VGroup(glow, dot))

        self.play_sfx("click")
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in data_dots], lag_ratio=0.08),
            run_time=1.0
        )

        # 3. Initial Line Setup: y = w*x + b
        w_tracker = ValueTracker(0.1)
        b_tracker = ValueTracker(2.0)

        def get_line():
            w = w_tracker.get_value()
            b = b_tracker.get_value()
            p1 = axes.c2p(0, b)
            p2 = axes.c2p(9.5, w * 9.5 + b)
            return Line(p1, p2, color=COLOR_PRIMARY, stroke_width=4)

        def get_residuals():
            w = w_tracker.get_value()
            b = b_tracker.get_value()
            res_group = VGroup()
            for x_val, y_val in raw_data:
                y_hat = w * x_val + b
                p_data = axes.c2p(x_val, y_val)
                p_line = axes.c2p(x_val, y_hat)
                res_line = DashedLine(p_data, p_line, dash_length=0.08, color=COLOR_RESIDUAL, stroke_width=2)
                res_group.add(res_line)
            return res_group

        regression_line = get_line()
        residuals = get_residuals()

        # Formula Label
        eq_box = RoundedRectangle(
            corner_radius=0.10,
            width=2.2,
            height=0.36,
            color=COLOR_CARD_BORDER,
            stroke_width=1.5,
            fill_color=COLOR_CARD_BG,
            fill_opacity=0.9
        ).move_to(np.array([0.0, -2.85, 0]))
        
        eq_text = Text("ŷ = w·x + b", font="Consolas", font_size=13, weight=BOLD, color=COLOR_PRIMARY).move_to(eq_box)
        eq_group = VGroup(eq_box, eq_text)

        loss_card = LossCard(pos=np.array([0.0, -3.55, 0]))

        def compute_mse(w, b):
            errs = [(y_val - (w * x_val + b)) ** 2 for x_val, y_val in raw_data]
            return float(np.mean(errs))

        def update_loss_card(card):
            w = w_tracker.get_value()
            b = b_tracker.get_value()
            mse = compute_mse(w, b)
            new_val = Text(f"Loss: {mse:.3f}", font="Consolas", font_size=18, weight=BOLD, color=COLOR_RESIDUAL if mse > 0.5 else COLOR_SUCCESS)
            new_val.move_to(card.value_text.get_center())
            card.value_text.become(new_val)

        self.play_sfx("compare")
        self.play(
            Create(regression_line),
            Create(residuals),
            FadeIn(eq_group, shift=UP * 0.2),
            FadeIn(loss_card, shift=UP * 0.2),
            run_time=1.2
        )

        # Attach dynamic updaters after Create animation finishes
        regression_line.add_updater(lambda m: m.become(get_line()))
        residuals.add_updater(lambda m: m.become(get_residuals()))
        loss_card.add_updater(update_loss_card)

        self.wait(0.5)

        # 4. Gradient Descent Steps
        # Intermediate step 1: w -> 0.45, b -> 1.8
        self.play_sfx("swap")
        self.play(
            w_tracker.animate.set_value(0.45),
            b_tracker.animate.set_value(1.8),
            run_time=1.4,
            rate_func=smooth
        )
        self.wait(0.3)

        # Intermediate step 2: w -> 0.70, b -> 1.5
        self.play_sfx("compare")
        self.play(
            w_tracker.animate.set_value(0.70),
            b_tracker.animate.set_value(1.5),
            run_time=1.4,
            rate_func=smooth
        )
        self.wait(0.3)

        # Optimal Convergence step: w -> 0.86, b -> 1.15
        self.play_sfx("swap")
        self.play(
            w_tracker.animate.set_value(0.86),
            b_tracker.animate.set_value(1.15),
            run_time=1.5,
            rate_func=smooth
        )

        regression_line.clear_updaters()
        residuals.clear_updaters()
        loss_card.clear_updaters()

        # 5. Convergence Success Animation
        opt_line = get_line()
        opt_line.set_color(COLOR_SUCCESS)

        self.play_sfx("success")
        self.play(
            Transform(regression_line, opt_line),
            eq_text.animate.set_color(COLOR_SUCCESS),
            run_time=0.8
        )

        # Predict demonstration: Test point at X = 6.0
        x_test = 6.0
        y_test_pred = 0.86 * x_test + 1.15
        p_x = axes.c2p(x_test, 0)
        p_line_pred = axes.c2p(x_test, y_test_pred)
        p_y = axes.c2p(0, y_test_pred)

        proj_x = DashedLine(p_x, p_line_pred, dash_length=0.08, color=COLOR_SUCCESS, stroke_width=2)
        proj_y = DashedLine(p_line_pred, p_y, dash_length=0.08, color=COLOR_SUCCESS, stroke_width=2)
        pred_dot = Dot(point=p_line_pred, radius=0.1, color=COLOR_SUCCESS)

        pred_tag = Text(f"Predict X=6 -> Y={y_test_pred:.1f}", font="Consolas", font_size=11, weight=BOLD, color=COLOR_SUCCESS)
        pred_tag.next_to(p_line_pred, UP + LEFT, buff=0.15)

        self.play(
            Create(proj_x),
            Create(proj_y),
            FadeIn(pred_dot, scale=0.5),
            Write(pred_tag),
            run_time=1.2
        )

        self.wait(2.5)

if __name__ == "__main__":
    pass
