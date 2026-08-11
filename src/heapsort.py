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

# Heap Sort State Palette
COLOR_NODE_IDLE = "#386CFA"        # Royal Ink Blue (Active Heap Node)
COLOR_NODE_FILL = "#1E293B"        # Dark Slate Fill
COLOR_HEAPIFY = "#FF9F1C"          # Gold / Amber (Heapifying / Violation)
COLOR_SWAP = "#C026D3"             # Magenta Violet (Swapping)
COLOR_SORTED = "#73E6D0"           # Mint Green (Sorted & Fixed)
COLOR_SORTED_FILL = "#064E3B"      # Dark Emerald Fill

# High-Contrast Status Text Palette (Crisp Readability on Light Paper)
COLOR_STATUS_INIT = "#B45309"       # Rich Amber Bronze (High Contrast 7:1)
COLOR_STATUS_SWAP = "#404AA8"       # Rich Magenta Violet (High Contrast 7:1)
COLOR_STATUS_SORTED = "#047857"       # Rich Emerald Green (High Contrast 7:1)

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
    """Compact status card displaying Phase and Heap Sort metrics."""
    def __init__(self, pos=np.array([0.0, -2.70, 0])):
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
        
        self.title_label = Text("HEAP SORT STATUS", font="Consolas", font_size=10, weight=BOLD, color=COLOR_MUTED)
        self.title_label.move_to(pos + UP * 0.16)
        
        self.value_text = Text("Status: Unsorted Array [4, 10, 3, 5, 1]", font="Consolas", font_size=13, weight=BOLD, color=COLOR_TEXT)
        self.value_text.move_to(pos + DOWN * 0.12)
        
        self.add(self.box, self.title_label, self.value_text)
        self.set_z_index(10)

    def update_status(self, text: str, color=COLOR_TEXT):
        new_text = Text(text, font="Consolas", font_size=13, weight=BOLD, color=color)
        new_text.move_to(self.value_text.get_center())
        self.value_text.become(new_text)

class HeapNode(VGroup):
    """Individual binary heap node with index tag and value."""
    def __init__(self, index: int, val: int, pos: np.ndarray):
        super().__init__()
        self.index = index
        self.val = val
        self.pos = pos

        self.circle = Circle(
            radius=0.38,
            color=COLOR_NODE_IDLE,
            stroke_width=2.5,
            fill_color=COLOR_NODE_FILL,
            fill_opacity=0.95
        ).move_to(pos)

        self.val_text = Text(str(val), font="Consolas", font_size=16, color="#F8FAFC", weight=BOLD).move_to(pos)
        self.idx_tag = Text(f"[{index}]", font="Consolas", font_size=10, color=COLOR_MUTED).next_to(self.circle, UP, buff=0.06)

        self.add(self.circle, self.val_text, self.idx_tag)
        self.set_z_index(5)

class ArraySlot(VGroup):
    """Memory array slot box corresponding to heap index."""
    def __init__(self, index: int, val: int, pos: np.ndarray):
        super().__init__()
        self.index = index
        self.val = val
        self.pos = pos

        self.box = RoundedRectangle(
            corner_radius=0.10,
            width=0.95,
            height=0.68,
            color=COLOR_NODE_IDLE,
            stroke_width=2.0,
            fill_color=COLOR_NODE_FILL,
            fill_opacity=0.95
        ).move_to(pos)

        self.val_text = Text(str(val), font="Consolas", font_size=15, color="#F8FAFC", weight=BOLD).move_to(pos)
        self.idx_label = Text(f"[{index}]", font="Consolas", font_size=10, color=COLOR_MUTED).next_to(self.box, DOWN, buff=0.08)

        self.add(self.box, self.val_text, self.idx_label)
        self.set_z_index(5)

    def update_val(self, new_val: int):
        self.val = new_val
        new_text = Text(str(new_val), font="Consolas", font_size=15, color="#F8FAFC", weight=BOLD).move_to(self.pos)
        return Transform(self.val_text, new_text)

