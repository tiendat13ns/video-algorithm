from manim import *
import numpy as np
import os

# ====================================================
# FORMAT & COLOR PALETTE (Warm Paper Aesthetic)
# Output: 1080x1920 (9:16 Vertical), 60fps, 8000 KBPS
# Target Duration: 20s - 30s
# ====================================================
COLOR_BG          = "#F4ECE1"   # Warm Cream Paper
COLOR_INK         = "#1C1917"   # Dark Charcoal Ink Text
COLOR_MUTED       = "#57534E"   # Warm Stone Gray (Subtitles/Author)
COLOR_GRID        = "#D6CBB8"   # Soft Parchment Grid Lines
COLOR_CARD_BG     = "#EFE6D8"   # Warm Container Fill
COLOR_CARD_BORDER = "#B8A995"   # Warm Card Border

# Soft Pastel Element Palette
COLOR_EL_10       = "#A0C4FF"   # Soft Pastel Blue
COLOR_EL_20       = "#FFD185"   # Soft Pastel Peach
COLOR_EL_30       = "#73E6D0"   # Soft Pastel Mint
COLOR_EL_40       = "#FF9999"   # Soft Pastel Coral Red
COLOR_EL_50       = "#D8B4FE"   # Soft Pastel Lavender
COLOR_EL_60       = "#FDE047"   # Soft Pastel Gold
COLOR_EL_70       = "#6EE7B7"   # Soft Pastel Aqua
COLOR_FRONT_PTR   = "#1D4ED8"   # Royal Blue
COLOR_REAR_PTR    = "#C2410C"   # Deep Amber / Coral
COLOR_ERROR       = "#DC2626"   # Warning Red
COLOR_SUCCESS     = "#047857"   # Emerald Green

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
        for x in np.arange(-3.6, 3.8, 0.8):
            for y in np.arange(-7.2, 7.8, 0.8):
                dot = Dot(point=[x, y, 0], radius=0.025, color=COLOR_GRID)
                dot.set_opacity(0.65)
                dots.add(dot)
        self.add(dots)

