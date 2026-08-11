from manim import *
import numpy as np
import os

# ====================================================
# FORMAT & USER PASTEL COLOR PALETTE (PRESERVED EXACTLY)
# Output: 1080x1920 (9:16 Vertical), 60fps, 8000 KBPS
# ====================================================
COLOR_BG = "#F4ECE1"               # Warm Cream Paper
COLOR_INK = "#1C1917"              # Dark Charcoal Ink Text
COLOR_MUTED = "#57534E"            # Warm Stone Gray (Subtitles/Author)
COLOR_GRID = "#D6CBB8"             # Soft Parchment Grid Lines
COLOR_CARD_BG = "#EFE6D8"          # Warm Container Fill
COLOR_CARD_BORDER = "#B8A995"      # Warm Card Border

# Custom Soft Pastel Bar Palette
COLOR_BAR_IDLE = "#A0C4FF"         # Soft Pastel Blue
COLOR_COMPARE = "#FFD185"          # Soft Pastel Peach (Scanning)
COLOR_MIN_CANDIDATE = "#FF9999"    # Soft Pastel Coral Red (Current Min Candidate)
COLOR_SORTED = "#73E6D0"           # Soft Pastel Mint / Cyan (Sorted)

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

class SelectionSort(Scene):
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
            "SELECTION SORT",
            font="Segoe UI",
            font_size=34,
            weight=BOLD,
            color=COLOR_INK
        ).move_to(np.array([0.0, 4.8, 0]))

        subtitle = Text(
            "Visual Sorting Mechanism",
            font="Verdana",
            font_size=14,
            color=COLOR_MUTED
        ).next_to(title, DOWN, buff=0.15)
        
        title.set_z_index(10)
        subtitle.set_z_index(10)

        author_badge = AuthorBadge(handle="@tiendatbrn", pos=np.array([0.0, -4.15, 0]))

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
            bar.set_z_index(2)

            # Move bar rectangle so its bottom edge sits precisely at baseline_y
            bar.move_to(
                RIGHT * (start_x + spacing * i) +
                UP * (baseline_y + value * scale / 2)
            )

            # Create text label & pin it 0.30 units below the bar's bottom edge
            label = Text(str(value), font="Segoe UI", font_size=24, color=COLOR_INK, weight=BOLD)
            label.set_z_index(3)
            label.move_to(bar.get_bottom() + DOWN * 0.30)
            
            # Dynamic updater ensures label ALWAYS follows bar's bottom edge automatically
            label.add_updater(lambda l, b=bar: l.move_to(b.get_bottom() + DOWN * 0.30))

            bars.append(bar)
            labels.append(label)

        def get_bar_pos(val: int, col_idx: int):
            """Calculate exact center position for bar at column index."""
            x = start_x + spacing * col_idx
            y = baseline_y + val * scale / 2
            return RIGHT * x + UP * y

        # ----------------------------------------------------
        # 2. ANIMATION TIMELINE — Everything appears simultaneously
        # ----------------------------------------------------

        # INTRO: All elements fade in at once — no staggered delays
        self.play_sfx("click")
        self.play(
            Write(title),
            FadeIn(subtitle, shift=DOWN * 0.1),
            FadeIn(author_badge, shift=UP * 0.1),
            *[FadeIn(b, shift=UP * 0.2) for b in bars],
            *[FadeIn(l, shift=UP * 0.2) for l in labels],
            run_time=0.8
        )

        n = len(values)
        for i in range(n - 1):
            min_idx = i

            # Mark starting index i as current minimum candidate immediately
            self.play_sfx("click")
            self.play(
                bars[i].animate.set_fill(COLOR_MIN_CANDIDATE),
                run_time=0.25
            )

            # Scan remaining elements — combine color reset + new highlight in ONE play()
            for j in range(i + 1, n):
                self.play_sfx("compare")

                if values[j] < values[min_idx]:
                    if min_idx != i:
                        # Reset old min candidate AND highlight new candidate + scanned bar simultaneously
                        self.play(
                            bars[min_idx].animate.set_fill(COLOR_BAR_IDLE),
                            bars[j].animate.set_fill(COLOR_MIN_CANDIDATE),
                            run_time=0.22
                        )
                    else:
                        # First candidate found: highlight it (bar i already stays as candidate)
                        self.play(
                            bars[j].animate.set_fill(COLOR_MIN_CANDIDATE),
                            run_time=0.22
                        )
                    min_idx = j
                else:
                    # Scanned bar: flash yellow then reset to idle in ONE combined animation
                    self.play(
                        bars[j].animate.set_fill(COLOR_COMPARE),
                        run_time=0.15
                    )
                    self.play(
                        bars[j].animate.set_fill(COLOR_BAR_IDLE),
                        run_time=0.12
                    )

            # Swap bars at index i and min_idx if needed, then immediately mark sorted
            if min_idx != i:
                self.play_sfx("swap")
                pos_i   = get_bar_pos(values[i],       min_idx)
                pos_min = get_bar_pos(values[min_idx], i)

                self.play(
                    bars[i].animate.move_to(pos_i),
                    bars[min_idx].animate.move_to(pos_min),
                    run_time=0.5,
                    rate_func=smooth
                )

                # Swap Python references
                bars[i], bars[min_idx]     = bars[min_idx], bars[i]
                values[i], values[min_idx] = values[min_idx], values[i]

            # Mark element i as sorted immediately after swap (no extra wait)
            self.play_sfx("success")
            self.play(
                bars[i].animate.set_fill(COLOR_SORTED),
                run_time=0.25
            )

        # Mark final element sorted + full celebration in one shot
        self.play_sfx("success")
        self.play(
            *[bars[k].animate.set_fill(COLOR_SORTED) for k in range(n)],
            run_time=0.4
        )

        self.wait(2.5)
