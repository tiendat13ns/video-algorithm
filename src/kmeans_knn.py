from manim import *
from collections import Counter
import numpy as np
import os

# ====================================================
# FORMAT & COLOR PALETTE
# Output: 1080x1920 (9:16 Vertical), 60fps, 8000 KBPS
# ====================================================
COLOR_BG          = "#F4ECE1"   # Warm Cream Paper
COLOR_INK         = "#1C1917"   # Dark Charcoal Ink
COLOR_MUTED       = "#57534E"   # Warm Stone Gray
COLOR_GRID        = "#D6CBB8"   # Soft Parchment Grid
COLOR_CARD_BG     = "#EFE6D8"   # Warm Container Fill
COLOR_CARD_BORDER = "#B8A995"   # Warm Card Border

COLOR_C1      = "#6B8FF1"   # Royal Blue  (Cluster 1 / Class 1)
COLOR_C2      = "#A374F3"   # Deep Violet (Cluster 2 / Class 2)
COLOR_C3      = "#F56E39"   # Coral Amber (Cluster 3 / Class 3)
COLOR_INIT    = "#78716C"   # Neutral Stone — Unassigned
COLOR_SUCCESS = "#0F8866"   # Emerald Green — Convergence / Done
COLOR_QUERY   = "#FDAF41"   # Warm Gold — KNN Query Points

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

class TechGrid(VGroup):
    """Subtle dot grid for warm paper aesthetic."""
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
    """Sleek author watermark badge."""
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
            fill_opacity=0.95,
        )
        self.handle_text.move_to(self.box.get_center())
        self.add(self.box, self.handle_text)
        self.move_to(pos)
        self.set_z_index(10)

class StatusCard(VGroup):
    """Compact status card — unified for both K-Means and KNN phases."""
    def __init__(self, pos=np.array([0.0, -3.10, 0])):
        super().__init__()
        self.box = RoundedRectangle(
            corner_radius=0.14,
            width=6.0,
            height=0.72,
            color=COLOR_CARD_BORDER,
            stroke_width=1.5,
            fill_color=COLOR_CARD_BG,
            fill_opacity=0.95,
        ).move_to(pos)
        self.title_label = Text(
            "ALGORITHM STATUS",
            font="Consolas", font_size=10, weight=BOLD, color=COLOR_MUTED,
        ).move_to(pos + UP * 0.16)
        self.value_text = Text(
            "K-Means: Initialize K=3",
            font="Consolas", font_size=13, weight=BOLD, color=COLOR_C1,
        ).move_to(pos + DOWN * 0.12)
        self.add(self.box, self.title_label, self.value_text)
        self.set_z_index(10)

    def update_status(self, text: str, color=COLOR_INK):
        new_text = Text(text, font="Consolas", font_size=13, weight=BOLD, color=color)
        new_text.move_to(self.value_text.get_center())
        self.value_text.become(new_text)

# ====================================================
# MAIN SCENE
# ====================================================