class HeapSort(Scene):
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
            "HEAP SORT",
            font="Segoe UI",
            font_size=36,
            weight=BOLD,
            color=COLOR_TEXT
        ).move_to(np.array([0.0, 4.8, 0])).set_z_index(10)

        subtitle = Text(
            "Max-Heap & Memory Array Dual Representation",
            font="Verdana",
            font_size=13,
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

        # Labels for Tree & Array Sections
        label_tree = Text("BINARY MAX-HEAP TREE", font="Consolas", font_size=11, color=COLOR_MUTED, weight=BOLD).move_to(np.array([0.0, 3.4, 0]))
        label_array = Text("MEMORY ARRAY REPRESENTATION", font="Consolas", font_size=11, color=COLOR_MUTED, weight=BOLD).move_to(np.array([0.0, -1.1, 0]))

        # Binary Tree Node Positions (Safe Zone: Y = 2.6 to 0.1)
        tree_positions = [
            np.array([0.0, 2.6, 0]),       # Root [0]
            np.array([-1.8, 1.35, 0]),    # Left [1]
            np.array([1.8, 1.35, 0]),     # Right [2]
            np.array([-2.6, 0.1, 0]),     # Left-Left [3]
            np.array([-1.0, 0.1, 0])      # Left-Right [4]
        ]

        values = [4, 10, 3, 5, 1]
        nodes = [HeapNode(i, values[i], tree_positions[i]) for i in range(5)]

        edges = [
            Line(tree_positions[0], tree_positions[1], color=COLOR_MUTED, stroke_width=2).set_z_index(2),
            Line(tree_positions[0], tree_positions[2], color=COLOR_MUTED, stroke_width=2).set_z_index(2),
            Line(tree_positions[1], tree_positions[3], color=COLOR_MUTED, stroke_width=2).set_z_index(2),
            Line(tree_positions[1], tree_positions[4], color=COLOR_MUTED, stroke_width=2).set_z_index(2),
        ]

        # Array Slot Positions (Safe Zone: Y = -1.8)
        array_start_x = -2.1
        array_spacing = 1.05
        array_slots = []
        for i in range(5):
            p = np.array([array_start_x + i * array_spacing, -1.8, 0])
            array_slots.append(ArraySlot(i, values[i], p))

        # Helper to swap 2 nodes & array slots with smooth arc motion
        def swap_nodes(idx1: int, idx2: int, status_msg: str):
            p1, p2 = nodes[idx1].pos, nodes[idx2].pos
            self.play_sfx("swap")
            values[idx1], values[idx2] = values[idx2], values[idx1]

            status_card.update_status(status_msg, COLOR_STATUS_SWAP)
            self.play(
                nodes[idx1].circle.animate.set_stroke(color=COLOR_SWAP, width=3.5),
                nodes[idx2].circle.animate.set_stroke(color=COLOR_SWAP, width=3.5),
                nodes[idx1].animate.move_to(p2),
                nodes[idx2].animate.move_to(p1),
                array_slots[idx1].update_val(values[idx1]),
                array_slots[idx2].update_val(values[idx2]),
                run_time=1.0,
                rate_func=smooth
            )
            # Swap objects in nodes tracking list
            nodes[idx1], nodes[idx2] = nodes[idx2], nodes[idx1]
            nodes[idx1].pos, nodes[idx2].pos = p1, p2

        # ----------------------------------------------------
        # 2. INITIAL DISPLAY & BUILD MAX-HEAP
        # ----------------------------------------------------
        self.play_sfx("click")
        self.play(
            FadeIn(label_tree),
            FadeIn(label_array),
            *[Create(e) for e in edges],
            *[FadeIn(n, shift=DOWN * 0.15) for n in nodes],
            *[FadeIn(s, shift=UP * 0.15) for s in array_slots],
            run_time=1.2
        )
        self.wait(0.4)

        # Build Max-Heap Phase 1: Heapify Root Index 0 (4 < 10 violation)
        status_card.update_status("Phase 1: Build Max-Heap (Heapify Root 0)", COLOR_STATUS_INIT)
        self.play_sfx("compare")
        self.play(
            nodes[0].circle.animate.set_stroke(color=COLOR_HEAPIFY, width=3.5),
            nodes[1].circle.animate.set_stroke(color=COLOR_HEAPIFY, width=3.5),
            run_time=0.7
        )

        swap_nodes(0, 1, "Swap Root (4) with Max Child (10)")
        self.wait(0.3)

        # Sift-Down Index 1 (4 < 5 violation)
        status_card.update_status("Heapify Index 1: 4 < 5 Violation!", COLOR_STATUS_INIT)
        self.play_sfx("compare")
        self.play(
            nodes[1].circle.animate.set_stroke(color=COLOR_HEAPIFY, width=3.5),
            nodes[3].circle.animate.set_stroke(color=COLOR_HEAPIFY, width=3.5),
            run_time=0.7
        )

        swap_nodes(1, 3, "Swap Node [1] (4) with Child (5)")
        
        self.play_sfx("success")
        self.play(
            *[n.circle.animate.set_stroke(color=COLOR_NODE_IDLE, width=2.5) for n in nodes],
            run_time=0.5
        )
        status_card.update_status("Max-Heap Property Established!", COLOR_STATUS_SORTED)
        self.wait(0.5)

        # ----------------------------------------------------
        # 3. PHASE 2: EXTRACT MAX REPEATEDLY
        # ----------------------------------------------------
        # Extract 1: Swap Root [0] (val 10) with Last [4] (val 1)
        status_card.update_status("Extract Max: Swap Root [10] & Last [1]", COLOR_STATUS_SWAP)
        swap_nodes(0, 4, "Extracted Max (10) -> Placed at [4]")

        # Lock Node 4 and Slot 4 in Mint Green!
        self.play_sfx("click")
        self.play(
            nodes[4].circle.animate.set_stroke(color=COLOR_SORTED, width=3.5),
            array_slots[4].box.animate.set_stroke(color=COLOR_SORTED, width=3.0).set_fill(color=COLOR_SORTED_FILL),
            array_slots[4].val_text.animate.set_color(COLOR_SORTED),
            edges[3].animate.set_stroke(color=COLOR_MUTED, opacity=0.3),
            run_time=0.7
        )
        status_card.update_status("Element [10] Sorted & Locked!", COLOR_STATUS_SORTED)
        self.wait(0.4)

        # Sift-Down Root [0] (val 1) vs Children (5, 3) -> Swap with 5 at index 1
        status_card.update_status("Sift-Down Root (1) vs Child (5)", COLOR_STATUS_INIT)
        swap_nodes(0, 1, "Swap Root (1) with Max Child (5)")

        # Sift-Down Index 1 (val 1) vs Child 4 at index 3 -> Swap with 4
        swap_nodes(1, 3, "Swap Node [1] (1) with Child (4)")

        self.play(
            *[nodes[i].circle.animate.set_stroke(color=COLOR_NODE_IDLE, width=2.5) for i in range(4)],
            run_time=0.4
        )

        # Extract 2: Swap Root [0] (val 5) with Last Unsorted [3] (val 1)
        status_card.update_status("Extract Max: Swap Root [5] & Last [1]", COLOR_STATUS_SWAP)
        swap_nodes(0, 3, "Extracted Max (5) -> Placed at [3]")

        self.play_sfx("click")
        self.play(
            nodes[3].circle.animate.set_stroke(color=COLOR_SORTED, width=3.5),
            array_slots[3].box.animate.set_stroke(color=COLOR_SORTED, width=3.0).set_fill(color=COLOR_SORTED_FILL),
            array_slots[3].val_text.animate.set_color(COLOR_SORTED),
            edges[2].animate.set_stroke(color=COLOR_MUTED, opacity=0.3),
            run_time=0.7
        )
        status_card.update_status("Element [5] Sorted & Locked!", COLOR_STATUS_SORTED)
        self.wait(0.4)

        # Sift-Down Root [0] (val 1) vs Child (4) at index 1 -> Swap with 4
        swap_nodes(0, 1, "Swap Root (1) with Child (4)")

        # Extract 3: Swap Root [0] (val 4) with Last Unsorted [2] (val 3)
        swap_nodes(0, 2, "Extracted Max (4) -> Placed at [2]")

        self.play_sfx("click")
        self.play(
            nodes[2].circle.animate.set_stroke(color=COLOR_SORTED, width=3.5),
            array_slots[2].box.animate.set_stroke(color=COLOR_SORTED, width=3.0).set_fill(color=COLOR_SORTED_FILL),
            array_slots[2].val_text.animate.set_color(COLOR_SORTED),
            edges[1].animate.set_stroke(color=COLOR_MUTED, opacity=0.3),
            run_time=0.6
        )

        # Final Swap Root [0] (val 3) with [1] (val 1)
        swap_nodes(0, 1, "Extracted Max (3) -> Placed at [1]")

        # Lock Remaining Nodes & Slots
        self.play_sfx("success")
        self.play(
            nodes[0].circle.animate.set_stroke(color=COLOR_SORTED, width=3.5),
            nodes[1].circle.animate.set_stroke(color=COLOR_SORTED, width=3.5),
            array_slots[0].box.animate.set_stroke(color=COLOR_SORTED, width=3.0).set_fill(color=COLOR_SORTED_FILL),
            array_slots[0].val_text.animate.set_color(COLOR_SORTED),
            array_slots[1].box.animate.set_stroke(color=COLOR_SORTED, width=3.0).set_fill(color=COLOR_SORTED_FILL),
            array_slots[1].val_text.animate.set_color(COLOR_SORTED),
            edges[0].animate.set_stroke(color=COLOR_MUTED, opacity=0.3),
            run_time=0.8
        )
        status_card.update_status("SORTED! Heap Sort Complete", COLOR_STATUS_SORTED)

        self.wait(3.0)
