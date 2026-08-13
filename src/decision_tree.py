from manim import *
import numpy as np
import os

# ====================================================
# CONFIGURATION & COLOR PALETTE (PRESERVED EXACTLY)
# Output: 1080x1920 (9:16 Vertical), 60fps, 8000 KBPS
# ====================================================
COLOR_BG          = "#F4ECE1"   # Warm Cream Paper
COLOR_INK         = "#1C1917"   # Dark Charcoal Ink
COLOR_MUTED       = "#57534E"   # Warm Stone Gray
COLOR_GRID        = "#D6CBB8"   # Soft Parchment Grid
COLOR_CARD_BG     = "#EFE6D8"   # Warm Container Fill
COLOR_CARD_BORDER = "#B8A995"   # Warm Card Border

# Soft Pastel Class Colors
COLOR_BLUE        = "#A0C4FF"   # Soft Pastel Blue (Class B)
COLOR_RED         = "#FF9999"   # Soft Pastel Coral/Red (Class A)
COLOR_SUCCESS     = "#73E6D0"   # Soft Pastel Mint / Green

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
    def __init__(self, handle="@tiendatbrn", pos=np.array([0.0, -3.70, 0])):
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
    """Compact status card displaying Phase and split metrics."""
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
        
        self.title_label = Text("DECISION TREE STATUS", font="Consolas", font_size=10, weight=BOLD, color=COLOR_MUTED)
        self.title_label.move_to(pos + UP * 0.15)
        
        self.value_text = Text("Classifying Feature Space", font="Consolas", font_size=13, weight=BOLD, color=COLOR_INK)
        self.value_text.move_to(pos + DOWN * 0.11)
        
        self.add(self.box, self.title_label, self.value_text)
        self.set_z_index(10)

    def update_status(self, text: str, color=COLOR_INK):
        new_text = Text(text, font="Consolas", font_size=13, weight=BOLD, color=color)
        new_text.move_to(self.value_text.get_center())
        self.value_text.become(new_text)

class DecisionNode(VGroup):
    """Internal split node styled as rounded card containing condition text."""
    def __init__(self, condition: str, pos: np.array, **kwargs):
        super().__init__(**kwargs)
        self.text = Text(condition, font="Consolas", font_size=14, weight=BOLD, color=COLOR_INK)
        self.box = RoundedRectangle(
            corner_radius=0.10,
            width=self.text.width + 0.40,
            height=0.48,
            color=COLOR_CARD_BORDER,
            stroke_width=1.5,
            fill_color=COLOR_CARD_BG,
            fill_opacity=0.95
        ).move_to(pos)
        self.text.move_to(self.box.get_center())
        self.add(self.box, self.text)
        self.set_z_index(5)

class LeafNode(VGroup):
    """Leaf classification node styled as a color-filled circle."""
    def __init__(self, label: str, color: str, pos: np.array, **kwargs):
        super().__init__(**kwargs)
        self.circle = Circle(
            radius=0.28,
            color=COLOR_INK,
            stroke_width=1.5,
            fill_color=color,
            fill_opacity=0.95
        ).move_to(pos)
        self.text = Text(label, font="Segoe UI", font_size=16, weight=BOLD, color=COLOR_INK)
        self.text.move_to(self.circle.get_center())
        self.add(self.circle, self.text)
        self.set_z_index(5)

# ====================================================
# MAIN SCENE
# ====================================================

