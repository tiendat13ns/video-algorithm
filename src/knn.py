from manim import *
import numpy as np
import os

# ====================================================
# FORMAT & USER PASTEL COLOR PALETTE (PRESERVED EXACTLY)
# Output: 1080x1920 (9:16 Vertical), 60fps, 8000 KBPS
# Target Video Duration: ~20.5 Seconds (3-Class Dataset)
# ====================================================
COLOR_BG = "#F4ECE1"               # Warm Cream Paper
COLOR_INK = "#1C1917"              # Dark Charcoal Ink Text
COLOR_MUTED = "#57534E"            # Warm Stone Gray (Subtitles/Author)
COLOR_GRID = "#D6CBB8"             # Soft Parchment Grid Lines
COLOR_CARD_BG = "#EFE6D8"          # Warm Container Fill
COLOR_CARD_BORDER = "#B8A995"      # Warm Card Border

# 3 Class Palette + Query Point
COLOR_CLASS_A = "#FC4747"          # Crimson / Coral Red (Class A)
COLOR_CLASS_B = "#386CFA"          # Royal Ink Blue (Class B)
COLOR_CLASS_C = "#059669"          # Emerald Green (Class C)
COLOR_QUERY = "#FF9F1C"            # Gold / Orange (New Query Point)

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
    """Compact status card displaying Phase and KNN metrics."""
    def __init__(self, pos=np.array([0.0, -3.10, 0])):
        super().__init__()
        self.pos = pos
        self.box = RoundedRectangle(
            corner_radius=0.14,
            width=6.0,
            height=0.72,
            color=COLOR_CARD_BORDER,
            stroke_width=1.5,
            fill_color=COLOR_CARD_BG,
            fill_opacity=0.95
        ).move_to(pos)
        
        self.title_label = Text("K-NEAREST NEIGHBORS (K=3)", font="Consolas", font_size=10, weight=BOLD, color=COLOR_MUTED)
        self.title_label.move_to(pos + UP * 0.16)
        
        self.value_text = Text("Status: 3-Class Dataset", font="Consolas", font_size=13, weight=BOLD, color=COLOR_INK)
        self.value_text.move_to(pos + DOWN * 0.12)
        
        self.add(self.box, self.title_label, self.value_text)
        self.set_z_index(10)

    def update_status(self, text: str, color=COLOR_INK):
        new_text = Text(text, font="Consolas", font_size=13, weight=BOLD, color=color)
        new_text.move_to(self.value_text.get_center())
        self.value_text.become(new_text)