class KMeansKNN(Scene):
    def play_sfx(self, sfx_name: str):
        path = os.path.join("sfx", f"{sfx_name}.wav")
        if os.path.exists(path):
            self.add_sound(path)

    def construct(self):
        # --------------------------------------------------
        # 1. SETUP — Static objects
        # --------------------------------------------------
        grid = TechGrid()
        grid.set_z_index(0)
        self.add(grid)

        # Title starts as K-MEANS, morphs to K-NN after convergence
        title = Text(
            "K-MEANS CLUSTERING",
            font="Segoe UI", font_size=34, weight=BOLD, color=COLOR_INK,
        ).move_to(np.array([0.0, 4.8, 0]))
        title.set_z_index(10)

        subtitle = Text(
            "Unsupervised Grouping (K=3 Clusters)",
            font="Verdana", font_size=13, color=COLOR_MUTED,
        ).next_to(title, DOWN, buff=0.15)
        subtitle.set_z_index(10)

        author_badge = AuthorBadge(pos=np.array([0.0, -4.15, 0]))
        status_card  = StatusCard(pos=np.array([0.0, -3.10, 0]))

        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=5.2,
            y_length=5.2,
            axis_config={"color": COLOR_MUTED, "stroke_width": 1.5, "include_numbers": False},
            tips=False,
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

        x_label = Text(
            "Feature 1 (X)", font="Verdana", font_size=13, color=COLOR_MUTED, weight=BOLD,
        ).next_to(axis_numbers, DOWN, buff=0.15).set_z_index(1)
        y_label = Text(
            "Feature 2 (Y)", font="Verdana", font_size=13, color=COLOR_MUTED, weight=BOLD,
        ).next_to(axes.y_axis, LEFT, buff=0.55).rotate(90 * DEGREES).set_z_index(1)

        # Shared dataset — same seed as kmeans_clustering.py
        np.random.seed(42)
        cluster1_pts = np.random.normal(loc=[2.5, 7.2], scale=0.65, size=(8, 2))
        cluster2_pts = np.random.normal(loc=[7.5, 6.8], scale=0.70, size=(8, 2))
        cluster3_pts = np.random.normal(loc=[4.8, 2.5], scale=0.65, size=(8, 2))
        all_coords   = np.vstack([cluster1_pts, cluster2_pts, cluster3_pts])

        point_mobs = VGroup()
        for x_val, y_val in all_coords:
            pt   = axes.c2p(x_val, y_val)
            glow = Dot(point=pt, radius=0.16, color=COLOR_INIT, fill_opacity=0.25)
            dot  = Dot(point=pt, radius=0.09, color=COLOR_INIT)
            pg   = VGroup(glow, dot).set_z_index(3)
            point_mobs.add(pg)

        # --------------------------------------------------
        # 2. INTRO — All elements simultaneously (Combine not Sequence)
        # --------------------------------------------------
        self.play_sfx("click")
        self.play(
            Write(title),
            FadeIn(subtitle, shift=DOWN * 0.1),
            FadeIn(author_badge, shift=UP * 0.1),
            Create(axes),
            FadeIn(axis_numbers),
            Write(x_label),
            Write(y_label),
            FadeIn(status_card, shift=UP * 0.1),
            run_time=1.0,
        )
        # All 24 data points at once — no lag
        self.play(*[FadeIn(p, scale=0.5) for p in point_mobs], run_time=0.7)

        # --------------------------------------------------
        # 3. ACT 1 — K-MEANS CLUSTERING
        # --------------------------------------------------
        colors   = [COLOR_C1, COLOR_C2, COLOR_C3]
        c_labels = ["C1", "C2", "C3"]

        # Initial centroid positions (far from true cluster centers)
        init_c_coords = np.array([
            [1.5, 4.0],  # C1 start — Blue
            [8.2, 3.5],  # C2 start — Violet
            [5.5, 8.5],  # C3 start — Coral
        ])

        centroid_mobs = []
        centroids     = VGroup()
        for i, coord in enumerate(init_c_coords):
            pt     = axes.c2p(coord[0], coord[1])
            c_bg   = Dot(point=pt, radius=0.22, color=colors[i], fill_opacity=0.35)
            c_ring = Circle(radius=0.18, color=colors[i], stroke_width=2.5).move_to(pt)
            c_dot  = Dot(point=pt, radius=0.10, color=colors[i])
            lbl    = Text(c_labels[i], font="Consolas", font_size=10, weight=BOLD, color=colors[i]).next_to(c_ring, UP, buff=0.06)
            c_grp  = VGroup(c_bg, c_ring, c_dot, lbl).set_z_index(6)
            centroid_mobs.append(c_grp)
            centroids.add(c_grp)

        def get_assignments(c_positions):
            return [int(np.argmin([np.linalg.norm(pt - cp) for cp in c_positions]))
                    for pt in all_coords]

        def compute_new_centroids(assignments):
            new_c = np.zeros((3, 2))
            for k in range(3):
                k_pts = all_coords[np.array(assignments) == k]
                if len(k_pts) > 0:
                    new_c[k] = np.mean(k_pts, axis=0)
            return new_c

        # --- Initialize centroids ---
        status_card.update_status("K-Means: Initialize K=3", COLOR_C1)
        self.play_sfx("click")
        self.play(
            LaggedStart(*[SpinInFromNothing(c) for c in centroids], lag_ratio=0.15),
            run_time=0.9,
        )

        # --- Iter 1: Assign points ---
        assignments_1 = get_assignments(init_c_coords)
        status_card.update_status("Iter 1: Assigning Points", COLOR_C1)
        self.play_sfx("compare")
        self.play(
            AnimationGroup(*[
                anim
                for p_mob, ai in zip(point_mobs, assignments_1)
                for anim in [
                    p_mob[0].animate.set_color(colors[ai]),
                    p_mob[1].animate.set_color(colors[ai]),
                ]
            ]),
            run_time=1.0,
        )

        # --- Iter 1: Move centroids ---
        new_c1 = compute_new_centroids(assignments_1)
        status_card.update_status("Iter 1: Updating Means", COLOR_C2)
        self.play_sfx("swap")
        self.play(
            AnimationGroup(*[
                centroid_mobs[k].animate.move_to(axes.c2p(new_c1[k][0], new_c1[k][1]))
                for k in range(3)
            ], rate_func=smooth),
            run_time=1.1,
        )

        # --- Iter 2: Re-assign points ---
        assignments_2 = get_assignments(new_c1)
        status_card.update_status("Iter 2: Re-Assigning Points", COLOR_C3)
        self.play_sfx("compare")
        self.play(
            AnimationGroup(*[
                anim
                for p_mob, ai in zip(point_mobs, assignments_2)
                for anim in [
                    p_mob[0].animate.set_color(colors[ai]),
                    p_mob[1].animate.set_color(colors[ai]),
                ]
            ]),
            run_time=1.0,
        )

        # --- Iter 2: Move centroids to final means ---
        new_c2 = compute_new_centroids(assignments_2)
        status_card.update_status("Iter 2: Final Means", COLOR_C2)
        self.play_sfx("swap")
        self.play(
            AnimationGroup(*[
                centroid_mobs[k].animate.move_to(axes.c2p(new_c2[k][0], new_c2[k][1]))
                for k in range(3)
            ], rate_func=smooth),
            run_time=1.1,
        )

        # --- Converged ---
        self.play_sfx("success")
        status_card.update_status("Converged! Clusters = Training Data", COLOR_SUCCESS)
        self.play(
            *[c[0].animate.set_color(COLOR_SUCCESS).set_opacity(0.5) for c in centroid_mobs],
            run_time=0.5,
        )

        # --------------------------------------------------
        # 4. TRANSITION — Title morph + centroids fade (1 play)
        # --------------------------------------------------
        title_knn = Text(
            "K-NEAREST NEIGHBORS",
            font="Segoe UI", font_size=34, weight=BOLD, color=COLOR_INK,
        ).move_to(title.get_center()).set_z_index(10)

        subtitle_knn = Text(
            "Classification K=3 | Trained on Clusters",
            font="Verdana", font_size=13, color=COLOR_MUTED,
        ).next_to(title_knn, DOWN, buff=0.15).set_z_index(10)

        status_card.update_status("K-NN K=3: Using Cluster Labels", COLOR_C1)
        self.play_sfx("click")
        self.play(
            ReplacementTransform(title, title_knn),
            FadeTransform(subtitle, subtitle_knn),
            FadeOut(centroids),
            run_time=0.7,
        )

        # --------------------------------------------------
        # 5. ACT 2 — KNN CLASSIFICATION
        # --------------------------------------------------
        # K-Means output → KNN training labels
        final_assignments = assignments_2
        all_colors_knn    = [colors[a] for a in final_assignments]
        class_names       = {0: "Blue", 1: "Violet", 2: "Coral"}

        def knn_query(q_coord, k=3):
            dists      = [np.linalg.norm(q_coord - pt) for pt in all_coords]
            sorted_idx = np.argsort(dists)[:k]
            votes      = [final_assignments[int(i)] for i in sorted_idx]
            winner     = int(Counter(votes).most_common(1)[0][0])
            radius     = float(dists[int(sorted_idx[k - 1])])
            return sorted_idx, winner, radius

        queries = [
            (np.array([5.5, 5.0]), "Q1"),   # Borderline — between clusters
            (np.array([2.5, 6.5]), "Q2"),   # Near C1 Blue
            (np.array([7.0, 7.0]), "Q3"),   # Near C2 Violet
        ]

        for q_coord, q_label in queries:
            q_pos = axes.c2p(q_coord[0], q_coord[1])

            # Query point widget (gold ring with "?")
            q_bg    = Dot(point=q_pos, radius=0.24, color=COLOR_QUERY, fill_opacity=0.35)
            q_ring  = Circle(radius=0.20, color=COLOR_QUERY, stroke_width=2.5).move_to(q_pos)
            q_dot   = Dot(point=q_pos, radius=0.11, color=COLOR_QUERY)
            q_qmark = Text("?", font="Consolas", font_size=12, weight=BOLD, color=COLOR_INK).move_to(q_pos)
            q_grp   = VGroup(q_bg, q_ring, q_dot, q_qmark).set_z_index(7)

            status_card.update_status(f"{q_label}: Finding K=3 Neighbors", COLOR_QUERY)
            self.play_sfx("compare")
            self.play(SpinInFromNothing(q_grp), run_time=0.5)

            # Compute KNN
            sorted_idx, winner_idx, radius = knn_query(q_coord)
            winner_color = colors[winner_idx]

            # KNN search radius circle
            p_far = axes.c2p(q_coord[0] + radius, q_coord[1])
            r_px  = float(np.linalg.norm(np.array(p_far) - np.array(q_pos)))
            knn_circle = Circle(
                radius=r_px, color=COLOR_QUERY, stroke_width=2.0, stroke_opacity=0.85,
            ).move_to(q_pos).set_z_index(2)

            # Dashed lines + highlight rings to K nearest neighbors
            lines = VGroup()
            glows = VGroup()
            for idx in sorted_idx:
                t_pos = axes.c2p(all_coords[int(idx)][0], all_coords[int(idx)][1])
                t_col = all_colors_knn[int(idx)]
                lines.add(DashedLine(q_pos, t_pos, color=t_col, stroke_width=2.0, dash_length=0.08).set_z_index(2))
                glows.add(Circle(radius=0.22, color=t_col, stroke_width=2.5).move_to(t_pos).set_z_index(4))

            # Circle + lines + glows — all at once
            self.play_sfx("compare")
            self.play(
                Create(knn_circle),
                Create(lines),
                LaggedStart(*[Create(g) for g in glows], lag_ratio=0.1),
                run_time=0.8,
            )

            # Classify: morph query point to winner color + fade circle + cleanup — combined
            cn = class_names[winner_idx]
            status_card.update_status(f"{q_label} → CLASS {cn}", winner_color)
            self.play_sfx("success")

            final_q = VGroup(
                Dot(point=q_pos, radius=0.18, color=winner_color, fill_opacity=0.35),
                Dot(point=q_pos, radius=0.10, color=winner_color),
            ).set_z_index(7)

            self.play(
                Transform(q_grp, final_q),
                knn_circle.animate.set_color(winner_color).set_opacity(0.3),
                run_time=0.55,
            )
            # Fade out helper visuals immediately
            self.play(FadeOut(lines), FadeOut(glows), FadeOut(knn_circle), run_time=0.25)

        # --------------------------------------------------
        # 6. FINAL
        # --------------------------------------------------
        self.play_sfx("success")
        status_card.update_status("K-Means + K-NN: Complete!", COLOR_SUCCESS)

        self.wait(3.0)