class DecisionTree(Scene):
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
            "DECISION TREE",
            font="Segoe UI",
            font_size=34,
            weight=BOLD,
            color=COLOR_INK
        ).move_to(np.array([0.0, 4.8, 0]))

        subtitle = Text(
            "Hierarchical Feature Space Splits",
            font="Verdana",
            font_size=13,
            color=COLOR_MUTED
        ).next_to(title, DOWN, buff=0.12)
        
        title.set_z_index(10)
        subtitle.set_z_index(10)

        author_badge = AuthorBadge(pos=np.array([0.0, -3.70, 0]))
        status_card = StatusCard(pos=np.array([0.0, -3.10, 0]))

        # Scatter Plot Axis Configuration
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=4.2,
            y_length=2.8,
            axis_config={
                "color": COLOR_MUTED,
                "stroke_width": 1.5,
                "include_numbers": False,
            },
            tips=False
        ).move_to(np.array([0.0, 1.9, 0]))
        axes.set_z_index(1)

        axis_numbers = VGroup()
        for x_val in range(2, 11, 2):
            lbl = Text(str(x_val), font="Consolas", font_size=10, color=COLOR_MUTED)
            lbl.next_to(axes.c2p(x_val, 0), DOWN, buff=0.08)
            axis_numbers.add(lbl)
        for y_val in range(2, 11, 2):
            lbl = Text(str(y_val), font="Consolas", font_size=10, color=COLOR_MUTED)
            lbl.next_to(axes.c2p(0, y_val), LEFT, buff=0.08)
            axis_numbers.add(lbl)
        axis_numbers.set_z_index(1)

        x_label = Text("Feature 1 (X)", font="Verdana", font_size=11, color=COLOR_MUTED, weight=BOLD).next_to(axis_numbers, DOWN, buff=0.10).set_z_index(1)
        y_label = Text("Feature 2 (Y)", font="Verdana", font_size=11, color=COLOR_MUTED, weight=BOLD).next_to(axes.y_axis, LEFT, buff=0.45).rotate(90 * DEGREES).set_z_index(1)

        # ----------------------------------------------------
        # 2. DATA POINTS GENERATION & GROUPING
        # ----------------------------------------------------
        # Blue points (left of X=5)
        pts_left_blue = np.array([
            [1.0, 3.0], [1.5, 7.5], [2.5, 4.5], [3.5, 2.0], [3.8, 8.0], [4.5, 6.0]
        ])
        # Red points (right of X=5, below Y=4)
        pts_right_red = np.array([
            [5.5, 1.5], [6.8, 3.0], [7.5, 1.0], [8.8, 2.5], [9.2, 3.5]
        ])
        # Blue points (right of X=5, above Y=4)
        pts_right_blue = np.array([
            [5.8, 6.5], [6.5, 8.5], [7.8, 5.0], [8.5, 7.2], [9.5, 9.0]
        ])

        all_points_coords = np.vstack([pts_left_blue, pts_right_red, pts_right_blue])
        point_colors = ([COLOR_BLUE] * len(pts_left_blue) + 
                        [COLOR_RED] * len(pts_right_red) + 
                        [COLOR_BLUE] * len(pts_right_blue))

        point_mobs = VGroup()
        for pt_coord, color in zip(all_points_coords, point_colors):
            pt = axes.c2p(pt_coord[0], pt_coord[1])
            glow = Dot(point=pt, radius=0.12, color=color, fill_opacity=0.25)
            dot = Dot(point=pt, radius=0.07, color=color)
            g = VGroup(glow, dot).set_z_index(3)
            point_mobs.add(g)

        # ----------------------------------------------------
        # 3. ANIMATION TIMELINE — "Combine, Not Sequence"
        # ----------------------------------------------------

        # INTRO: Fade in all initial visual components simultaneously
        self.play_sfx("click")
        self.play(
            Write(title),
            FadeIn(subtitle, shift=DOWN * 0.1),
            FadeIn(author_badge, shift=UP * 0.1),
            FadeIn(status_card, shift=UP * 0.1),
            Create(axes),
            FadeIn(axis_numbers),
            Write(x_label),
            Write(y_label),
            *[FadeIn(p, scale=0.5) for p in point_mobs],
            run_time=0.9
        )
        self.wait(0.3)

        # ----------------------------------------------------
        # STEP 1: SPLIT 1 (X < 5)
        # ----------------------------------------------------
        # Split line 1: Vertical line at X = 5
        line_x5 = DashedLine(
            axes.c2p(5, 0),
            axes.c2p(5, 10),
            color=COLOR_MUTED,
            stroke_width=2.5,
            dash_length=0.08
        ).set_z_index(2)

        # Left region shading: X < 5 (Class Blue)
        region_left_blue = Polygon(
            axes.c2p(0, 0), axes.c2p(5, 0), axes.c2p(5, 10), axes.c2p(0, 10),
            fill_color=COLOR_BLUE,
            fill_opacity=0.12,
            stroke_width=0
        ).set_z_index(1)

        # Tree Node 1: Root Node
        root_pos = np.array([0.0, -0.1, 0])
        root_node = DecisionNode("X < 5", root_pos)

        status_card.update_status("Split 1: Feature 1 (X) < 5", COLOR_INK)
        self.play_sfx("compare")
        self.play(
            Create(line_x5),
            FadeIn(root_node, shift=DOWN * 0.15),
            run_time=0.6
        )
        self.wait(0.2)

        # Left Child Node (Leaf: Class Blue)
        left_leaf_pos = np.array([-1.7, -1.1, 0])
        left_leaf = LeafNode("B", COLOR_BLUE, left_leaf_pos)

        # Yes branch arrow pointing Left
        arrow_yes = Arrow(
            start=root_pos + DOWN * 0.24,
            end=left_leaf_pos + UP * 0.28,
            buff=0.02,
            color=COLOR_CARD_BORDER,
            stroke_width=2.0,
            max_tip_length_to_length_ratio=0.35
        )
        label_yes = Text("Yes", font="Consolas", font_size=11, color=COLOR_MUTED).next_to(arrow_yes, LEFT, buff=0.05).shift(UP * 0.1)

        # Pulse animation for left classified blue points
        left_blue_indices = range(len(pts_left_blue))
        pulse_anims = [
            point_mobs[i].animate.scale(1.2) for i in left_blue_indices
        ] + [
            point_mobs[i].animate.scale(1.0) for i in left_blue_indices
        ]

        status_card.update_status("X < 5 (Yes) → Class Blue Region", COLOR_BLUE)
        self.play_sfx("success")
        self.play(
            Create(arrow_yes),
            FadeIn(label_yes),
            FadeIn(left_leaf, scale=0.5),
            FadeIn(region_left_blue),
            AnimationGroup(*pulse_anims, lag_ratio=0.02),
            run_time=0.8
        )
        self.wait(0.2)

        # ----------------------------------------------------
        # STEP 2: SPLIT 2 (Y < 4)
        # ----------------------------------------------------
        # Split line 2: Horizontal line at Y = 4 on the right side (X >= 5)
        line_y4 = DashedLine(
            axes.c2p(5, 4),
            axes.c2p(10, 4),
            color=COLOR_MUTED,
            stroke_width=2.5,
            dash_length=0.08
        ).set_z_index(2)

        # Right child split node (Y < 4)
        right_node_pos = np.array([1.7, -1.1, 0])
        right_node = DecisionNode("Y < 4", right_node_pos)

        # No branch arrow pointing Right
        arrow_no = Arrow(
            start=root_pos + DOWN * 0.24,
            end=right_node_pos + UP * 0.24,
            buff=0.02,
            color=COLOR_CARD_BORDER,
            stroke_width=2.0,
            max_tip_length_to_length_ratio=0.35
        )
        label_no = Text("No", font="Consolas", font_size=11, color=COLOR_MUTED).next_to(arrow_no, RIGHT, buff=0.05).shift(UP * 0.1)

        status_card.update_status("Split 2: Feature 2 (Y) < 4", COLOR_INK)
        self.play_sfx("compare")
        self.play(
            Create(arrow_no),
            FadeIn(label_no),
            Create(line_y4),
            FadeIn(right_node, shift=DOWN * 0.15),
            run_time=0.8
        )
        self.wait(0.2)

        # Grandchildren nodes (Leafs: Red and Blue)
        g_left_pos = np.array([0.9, -2.2, 0])  # Y < 4? Yes (Red Leaf)
        g_right_pos = np.array([2.5, -2.2, 0]) # Y < 4? No  (Blue Leaf)
        
        g_left_leaf = LeafNode("R", COLOR_RED, g_left_pos)
        g_right_leaf = LeafNode("B", COLOR_BLUE, g_right_pos)

        # Arrows connecting Right Node to Grandchildren
        arrow_g_yes = Arrow(
            start=right_node_pos + DOWN * 0.24,
            end=g_left_pos + UP * 0.28,
            buff=0.02,
            color=COLOR_CARD_BORDER,
            stroke_width=2.0,
            max_tip_length_to_length_ratio=0.35
        )
        label_g_yes = Text("Yes", font="Consolas", font_size=10, color=COLOR_MUTED).next_to(arrow_g_yes, LEFT, buff=0.03).shift(UP * 0.05)

        arrow_g_no = Arrow(
            start=right_node_pos + DOWN * 0.24,
            end=g_right_pos + UP * 0.28,
            buff=0.02,
            color=COLOR_CARD_BORDER,
            stroke_width=2.0,
            max_tip_length_to_length_ratio=0.35
        )
        label_g_no = Text("No", font="Consolas", font_size=10, color=COLOR_MUTED).next_to(arrow_g_no, RIGHT, buff=0.03).shift(UP * 0.05)

        # Region Shading rectangles
        # X >= 5, Y < 4 (Class Red)
        region_right_red = Polygon(
            axes.c2p(5, 0), axes.c2p(10, 0), axes.c2p(10, 4), axes.c2p(5, 4),
            fill_color=COLOR_RED,
            fill_opacity=0.12,
            stroke_width=0
        ).set_z_index(1)

        # X >= 5, Y >= 4 (Class Blue)
        region_right_blue = Polygon(
            axes.c2p(5, 4), axes.c2p(10, 4), axes.c2p(10, 10), axes.c2p(5, 10),
            fill_color=COLOR_BLUE,
            fill_opacity=0.12,
            stroke_width=0
        ).set_z_index(1)

        # Pulse remaining points on the right
        right_point_indices = range(len(pts_left_blue), len(all_points_coords))
        right_pulse_anims = [
            point_mobs[i].animate.scale(1.2) for i in right_point_indices
        ] + [
            point_mobs[i].animate.scale(1.0) for i in right_point_indices
        ]

        status_card.update_status("Leaves Classified Successfully", COLOR_SUCCESS)
        self.play_sfx("success")
        self.play(
            Create(arrow_g_yes),
            FadeIn(label_g_yes),
            Create(arrow_g_no),
            FadeIn(label_g_no),
            FadeIn(g_left_leaf, scale=0.5),
            FadeIn(g_right_leaf, scale=0.5),
            FadeIn(region_right_red),
            FadeIn(region_right_blue),
            AnimationGroup(*right_pulse_anims, lag_ratio=0.02),
            run_time=0.9
        )
        self.wait(0.2)

        # ----------------------------------------------------
        # 4. FINAL STATE & SUCCESS CELEBRATION
        # ----------------------------------------------------
        status_card.update_status("Decision Tree Complete!", COLOR_SUCCESS)
        self.play_sfx("success")
        
        # Highlight active elements with a pulse
        self.play(
            left_leaf[0].animate.scale(1.1),
            g_left_leaf[0].animate.scale(1.1),
            g_right_leaf[0].animate.scale(1.1),
            run_time=0.4
        )
        self.play(
            left_leaf[0].animate.scale(1.0),
            g_left_leaf[0].animate.scale(1.0),
            g_right_leaf[0].animate.scale(1.0),
            run_time=0.3
        )

        self.wait(3.0)