class KNNClassification(Scene):
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
            "K-NEAREST NEIGHBORS",
            font="Segoe UI",
            font_size=34,
            weight=BOLD,
            color=COLOR_INK
        ).move_to(np.array([0.0, 4.8, 0]))

        subtitle = Text(
            "Classification Mechanism (3 Classes, K=3)",
            font="Verdana",
            font_size=13,
            color=COLOR_MUTED
        ).next_to(title, DOWN, buff=0.15)
        
        title.set_z_index(10)
        subtitle.set_z_index(10)

        author_badge = AuthorBadge(handle="@tiendatbrn", pos=np.array([0.0, -4.15, 0]))

        # Central Feature Axes Setup (5.2 x 5.2 canvas centered at Y = 0.85)
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=5.2,
            y_length=5.2,
            axis_config={
                "color": COLOR_MUTED,
                "stroke_width": 1.5,
                "include_numbers": False,
            },
            tips=False
        ).move_to(np.array([0.1, 0.85, 0]))
        axes.set_z_index(1)

        axis_numbers = VGroup()
        for x_val in range(0, 11, 2):
            lbl = Text(str(x_val), font="Consolas", font_size=11, color=COLOR_MUTED)
            lbl.next_to(axes.c2p(x_val, 0), DOWN, buff=0.10)
            axis_numbers.add(lbl)
            
        for y_val in range(2, 11, 2):
            lbl = Text(str(y_val), font="Consolas", font_size=11, color=COLOR_MUTED)
            lbl.next_to(axes.c2p(0, y_val), LEFT, buff=0.10)
            axis_numbers.add(lbl)
        axis_numbers.set_z_index(1)

        x_label = Text("Feature 1 (X)", font="Verdana", font_size=13, color=COLOR_MUTED, weight=BOLD).next_to(axis_numbers, DOWN, buff=0.15)
        y_label = Text("Feature 2 (Y)", font="Verdana", font_size=13, color=COLOR_MUTED, weight=BOLD).next_to(axes.y_axis, LEFT, buff=0.55).rotate(90 * DEGREES)
        x_label.set_z_index(1)
        y_label.set_z_index(1)

        status_card = StatusCard(pos=np.array([0.0, -3.10, 0]))

        # ----------------------------------------------------
        # 2. ANIMATION TIMELINE
        # ----------------------------------------------------
        self.play_sfx("click")
        self.play(
            Write(title),
            FadeIn(subtitle, shift=DOWN * 0.1),
            FadeIn(author_badge, shift=UP * 0.1),
            run_time=0.8
        )

        self.play(
            Create(axes),
            FadeIn(axis_numbers),
            Write(x_label),
            Write(y_label),
            FadeIn(status_card, shift=UP * 0.1),
            run_time=1.0
        )

        # 3 Clusters: Class A (Red), Class B (Blue), Class C (Green - Top-Right Area)
        pts_A_coords = np.array([
            [2.0, 7.5], [2.8, 6.8], [1.8, 6.2], [3.2, 7.8], 
            [2.4, 8.2], [3.5, 6.5], [1.5, 7.0], [5.5, 5.5]
        ])
        pts_B_coords = np.array([
            [7.2, 2.5], [8.0, 3.2], [6.5, 2.8], [7.8, 1.8], 
            [8.5, 2.6], [6.8, 3.8], [5.8, 4.0], [7.5, 4.5]
        ])
        pts_C_coords = np.array([
            [7.5, 7.8], [8.2, 8.2], [7.0, 7.2], [8.5, 7.5], 
            [7.8, 8.6], [8.8, 8.0], [7.2, 8.4], [8.2, 7.0]
        ])

        mobs_A = VGroup()
        for x_val, y_val in pts_A_coords:
            pt = axes.c2p(x_val, y_val)
            glow = Dot(point=pt, radius=0.16, color=COLOR_CLASS_A, fill_opacity=0.25)
            dot = Dot(point=pt, radius=0.09, color=COLOR_CLASS_A)
            g = VGroup(glow, dot).set_z_index(3)
            mobs_A.add(g)

        mobs_B = VGroup()
        for x_val, y_val in pts_B_coords:
            pt = axes.c2p(x_val, y_val)
            glow = Dot(point=pt, radius=0.16, color=COLOR_CLASS_B, fill_opacity=0.25)
            dot = Dot(point=pt, radius=0.09, color=COLOR_CLASS_B)
            g = VGroup(glow, dot).set_z_index(3)
            mobs_B.add(g)

        mobs_C = VGroup()
        for x_val, y_val in pts_C_coords:
            pt = axes.c2p(x_val, y_val)
            glow = Dot(point=pt, radius=0.16, color=COLOR_CLASS_C, fill_opacity=0.25)
            dot = Dot(point=pt, radius=0.09, color=COLOR_CLASS_C)
            g = VGroup(glow, dot).set_z_index(3)
            mobs_C.add(g)

        self.play_sfx("click")
        self.play(
            LaggedStart(*[FadeIn(p, scale=0.5) for p in mobs_A], lag_ratio=0.04),
            LaggedStart(*[FadeIn(p, scale=0.5) for p in mobs_B], lag_ratio=0.04),
            LaggedStart(*[FadeIn(p, scale=0.5) for p in mobs_C], lag_ratio=0.04),
            run_time=1.2
        )
        self.wait(0.4)

        all_pts = np.vstack([pts_A_coords, pts_B_coords, pts_C_coords])
        all_colors = [COLOR_CLASS_A]*len(pts_A_coords) + [COLOR_CLASS_B]*len(pts_B_coords) + [COLOR_CLASS_C]*len(pts_C_coords)

        # ====================================================
        # EXAMPLE 1: Query Point Q1 -> Class B (Royal Blue)
        # ====================================================
        q1_coord = np.array([6.4, 4.2])
        q1_pos = axes.c2p(q1_coord[0], q1_coord[1])

        q1_bg = Dot(point=q1_pos, radius=0.24, color=COLOR_QUERY, fill_opacity=0.35)
        q1_ring = Circle(radius=0.20, color=COLOR_QUERY, stroke_width=2.5).move_to(q1_pos)
        q1_dot = Dot(point=q1_pos, radius=0.11, color=COLOR_QUERY)
        q1_qmark = Text("?", font="Consolas", font_size=12, weight=BOLD, color=COLOR_INK).move_to(q1_pos)
        q1_group = VGroup(q1_bg, q1_ring, q1_dot, q1_qmark).set_z_index(7)

        self.play_sfx("compare")
        status_card.update_status("Ex 1: Query Point Q1 ?", COLOR_QUERY)
        self.play(SpinInFromNothing(q1_group), run_time=0.7)

        dists_1 = [np.linalg.norm(q1_coord - pt) for pt in all_pts]
        sorted_1 = np.argsort(dists_1)[:3]
        radius_1 = dists_1[sorted_1[2]]

        p_far_1 = axes.c2p(q1_coord[0] + radius_1, q1_coord[1])
        r_pixels_1 = np.linalg.norm(p_far_1 - q1_pos)

        circle_1 = Circle(radius=r_pixels_1, color=COLOR_QUERY, stroke_width=2.0, stroke_opacity=0.85).move_to(q1_pos).set_z_index(2)

        lines_1 = VGroup()
        glows_1 = VGroup()
        for idx in sorted_1:
            t_pos = axes.c2p(all_pts[idx][0], all_pts[idx][1])
            t_col = all_colors[idx]
            l = DashedLine(q1_pos, t_pos, color=t_col, stroke_width=2.0, dash_length=0.08).set_z_index(2)
            lines_1.add(l)
            g = Circle(radius=0.22, color=t_col, stroke_width=2.5).move_to(t_pos).set_z_index(4)
            glows_1.add(g)

        self.play_sfx("compare")
        self.play(
            Create(circle_1),
            Create(lines_1),
            LaggedStart(*[Create(g) for g in glows_1], lag_ratio=0.1),
            run_time=1.0
        )

        status_card.update_status("Q1 Vote: 2 Blue vs 1 Red", COLOR_CLASS_B)
        self.play_sfx("swap")
        self.play(glows_1.animate.scale(1.2), run_time=0.4)

        final_blue_1 = VGroup(
            Dot(point=q1_pos, radius=0.18, color=COLOR_CLASS_B, fill_opacity=0.35),
            Dot(point=q1_pos, radius=0.10, color=COLOR_CLASS_B)
        ).set_z_index(7)

        self.play_sfx("success")
        status_card.update_status("Q1 -> CLASS B (Blue)", COLOR_CLASS_B)
        self.play(
            Transform(q1_group, final_blue_1),
            circle_1.animate.set_color(COLOR_CLASS_B).set_opacity(0.3),
            run_time=0.7
        )
        self.wait(0.3)
        self.play(FadeOut(lines_1), FadeOut(glows_1), FadeOut(circle_1), run_time=0.4)

        # ====================================================
        # EXAMPLE 2: Query Point Q2 -> Class A (Crimson Red)
        # ====================================================
        q2_coord = np.array([2.2, 5.8])
        q2_pos = axes.c2p(q2_coord[0], q2_coord[1])

        q2_bg = Dot(point=q2_pos, radius=0.24, color=COLOR_QUERY, fill_opacity=0.35)
        q2_ring = Circle(radius=0.20, color=COLOR_QUERY, stroke_width=2.5).move_to(q2_pos)
        q2_dot = Dot(point=q2_pos, radius=0.11, color=COLOR_QUERY)
        q2_qmark = Text("?", font="Consolas", font_size=12, weight=BOLD, color=COLOR_INK).move_to(q2_pos)
        q2_group = VGroup(q2_bg, q2_ring, q2_dot, q2_qmark).set_z_index(7)

        self.play_sfx("compare")
        status_card.update_status("Ex 2: Query Point Q2 ?", COLOR_QUERY)
        self.play(SpinInFromNothing(q2_group), run_time=0.7)

        dists_2 = [np.linalg.norm(q2_coord - pt) for pt in all_pts]
        sorted_2 = np.argsort(dists_2)[:3]
        radius_2 = dists_2[sorted_2[2]]

        p_far_2 = axes.c2p(q2_coord[0] + radius_2, q2_coord[1])
        r_pixels_2 = np.linalg.norm(p_far_2 - q2_pos)

        circle_2 = Circle(radius=r_pixels_2, color=COLOR_QUERY, stroke_width=2.0, stroke_opacity=0.85).move_to(q2_pos).set_z_index(2)

        lines_2 = VGroup()
        glows_2 = VGroup()
        for idx in sorted_2:
            t_pos = axes.c2p(all_pts[idx][0], all_pts[idx][1])
            t_col = all_colors[idx]
            l = DashedLine(q2_pos, t_pos, color=t_col, stroke_width=2.0, dash_length=0.08).set_z_index(2)
            lines_2.add(l)
            g = Circle(radius=0.22, color=t_col, stroke_width=2.5).move_to(t_pos).set_z_index(4)
            glows_2.add(g)

        self.play_sfx("compare")
        self.play(
            Create(circle_2),
            Create(lines_2),
            LaggedStart(*[Create(g) for g in glows_2], lag_ratio=0.1),
            run_time=1.0
        )

        status_card.update_status("Q2 Vote: 3 Red vs 0 Blue", COLOR_CLASS_A)
        self.play_sfx("swap")
        self.play(glows_2.animate.scale(1.2), run_time=0.4)

        final_red_2 = VGroup(
            Dot(point=q2_pos, radius=0.18, color=COLOR_CLASS_A, fill_opacity=0.35),
            Dot(point=q2_pos, radius=0.10, color=COLOR_CLASS_A)
        ).set_z_index(7)

        self.play_sfx("success")
        status_card.update_status("Q2 -> CLASS A (Red)", COLOR_CLASS_A)
        self.play(
            Transform(q2_group, final_red_2),
            circle_2.animate.set_color(COLOR_CLASS_A).set_opacity(0.3),
            run_time=0.7
        )
        self.wait(0.3)
        self.play(FadeOut(lines_2), FadeOut(glows_2), FadeOut(circle_2), run_time=0.4)

        # ====================================================
        # EXAMPLE 3: Query Point Q3 -> Class C (Emerald Green - Top Right)
        # ====================================================
        q3_coord = np.array([7.6, 7.5])
        q3_pos = axes.c2p(q3_coord[0], q3_coord[1])

        q3_bg = Dot(point=q3_pos, radius=0.24, color=COLOR_QUERY, fill_opacity=0.35)
        q3_ring = Circle(radius=0.20, color=COLOR_QUERY, stroke_width=2.5).move_to(q3_pos)
        q3_dot = Dot(point=q3_pos, radius=0.11, color=COLOR_QUERY)
        q3_qmark = Text("?", font="Consolas", font_size=12, weight=BOLD, color=COLOR_INK).move_to(q3_pos)
        q3_group = VGroup(q3_bg, q3_ring, q3_dot, q3_qmark).set_z_index(7)

        self.play_sfx("compare")
        status_card.update_status("Ex 3: Query Point Q3 ?", COLOR_QUERY)
        self.play(SpinInFromNothing(q3_group), run_time=0.7)

        dists_3 = [np.linalg.norm(q3_coord - pt) for pt in all_pts]
        sorted_3 = np.argsort(dists_3)[:3]
        radius_3 = dists_3[sorted_3[2]]

        p_far_3 = axes.c2p(q3_coord[0] + radius_3, q3_coord[1])
        r_pixels_3 = np.linalg.norm(p_far_3 - q3_pos)

        circle_3 = Circle(radius=r_pixels_3, color=COLOR_QUERY, stroke_width=2.0, stroke_opacity=0.85).move_to(q3_pos).set_z_index(2)

        lines_3 = VGroup()
        glows_3 = VGroup()
        for idx in sorted_3:
            t_pos = axes.c2p(all_pts[idx][0], all_pts[idx][1])
            t_col = all_colors[idx]
            l = DashedLine(q3_pos, t_pos, color=t_col, stroke_width=2.0, dash_length=0.08).set_z_index(2)
            lines_3.add(l)
            g = Circle(radius=0.22, color=t_col, stroke_width=2.5).move_to(t_pos).set_z_index(4)
            glows_3.add(g)

        self.play_sfx("compare")
        self.play(
            Create(circle_3),
            Create(lines_3),
            LaggedStart(*[Create(g) for g in glows_3], lag_ratio=0.1),
            run_time=1.0
        )

        status_card.update_status("Q3 Vote: 3 Green", COLOR_CLASS_C)
        self.play_sfx("swap")
        self.play(glows_3.animate.scale(1.2), run_time=0.4)

        final_green_3 = VGroup(
            Dot(point=q3_pos, radius=0.18, color=COLOR_CLASS_C, fill_opacity=0.35),
            Dot(point=q3_pos, radius=0.10, color=COLOR_CLASS_C)
        ).set_z_index(7)

        self.play_sfx("success")
        status_card.update_status("Q3 -> CLASS C (Green)", COLOR_CLASS_C)
        self.play(
            Transform(q3_group, final_green_3),
            circle_3.animate.set_color(COLOR_CLASS_C).set_opacity(0.3),
            run_time=0.7
        )

        self.wait(3.0)
