from manim import *
import numpy as np
import os

# ====================================================
# CONFIGURATION & WARM PAPER THEME CONFIGURATION
# Output: 1080x1920 (9:16 Vertical), 60fps, 8000 KBPS
# ====================================================
COLOR_BG = "#F4ECE1"               # Warm Cream Paper
COLOR_TEXT = "#1C1917"              # Dark Charcoal Ink Text
COLOR_MUTED = "#57534E"            # Warm Stone Charcoal
COLOR_GRID = "#D6CBB8"             # Soft Parchment Grid Lines
COLOR_CARD_BG = "#EFE6D8"          # Warm Paper Container Fill
COLOR_CARD_BORDER = "#B8A995"      # Warm Card Border

# 3 Cluster Palette (High contrast pastel/ink tones)
COLOR_C1 = "#1D4ED8"               # Royal Blue
COLOR_C2 = "#7C3AED"               # Deep Violet
COLOR_C3 = "#C2410C"               # Warm Coral Amber
COLOR_INIT = "#78716C"             # Neutral Stone Gray (Unassigned)
COLOR_SUCCESS = "#047857"          # Emerald Green for Convergence

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
    """Subtle technical grid styled for warm paper aesthetic."""
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
        self.handle_text = Text(handle, font="Consolas", font_size=13, weight=BOLD, color=COLOR_MUTED)
        self.box = RoundedRectangle(
            corner_radius=0.14,
            width=self.handle_text.width + 0.40,
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
    """Compact status card displaying Phase and Iteration."""
    def __init__(self, pos=np.array([0.0, -3.10, 0])):
        super().__init__()
        self.pos = pos
        self.box = RoundedRectangle(
            corner_radius=0.14,
            width=5.2,
            height=0.72,
            color=COLOR_CARD_BORDER,
            stroke_width=1.5,
            fill_color=COLOR_CARD_BG,
            fill_opacity=0.95
        ).move_to(pos)
        
        self.title_label = Text("K-MEANS CLUSTERING STATUS", font="Consolas", font_size=10, weight=BOLD, color=COLOR_MUTED)
        self.title_label.move_to(pos + UP * 0.16)
        
        self.value_text = Text("Status: Initialize  |  Iter: 0", font="Consolas", font_size=13, weight=BOLD, color=COLOR_C1)
        self.value_text.move_to(pos + DOWN * 0.12)
        
        self.add(self.box, self.title_label, self.value_text)
        self.set_z_index(10)

    def update_status(self, status: str, iter_num: int, color=COLOR_C1):
        new_text = Text(f"Status: {status}  |  Iter: {iter_num}", font="Consolas", font_size=13, weight=BOLD, color=color)
        new_text.move_to(self.value_text.get_center())
        self.value_text.become(new_text)

# ====================================================
# MAIN SCENE
# ====================================================

class KMeansClustering(Scene):
    def play_sfx(self, sfx_name: str):
        """Helper to play SFX safely from sfx/ directory."""
        path = os.path.join("sfx", f"{sfx_name}.wav")
        if os.path.exists(path):
            self.add_sound(path)

    def construct(self):
        # 1. Setup Static Grid & Header (Safe Zone Top: Y = 4.8)
        grid = TechGrid()
        grid.set_z_index(0)
        badge = AuthorBadge(pos=np.array([0.0, -4.15, 0]))
        self.add(grid, badge)

        title = Text("K-MEANS CLUSTERING", font="Segoe UI", font_size=34, weight=BOLD, color=COLOR_TEXT)
        title.move_to(np.array([0.0, 4.8, 0]))
        title.set_z_index(10)
        
        subtitle = Text("Grouping Data Points into K Clusters", font="Verdana", font_size=14, color=COLOR_C1)
        subtitle.next_to(title, DOWN, buff=0.15)
        subtitle.set_z_index(10)

        self.play_sfx("click")
        self.play(
            FadeIn(title, shift=DOWN * 0.2),
            FadeIn(subtitle, shift=DOWN * 0.1),
            run_time=0.9
        )

        # 2. Axes & Scatter Plot Setup (5.2 x 5.2 canvas centered at Y = 0.85)
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

        self.play(
            Create(axes),
            FadeIn(axis_numbers),
            Write(x_label),
            Write(y_label),
            FadeIn(status_card, shift=UP * 0.1),
            run_time=1.2
        )

        # 3. Data Points Setup (~24 points in 3 natural clusters)
        np.random.seed(42)
        cluster1_pts = np.random.normal(loc=[2.5, 7.2], scale=0.65, size=(8, 2))
        cluster2_pts = np.random.normal(loc=[7.5, 6.8], scale=0.70, size=(8, 2))
        cluster3_pts = np.random.normal(loc=[4.8, 2.5], scale=0.65, size=(8, 2))

        all_coords = np.vstack([cluster1_pts, cluster2_pts, cluster3_pts])

        point_mobs = VGroup()
        for x_val, y_val in all_coords:
            pt = axes.c2p(x_val, y_val)
            dot = Dot(point=pt, radius=0.09, color=COLOR_INIT)
            glow = Dot(point=pt, radius=0.16, color=COLOR_INIT, fill_opacity=0.25)
            pt_g = VGroup(glow, dot)
            pt_g.set_z_index(3)
            point_mobs.add(pt_g)

        self.play_sfx("click")
        self.play(
            LaggedStart(*[FadeIn(p, scale=0.5) for p in point_mobs], lag_ratio=0.04),
            run_time=1.0
        )

        self.wait(0.4)

        # 4. Initialize 3 Centroids (C1, C2, C3)
        init_c_coords = np.array([
            [1.5, 4.0],   # C1 initial (Blue)
            [8.2, 3.5],   # C2 initial (Violet)
            [5.5, 8.5]    # C3 initial (Coral Amber)
        ])

        colors = [COLOR_C1, COLOR_C2, COLOR_C3]
        labels = ["C1", "C2", "C3"]

        centroids = VGroup()
        centroid_mobs = []

        for i, coord in enumerate(init_c_coords):
            pt = axes.c2p(coord[0], coord[1])
            c_bg = Dot(point=pt, radius=0.22, color=colors[i], fill_opacity=0.35)
            c_ring = Circle(radius=0.18, color=colors[i], stroke_width=2.5).move_to(pt)
            c_dot = Dot(point=pt, radius=0.10, color=colors[i])
            lbl = Text(labels[i], font="Consolas", font_size=10, weight=BOLD, color=colors[i]).next_to(c_ring, UP, buff=0.06)
            c_group = VGroup(c_bg, c_ring, c_dot, lbl)
            c_group.set_z_index(6)
            centroid_mobs.append(c_group)
            centroids.add(c_group)

        self.play_sfx("click")
        status_card.update_status("Initialize K=3", 0, COLOR_C1)
        self.play(
            LaggedStart(*[SpinInFromNothing(c) for c in centroids], lag_ratio=0.15),
            run_time=1.0
        )

        self.wait(0.5)

        # Helper function for assignment
        def get_assignments(c_positions):
            assignments = []
            for pt_coord in all_coords:
                dists = [np.linalg.norm(pt_coord - c_pos) for c_pos in c_positions]
                nearest = np.argmin(dists)
                assignments.append(nearest)
            return assignments

        # ====================================================
        # ITERATION 1: ASSIGN & UPDATE
        # ====================================================
        status_card.update_status("Assigning Points", 1, COLOR_C1)
        self.play_sfx("compare")

        current_c_coords = init_c_coords.copy()
        assignments_1 = get_assignments(current_c_coords)

        # Color points based on nearest centroid
        anim_group = []
        for idx, (p_mob, assign_idx) in enumerate(zip(point_mobs, assignments_1)):
            target_color = colors[assign_idx]
            glow_mob, dot_mob = p_mob[0], p_mob[1]
            anim_group.append(glow_mob.animate.set_color(target_color))
            anim_group.append(dot_mob.animate.set_color(target_color))

        self.play(
            AnimationGroup(*anim_group, run_time=1.2)
        )
        self.wait(0.4)

        # Update Centroids Step 1
        status_card.update_status("Updating Means", 1, COLOR_C2)
        self.play_sfx("swap")

        new_c_coords_1 = np.zeros_like(current_c_coords)
        for k in range(3):
            k_pts = all_coords[np.array(assignments_1) == k]
            if len(k_pts) > 0:
                new_c_coords_1[k] = np.mean(k_pts, axis=0)

        move_c_anims = []
        for k in range(3):
            target_pt = axes.c2p(new_c_coords_1[k][0], new_c_coords_1[k][1])
            move_c_anims.append(centroid_mobs[k].animate.move_to(target_pt))

        self.play(
            AnimationGroup(*move_c_anims, run_time=1.4, rate_func=smooth)
        )
        self.wait(0.5)

        # ====================================================
        # ITERATION 2: RE-ASSIGN & CONVERGE
        # ====================================================
        status_card.update_status("Re-Assigning Points", 2, COLOR_C3)
        self.play_sfx("compare")

        current_c_coords = new_c_coords_1.copy()
        assignments_2 = get_assignments(current_c_coords)

        anim_group_2 = []
        for idx, (p_mob, assign_idx) in enumerate(zip(point_mobs, assignments_2)):
            target_color = colors[assign_idx]
            glow_mob, dot_mob = p_mob[0], p_mob[1]
            anim_group_2.append(glow_mob.animate.set_color(target_color))
            anim_group_2.append(dot_mob.animate.set_color(target_color))

        self.play(
            AnimationGroup(*anim_group_2, run_time=1.2)
        )
        self.wait(0.4)

        # Update Centroids Step 2
        status_card.update_status("Final Means", 2, COLOR_C3)
        self.play_sfx("swap")

        new_c_coords_2 = np.zeros_like(current_c_coords)
        for k in range(3):
            k_pts = all_coords[np.array(assignments_2) == k]
            if len(k_pts) > 0:
                new_c_coords_2[k] = np.mean(k_pts, axis=0)

        move_c_anims_2 = []
        for k in range(3):
            target_pt = axes.c2p(new_c_coords_2[k][0], new_c_coords_2[k][1])
            move_c_anims_2.append(centroid_mobs[k].animate.move_to(target_pt))

        self.play(
            AnimationGroup(*move_c_anims_2, run_time=1.4, rate_func=smooth)
        )
        self.wait(0.5)

        # Final Convergence Status
        self.play_sfx("success")
        status_card.update_status("Converged!", 2, COLOR_SUCCESS)
        
        self.play(
            *[
                c[0].animate.set_color(COLOR_SUCCESS).set_opacity(0.5)
                for c in centroid_mobs
            ],
            run_time=0.8
        )

        self.wait(3.0)
