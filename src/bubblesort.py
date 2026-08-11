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

# User's Custom Soft Pastel Bar Palette (PRESERVED - DO NOT ALTER)
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

class BubbleSort(Scene):
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
            "BUBBLE SORT",
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

        bars = VGroup()

        # Center 7 bars horizontally: total width = 6 * 0.95 = 5.7
        start_x = -((len(values) - 1) * spacing) / 2
        # Baseline lowered to Y = -2.8 for balanced layout
        baseline_y = -2.8

        for i, value in enumerate(values):
            bar = Rectangle(
                width=width,
                height=value * scale,
                fill_color=COLOR_BAR_IDLE,
                fill_opacity=0.95,
                stroke_color=COLOR_INK,
                stroke_width=1.2,
            )

            # Move bars so their bottom edge sits precisely at baseline_y
            bar.move_to(
                RIGHT * (start_x + spacing * i) +
                UP * (baseline_y + value * scale / 2)
            )

            # Label placed cleanly below the baseline
            label = Text(str(value), font="Segoe UI", font_size=24, color=COLOR_INK, weight=BOLD)
            label.next_to(bar, DOWN, buff=0.32)

            group = VGroup(bar, label)
            bars.add(group)

        # Author / Watermark Badge placed centered below the bar numbers at Y = -4.2
        author_badge = AuthorBadge(handle="@tiendatbrn", pos=np.array([0.0, -4.2, 0]))

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
        self.play(LaggedStart(*[
            FadeIn(b, shift=UP * 0.2)
            for b in bars
        ], lag_ratio=0.12), run_time=1.2)
        self.wait(0.5)

        n = len(values)

        for i in range(n):
            for j in range(n - i - 1):
                left = bars[j]
                right = bars[j + 1]

                # Sound: Compare (Tick)
                self.play_sfx("compare")
                self.play(
                    left[0].animate.set_fill(COLOR_COMPARE),  # Soft Pastel Peach
                    right[0].animate.set_fill(COLOR_COMPARE),
                    run_time=0.5
                )

                if values[j] > values[j + 1]:
                    # Sound: Swap (Whoosh)
                    self.play_sfx("swap")
                    self.play(
                        left.animate.shift(RIGHT * spacing),
                        right.animate.shift(LEFT * spacing),
                        run_time=0.8,
                        rate_func=smooth
                    )

                    bars[j], bars[j + 1] = bars[j + 1], bars[j]
                    values[j], values[j + 1] = values[j + 1], values[j]

                self.play(
                    left[0].animate.set_fill(COLOR_BAR_IDLE),
                    right[0].animate.set_fill(COLOR_BAR_IDLE),
                    run_time=0.4
                )

            # Sound: Element Sorted (Green Chime)
            # Scale with about_edge=DOWN so bottom edge never moves down into the label
            self.play_sfx("success")
            bars[n - i - 1][0].set_fill(COLOR_SORTED)
            self.play(
                bars[n - i - 1][0].animate.scale(1.06, about_edge=DOWN),
                run_time=0.5
            )

        self.wait(2.0)