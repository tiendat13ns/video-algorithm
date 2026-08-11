from manim import *
import numpy as np
import os

# ====================================================
# FORMAT & WARM PAPER THEME CONFIGURATION
# Output: 1080x1920 (9:16 Vertical), 60fps, 8000 KBPS
# ====================================================
COLOR_BG = "#F4ECE1"               # Warm Cream Paper
COLOR_INK = "#1C1917"              # Dark Charcoal Ink Text
COLOR_MUTED = "#57534E"            # Warm Stone Charcoal (High Contrast)
COLOR_GRID = "#D6CBB8"             # Soft Parchment Grid Lines
COLOR_CONTAINER_BG = "#EFE6D8"     # Warm Paper Container Fill
COLOR_CONTAINER_BORDER = "#B8A995" # Warm Card Border
COLOR_QUERY = "#1D4ED8"            # Royal Ink Blue
COLOR_EMBED = "#5B21B6"            # Deep Violet
COLOR_SCAN = "#C2410C"             # Warm Amber / Rust
COLOR_MATCH = "#047857"            # Deep Emerald Green

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9.0
config.frame_height = 16.0
config.frame_rate = 60
config.bitrate = "8000k"
config.background_color = COLOR_BG

# ====================================================
# PROCEDURAL UI COMPONENTS (Fixed Kerning & Contrast)
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

class QueryInputBox(VGroup):
    """Top UI container for user query text with crisp typography."""
    def __init__(self, pos=np.array([0.0, 3.3, 0])):
        super().__init__()
        self.pos = pos
        self.box = RoundedRectangle(
            corner_radius=0.16,
            width=6.6,
            height=1.0,
            color=COLOR_CONTAINER_BORDER,
            stroke_width=2,
            fill_color=COLOR_CONTAINER_BG,
            fill_opacity=0.95
        ).move_to(pos)

        self.label = Text("SEARCH QUERY", font="Arial", font_size=11, color=COLOR_MUTED, weight=BOLD)
        self.label.move_to(pos + UP * 0.3)

        self.query_text = Text('"playful dog"', font="Arial", font_size=16, color=COLOR_QUERY, weight=BOLD)
        self.query_text.move_to(pos + DOWN * 0.12)

        self.add(self.box, self.label, self.query_text)

class EmbeddingNode(VGroup):
    """Middle UI container representing the Embedding Model with high contrast text."""
    def __init__(self, pos=np.array([0.0, 1.8, 0])):
        super().__init__()
        self.pos = pos
        self.box = RoundedRectangle(
            corner_radius=0.16,
            width=6.6,
            height=1.05,
            color=COLOR_EMBED,
            stroke_width=2,
            fill_color="#EDE9FE",
            fill_opacity=0.95
        ).move_to(pos)

        self.title = Text("EMBEDDING MODEL (Transformer)", font="Arial", font_size=11, color=COLOR_EMBED, weight=BOLD)
        self.title.move_to(pos + UP * 0.3)

        self.vector_text = Text("Dense Vector: [0.82, 0.94]", font="Arial", font_size=14, color=COLOR_INK, weight=BOLD)
        self.vector_text.move_to(pos + DOWN * 0.12)

        self.add(self.box, self.title, self.vector_text)

    def spin_anim(self):
        return AnimationGroup(
            Rotate(self.box, angle=2*PI, run_time=0.8, rate_func=smooth),
            Indicate(self.title, color=COLOR_EMBED, scale_factor=1.1, run_time=0.8)
        )

class VectorSpace2D(VGroup):
    """2D Vector Coordinate System with collision-free layout."""
    def __init__(self, pos=np.array([0.0, -0.9, 0])):
        super().__init__()
        self.pos = pos
        self.box = RoundedRectangle(
            corner_radius=0.18,
            width=6.8,
            height=3.8,
            color=COLOR_CONTAINER_BORDER,
            stroke_width=2,
            fill_color="#FAF5EE",
            fill_opacity=0.95
        ).move_to(pos)

        self.title = Text("2D VECTOR EMBEDDING SPACE", font="Arial", font_size=11, color=COLOR_MUTED, weight=BOLD)
        self.title.move_to(pos + UP * 1.65)

        self.origin = pos + DOWN * 0.1
        self.axis_x = Arrow(self.origin + LEFT * 2.5, self.origin + RIGHT * 2.5, color=COLOR_GRID, stroke_width=1.5, buff=0, max_tip_length_to_length_ratio=0.08)
        self.axis_y = Arrow(self.origin + DOWN * 1.2, self.origin + UP * 1.3, color=COLOR_GRID, stroke_width=1.5, buff=0, max_tip_length_to_length_ratio=0.08)

        self.add(self.box, self.title, self.axis_x, self.axis_y)