class AuthorBadge(VGroup):
    """Sleek modern author watermark badge with clean kerning."""
    def __init__(self, handle="@tiendatbrn", pos=np.array([0.0, -3.70, 0])):
        super().__init__()
        self.handle_text = Text(handle, font="Consolas", font_size=13, weight=BOLD, color=COLOR_MUTED)
        
        self.box = RoundedRectangle(
            corner_radius=0.16,
            width=self.handle_text.width + 0.45,
            height=0.38,
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
    """Compact status card displaying Current Queue Operation."""
    def __init__(self, pos=np.array([0.0, -3.10, 0])):
        super().__init__()
        self.box = RoundedRectangle(
            corner_radius=0.14,
            width=6.0,
            height=0.68,
            color=COLOR_CARD_BORDER,
            stroke_width=1.5,
            fill_color=COLOR_CARD_BG,
            fill_opacity=0.95
        ).move_to(pos)
        
        self.title_label = Text("QUEUE OPERATION", font="Consolas", font_size=10, weight=BOLD, color=COLOR_MUTED)
        self.title_label.move_to(pos + UP * 0.15)
        
        self.value_text = Text("Initialize Empty Queue", font="Consolas", font_size=13, weight=BOLD, color=COLOR_INK)
        self.value_text.move_to(pos + DOWN * 0.11)
        
        self.add(self.box, self.title_label, self.value_text)
        self.set_z_index(10)

    def update_status(self, text: str, color=COLOR_INK):
        new_text = Text(text, font="Consolas", font_size=12.5, weight=BOLD, color=color)
        new_text.move_to(self.value_text.get_center())
        self.value_text.become(new_text)

class QueueElement(VGroup):
    """Individual item stored in the queue."""
    def __init__(self, value: int, color: str, **kwargs):
        super().__init__(**kwargs)
        self.card = RoundedRectangle(
            corner_radius=0.15,
            width=1.10,
            height=1.10,
            fill_color=color,
            fill_opacity=0.95,
            stroke_color=COLOR_INK,
            stroke_width=1.5
        )
        self.label = Text(str(value), font="Segoe UI", font_size=24, weight=BOLD, color=COLOR_INK)
        self.label.move_to(self.card.get_center())
        self.add(self.card, self.label)
        self.set_z_index(4)

class Pointer(VGroup):
    """Arrow pointer pointing up to a slot index with a text label."""
    def __init__(self, label: str, color: str, length: float = 0.65, **kwargs):
        super().__init__(**kwargs)
        self.arrow = Arrow(
            start=DOWN * length,
            end=ORIGIN,
            buff=0.0,
            color=color,
            stroke_width=3.5,
            max_tip_length_to_length_ratio=0.35
        )
        self.text = Text(label, font="Consolas", font_size=13, color=color, weight=BOLD)
        self.text.next_to(self.arrow, DOWN, buff=0.08)
        self.add(self.arrow, self.text)
        self.set_z_index(8)

# ====================================================
# MAIN SCENE
# ====================================================

class QueueVisual(Scene):
    def play_sfx(self, sfx_name: str):
        """Helper to play SFX safely from sfx/ directory."""
        path = os.path.join("sfx", f"{sfx_name}.wav")
        if os.path.exists(path):
            self.add_sound(path)

    def construct(self):
        # ----------------------------------------------------
        # 1. STATIC DIAGRAM SETUP (Safe Zone Y <= 4.8)
        # ----------------------------------------------------
        grid = BackgroundGrid()
        grid.set_z_index(0)
        self.add(grid)

        # Header Titles (Instagram Reels Safe Zone: Y = 4.8)
        title = Text(
            "QUEUE DATA STRUCTURE",
            font="Segoe UI",
            font_size=32,
            weight=BOLD,
            color=COLOR_INK
        ).move_to(np.array([0.0, 4.8, 0]))

        subtitle = Text(
            "First-In, First-Out (FIFO) Architecture",
            font="Verdana",
            font_size=13,
            color=COLOR_MUTED
        ).next_to(title, DOWN, buff=0.12)
        
        title.set_z_index(10)
        subtitle.set_z_index(10)

        # Principle Info Card
        fifo_card = RoundedRectangle(
            corner_radius=0.12,
            width=5.8,
            height=0.45,
            color=COLOR_CARD_BORDER,
            stroke_width=1.2,
            fill_color=COLOR_CARD_BG,
            fill_opacity=0.9
        ).move_to(np.array([0.0, 3.65, 0]))
        fifo_card_text = Text(
            "ENQUEUE (Rear / Left)  -->  DEQUEUE (Front / Right)",
            font="Consolas",
            font_size=10.5,
            weight=BOLD,
            color=COLOR_INK
        ).move_to(fifo_card.get_center())
        fifo_group = VGroup(fifo_card, fifo_card_text).set_z_index(10)

        author_badge = AuthorBadge(pos=np.array([0.0, -3.70, 0]))
        status_card = StatusCard(pos=np.array([0.0, -3.10, 0]))

        # ----------------------------------------------------
        # 2. QUEUE CHANNEL & SLOTS (Centered at Y = 0.5)
        # ----------------------------------------------------
        channel_y = 0.5
        top_rail_y = channel_y + 0.80      # Y = 1.30
        bottom_rail_y = channel_y - 0.80   # Y = -0.30
        rail_left_x = -2.8
        rail_right_x = 2.8

        top_rail = Line(
            start=[rail_left_x, top_rail_y, 0],
            end=[rail_right_x, top_rail_y, 0],
            color=COLOR_CARD_BORDER,
            stroke_width=3.5
        ).set_z_index(2)

        bottom_rail = Line(
            start=[rail_left_x, bottom_rail_y, 0],
            end=[rail_right_x, bottom_rail_y, 0],
            color=COLOR_CARD_BORDER,
            stroke_width=3.5
        ).set_z_index(2)

        # Labels for Entrance (Rear) and Exit (Front)
        rear_in_label = Text("IN (REAR) -->", font="Consolas", font_size=10, color=COLOR_REAR_PTR, weight=BOLD)
        rear_in_label.next_to(Line([rail_left_x, top_rail_y, 0], [rail_left_x, bottom_rail_y, 0]), UP, buff=0.15).shift(LEFT * 0.1)
        rear_in_label.set_z_index(3)

        front_out_label = Text("--> OUT (FRONT)", font="Consolas", font_size=10, color=COLOR_FRONT_PTR, weight=BOLD)
        front_out_label.next_to(Line([rail_right_x, top_rail_y, 0], [rail_right_x, bottom_rail_y, 0]), UP, buff=0.15).shift(RIGHT * 0.1)
        front_out_label.set_z_index(3)

        # Slot Coordinate Map (4 slots: 0 is Front/Right, 3 is Rear/Left)
        slot_xs = [1.8, 0.6, -0.6, -1.8]
        
        slot_placeholders = VGroup()
        slot_labels = VGroup()
        for idx, sx in enumerate(slot_xs):
            box = RoundedRectangle(
                corner_radius=0.12,
                width=1.14,
                height=1.14,
                stroke_color=COLOR_GRID,
                stroke_width=1.5,
                fill_opacity=0.0
            ).move_to([sx, channel_y, 0])
            lbl = Text(f"[{idx}]", font="Consolas", font_size=10, color=COLOR_MUTED)
            lbl.next_to(box, DOWN, buff=0.08)
            slot_placeholders.add(box)
            slot_labels.add(lbl)
        slot_placeholders.set_z_index(1)
        slot_labels.set_z_index(1)

        # ----------------------------------------------------
        # 3. HELPER FUNCTIONS FOR POINTERS & MOVEMENT
        # ----------------------------------------------------
        def get_pointer_tip_pos(slot_idx: int, p_type: str):
            sx = slot_xs[slot_idx]
            tip_y = bottom_rail_y - 0.05
            if p_type == "FRONT":
                return np.array([sx + 0.18, tip_y, 0])
            else: # REAR
                return np.array([sx - 0.18, tip_y, 0])

        def place_pointer(pointer: Pointer, slot_idx: int, p_type: str):
            tip = get_pointer_tip_pos(slot_idx, p_type)
            pointer.move_to(tip + DOWN * (pointer.get_height() / 2))

        def move_pointer_to(pointer: Pointer, slot_idx: int, p_type: str):
            tip = get_pointer_tip_pos(slot_idx, p_type)
            target = tip + DOWN * (pointer.get_height() / 2)
            return pointer.animate.move_to(target)

        # Initialize Pointer objects
        front_ptr = Pointer("FRONT", COLOR_FRONT_PTR, length=0.65)
        rear_ptr = Pointer("REAR", COLOR_REAR_PTR, length=0.65)

        # ----------------------------------------------------
        # 4. ANIMATION TIMELINE (Target Duration: ~22s - 25s)
        # ----------------------------------------------------

        # INTRO: Fade in all base visual components in 1 synchronous play()
        self.play_sfx("click")
        self.play(
            Write(title),
            FadeIn(subtitle, shift=DOWN * 0.1),
            FadeIn(fifo_group, shift=DOWN * 0.1),
            FadeIn(author_badge, shift=UP * 0.1),
            FadeIn(status_card, shift=UP * 0.1),
            Create(top_rail),
            Create(bottom_rail),
            FadeIn(rear_in_label),
            FadeIn(front_out_label),
            FadeIn(slot_placeholders),
            FadeIn(slot_labels),
            run_time=1.0
        )
        self.wait(0.4)

        # ====================================================
        # STEP 1: ENQUEUE(10)
        # ====================================================
        el_10 = QueueElement(10, COLOR_EL_10)
        el_10.move_to(np.array([-4.2, channel_y, 0]))

        place_pointer(front_ptr, 0, "FRONT")
        place_pointer(rear_ptr, 0, "REAR")

        status_card.update_status("enqueue(10) --> Size: 1", COLOR_EL_10)
        self.play_sfx("click")
        self.play(
            el_10.animate.move_to(np.array([slot_xs[0], channel_y, 0])),
            FadeIn(front_ptr, shift=UP * 0.1),
            FadeIn(rear_ptr, shift=UP * 0.1),
            run_time=0.75,
            rate_func=smooth
        )
        self.wait(0.4)

        # ====================================================
        # STEP 2: ENQUEUE(20)
        # ====================================================
        el_20 = QueueElement(20, COLOR_EL_20)
        el_20.move_to(np.array([-4.2, channel_y, 0]))

        status_card.update_status("enqueue(20) --> Rear advances to [1]", COLOR_EL_20)
        self.play_sfx("click")
        self.play(
            el_20.animate.move_to(np.array([slot_xs[1], channel_y, 0])),
            move_pointer_to(rear_ptr, 1, "REAR"),
            run_time=0.75,
            rate_func=smooth
        )
        self.wait(0.4)

        # ====================================================
        # STEP 3: ENQUEUE(30)
        # ====================================================
        el_30 = QueueElement(30, COLOR_EL_30)
        el_30.move_to(np.array([-4.2, channel_y, 0]))

        status_card.update_status("enqueue(30) --> Rear advances to [2]", COLOR_EL_30)
        self.play_sfx("click")
        self.play(
            el_30.animate.move_to(np.array([slot_xs[2], channel_y, 0])),
            move_pointer_to(rear_ptr, 2, "REAR"),
            run_time=0.75,
            rate_func=smooth
        )
        self.wait(0.4)

        # ====================================================
        # STEP 4: ENQUEUE(40) (Queue Full Capacity)
        # ====================================================
        el_40 = QueueElement(40, COLOR_EL_40)
        el_40.move_to(np.array([-4.2, channel_y, 0]))

        status_card.update_status("enqueue(40) --> Queue Full (Capacity: 4)", COLOR_EL_40)
        self.play_sfx("click")
        self.play(
            el_40.animate.move_to(np.array([slot_xs[3], channel_y, 0])),
            move_pointer_to(rear_ptr, 3, "REAR"),
            run_time=0.75,
            rate_func=smooth
        )
        self.wait(0.45)

        # ====================================================
        # STEP 5: ATTEMPT ENQUEUE(50) (Queue Overflow Demo)
        # ====================================================
        el_50_overflow = QueueElement(50, COLOR_EL_50)
        el_50_overflow.move_to(np.array([-4.2, channel_y, 0]))

        status_card.update_status("enqueue(50) --> Queue Overflow! (Rejected)", COLOR_ERROR)
        self.play_sfx("compare")
        self.play(
            el_50_overflow.animate.move_to(np.array([-3.0, channel_y, 0])),
            run_time=0.45
        )
        self.play(
            el_50_overflow.animate.shift(LEFT * 0.5).set_opacity(0),
            run_time=0.40
        )
        self.wait(0.4)

        # ====================================================
        # STEP 6: PEEK() (Inspect Front without removing)
        # ====================================================
        status_card.update_status("peek() --> Returns Front (10) without removing", COLOR_FRONT_PTR)
        self.play_sfx("compare")
        self.play(
            el_10.animate.scale(1.12),
            run_time=0.35
        )
        self.play(
            el_10.animate.scale(1.0 / 1.12),
            run_time=0.30
        )
        self.wait(0.45)

        # ====================================================
        # STEP 7: DEQUEUE() --> Removes 10 (FIFO)
        # ====================================================
        status_card.update_status("dequeue() --> Remove 10 from Front", COLOR_FRONT_PTR)
        self.play_sfx("swap")
        self.play(
            el_10.animate.move_to(np.array([3.6, channel_y, 0])).set_opacity(0),
            el_20.animate.move_to(np.array([slot_xs[0], channel_y, 0])),
            el_30.animate.move_to(np.array([slot_xs[1], channel_y, 0])),
            el_40.animate.move_to(np.array([slot_xs[2], channel_y, 0])),
            move_pointer_to(rear_ptr, 2, "REAR"),
            run_time=0.85,
            rate_func=smooth
        )
        self.wait(0.4)

        # ====================================================
        # STEP 8: DEQUEUE() --> Removes 20 (FIFO)
        # ====================================================
        status_card.update_status("dequeue() --> Remove 20 from Front", COLOR_FRONT_PTR)
        self.play_sfx("swap")
        self.play(
            el_20.animate.move_to(np.array([3.6, channel_y, 0])).set_opacity(0),
            el_30.animate.move_to(np.array([slot_xs[0], channel_y, 0])),
            el_40.animate.move_to(np.array([slot_xs[1], channel_y, 0])),
            move_pointer_to(rear_ptr, 1, "REAR"),
            run_time=0.85,
            rate_func=smooth
        )
        self.wait(0.4)

        # ====================================================
        # STEP 9: ENQUEUE(50) (Interleaved operations)
        # ====================================================
        el_50 = QueueElement(50, COLOR_EL_50)
        el_50.move_to(np.array([-4.2, channel_y, 0]))

        status_card.update_status("enqueue(50) --> Rear advances to [2]", COLOR_EL_50)
        self.play_sfx("click")
        self.play(
            el_50.animate.move_to(np.array([slot_xs[2], channel_y, 0])),
            move_pointer_to(rear_ptr, 2, "REAR"),
            run_time=0.75,
            rate_func=smooth
        )
        self.wait(0.4)

        # ====================================================
        # STEP 10: ENQUEUE(60)
        # ====================================================
        el_60 = QueueElement(60, COLOR_EL_60)
        el_60.move_to(np.array([-4.2, channel_y, 0]))

        status_card.update_status("enqueue(60) --> Rear advances to [3]", COLOR_EL_60)
        self.play_sfx("click")
        self.play(
            el_60.animate.move_to(np.array([slot_xs[3], channel_y, 0])),
            move_pointer_to(rear_ptr, 3, "REAR"),
            run_time=0.75,
            rate_func=smooth
        )
        self.wait(0.4)

        # ====================================================
        # STEP 11: DEQUEUE() --> Removes 30 (FIFO)
        # ====================================================
        status_card.update_status("dequeue() --> Remove 30 from Front", COLOR_FRONT_PTR)
        self.play_sfx("swap")
        self.play(
            el_30.animate.move_to(np.array([3.6, channel_y, 0])).set_opacity(0),
            el_40.animate.move_to(np.array([slot_xs[0], channel_y, 0])),
            el_50.animate.move_to(np.array([slot_xs[1], channel_y, 0])),
            el_60.animate.move_to(np.array([slot_xs[2], channel_y, 0])),
            move_pointer_to(rear_ptr, 2, "REAR"),
            run_time=0.85,
            rate_func=smooth
        )
        self.wait(0.4)

        # ====================================================
        # STEP 12: ENQUEUE(70)
        # ====================================================
        el_70 = QueueElement(70, COLOR_EL_70)
        el_70.move_to(np.array([-4.2, channel_y, 0]))

        status_card.update_status("enqueue(70) --> Rear advances to [3]", COLOR_EL_70)
        self.play_sfx("click")
        self.play(
            el_70.animate.move_to(np.array([slot_xs[3], channel_y, 0])),
            move_pointer_to(rear_ptr, 3, "REAR"),
            run_time=0.75,
            rate_func=smooth
        )
        self.wait(0.4)

        # ====================================================
        # STEP 13: DEQUEUE() --> Removes 40 (FIFO)
        # ====================================================
        status_card.update_status("dequeue() --> Remove 40 from Front", COLOR_FRONT_PTR)
        self.play_sfx("swap")
        self.play(
            el_40.animate.move_to(np.array([3.6, channel_y, 0])).set_opacity(0),
            el_50.animate.move_to(np.array([slot_xs[0], channel_y, 0])),
            el_60.animate.move_to(np.array([slot_xs[1], channel_y, 0])),
            el_70.animate.move_to(np.array([slot_xs[2], channel_y, 0])),
            move_pointer_to(rear_ptr, 2, "REAR"),
            run_time=0.85,
            rate_func=smooth
        )
        self.wait(0.4)

        # ====================================================
        # 5. CELEBRATION & FINAL HOLD
        # ====================================================
        status_card.update_status("Queue Operations Complete! (O(1) Time)", COLOR_SUCCESS)
        self.play_sfx("success")
        self.play(
            el_50.card.animate.set_fill(COLOR_SUCCESS),
            el_60.card.animate.set_fill(COLOR_SUCCESS),
            el_70.card.animate.set_fill(COLOR_SUCCESS),
            el_50.animate.scale(1.08),
            el_60.animate.scale(1.08),
            el_70.animate.scale(1.08),
            run_time=0.5
        )
        self.play(
            el_50.animate.scale(1.0 / 1.08),
            el_60.animate.scale(1.0 / 1.08),
            el_70.animate.scale(1.0 / 1.08),
            run_time=0.35
        )

        self.wait(3.0)
