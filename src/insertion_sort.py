from manim import *
import os

# ====================================================
# FORMAT & USER PASTEL COLOR PALETTE (PRESERVED EXACTLY)
# Output: 1080x1920 (9:16 Vertical), 60fps, 8000 KBPS
# ====================================================
COLOR_BG = "#F4ECE1"               # Warm Cream Paper
COLOR_INK = "#1C1917"              # Dark Charcoal Ink Text
COLOR_MUTED = "#57534E"            # Warm Stone Gray (Subtitles/Author)
COLOR_GRID = "#D6CBB8"             # Soft Parchment Grid Lines

# Custom Soft Pastel Bar Palette
COLOR_BAR_IDLE = "#A0C4FF"         # Soft Pastel Blue
COLOR_COMPARE = "#FFD185"          # Soft Pastel Peach / Warm Orange
COLOR_SORTED = "#73E6D0"           # Soft Pastel Mint / Cyan

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
    def __init__(self, handle="@tiendatbrn", pos=np.array([0.0, -4.2, 0])):
        super().__init__()
        self.handle_text = Text(handle, font="Consolas", font_size=14, weight=BOLD, color=COLOR_MUTED)
        
        self.box = RoundedRectangle(
            corner_radius=0.16,
            width=self.handle_text.width + 0.45,
            height=0.42,
            color="#CFC4B2",
            stroke_width=1.5,
            fill_color="#EFE6D8",
            fill_opacity=0.95
        )
        self.handle_text.move_to(self.box.get_center())
        self.add(self.box, self.handle_text)
        self.move_to(pos)

class InsertionSort(Scene):
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
        self.add(grid)

        # Header Titles (Instagram Reels Safe Zone: Y = 4.8)
        title = Text(
            "INSERTION SORT",
            font="Segoe UI",
            font_size=34,
            weight=BOLD,
            color=COLOR_INK
        ).move_to(np.array([0.0, 4.8, 0]))

        subtitle = Text(
            "Visual Sorting Mechanism",
            font="Segoe UI",
            font_size=15,
            color=COLOR_MUTED
        ).next_to(title, DOWN, buff=0.15)

        values = [7, 3, 5, 2, 8, 1, 4]

        # Bar sizing & spacing
        width = 0.65
        spacing = 0.95
        scale = 0.55

        # Center 7 bars horizontally: total width = 6 * 0.95 = 5.7
        start_x = -((len(values) - 1) * spacing) / 2
        baseline_y = -2.8

        bars = []
        labels = []

        for i, value in enumerate(values):
            bar = Rectangle(
                width=width,
                height=value * scale,
                fill_color=COLOR_BAR_IDLE,
                fill_opacity=0.95,
                stroke_color=COLOR_INK,
                stroke_width=1.2,
            )

            # Move bar rectangle so its bottom edge sits precisely at baseline_y
            bar.move_to(
                RIGHT * (start_x + spacing * i) +
                UP * (baseline_y + value * scale / 2)
            )

            # Create text label & pin it 0.30 units below the bar's bottom edge
            label = Text(str(value), font="Segoe UI", font_size=24, color=COLOR_INK, weight=BOLD)
            label.move_to(bar.get_bottom() + DOWN * 0.30)
            
            # Dynamic updater ensures label ALWAYS follows bar's bottom edge automatically
            label.add_updater(lambda l, b=bar: l.move_to(b.get_bottom() + DOWN * 0.30))

            bars.append(bar)
            labels.append(label)

        # Author / Watermark Badge placed centered below the bar numbers at Y = -4.2
        author_badge = AuthorBadge(handle="@tiendatbrn", pos=np.array([0.0, -4.2, 0]))

        def get_bar_pos(val: int, col_idx: int, lifted: bool = False):
            """Calculate exact center position for bar at column index."""
            x = start_x + spacing * col_idx
            y = (baseline_y + val * scale / 2) + (0.8 if lifted else 0.0)
            return RIGHT * x + UP * y

        # ----------------------------------------------------
        # 2. ANIMATION TIMELINE
        # ----------------------------------------------------
        self.play_sfx("click")
        self.play(
            Write(title),
            FadeIn(subtitle, shift=DOWN * 0.1),
            FadeIn(author_badge, shift=UP * 0.1),
            run_time=1.0
        )
        self.play(
            LaggedStart(*[
                FadeIn(b, shift=UP * 0.2)
                for b in bars
            ], lag_ratio=0.12),
            LaggedStart(*[
                FadeIn(l, shift=UP * 0.2)
                for l in labels
            ], lag_ratio=0.12),
            run_time=1.2
        )
        self.wait(0.5)

        # Initial state: Mark 1st element as sorted
        self.play_sfx("success")
        self.play(
            bars[0].animate.set_fill(COLOR_SORTED),
            run_time=0.4
        )
        self.wait(0.3)

        n = len(values)
        for i in range(1, n):
            key_bar = bars[i]
            key_val = values[i]

            # Sound: Compare / Lift Key
            self.play_sfx("compare")
            self.play(
                key_bar.animate.move_to(get_bar_pos(key_val, i, lifted=True)).set_fill(COLOR_COMPARE),
                run_time=0.5
            )

            j = i - 1
            while j >= 0 and values[j] > key_val:
                # Sound: Shift / Swap element right to slot j + 1
                self.play_sfx("swap")
                self.play(
                    bars[j].animate.move_to(get_bar_pos(values[j], j + 1, lifted=False)),
                    run_time=0.4,
                    rate_func=smooth
                )

                bars[j + 1] = bars[j]
                values[j + 1] = values[j]
                j -= 1

            target_idx = j + 1

            # Move key horizontally to target slot while lifted
            if target_idx != i:
                self.play(
                    key_bar.animate.move_to(get_bar_pos(key_val, target_idx, lifted=True)),
                    run_time=0.4,
                    rate_func=smooth
                )

            # Lower key down into baseline at target slot
            self.play(
                key_bar.animate.move_to(get_bar_pos(key_val, target_idx, lifted=False)),
                run_time=0.4,
                rate_func=smooth
            )

            bars[target_idx] = key_bar
            values[target_idx] = key_val

            # Sound: Highlight sorted prefix elements
            self.play_sfx("success")
            self.play(*[
                bars[k].animate.set_fill(COLOR_SORTED)
                for k in range(i + 1)
            ], run_time=0.4)

            self.wait(0.3)

        # Final success chime celebrating fully sorted array
        self.play_sfx("success")
        self.play(*[
            bars[k].animate.set_fill(COLOR_SORTED)
            for k in range(n)
        ], run_time=0.5)

        self.wait(2.0)