class ResultPanel(VGroup):
    """Bottom UI panel displaying top vector similarity match."""
    def __init__(self, pos=np.array([0.0, -4.3, 0])):
        super().__init__()
        self.pos = pos
        self.box = RoundedRectangle(
            corner_radius=0.16,
            width=6.8,
            height=1.15,
            color=COLOR_CONTAINER_BORDER,
            stroke_width=2,
            fill_color=COLOR_CONTAINER_BG,
            fill_opacity=0.95
        ).move_to(pos)

        self.title = Text("VECTOR DATABASE MATCH", font="Arial", font_size=11, color=COLOR_MUTED, weight=BOLD)
        self.title.move_to(pos + UP * 0.3)

        self.status = Text("Status: Scanning Embeddings...", font="Arial", font_size=14, color=COLOR_INK, weight=BOLD)
        self.status.move_to(pos + DOWN * 0.12)

        self.add(self.box, self.title, self.status)

    def set_status_anim(self, text_str: str, color=COLOR_INK):
        new_status = Text(text_str, font="Arial", font_size=14, color=color, weight=BOLD).move_to(self.pos + DOWN * 0.12)
        return Transform(self.status, new_status)

# ====================================================
# MAIN SINGLE-SCENE ANIMATION
# ====================================================

class SemanticSearchScene(Scene):
    """Single-scene technical animation explaining Semantic Search with collision-free layout."""

    def play_sfx(self, sfx_name: str):
        path = os.path.join("sfx", f"{sfx_name}.wav")
        if os.path.exists(path):
            self.add_sound(path)

    def construct(self):
        # ----------------------------------------------------
        # 1. SETUP STATIC SYSTEM DIAGRAM
        # ----------------------------------------------------
        grid = BackgroundGrid()
        self.add(grid)

        # Header Title (Safe Zone: Y = 4.5)
        title_main = Text("SEMANTIC SEARCH", font="Arial", font_size=22, color=COLOR_INK, weight=BOLD).move_to(np.array([0.0, 4.5, 0]))
        title_sub = Text("Vector Embeddings & Cosine Similarity", font="Arial", font_size=12, color=COLOR_MUTED).move_to(np.array([0.0, 4.1, 0]))
        self.add(title_main, title_sub)

        # Static Components
        query_box = QueryInputBox(pos=np.array([0.0, 3.3, 0]))
        embed_node = EmbeddingNode(pos=np.array([0.0, 1.8, 0]))
        vector_space = VectorSpace2D(pos=np.array([0.0, -0.9, 0]))
        result_panel = ResultPanel(pos=np.array([0.0, -4.3, 0]))

        # Watermark Text placed centered below Result Panel
        watermark = Text("@tiendatbrn", font="Arial", font_size=15, weight=BOLD, color=COLOR_MUTED).move_to(np.array([0.0, -5.3, 0]))

        # Connection lines
        line1 = Line(query_box.box.get_bottom(), embed_node.box.get_top(), color=COLOR_GRID, stroke_width=2)
        line2 = Line(embed_node.box.get_bottom(), vector_space.box.get_top(), color=COLOR_GRID, stroke_width=2)

        origin_pt = vector_space.origin

        # Doc C: "quantum physics"
        doc_c_pt = origin_pt + LEFT * 2.0 + DOWN * 0.8
        doc_c_dot = Dot(doc_c_pt, radius=0.08, color=COLOR_MUTED)
        doc_c_label = Text("Doc C: 'quantum physics'", font="Arial", font_size=10, color=COLOR_MUTED).move_to(doc_c_pt + DOWN * 0.3 + LEFT * 0.2)
        doc_c_vec = Arrow(origin_pt, doc_c_pt, color=COLOR_MUTED, stroke_width=1.5, buff=0, max_tip_length_to_length_ratio=0.12)

        # Doc A: "cute kitten"
        doc_a_pt = origin_pt + LEFT * 1.8 + UP * 0.6
        doc_a_dot = Dot(doc_a_pt, radius=0.08, color=COLOR_MUTED)
        doc_a_label = Text("Doc A: 'cute kitten'", font="Arial", font_size=10, color=COLOR_MUTED).move_to(doc_a_pt + UP * 0.28 + LEFT * 0.2)
        doc_a_vec = Arrow(origin_pt, doc_a_pt, color=COLOR_MUTED, stroke_width=1.5, buff=0, max_tip_length_to_length_ratio=0.12)

        # Doc B: "playful canine"
        doc_b_pt = origin_pt + RIGHT * 2.1 + UP * 0.4
        doc_b_dot = Dot(doc_b_pt, radius=0.09, color=COLOR_QUERY)
        doc_b_label = Text("Doc B: 'playful canine'", font="Arial", font_size=11, color=COLOR_INK, weight=BOLD).move_to(doc_b_pt + DOWN * 0.35 + RIGHT * 0.1)
        doc_b_vec = Arrow(origin_pt, doc_b_pt, color=COLOR_QUERY, stroke_width=2, buff=0, max_tip_length_to_length_ratio=0.12)

        # Query Vector: "playful dog"
        query_vec_pt = origin_pt + RIGHT * 1.8 + UP * 0.95
        query_dot = Dot(query_vec_pt, radius=0.1, color=COLOR_SCAN)
        query_label = Text("Query: 'playful dog'", font="Arial", font_size=11, color=COLOR_SCAN, weight=BOLD).move_to(query_vec_pt + UP * 0.35 + LEFT * 0.2)
        query_arrow = Arrow(origin_pt, query_vec_pt, color=COLOR_SCAN, stroke_width=2.5, buff=0, max_tip_length_to_length_ratio=0.12)

        sim_arc = ArcBetweenPoints(
            origin_pt + RIGHT * 1.0 + UP * 0.52,
            origin_pt + RIGHT * 1.1 + UP * 0.21,
            radius=0.7,
            color=COLOR_MATCH,
            stroke_width=2.5
        )
        sim_label = Text("θ = 6° (94% Match)", font="Arial", font_size=11, color=COLOR_MATCH, weight=BOLD).move_to(doc_b_pt + UP * 0.35 + RIGHT * 0.2)

        # BEAT 1: Init
        self.play_sfx("click")
        self.play(
            FadeIn(query_box, shift=DOWN * 0.2),
            FadeIn(embed_node, shift=DOWN * 0.2),
            FadeIn(vector_space, shift=UP * 0.2),
            FadeIn(result_panel, shift=UP * 0.2),
            FadeIn(watermark),
            Create(line1),
            Create(line2),
            run_time=1.2,
            rate_func=smooth
        )
        self.wait(0.4)

        # BEAT 2: Text to Embedding Vector
        self.play_sfx("compare")
        self.play(
            embed_node.spin_anim(),
            result_panel.set_status_anim("Generating Text Embeddings...", color=COLOR_EMBED),
            run_time=0.9
        )
        self.wait(0.3)

        # BEAT 3: Plot Document Vectors
        self.play_sfx("click")
        self.play(
            Create(doc_a_vec), FadeIn(doc_a_dot), Write(doc_a_label),
            Create(doc_b_vec), FadeIn(doc_b_dot), Write(doc_b_label),
            Create(doc_c_vec), FadeIn(doc_c_dot), Write(doc_c_label),
            run_time=1.2,
            rate_func=smooth
        )
        self.wait(0.4)

        # Project Query Vector
        self.play_sfx("swap")
        self.play(
            Create(query_arrow),
            FadeIn(query_dot, scale=1.2),
            Write(query_label),
            result_panel.set_status_anim("Projecting Query into Vector Space...", color=COLOR_SCAN),
            run_time=1.0,
            rate_func=smooth
        )
        self.wait(0.4)

        # BEAT 4: Cosine Similarity Scan
        self.play_sfx("compare")
        self.play(
            result_panel.set_status_anim("Computing Cosine Similarity...", color=COLOR_SCAN),
            Indicate(doc_c_dot, color=COLOR_MUTED, scale_factor=1.2),
            run_time=0.6
        )

        self.play_sfx("compare")
        self.play(
            Indicate(doc_a_dot, color=COLOR_MUTED, scale_factor=1.2),
            run_time=0.6
        )

        # Nearest Neighbor Match
        self.play_sfx("success")
        self.play(
            Create(sim_arc),
            Write(sim_label),
            doc_b_dot.animate.set_color(COLOR_MATCH).scale(1.3),
            doc_b_label.animate.set_color(COLOR_MATCH),
            result_panel.set_status_anim("FOUND MATCH: 'playful canine' (94% Similarity)", color=COLOR_MATCH),
            run_time=1.0,
            rate_func=smooth
        )
        self.wait(0.5)

        # BEAT 5: Final State
        dim_elements = Group(doc_a_dot, doc_a_label, doc_a_vec, doc_c_dot, doc_c_label, doc_c_vec)
        self.play(
            dim_elements.animate.set_opacity(0.25),
            doc_b_dot.animate.set_opacity(1.0),
            query_dot.animate.set_opacity(1.0),
            run_time=1.0
        )
        self.wait(2.0)
