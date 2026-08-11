from manim import *
import numpy as np

# ====================================================
# CONSTANTS & CONFIGURATION
# ====================================================
COLOR_BG = "#09090B"
COLOR_PRIMARY = "#3B82F6"        # Blue - Key / Input
COLOR_HASH = "#8B5CF6"           # Purple - Hash Function
COLOR_BUCKET = "#6B7280"         # Gray - Default Bucket
COLOR_ACTIVE_BUCKET = "#F59E0B"  # Amber - Active Bucket
COLOR_COLLISION = "#FB923C"      # Orange - Collision
COLOR_SUCCESS = "#22C55E"        # Green - Success / Found
COLOR_TEXT = "#F3F4F6"
COLOR_MUTED = "#64748B"
COLOR_LINE = "#1E293B"

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9.0
config.frame_height = 16.0
config.frame_rate = 30
config.background_color = COLOR_BG

# ====================================================
# PROCEDURAL UI COMPONENTS (OOP ARCHITECTURE)
# ====================================================

class BackgroundGrid(VGroup):
    """Subtle technical grid background."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        dots = VGroup()
        for x in np.arange(-4.0, 4.5, 0.8):
            for y in np.arange(-7.5, 8.0, 0.8):
                dot = Dot(point=[x, y, 0], radius=0.025, color=COLOR_LINE)
                dot.set_opacity(0.35)
                dots.add(dot)
        self.add(dots)

class GlowEffect(VGroup):
    """Procedural multi-layer glow effect around target mobjects."""
    def __init__(self, target_mobject: Mobject, color=COLOR_PRIMARY, num_layers=3, opacity=0.15):
        super().__init__()
        for i in range(1, num_layers + 1):
            glow = target_mobject.copy()
            glow.set_stroke(color=color, width=3 + i * 3, opacity=opacity / i)
            glow.set_fill(opacity=0)
            self.add(glow)

class KeyInputBox(VGroup):
    """Left UI container for incoming Key-Value input."""
    def __init__(self, pos=np.array([-2.7, 4.5, 0])):
        super().__init__()
        self.pos = pos
        self.box = RoundedRectangle(
            corner_radius=0.18,
            width=2.5,
            height=1.4,
            color=COLOR_PRIMARY,
            stroke_width=2,
            fill_color="#0F172A",
            fill_opacity=0.9
        ).move_to(pos)
        
        self.title = Text("KEY INPUT", font_size=13, color=COLOR_MUTED, weight=BOLD)
        self.title.move_to(pos + UP * 0.45)
        
        self.val_text = Text('key: ""', font_size=15, color=COLOR_TEXT, weight=BOLD)
        self.val_text.move_to(pos + DOWN * 0.1)
        
        self.add(self.box, self.title, self.val_text)

    def set_key_anim(self, key_str: str, val_str: str):
        new_text = Text(f'"{key_str}": {val_str}', font_size=15, color=COLOR_PRIMARY, weight=BOLD)
        new_text.move_to(self.pos + DOWN * 0.1)
        return Transform(self.val_text, new_text)

class HashNode(VGroup):
    """Center UI container for the Hash() function."""
    def __init__(self, pos=np.array([-0.2, 4.5, 0])):
        super().__init__()
        self.pos = pos
        self.box = RoundedRectangle(
            corner_radius=0.18,
            width=1.9,
            height=1.4,
            color=COLOR_HASH,
            stroke_width=2,
            fill_color="#1E1B4B",
            fill_opacity=0.9
        ).move_to(pos)
        
        self.title = Text("Hash()", font_size=16, color=COLOR_HASH, weight=BOLD)
        self.title.move_to(pos + UP * 0.35)
        
        self.formula = Text("h(k) % 6", font_size=13, color=COLOR_TEXT)
        self.formula.move_to(pos + DOWN * 0.15)
        
        self.add(self.box, self.title, self.formula)

    def spin_anim(self):
        return AnimationGroup(
            Rotate(self.box, angle=2*PI, run_time=0.8, rate_func=smooth),
            Indicate(self.title, color=COLOR_HASH, scale_factor=1.2, run_time=0.8)
        )

class Bucket(VGroup):
    """Individual array bucket slot."""
    def __init__(self, index: int, pos: np.ndarray):
        super().__init__()
        self.index = index
        self.pos = pos
        self.box = RoundedRectangle(
            corner_radius=0.12,
            width=1.3,
            height=0.9,
            color=COLOR_BUCKET,
            stroke_width=2,
            fill_color="#111827",
            fill_opacity=0.85
        ).move_to(pos)
        
        self.idx_label = Text(f"[{index}]", font_size=14, color=COLOR_MUTED, weight=BOLD)
        self.idx_label.move_to(pos + LEFT * 0.35)
        
        self.add(self.box, self.idx_label)

    def activate_anim(self, color=COLOR_ACTIVE_BUCKET):
        return AnimationGroup(
            self.box.animate.set_stroke(color=color, width=3).set_fill(color="#1F2937", opacity=0.95),
            self.idx_label.animate.set_color(color)
        )

    def reset_anim(self):
        return AnimationGroup(
            self.box.animate.set_stroke(color=COLOR_BUCKET, width=2).set_fill(color="#111827", opacity=0.85),
            self.idx_label.animate.set_color(COLOR_MUTED)
        )

class BucketArray(VGroup):
    """Vertical array of buckets (0 to 5)."""
    def __init__(self, count=6, start_pos=np.array([0.2, 4.2, 0]), spacing=1.15):
        super().__init__()
        self.buckets = []
        for i in range(count):
            p = start_pos + DOWN * (i * spacing)
            b = Bucket(i, p)
            self.buckets.append(b)
            self.add(b)

class Packet(VGroup):
    """Data packet representing a key:value payload in motion."""
    def __init__(self, key: str, val: str, color=COLOR_PRIMARY):
        super().__init__()
        self.key = key
        self.val = val
        self.bg = RoundedRectangle(
            corner_radius=0.14,
            width=1.5,
            height=0.65,
            color=color,
            stroke_width=2,
            fill_color="#090D16",
            fill_opacity=0.95
        )
        self.label = Text(f"{key}:{val}", font_size=13, color=COLOR_TEXT, weight=BOLD)
        self.label.move_to(self.bg.get_center())
        self.add(self.bg, self.label)

class ChainNode(VGroup):
    """Node element in a linked-list collision chain."""
    def __init__(self, key: str, val: str, pos: np.ndarray, color=COLOR_PRIMARY):
        super().__init__()
        self.key = key
        self.val = val
        self.pos = pos
        self.box = RoundedRectangle(
            corner_radius=0.12,
            width=1.3,
            height=0.65,
            color=color,
            stroke_width=2,
            fill_color="#1E293B",
            fill_opacity=0.95
        ).move_to(pos)
        self.label = Text(f"{key}:{val}", font_size=12, color=COLOR_TEXT, weight=BOLD)
        self.label.move_to(pos)
        self.add(self.box, self.label)

class CollisionChain(VGroup):
    """LinkedList collision chain anchored at Bucket [3]."""
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.arrows = []

    def add_node_anim(self, key: str, val: str, pos: np.ndarray, color=COLOR_PRIMARY):
        new_node = ChainNode(key, val, pos, color=color)
        anims = []
        if len(self.nodes) > 0:
            prev_node = self.nodes[-1]
            arrow = Arrow(
                start=prev_node.box.get_right() + RIGHT * 0.05,
                end=new_node.box.get_left() + LEFT * 0.05,
                buff=0.02,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.25,
                color=COLOR_COLLISION
            )
            self.arrows.append(arrow)
            self.add(arrow)
            anims.append(Create(arrow, rate_func=smooth))
        
        self.nodes.append(new_node)
        self.add(new_node)
        anims.append(FadeIn(new_node, shift=RIGHT * 0.2, rate_func=smooth))
        return AnimationGroup(*anims)

class LookupResultPanel(VGroup):
    """Bottom UI panel for displaying lookup queries and return values."""
    def __init__(self, pos=np.array([0.0, -5.8, 0])):
        super().__init__()
        self.pos = pos
        self.box = RoundedRectangle(
            corner_radius=0.18,
            width=7.2,
            height=1.5,
            color=COLOR_LINE,
            stroke_width=2,
            fill_color="#0F172A",
            fill_opacity=0.95
        ).move_to(pos)
        
        self.title = Text("LOOKUP RESULT", font_size=13, color=COLOR_MUTED, weight=BOLD)
        self.title.move_to(pos + UP * 0.45 + LEFT * 2.2)
        
        self.status = Text("Status: Ready", font_size=15, color=COLOR_TEXT)
        self.status.move_to(pos + DOWN * 0.15)
        
        self.add(self.box, self.title, self.status)

    def set_status_anim(self, text_str: str, color=COLOR_TEXT):
        new_status = Text(text_str, font_size=15, color=color, weight=BOLD)
        new_status.move_to(self.pos + DOWN * 0.15)
        return Transform(self.status, new_status)

# ====================================================
# MOTION UTILITIES
# ====================================================

class MotionUtils:
    """Helper procedures for bezier curves and glow pulses."""
    @staticmethod
    def create_bezier_path(start: np.ndarray, end: np.ndarray, via: np.ndarray):
        return CubicBezier(start, via, via, end)

# ====================================================
# MAIN SINGLE-SCENE ANIMATION
# ====================================================

class HashMapScene(Scene):
    """Complete single-scene procedural animation explaining Hash Map."""
    def construct(self):
        # ----------------------------------------------------
        # SETUP & INITIALIZATION
        # ----------------------------------------------------
        grid = BackgroundGrid()
        self.add(grid)

        # Header Title
        title_header = Text("HASH MAP ARCHITECTURE", font_size=20, color=COLOR_TEXT, weight=BOLD)
        title_header.move_to(np.array([0.0, 7.0, 0]))
        title_sub = Text("Single-Scene Execution Model", font_size=12, color=COLOR_MUTED)
        title_sub.move_to(np.array([0.0, 6.6, 0]))
        self.add(title_header, title_sub)

        # Main Static UI Layout Components
        key_input = KeyInputBox(pos=np.array([-2.8, 4.5, 0]))
        hash_node = HashNode(pos=np.array([-0.3, 4.5, 0]))
        bucket_array = BucketArray(count=6, start_pos=np.array([1.8, 4.5, 0]), spacing=1.15)
        lookup_panel = LookupResultPanel(pos=np.array([0.0, -5.8, 0]))

        # Static Connection Lines
        line1 = Line(key_input.box.get_right(), hash_node.box.get_left(), color=COLOR_LINE, stroke_width=2)
        line2 = Line(hash_node.box.get_right(), bucket_array.buckets[0].box.get_left(), color=COLOR_LINE, stroke_width=2)

        # Linked List Collision Chain instance anchored at Bucket 3
        bucket3_pos = bucket_array.buckets[3].pos
        collision_chain = CollisionChain()

        # ====================================================
        # BEAT 1: System Initialization
        # ====================================================
        self.play(
            FadeIn(key_input, shift=DOWN * 0.2),
            FadeIn(hash_node, shift=DOWN * 0.2),
            FadeIn(bucket_array, shift=LEFT * 0.2),
            FadeIn(lookup_panel, shift=UP * 0.2),
            Create(line1),
            Create(line2),
            run_time=1.5,
            rate_func=smooth
        )
        self.wait(0.5)

        # ====================================================
        # BEAT 2: Insert Alice ("Alice": 25 -> Bucket 3)
        # ====================================================
        self.play(key_input.set_key_anim("Alice", "25"), run_time=0.6)
        
        # Create Packet Alice
        packet_alice = Packet("Alice", "25", color=COLOR_PRIMARY)
        packet_alice.move_to(key_input.box.get_center())
        
        # Packet enters Hash Node
        self.play(
            packet_alice.animate.move_to(hash_node.box.get_center()),
            run_time=0.8,
            rate_func=smooth
        )
        
        # Hash Spins & computes hash("Alice") % 6 = 3
        hash_text = Text("h('Alice') -> 3", font_size=13, color=COLOR_HASH, weight=BOLD)
        hash_text.move_to(hash_node.pos + DOWN * 0.15)
        
        self.play(
            hash_node.spin_anim(),
            Transform(hash_node.formula, hash_text),
            run_time=0.8
        )
        
        # Packet moves along bezier curve to Bucket [3]
        b3_target = bucket_array.buckets[3].pos + RIGHT * 1.3
        path_alice = MotionUtils.create_bezier_path(
            hash_node.box.get_right(),
            b3_target,
            via=np.array([1.0, 2.5, 0])
        )
        
        self.play(
            MoveAlongPath(packet_alice, path_alice),
            bucket_array.buckets[3].activate_anim(COLOR_ACTIVE_BUCKET),
            run_time=1.0,
            rate_func=smooth
        )
        
        # Place Alice in Collision Chain
        self.play(
            FadeOut(packet_alice),
            collision_chain.add_node_anim("Alice", "25", b3_target, color=COLOR_PRIMARY),
            run_time=0.6
        )
        self.play(bucket_array.buckets[3].reset_anim(), run_time=0.4)
        self.wait(0.5)

        # ====================================================
        # BEAT 3: Insert Bob ("Bob": 30 -> Collision at Bucket 3)
        # ====================================================
        self.play(key_input.set_key_anim("Bob", "30"), run_time=0.5)
        
        packet_bob = Packet("Bob", "30", color=COLOR_COLLISION)
        packet_bob.move_to(key_input.box.get_center())
        
        self.play(
            packet_bob.animate.move_to(hash_node.box.get_center()),
            run_time=0.7,
            rate_func=smooth
        )
        
        hash_bob = Text("h('Bob') -> 3", font_size=13, color=COLOR_COLLISION, weight=BOLD)
        hash_bob.move_to(hash_node.pos + DOWN * 0.15)
        
        self.play(
            hash_node.spin_anim(),
            Transform(hash_node.formula, hash_bob),
            run_time=0.8
        )
        
        b3_bob_target = b3_target + RIGHT * 1.5
        path_bob = MotionUtils.create_bezier_path(
            hash_node.box.get_right(),
            b3_bob_target,
            via=np.array([1.2, 2.0, 0])
        )
        
        self.play(
            MoveAlongPath(packet_bob, path_bob),
            bucket_array.buckets[3].activate_anim(COLOR_COLLISION),
            run_time=1.0,
            rate_func=smooth
        )
        
        # Collision detected -> Expand linked list (Alice -> Bob)
        self.play(
            FadeOut(packet_bob),
            collision_chain.add_node_anim("Bob", "30", b3_bob_target, color=COLOR_COLLISION),
            run_time=0.6
        )
        self.play(bucket_array.buckets[3].reset_anim(), run_time=0.4)
        self.wait(0.5)

        # ====================================================
        # BEAT 4: Insert Charlie ("Charlie": 42 -> Chain Grows)
        # ====================================================
        self.play(key_input.set_key_anim("Charlie", "42"), run_time=0.5)
        
        packet_charlie = Packet("Charlie", "42", color=COLOR_COLLISION)
        packet_charlie.move_to(key_input.box.get_center())
        
        self.play(
            packet_charlie.animate.move_to(hash_node.box.get_center()),
            run_time=0.7,
            rate_func=smooth
        )
        
        hash_charlie = Text("h('Charlie') -> 3", font_size=13, color=COLOR_COLLISION, weight=BOLD)
        hash_charlie.move_to(hash_node.pos + DOWN * 0.15)
        
        self.play(
            hash_node.spin_anim(),
            Transform(hash_node.formula, hash_charlie),
            run_time=0.8
        )
        
        # Position Charlie below Bob or aligned to the right (x=4.3, y=-0.5) to stay safely in 9x16 frame
        b3_charlie_target = b3_bob_target + DOWN * 1.0
        path_charlie = MotionUtils.create_bezier_path(
            hash_node.box.get_right(),
            b3_charlie_target,
            via=np.array([1.5, 1.0, 0])
        )
        
        self.play(
            MoveAlongPath(packet_charlie, path_charlie),
            bucket_array.buckets[3].activate_anim(COLOR_COLLISION),
            run_time=1.0,
            rate_func=smooth
        )
        
        # Collision chain expands (Alice -> Bob -> Charlie)
        self.play(
            FadeOut(packet_charlie),
            collision_chain.add_node_anim("Charlie", "42", b3_charlie_target, color=COLOR_COLLISION),
            run_time=0.6
        )
        self.play(bucket_array.buckets[3].reset_anim(), run_time=0.4)
        self.wait(0.5)

        # ====================================================
        # BEAT 5: Lookup Charlie ("Charlie" -> Sequential Scan)
        # ====================================================
        self.play(
            lookup_panel.set_status_anim("Lookup('Charlie')...", color=COLOR_PRIMARY),
            key_input.set_key_anim("Get", "Charlie"),
            run_time=0.6
        )
        
        lookup_packet = Packet("Query", "Charlie", color=COLOR_PRIMARY)
        lookup_packet.move_to(key_input.box.get_center())
        
        self.play(
            lookup_packet.animate.move_to(hash_node.box.get_center()),
            run_time=0.7,
            rate_func=smooth
        )
        
        self.play(hash_node.spin_anim(), run_time=0.6)
        
        # Move query packet to Bucket [3]
        self.play(
            lookup_packet.animate.move_to(bucket_array.buckets[3].pos + RIGHT * 0.4),
            bucket_array.buckets[3].activate_anim(COLOR_ACTIVE_BUCKET),
            run_time=0.8,
            rate_func=smooth
        )
        
        # Sequential Scan: Check Alice -> Check Bob -> Match Charlie!
        alice_node = collision_chain.nodes[0]
        bob_node = collision_chain.nodes[1]
        charlie_node = collision_chain.nodes[2]
        
        # Scan Alice (Miss)
        self.play(
            lookup_packet.animate.move_to(alice_node.pos),
            Indicate(alice_node.box, color=COLOR_COLLISION, scale_factor=1.1),
            run_time=0.6
        )
        
        # Scan Bob (Miss)
        self.play(
            lookup_packet.animate.move_to(bob_node.pos),
            Indicate(bob_node.box, color=COLOR_COLLISION, scale_factor=1.1),
            run_time=0.6
        )
        
        # Scan Charlie (Match! Glow Green)
        self.play(
            lookup_packet.animate.move_to(charlie_node.pos),
            charlie_node.box.animate.set_stroke(color=COLOR_SUCCESS, width=4).set_fill(color="#064E3B"),
            charlie_node.label.animate.set_color(COLOR_SUCCESS),
            run_time=0.8
        )
        
        glow_charlie = GlowEffect(charlie_node.box, color=COLOR_SUCCESS)
        self.play(
            FadeIn(glow_charlie),
            lookup_panel.set_status_anim("Found! Charlie -> 42", color=COLOR_SUCCESS),
            FadeOut(lookup_packet),
            run_time=0.8
        )
        self.wait(0.5)

        # ====================================================
        # BEAT 6: Final State Highlight
        # ====================================================
        # Dim unrelated components, leaving Bucket 3, Charlie Node, and Lookup Panel highlighted
        dim_elements = Group(
            grid,
            key_input,
            hash_node,
            bucket_array.buckets[0],
            bucket_array.buckets[1],
            bucket_array.buckets[2],
            bucket_array.buckets[4],
            bucket_array.buckets[5],
            line1,
            line2,
            alice_node,
            bob_node,
            collision_chain.arrows[0],
            collision_chain.arrows[1]
        )
        
        self.play(
            dim_elements.animate.set_opacity(0.2),
            bucket_array.buckets[3].animate.set_opacity(1.0),
            charlie_node.animate.set_opacity(1.0),
            lookup_panel.animate.set_opacity(1.0),
            run_time=1.2,
            rate_func=smooth
        )
        self.wait(1.5)
