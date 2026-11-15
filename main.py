import random
import numpy as np
import pygame as pg

pg.init()
wid, hig = 1000, 500
scr = pg.display.set_mode((wid, hig))
pg.display.set_caption('gem')
clk = pg.time.Clock()


def load_font(names, size, bold=False):
    avail = set(pg.font.get_fonts())
    for n in names:
        key = n.lower().replace(" ", "")
        if key in avail:
            return pg.font.SysFont(n, size, bold=bold)
    return pg.font.SysFont(None, size, bold=bold)


FONTS = {
    "default": (
        load_font(["consolas", "dejavusansmono", "monospace"], 16),
        load_font(["consolas", "dejavusansmono", "monospace"], 22),
        load_font(["consolas", "dejavusansmono", "monospace"], 38, bold=True),
    ),
    "glitch": (
        load_font(["fixedsys", "terminal", "couriernew", "lucidaconsole", "dejavusansmono"], 16, bold=True),
        load_font(["fixedsys", "terminal", "couriernew", "lucidaconsole", "dejavusansmono"], 22, bold=True),
        load_font(["fixedsys", "terminal", "couriernew", "lucidaconsole", "dejavusansmono"], 36, bold=True),
    ),
    "paper": (
        load_font(["georgia", "cambria", "timesnewroman", "dejavuserif", "consolas"], 16),
        load_font(["georgia", "cambria", "timesnewroman", "dejavuserif", "consolas"], 22),
        load_font(["georgia", "cambria", "timesnewroman", "dejavuserif", "consolas"], 36, bold=True),
    ),
}

THEMES = {
    "default": {
        "label": "COMET EXPRESS (DEFAULT)",
        "font_key": "default",
        "bg": (4, 6, 12),
        "grid": (80, 120, 175),
        "ship": (120, 255, 190),
        "trail": (120, 255, 190),
        "accent": (90, 255, 255),
        "accent2": (120, 255, 190),
        "warn": (255, 230, 120),
        "text": (180, 220, 255),
        "text_dim": (140, 160, 190),
        "panel_bg": (6, 10, 20, 220),
        "panel_text": (200, 225, 255),
        "menu_bg": (10, 16, 30),
        "btn_bg": (14, 22, 38),
        "btn_sel": (22, 45, 68),
        "btn_border": (55, 85, 115),
        "fog_explored": (10, 16, 30),
        "fog_unexplored": (46, 54, 72),
        "map_star": (255, 210, 80),
        "map_hole": (170, 90, 255),
        "hole_core": (170, 90, 255),
        "hole_ring1": (255, 170, 80),
        "hole_ring2": (255, 120, 80),
        "relay_beacon": (255, 255, 255),
        "star_prefix": "SOL",
        "hole_prefix": "BH",
        "star_word": "star",
        "planet_word": "planet",
        "spaghetti_msg": "SPAGHETTIFIED - respawned at last safe point (+15s)",
        "menu_title": "COMET EXPRESS",
        "menu_sub": "SELECT FLIGHT PROTOCOL",
        "intro": (
            "Welcome to COMET EXPRESS, courier! You have one ship, one crate, and 8 customers who have been "
            "waiting WAY too long. Find each one, land softly, and collect your thanks. "
            "Dark dips in the map are black holes - they eat packages AND couriers. [SPACE to close]"
        ),
        "free_intro": (
            "FREE ROAM MODE: A newly generated galaxy awaits! Explore uncharted systems, "
            "slingshot around gravity wells, and land on any planet you like. [SPACE to close]"
        ),
        "cargos": [
            "a lukewarm pizza", "123 rubber ducks", "one mystery crate", "a birthday cake",
            "a very grumpy cat", "a mountain of socks", "a tiny trophy", "the GOLDEN package"
        ],
        "fragments": [
            "Finally, pizza! I ordered this 40 years ago. I'm not even mad. Okay, a little.",
            "Rubber ducks?! I asked for rubber TIRES. ...Eh, keep them coming, they're adorable.",
            "The crate said DO NOT OPEN. I opened it. It was more socks. Great.",
            "A cake! It's my birthday! It was also my birthday last time you were late. Hmm.",
            "The cat knocked over my beacon, then sat on it. We've elected it mayor.",
            "SOCKS! The black holes keep eating mine. Please tell them to stop.",
            "A trophy for 'Best Courier'? I didn't order this... I think it's for you.",
            "Last delivery! The whole planet is cheering. You've earned this big shiny button.",
        ],
        "guild": [
            "DISPATCH: Nice landing! Next up: 123 rubber ducks. Don't ask.",
            "DISPATCH: Next is a mystery crate. Do NOT open it. (Everyone opens it.)",
            "DISPATCH: Birthday cake next. Keep it level, it's already a little crooked.",
            "DISPATCH: Halfway! Next: a grumpy cat. Slow landings only.",
            "DISPATCH: Mountain of socks next. Smells like victory. And feet.",
            "DISPATCH: Tiny trophy next. Careful, it's shinier than you.",
            "DISPATCH: Last one! The GOLDEN package. Don't dent it."
        ],
        "choice_title": "THE GOLDEN PACKAGE",
        "choice_txt": (
            "The last customer hands you a big, shiny red button. 'Your tip,' they say.\n\n"
            "[1] Press the button.\n[2] Don't press it. Keep it as a souvenir."
        ),
        "end_good_title": "SOCK-ASTROPHE",
        "end_good": (
            "BOOM! Confetti everywhere. Every black hole burps out all the socks it ever swallowed, and the fog "
            "blows away. Every customer gets their stuff, plus 40,000 extra socks.\n\n"
            "ENDING: SOCK-ASTROPHE   (free flight - [R] restarts)"
        ),
        "end_quiet_title": "EMPLOYEE OF THE MILLENNIUM",
        "end_quiet": (
            "You tuck the button safely in your glovebox. Somewhere, a black hole feels a strange tingle... "
            "but nothing happens. You cruise off as the greatest courier in the galaxy.\n\n"
            "ENDING: EMPLOYEE OF THE MILLENNIUM   (free flight - [R] restarts)"
        ),
    },
    "glitch": {
        "label": "404: PARCEL NOT FOUND",
        "font_key": "glitch",
        "bg": (0, 0, 0),
        "grid": (40, 220, 90),
        "ship": (90, 255, 130),
        "trail": (40, 220, 90),
        "accent": (70, 255, 120),
        "accent2": (180, 255, 190),
        "warn": (255, 60, 60),
        "text": (65, 235, 110),
        "text_dim": (35, 145, 65),
        "panel_bg": (0, 12, 4, 230),
        "panel_text": (90, 255, 130),
        "menu_bg": (0, 10, 4),
        "btn_bg": (4, 18, 8),
        "btn_sel": (12, 48, 22),
        "btn_border": (30, 130, 55),
        "fog_explored": (0, 12, 4),
        "fog_unexplored": (14, 48, 22),
        "map_star": (140, 255, 160),
        "map_hole": (255, 45, 45),
        "hole_core": (255, 40, 40),
        "hole_ring1": (255, 30, 30),
        "hole_ring2": (255, 95, 50),
        "relay_beacon": (255, 70, 70),
        "star_prefix": "SRV",
        "hole_prefix": "ERR",
        "star_word": "server",
        "planet_word": "node",
        "spaghetti_msg": "SEGMENTATION FAULT - PACKET DROPPED (+15s RETRANSMIT)",
        "menu_title": "404: PARCEL NOT FOUND",
        "menu_sub": "ROGUE PACKET ROUTING TERMINAL",
        "intro": (
            "BOOTING ROGUE_PACKET.EXE... You are a stray data-packet surfing a decaying motherboard. "
            "Route 8 lost files to their target Nodes without falling into red Corrupted Sectors. "
            "Watch for CRT signal interference near gravity wells. [SPACE to close]"
        ),
        "free_intro": (
            "SANDBOX KERNEL: Unindexed motherboard topology loaded. Ping any Server, "
            "orbit unstable Nodes, and stress-test sector boundaries. [SPACE to close]"
        ),
        "cargos": [
            "grandma_cookies.zip", "cat_video_final_FINAL.mp4", "DO_NOT_DELETE.dll",
            "birthday_wishes_1999.txt", "angry_meow_v2.wav", "missing_socks_db.sql",
            "sysadmin_trophy.iso", "ROOT_KEY_GOLD.bin"
        ],
        "fragments": [
            "CHECKSUM OK: grandma_cookies.zip unpacked! Zero crumbs lost in transit.",
            "NODE ACK: cat_video_final_FINAL.mp4 buffered at 60fps. Worth the lag.",
            "WARNING: You opened DO_NOT_DELETE.dll. It was just recursive sock pointers.",
            "SYNC COMPLETE: birthday_wishes_1999.txt arrived 27 years late. Clock skew noted.",
            "NODE LOG: angry_meow_v2.wav overwrote our firewall. The cat has sudo now.",
            "DB RESTORED: missing_socks_db.sql! Corrupted sectors keep eating our cache.",
            "HASH VERIFIED: sysadmin_trophy.iso... wait, this is addressed to your MAC address.",
            "FINAL PACKET DELIVERED! Root terminal unlocked. Execute override command.",
        ],
        "guild": [
            "KERNEL: Hop verified! Queuing cat_video_final_FINAL.mp4. High bandwidth.",
            "KERNEL: Next payload: DO_NOT_DELETE.dll. Keep headers intact.",
            "KERNEL: Routing birthday_wishes_1999.txt. Avoid red sector sinks.",
            "KERNEL: 50% synced. Next: angry_meow_v2.wav. Low-jitter docking required.",
            "KERNEL: Next packet: missing_socks_db.sql. Smells like legacy code.",
            "KERNEL: Routing sysadmin_trophy.iso. Watch your latency.",
            "KERNEL: Final payload: ROOT_KEY_GOLD.bin. Do not drop this packet."
        ],
        "choice_title": "ROOT OVERRIDE PROMPT",
        "choice_txt": (
            "The final Node exposes an unguarded root prompt: ./flush_corrupted_sectors.sh\n\n"
            "[1] Execute script (purge bad sectors).\n[2] Abort and stay stealth in RAM."
        ),
        "end_good_title": "KERNEL RESTORED",
        "end_good": (
            "0x00 SUCCESS! All corrupted sectors dump their swallowed cache, clearing the fog map. "
            "Every lost file and 40,000 orphaned sock.tmp files are restored.\n\n"
            "ENDING: SYSTEM RESTORED   (free flight - [R] reboots)"
        ),
        "end_quiet_title": "GHOST IN THE SILICON",
        "end_quiet": (
            "You close the shell and vanish into background memory. Somewhere on the board, a red "
            "sector flickers... then stabilizes. You remain the fastest packet on the bus.\n\n"
            "ENDING: GHOST IN THE SILICON   (free flight - [R] reboots)"
        ),
    },
    "blueprint": {
        "label": "PAPER PLANES (BLUEPRINT)",
        "font_key": "paper",
        "bg": (20, 55, 110),
        "grid": (220, 235, 255),
        "ship": (255, 255, 255),
        "trail": (200, 230, 255),
        "accent": (255, 240, 140),
        "accent2": (255, 255, 255),
        "warn": (255, 175, 110),
        "text": (225, 240, 255),
        "text_dim": (165, 195, 235),
        "panel_bg": (14, 40, 84, 230),
        "panel_text": (235, 245, 255),
        "menu_bg": (16, 46, 94),
        "btn_bg": (24, 62, 122),
        "btn_sel": (38, 86, 160),
        "btn_border": (150, 185, 235),
        "fog_explored": (24, 64, 124),
        "fog_unexplored": (14, 42, 86),
        "map_star": (255, 235, 130),
        "map_hole": (255, 140, 120),
        "hole_core": (255, 130, 110),
        "hole_ring1": (255, 220, 150),
        "hole_ring2": (220, 235, 255),
        "relay_beacon": (255, 240, 140),
        "star_prefix": "FIG",
        "hole_prefix": "WELL",
        "star_word": "datum",
        "planet_word": "node",
        "spaghetti_msg": "MODEL SINGULARITY - FOLDED BACK TO ORIGIN (+15s)",
        "menu_title": "PAPER PLANES IN DEEP SPACE",
        "menu_sub": "ARCHITECTURAL GRAVITY DRAFTING TABLE",
        "intro": (
            "SHEET 01-A: Theoretical orbital mechanics on folded vellum. Glide your origami craft "
            "across the gravity grid to deliver 8 annotated proofs. Mind the inked singularities—they "
            "crumple loose-leaf gliders. [SPACE to close]"
        ),
        "free_intro": (
            "OPEN DRAFTING SHEET: Unconstrained physics sandbox. Test orbital trajectories, "
            "measure gravity-well curvature, and touch down on any plotted body. [SPACE to close]"
        ),
        "cargos": [
            "a folded lunch-break note", "123 origami cranes", "a sealed blueprint tube",
            "a protractor & birthday card", "a doodle of a grumpy cat", "a sketch of missing socks",
            "a brass compass", "the GOLDEN theorem"
        ],
        "fragments": [
            "Note unfolded! 'Meet by the chalkboard after class.' Margin calculations check out.",
            "123 origami cranes! Our aerodynamist is thrilled—and slightly intimidated.",
            "Blueprint tube unrolled! Inside was another grid folded into a tiny sock.",
            "A protractor and a card! 'Happy Birthday—may your angles always be acute.'",
            "The cat doodle slid off the drafting table and claimed the inkwell.",
            "Aha! The inkwells were absorbing all our spare socks via capillary action!",
            "A brass compass for 'Master Navigator'? Looks like it belongs on your desk.",
            "Final proof delivered! The entire drafting room applauds. Take this red wax seal.",
        ],
        "guild": [
            "DESK NOTE: Clean glide! Next parcel: 123 origami cranes. Keep wings level.",
            "DESK NOTE: Next up: a sealed blueprint tube. Do not crease.",
            "DESK NOTE: Protractor & birthday card next. Mind the crosswinds.",
            "DESK NOTE: Halfway across the sheet! Next: a grumpy cat doodle.",
            "DESK NOTE: Sketch of missing socks next. Watch the gravity wells.",
            "DESK NOTE: Brass compass next. Delicate landing gear required.",
            "DESK NOTE: Final run! The GOLDEN theorem. Stick the landing."
        ],
        "choice_title": "THE GOLDEN THEOREM",
        "choice_txt": (
            "The lead architect slides a crimson stamp across the blueprint: 'Sign off the sheet?'\n\n"
            "[1] Stamp APPROVED (reveal full schematic).\n[2] Tuck the stamp away unsigned."
        ),
        "end_good_title": "SCHEMATIC COMPLETE",
        "end_good": (
            "STAMPED! Crisp white chalk lines snap across the entire drafting table, revealing every "
            "un-sketched margin and 40,000 neatly folded paper socks.\n\n"
            "ENDING: MASTER DRAFTSMAN   (free flight - [R] restarts)"
        ),
        "end_quiet_title": "UNFINISHED MARGINALIA",
        "end_quiet": (
            "You pocket the stamp and bank into a lazy figure-eight over the blueprint grid. "
            "Some theorems are better left open-ended.\n\n"
            "ENDING: QUIET ARCHITECT   (free flight - [R] restarts)"
        ),
    },
    "parchment": {
        "label": "PAPER PLANES (PARCHMENT)",
        "font_key": "paper",
        "bg": (240, 235, 220),
        "grid": (30, 35, 45),
        "ship": (20, 25, 35),
        "trail": (70, 80, 95),
        "accent": (185, 45, 35),
        "accent2": (25, 75, 130),
        "warn": (185, 45, 35),
        "text": (30, 35, 45),
        "text_dim": (95, 100, 110),
        "panel_bg": (232, 225, 206, 238),
        "panel_text": (30, 35, 45),
        "menu_bg": (234, 227, 208),
        "btn_bg": (224, 216, 196),
        "btn_sel": (206, 196, 174),
        "btn_border": (110, 115, 125),
        "fog_explored": (236, 230, 214),
        "fog_unexplored": (212, 204, 185),
        "map_star": (195, 110, 20),
        "map_hole": (185, 45, 35),
        "hole_core": (185, 45, 35),
        "hole_ring1": (120, 45, 40),
        "hole_ring2": (55, 60, 70),
        "relay_beacon": (185, 45, 35),
        "star_prefix": "FIG",
        "hole_prefix": "INK",
        "star_word": "datum",
        "planet_word": "node",
        "spaghetti_msg": "INK BLOTCH - REFOLDED AT LAST SAFE CREASE (+15s)",
        "menu_title": "PAPER PLANES IN DEEP SPACE",
        "menu_sub": "CLASSROOM NOTE-PASSING SIMULATOR",
        "intro": (
            "PERIOD 4 PHYSICS: Pass 8 folded notes across the graph-paper cosmos without letting "
            "the teacher's red-ink wells blot your glider. Keep your approach gentle so the paper "
            "doesn't crumple on touchdown. [SPACE to close]"
        ),
        "free_intro": (
            "STUDY HALL FREE FLIGHT: A fresh sheet of quad-ruled parchment. Practice gravity "
            "slingshots and land on any sketched world. [SPACE to close]"
        ),
        "cargos": [
            "a folded lunch-break note", "123 origami cranes", "a sealed blueprint tube",
            "a protractor & birthday card", "a doodle of a grumpy cat", "a sketch of missing socks",
            "a brass compass", "the GOLDEN theorem"
        ],
        "fragments": [
            "Note unfolded! 'Meet by the chalkboard after class.' Margin calculations check out.",
            "123 origami cranes! The back row is thrilled—and slightly intimidated.",
            "Blueprint tube unrolled! Inside was another grid folded into a tiny sock.",
            "A protractor and a card! 'Happy Birthday—may your angles always be acute.'",
            "The cat doodle slid off the notebook and claimed the eraser.",
            "Aha! The inkwells were absorbing all our spare socks via capillary action!",
            "A brass compass for 'Master Navigator'? Looks like it belongs on your desk.",
            "Final note delivered! The whole row cheers. Take this red wax seal.",
        ],
        "guild": [
            "MARGIN NOTE: Clean glide! Next parcel: 123 origami cranes. Keep wings level.",
            "MARGIN NOTE: Next up: a sealed blueprint tube. Do not crease.",
            "MARGIN NOTE: Protractor & birthday card next. Mind the drafts.",
            "MARGIN NOTE: Halfway across the page! Next: a grumpy cat doodle.",
            "MARGIN NOTE: Sketch of missing socks next. Watch the inkwells.",
            "MARGIN NOTE: Brass compass next. Delicate landing gear required.",
            "MARGIN NOTE: Final run! The GOLDEN theorem. Stick the landing."
        ],
        "choice_title": "THE GOLDEN THEOREM",
        "choice_txt": (
            "Your lab partner slides a red wax seal across the desk: 'Stamp the final proof?'\n\n"
            "[1] Press the seal (ink the whole page).\n[2] Keep the seal as a souvenir."
        ),
        "end_good_title": "A+ EXTRA CREDIT",
        "end_good": (
            "STAMPED! Crisp ink lines sketch across the entire sheet, revealing every un-drawn "
            "corner and 40,000 neatly folded paper socks.\n\n"
            "ENDING: A+ EXTRA CREDIT   (free flight - [R] restarts)"
        ),
        "end_quiet_title": "UNFINISHED MARGINALIA",
        "end_quiet": (
            "You pocket the seal and bank into a lazy figure-eight over the graph paper. "
            "Some notes are better left ungraded.\n\n"
            "ENDING: QUIET SCHOLAR   (free flight - [R] restarts)"
        ),
    },
}

THEME_ORDER = ["default", "glitch", "blueprint", "parchment"]
theme_idx = 0
theme_key = THEME_ORDER[theme_idx]
T = THEMES[theme_key]
font, big_font, title_font = FONTS[T["font_key"]]


def set_theme(new_key):
    global theme_key, theme_idx, T, font, big_font, title_font
    theme_key = new_key
    theme_idx = THEME_ORDER.index(new_key)
    T = THEMES[theme_key]
    font, big_font, title_font = FONTS[T["font_key"]]
    star_n = 0
    hole_n = 0
    cur_star_name = ""
    planet_sub = 0
    for b in bodies:
        if b["kind"] == "hole":
            hole_n += 1
            b["name"] = f"{T['hole_prefix']}-{hole_n}"
        elif b["kind"] == "star":
            star_n += 1
            planet_sub = 0
            cur_star_name = f"{T['star_prefix']}-{star_n}"
            b["name"] = cur_star_name
        elif b["kind"] == "planet":
            b["name"] = f"{cur_star_name}{'bcde'[planet_sub % 4]}"
            planet_sub += 1
    if mission and mission.get("target") is not None:
        cargos = T["cargos"]
        mission["cargo"] = cargos[min(mi, len(cargos) - 1)]


HALF = 1600.0
HOLE_RING = 1350.0
N_SYSTEMS = 8
N_HOLES = 6
GRID_STEP = 3.0
G = 45.0
HOVER_OFFSET = 1.0
MIN_DELIVERY_DIST = 900.0
DOCK_SPEED = 10.0


def make_sphere(radius=1.0, lat_divs=8, lon_divs=12):
    verts, edges = [], []
    for i in range(lat_divs + 1):
        lat = np.pi * (-0.5 + i / lat_divs)
        y = radius * np.sin(lat)
        r = radius * np.cos(lat)
        for j in range(lon_divs):
            lon = 2 * np.pi * j / lon_divs
            verts.append([r * np.cos(lon), y, r * np.sin(lon), 1.0])
    for i in range(lat_divs + 1):
        for j in range(lon_divs):
            curr = i * lon_divs + j
            nxt = i * lon_divs + (j + 1) % lon_divs
            edges.append([curr, nxt])
            if i < lat_divs:
                edges.append([curr, (i + 1) * lon_divs + j])
    return np.array(verts, dtype=float), np.array(edges, dtype=int)


def make_ship():
    verts = np.array([
        [0.00, 0.00, 0.55, 1.0],
        [-0.32, -0.05, -0.35, 1.0],
        [0.32, -0.05, -0.35, 1.0],
        [0.00, 0.14, -0.25, 1.0],
    ], dtype=float)
    edges = np.array([[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]], dtype=int)
    return verts, edges


def make_ring(n=72):
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    verts = np.stack([np.cos(a), np.zeros(n), np.sin(a), np.ones(n)], axis=1)
    edges = np.array([[i, (i + 1) % n] for i in range(n)], dtype=int)
    return verts, edges


def make_octa():
    verts = np.array([
        [1, 0, 0, 1], [-1, 0, 0, 1], [0, 1, 0, 1],
        [0, -1, 0, 1], [0, 0, 1, 1], [0, 0, -1, 1]
    ], dtype=float)
    edges = np.array([
        [0, 2], [0, 3], [0, 4], [0, 5], [1, 2], [1, 3],
        [1, 4], [1, 5], [2, 4], [2, 5], [3, 4], [3, 5]
    ], dtype=int)
    return verts, edges


def make_grid(size=48.0, step=GRID_STEP):
    coords = np.arange(-size, size + step / 2, step)
    verts, edges = [], []
    idx = 0
    for c in coords:
        for k in range(len(coords) - 1):
            verts.append([c, 0.0, coords[k], 1.0])
            verts.append([c, 0.0, coords[k + 1], 1.0])
            edges.append([idx, idx + 1])
            idx += 2
            verts.append([coords[k], 0.0, c, 1.0])
            verts.append([coords[k + 1], 0.0, c, 1.0])
            edges.append([idx, idx + 1])
            idx += 2
    return np.array(verts, dtype=float), np.array(edges, dtype=int)


base_grdvrts, grid_edjs = make_grid()
sphere_verts, sphere_edges = make_sphere(1.0, 8, 14)
ship_verts, ship_edges = make_ship()
ring_verts, ring_edges = make_ring()
octa_verts, octa_edges = make_octa()


def hsv(h, s=65, v=100):
    c = pg.Color(0, 0, 0)
    c.hsva = (h % 360, s, v, 100)
    return (c.r, c.g, c.b)


def themed_body_color(b):
    if b["kind"] == "hole":
        return T["hole_core"]
    if theme_key == "glitch":
        return (120, 255, 150) if b["kind"] == "star" else (55, 225, 100)
    if theme_key == "blueprint":
        return (255, 240, 145) if b["kind"] == "star" else (210, 232, 255)
    if theme_key == "parchment":
        return (180, 95, 20) if b["kind"] == "star" else (35, 55, 95)
    return b["color"]


def gen_galaxy(seed):
    rng = np.random.default_rng(seed)
    bodies = []
    sites = [(0.0, 0.0, 120.0)]

    for k in range(N_HOLES):
        a = 2 * np.pi * k / N_HOLES + 0.3
        x, z = HOLE_RING * np.cos(a), HOLE_RING * np.sin(a)
        sites.append((x, z, 90.0))
        bodies.append(dict(
            name=f"{T['hole_prefix']}-{k + 1}", kind="hole", pos=np.array([x, 0.0, z]),
            vel=np.zeros(3), radius=4.0, mass=320.0, well_depth=600.0,
            soft=10.0, color=(170, 90, 255), parent=-1,
            orbit_r=0.0, speed=0.0, angle=0.0
        ))

    clear, placed, tries = 330.0, 0, 0
    while placed < N_SYSTEMS and tries < 9000:
        tries += 1
        if tries % 1500 == 0:
            clear -= 25.0
        x, z = rng.uniform(-HALF * 0.9, HALF * 0.9, 2)
        if not all(np.hypot(x - sx, z - sz) > clear + sr for sx, sz, sr in sites):
            continue
        sites.append((x, z, clear))
        placed += 1
        sun_r = rng.uniform(2.0, 4.0)
        sun_mass = sun_r * 60.0
        sun_idx = len(bodies)
        sname = f"{T['star_prefix']}-{placed}"
        bodies.append(dict(
            name=sname, kind="star", pos=np.array([x, 0.0, z]),
            vel=np.zeros(3), radius=sun_r * 5.0, mass=sun_mass,
            well_depth=sun_mass * 4.0, soft=sun_r * 10.0,
            color=hsv(rng.uniform(20, 60), 70, 100), parent=-1,
            orbit_r=0.0, speed=0.0, angle=0.0
        ))
        n_planets = int(rng.integers(1, 5))
        for i in range(n_planets):
            orb = 90.0 + i * 55.0 + rng.uniform(0, 15)
            pr = rng.uniform(0.7, 1.8)
            pm = pr * 18.0
            sign = 1.0 if rng.random() < 0.8 else -1.0
            bodies.append(dict(
                name=f"{sname}{'bcde'[i]}", kind="planet", pos=np.array([x, 0.0, z]),
                vel=np.zeros(3), radius=pr * 2.5, ring=bool(rng.random() < 0.3),
                mass=pm, well_depth=pm * 1.5, soft=6.0 + pr * 3.0,
                color=hsv(rng.uniform(0, 360), 60, 100), parent=sun_idx, orbit_r=orb,
                speed=sign * np.sqrt(G * sun_mass / ((orb ** 2 + (sun_r * 10.0) ** 2) * orb)) * rng.uniform(0.9, 1.1),
                angle=rng.uniform(0, 2 * np.pi), relay=False
            ))
        bodies[sun_idx + 1 + int(rng.integers(n_planets))]["relay"] = True
    return bodies


def update_orbits(dt):
    for b in bodies:
        if b["parent"] >= 0:
            P = bodies[b["parent"]]["pos"]
            b["angle"] += b["speed"] * dt
            ca, sa = np.cos(b["angle"]), np.sin(b["angle"])
            b["pos"][0] = P[0] + ca * b["orbit_r"]
            b["pos"][2] = P[2] + sa * b["orbit_r"]
            b["vel"] = np.array([-sa * b["orbit_r"] * b["speed"], 0.0, ca * b["orbit_r"] * b["speed"]])


def rebuild_static():
    global BM, BS2, BWD, BRAD, HOR, BRV, ISHOLE, ISPLANET
    BM = np.array([b["mass"] for b in bodies])
    BS2 = np.array([b["soft"] ** 2 for b in bodies])
    BWD = np.array([b["well_depth"] for b in bodies])
    BRAD = np.array([0.0 if b["kind"] == "hole" else b["radius"] * 1.15 for b in bodies])
    HOR = np.array([b["radius"] if b["kind"] == "hole" else 0.0 for b in bodies])
    BRV = np.array([b["radius"] for b in bodies])
    ISHOLE = np.array([b["kind"] == "hole" for b in bodies])
    ISPLANET = np.array([b["kind"] == "planet" for b in bodies])


def refresh_positions():
    global BP
    BP = np.array([b["pos"] for b in bodies])


def wells_height(xs, zs):
    dx = xs[:, None] - BP[None, :, 0]
    dz = zs[:, None] - BP[None, :, 2]
    return -2.0 - (BWD / np.sqrt(dx * dx + dz * dz + BS2)).sum(axis=1)


def grid_height_at(x, z):
    return wells_height(np.array([x]), np.array([z]))[0]


USE_AA = True


def m(trn, rot, scl):
    tx, ty, tz = trn
    rx, ry, rz = rot
    sx, sy, sz = scl
    S = np.array([[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0], [0, 0, 0, 1]], dtype=float)
    T = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [tx, ty, tz, 1]], dtype=float)
    cox, six = np.cos(rx), np.sin(rx)
    coy, siy = np.cos(ry), np.sin(ry)
    coz, siz = np.cos(rz), np.sin(rz)
    XR = np.array([[1, 0, 0, 0], [0, cox, six, 0], [0, -six, cox, 0], [0, 0, 0, 1]], dtype=float)
    YR = np.array([[coy, 0, -siy, 0], [0, 1, 0, 0], [siy, 0, coy, 0], [0, 0, 0, 1]], dtype=float)
    ZR = np.array([[coz, siz, 0, 0], [-siz, coz, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=float)
    return S @ (XR @ YR @ ZR) @ T


def v(trn, rot):
    tx, ty, tz = trn
    rx, ry, rz = rot
    T = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [-tx, -ty, -tz, 1]], dtype=float)
    cox, six = np.cos(-rx), np.sin(-rx)
    coy, siy = np.cos(-ry), np.sin(-ry)
    coz, siz = np.cos(-rz), np.sin(-rz)
    XR = np.array([[1, 0, 0, 0], [0, cox, six, 0], [0, -six, cox, 0], [0, 0, 0, 1]], dtype=float)
    YR = np.array([[coy, 0, -siy, 0], [0, 1, 0, 0], [siy, 0, coy, 0], [0, 0, 0, 1]], dtype=float)
    ZR = np.array([[coz, siz, 0, 0], [-siz, coz, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=float)
    return T @ (ZR @ YR @ XR)


def p(fov):
    rad = np.radians(fov)
    f = 1.0 / np.tan(rad / 2.0)
    ar = wid / hig
    nr, fr = 0.1, 400.0
    return np.array([
        [f / ar, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, fr / (fr - nr), 1],
        [0, 0, -(fr * nr) / (fr - nr), 0]
    ], dtype=float)


def draw_mesh(vertices, edges, model_mat, view_mat, proj_mat, color, width=1, max_dist=38.0):
    clip = vertices @ model_mat @ view_mat @ proj_mat
    near = 0.1
    base_col = np.array(color, dtype=float)
    bg_col = np.array(T["bg"], dtype=float)
    p1 = clip[edges[:, 0]]
    p2 = clip[edges[:, 1]]
    w1, w2 = p1[:, 3], p2[:, 3]
    valid = (w1 >= near) | (w2 >= near)
    p1, p2, w1, w2 = p1[valid], p2[valid], w1[valid], w2[valid]
    c1 = w1 < near
    if np.any(c1):
        t1 = ((near - w1[c1]) / (w2[c1] - w1[c1]))[:, None]
        p1[c1] = p1[c1] + t1 * (p2[c1] - p1[c1])
    c2 = w2 < near
    if np.any(c2):
        t2 = ((near - w2[c2]) / (w1[c2] - w2[c2]))[:, None]
        p2[c2] = p2[c2] + t2 * (p1[c2] - p2[c2])
    avg_dist = 0.5 * (p1[:, 3] + p2[:, 3])
    keep = avg_dist < max_dist
    p1, p2, avg_dist = p1[keep], p2[keep], avg_dist[keep]
    brightness = np.clip(1.0 - (avg_dist / max_dist), 0.0, 1.0)[:, None]
    cols = (bg_col + (base_col - bg_col) * brightness).astype(int)
    ndc1 = p1[:, :2] / p1[:, 3:4]
    ndc2 = p2[:, :2] / p2[:, 3:4]
    x1 = (ndc1[:, 0] + 1) * 0.5 * wid
    y1 = (1 - ndc1[:, 1]) * 0.5 * hig
    x2 = (ndc2[:, 0] + 1) * 0.5 * wid
    y2 = (1 - ndc2[:, 1]) * 0.5 * hig
    pad = 30.0
    vis = ~(((x1 < -pad) & (x2 < -pad)) | ((x1 > wid + pad) & (x2 > wid + pad)) |
            ((y1 < -pad) & (y2 < -pad)) | ((y1 > hig + pad) & (y2 > hig + pad)))
    vis &= (np.abs(x1) < 1e5) & (np.abs(x2) < 1e5) & (np.abs(y1) < 1e5) & (np.abs(y2) < 1e5)
    x1, y1, x2, y2, cols = x1[vis], y1[vis], x2[vis], y2[vis], cols[vis]
    X1, Y1, X2, Y2, CL = x1.tolist(), y1.tolist(), x2.tolist(), y2.tolist(), cols.tolist()
    if not USE_AA or theme_key == "glitch":
        for i in range(len(X1)):
            pg.draw.line(scr, CL[i], (round(X1[i]), round(Y1[i])), (round(X2[i]), round(Y2[i])), width)
    elif width <= 1:
        for i in range(len(X1)):
            pg.draw.aaline(scr, CL[i], (X1[i], Y1[i]), (X2[i], Y2[i]))
    else:
        d = np.hypot(x2 - x1, y2 - y1) + 1e-6
        NX, NY = (-(y2 - y1) / d).tolist(), ((x2 - x1) / d).tolist()
        offs = [k - (width - 1) / 2 for k in range(width)]
        for i in range(len(X1)):
            for o in offs:
                pg.draw.aaline(
                    scr, CL[i],
                    (X1[i] + NX[i] * o, Y1[i] + NY[i] * o),
                    (X2[i] + NX[i] * o, Y2[i] + NY[i] * o)
                )


FIXED_SEED = 1337
SHIP_SCALE = 0.5
LAND_T, STAY_T, TAKE_T = 2.4, 2.2, 1.8
EL_LAND = np.radians(60)
SPIN = 0.4
SCAN_BASE = 150.0
SCAN_PER_RELAY = 20.0
FOG_N = 32
FOG_CELL = 2 * HALF / FOG_N
_cc = -HALF + (np.arange(FOG_N) + 0.5) * FOG_CELL
FOG_CX, FOG_CZ = np.meshgrid(_cc, _cc, indexing="ij")

game_state = "menu"
game_mode = "delivery"
menu_idx = 0


def set_mouse_capture(captured):
    pg.event.set_grab(captured)
    pg.mouse.set_visible(not captured)
    pg.mouse.get_rel()


def new_mission():
    global mission
    if game_mode == "freeroam" or mi >= len(relay_order):
        mission = dict(target=None, cargo="", t=0.0)
    else:
        cargos = T["cargos"]
        mission = dict(target=relay_order[mi], cargo=cargos[min(mi, len(cargos) - 1)], t=0.0)


def reset_world(seed_):
    global bodies, ship_pos, vel, trail, safe_pos, mode, land, cooldown
    global disc, explored, scan_r, mi, relay_order, relay_done, ISSTAR
    global story, log, ending, delivered, show_log
    bodies = gen_galaxy(seed_)
    rebuild_static()
    refresh_positions()
    ISSTAR = np.array([b["kind"] == "star" for b in bodies])
    ship_pos = np.array([0.0, grid_height_at(0.0, 0.0) + HOVER_OFFSET, 0.0])
    safe_pos = np.array([0.0, 0.0, 0.0])
    vel = np.zeros(3)
    trail = []
    mode, land, cooldown = "fly", None, 0.0
    disc = np.zeros(len(bodies), dtype=bool)
    explored = np.zeros((FOG_N, FOG_N), dtype=bool)
    scan_r = SCAN_BASE
    relays = [i for i, b in enumerate(bodies) if b.get("relay")]
    relay_order = sorted(relays, key=lambda i: np.hypot(*bodies[bodies[i]["parent"]]["pos"][[0, 2]]))
    relay_done = set()
    mi, delivered, ending, show_log = 0, 0, "none", False
    log = []
    story = None
    if game_mode == "freeroam":
        disc[:] = True
        explored[:] = True
        new_mission()
        push_story("FREE ROAM", T["free_intro"], 10.0)
    else:
        new_mission()
        push_story(T["menu_title"], T["intro"], 16.0)


def start_mode(selected_mode):
    global game_mode, game_state, menu_idx
    game_mode = selected_mode
    seed = FIXED_SEED if game_mode == "delivery" else random.randint(10000, 9999999)
    reset_world(seed)
    game_state = "play"
    menu_idx = 0
    set_mouse_capture(True)


def push_story(title, text, secs=12.0):
    global story
    story = dict(title=title, text=text, t=secs)
    log.append((title, text))


bodies = []
ship_pos = np.zeros(3)
vel = np.zeros(3)
trail = []
safe_pos = np.zeros(3)
mission = {}
mode, land, cooldown = "fly", None, 0.0
msg, msg_t = "", 0.0
disc = np.zeros(0, dtype=bool)
explored = np.zeros((FOG_N, FOG_N), dtype=bool)
scan_r, mi, relay_order, relay_done = SCAN_BASE, 0, [], set()
ISSTAR = np.zeros(0, dtype=bool)
story, log, ending, delivered, show_log = None, [], "none", 0, False

reset_world(FIXED_SEED)
story = None
set_mouse_capture(False)
yaw, pitch = 0.0, 0.35
sensitivity = 0.003
proj_mat = p(70)
identity_mat = np.eye(4)
trail_timer = 0.0
cam_dist = 3.6
runig = True


def say(text, secs=3.0):
    global msg, msg_t
    msg, msg_t = text, secs


def unit(a):
    return a / max(np.linalg.norm(a), 1e-9)


def ease(x):
    return x * x * (3 - 2 * x)


def rot_y(vec, ry):
    c, s = np.cos(ry), np.sin(ry)
    return np.array([vec[0] * c + vec[2] * s, vec[1], -vec[0] * s + vec[2] * c])


def polar(C, az, el, rad):
    return C + rad * np.array([np.cos(el) * np.cos(az), np.sin(el), np.cos(el) * np.sin(az)])


def basis_matrix(bs, pos, s):
    M = np.eye(4)
    M[0, :3], M[1, :3], M[2, :3], M[3, :3] = bs[0] * s, bs[1] * s, bs[2] * s, pos
    return M


def blend_basis(b0, b1, e):
    up = unit(b0[1] * (1 - e) + b1[1] * e)
    fw = b0[2] * (1 - e) + b1[2] * e
    fw = unit(fw - up * np.dot(fw, up))
    return np.cross(up, fw), up, fw


def surface_basis(u, head):
    fw = head - u * np.dot(head, u)
    if np.linalg.norm(fw) < 1e-3:
        fw = np.cross(u, np.array([0.0, 0.0, 1.0]))
    fw = unit(fw)
    return np.cross(u, fw), u, fw


def reveal_system(star_idx):
    for j, b in enumerate(bodies):
        if j == star_idx or b["parent"] == star_idx:
            disc[j] = True


def reveal_area(x, z, rad):
    global explored
    explored |= np.hypot(FOG_CX - x, FOG_CZ - z) < rad
    disc[np.hypot(BP[:, 0] - x, BP[:, 2] - z) < rad] = True


def wrap_text(text, fnt, max_w):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split(" "):
            t = (cur + " " + w).strip()
            if fnt.size(t)[0] <= max_w:
                cur = t
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def draw_panel(title, text, tint=None):
    if tint is None:
        tint = T["accent"]
    lines = wrap_text(text, font, wid - 160)
    h = 46 + 20 * len(lines)
    top = hig - h - 16
    surf = pg.Surface((wid - 120, h), pg.SRCALPHA)
    surf.fill(T["panel_bg"])
    scr.blit(surf, (60, top))
    pg.draw.rect(scr, tint, (60, top, wid - 120, h), 1)
    scr.blit(font.render(title, True, tint), (76, top + 8))
    for k, l in enumerate(lines):
        scr.blit(font.render(l, True, T["panel_text"]), (76, top + 34 + 20 * k))


def draw_arrow(tx, tz):
    dx, dz = tx - ship_pos[0], tz - ship_pos[2]
    f = dx * np.sin(yaw) + dz * np.cos(yaw)
    r = dx * np.cos(yaw) - dz * np.sin(yaw)
    d = np.array([r, -f])
    d = d / max(np.linalg.norm(d), 1e-6)
    c = np.array([wid / 2, 70.0])
    tip, tail = c + d * 26, c - d * 14
    perp = np.array([-d[1], d[0]])
    col = T["accent"]
    pg.draw.line(scr, col, tail, tip, 3)
    pg.draw.line(scr, col, tip, tip - d * 12 + perp * 8, 3)
    pg.draw.line(scr, col, tip, tip - d * 12 - perp * 8, 3)


HEX_RAD = 78
HEX_SIZE = HEX_RAD * 2
HEX_LOCAL = [
    (HEX_RAD + HEX_RAD * np.cos(np.radians(60 * i)),
     HEX_RAD + HEX_RAD * np.sin(np.radians(60 * i)))
    for i in range(6)
]
HEX_MASK = pg.Surface((HEX_SIZE, HEX_SIZE), pg.SRCALPHA)
pg.draw.polygon(HEX_MASK, (255, 255, 255, 255), HEX_LOCAL)


def clamp_to_hex(px, py, cx, cy, max_r):
    dx, dy = px - cx, py - cy
    ang = np.arctan2(dy, dx)
    sector_ang = (ang + np.pi) % (np.pi / 3) - (np.pi / 6)
    hex_edge_r = (max_r * np.cos(np.pi / 6)) / max(np.cos(sector_ang), 1e-5)
    dist = np.hypot(dx, dy)
    if dist > hex_edge_r:
        scale = hex_edge_r / dist
        return int(cx + dx * scale), int(cy + dy * scale)
    return int(px), int(py)


def draw_minimap():
    rx, ry = wid - HEX_SIZE - 16, 12
    cx, cy = rx + HEX_RAD, ry + HEX_RAD
    img = np.where(explored[:, :, None], np.array(T["fog_explored"]), np.array(T["fog_unexplored"])).astype(np.uint8)
    fog_surf = pg.Surface((FOG_N, FOG_N))
    pg.surfarray.blit_array(fog_surf, np.ascontiguousarray(img[:, ::-1]))
    map_surf = pg.transform.smoothscale(fog_surf, (HEX_SIZE, HEX_SIZE)).convert_alpha()
    span = HALF * 2.0

    if theme_key in ("blueprint", "parchment"):
        grid_c = (150, 185, 235, 55) if theme_key == "blueprint" else (70, 75, 85, 45)
        hatch_c = (180, 210, 250, 75) if theme_key == "blueprint" else (120, 125, 135, 70)
        for g in range(0, HEX_SIZE, 16):
            pg.draw.line(map_surf, grid_c, (g, 0), (g, HEX_SIZE), 1)
            pg.draw.line(map_surf, grid_c, (0, g), (HEX_SIZE, g), 1)
        cell_px = HEX_SIZE / FOG_N
        for ix in range(FOG_N):
            for iz in range(FOG_N):
                if not explored[ix, iz]:
                    px0 = int(ix * cell_px)
                    py0 = int((FOG_N - 1 - iz) * cell_px)
                    pg.draw.line(map_surf, hatch_c, (px0, py0), (px0 + int(cell_px), py0 + int(cell_px)), 1)

    def tomap_local(x, z):
        return int((x + HALF) / span * HEX_SIZE), int((1 - (z + HALF) / span) * HEX_SIZE)

    holes = [bodies[i] for i in range(len(bodies)) if bodies[i]["kind"] == "hole"]
    if ending == "good":
        pg.draw.lines(map_surf, T["map_hole"], True, [tomap_local(h["pos"][0], h["pos"][2]) for h in holes], 1)
    for i, b in enumerate(bodies):
        if not disc[i]:
            continue
        pt = tomap_local(b["pos"][0], b["pos"][2])
        if b["kind"] == "star":
            pg.draw.circle(map_surf, T["map_star"], pt, 3)
        elif b["kind"] == "hole":
            pg.draw.circle(map_surf, T["map_hole"], pt, 3, 1)
        elif i in relay_done:
            pg.draw.circle(map_surf, T["accent2"], pt, 3, 1)
        else:
            pg.draw.circle(map_surf, themed_body_color(b), pt, 1)

    map_surf.blit(HEX_MASK, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
    scr.blit(map_surf, (rx, ry))
    hex_pts = [(rx + x, ry + y) for x, y in HEX_LOCAL]
    pg.draw.polygon(scr, T["accent"], hex_pts, 2)

    tgt = mission["target"]
    if tgt is not None:
        if disc[tgt]:
            tx, ty = tomap_local(bodies[tgt]["pos"][0], bodies[tgt]["pos"][2])
            pg.draw.circle(scr, T["accent"], clamp_to_hex(rx + tx, ry + ty, cx, cy, HEX_RAD - 4), 6, 1)
        else:
            star = bodies[bodies[tgt]["parent"]]["pos"]
            sx, sy = tomap_local(star[0], star[2])
            pg.draw.circle(scr, T["accent"], clamp_to_hex(rx + sx, ry + sy, cx, cy, HEX_RAD - 6), 11, 1)
    px, py = tomap_local(ship_pos[0], ship_pos[2])
    pg.draw.circle(scr, T["accent2"], clamp_to_hex(rx + px, ry + py, cx, cy, HEX_RAD - 3), 3)


def apply_glitch_fx(hole_proximity, t_sec):
    if theme_key != "glitch":
        return
    for y in range(0, hig, 4):
        pg.draw.line(scr, (0, 14, 4), (0, y), (wid, y), 1)
    if hole_proximity > 0.0:
        if random.random() < 0.25 + 0.55 * hole_proximity:
            strips = 1 + int(hole_proximity * 5)
            for _ in range(strips):
                sy = random.randint(0, hig - 24)
                sh = random.randint(4, 18)
                shift = random.randint(-int(12 + 30 * hole_proximity), int(12 + 30 * hole_proximity))
                row = scr.subsurface((0, sy, wid, sh)).copy()
                scr.blit(row, (shift, sy))
        if random.random() < 0.12 * hole_proximity:
            flash = pg.Surface((wid, hig), pg.SRCALPHA)
            flash.fill((255, 30, 30, int(35 * hole_proximity)))
            scr.blit(flash, (0, 0))


def get_menu_items():
    theme_desc = f"Active: {T['label']}  (Click or LEFT/RIGHT to switch)"
    if game_state == "paused":
        return [
            ("RESUME FLIGHT", "Return to active cockpit"),
            ("SET DELIVERY", "Start story campaign (fixed galaxy)"),
            ("FREE ROAM", "Generate a random galaxy to explore"),
            ("THEME", theme_desc),
            ("QUIT", "Exit to desktop"),
        ]
    return [
        ("SET DELIVERY", "8-stop story campaign in a fixed galaxy"),
        ("FREE ROAM", "Explore a freshly generated random galaxy"),
        ("THEME", theme_desc),
        ("QUIT", "Exit to desktop"),
    ]


def cycle_theme(step=1):
    nxt = THEME_ORDER[(theme_idx + step) % len(THEME_ORDER)]
    set_theme(nxt)


def execute_menu_option(label):
    global game_state, runig
    if label == "RESUME FLIGHT":
        game_state = "play"
        set_mouse_capture(True)
    elif label == "SET DELIVERY":
        start_mode("delivery")
    elif label == "FREE ROAM":
        start_mode("freeroam")
    elif label == "THEME":
        cycle_theme(1)
    elif label == "QUIT":
        runig = False


def draw_menu_overlay():
    overlay = pg.Surface((wid, hig), pg.SRCALPHA)
    bg_r, bg_g, bg_b = T["bg"]
    overlay.fill((bg_r, bg_g, bg_b, 195))
    scr.blit(overlay, (0, 0))
    items = get_menu_items()
    box_w = 600
    box_h = 135 + len(items) * 52
    bx, by = (wid - box_w) // 2, (hig - box_h) // 2
    pg.draw.rect(scr, T["menu_bg"], (bx, by, box_w, box_h))
    pg.draw.rect(scr, T["accent"], (bx, by, box_w, box_h), 2)
    heading = "SYSTEM PAUSED" if game_state == "paused" else T["menu_title"]
    sub = (f"ACTIVE MODE: {game_mode.upper()}" if game_state == "paused"
           else T["menu_sub"])
    t_surf = title_font.render(heading, True, T["accent"])
    s_surf = font.render(sub, True, T["text"])
    scr.blit(t_surf, (wid // 2 - t_surf.get_width() // 2, by + 18))
    scr.blit(s_surf, (wid // 2 - s_surf.get_width() // 2, by + 62))
    btn_rects = []
    start_y = by + 96
    for idx, (label, desc) in enumerate(items):
        rect = pg.Rect(bx + 32, start_y + idx * 52, box_w - 64, 44)
        btn_rects.append((rect, label, idx))
        selected = (idx == menu_idx)
        bg = T["btn_sel"] if selected else T["btn_bg"]
        border = T["accent2"] if selected else T["btn_border"]
        pg.draw.rect(scr, bg, rect)
        pg.draw.rect(scr, border, rect, 2 if selected else 1)
        prefix = "> " if selected else "  "
        disp_label = f"THEME: < {T['label']} >" if label == "THEME" else label
        l_col = T["accent2"] if selected else T["text"]
        scr.blit(big_font.render(prefix + disp_label, True, l_col), (rect.x + 12, rect.y + 3))
        scr.blit(font.render(desc, True, T["text_dim"]), (rect.x + 34, rect.y + 25))
    hint = "UP/DOWN or MOUSE to select  |  LEFT/RIGHT theme  |  ENTER/CLICK confirm"
    if game_state == "paused":
        hint += "  |  ESC resume"
    h_surf = font.render(hint, True, T["text_dim"])
    scr.blit(h_surf, (wid // 2 - h_surf.get_width() // 2, by + box_h - 22))
    return btn_rects


btn_rects = []
while runig:
    dt = min(clk.tick(60) / 1000.0, 0.05)
    t_sec = pg.time.get_ticks() * 0.001
    for evnt in pg.event.get():
        if evnt.type == pg.QUIT:
            runig = False
        elif game_state in ("menu", "paused"):
            items = get_menu_items()
            if evnt.type == pg.MOUSEMOTION:
                for rect, _, idx in btn_rects:
                    if rect.collidepoint(evnt.pos):
                        menu_idx = idx
            elif evnt.type == pg.MOUSEBUTTONDOWN and evnt.button == 1:
                for rect, label, idx in btn_rects:
                    if rect.collidepoint(evnt.pos):
                        menu_idx = idx
                        execute_menu_option(label)
            elif evnt.type == pg.KEYDOWN:
                if evnt.key in (pg.K_UP, pg.K_w):
                    menu_idx = (menu_idx - 1) % len(items)
                elif evnt.key in (pg.K_DOWN, pg.K_s):
                    menu_idx = (menu_idx + 1) % len(items)
                elif evnt.key in (pg.K_LEFT, pg.K_a):
                    cycle_theme(-1)
                elif evnt.key in (pg.K_RIGHT, pg.K_d, pg.K_t):
                    cycle_theme(1)
                elif evnt.key in (pg.K_RETURN, pg.K_SPACE):
                    execute_menu_option(items[menu_idx][0])
                elif evnt.key == pg.K_ESCAPE and game_state == "paused":
                    game_state = "play"
                    set_mouse_capture(True)
        elif game_state == "play":
            if evnt.type == pg.MOUSEMOTION:
                dx, dy = evnt.rel
                yaw += dx * sensitivity
                pitch = np.clip(pitch + dy * sensitivity, 0.05, 1.35)
            elif evnt.type == pg.KEYDOWN:
                if evnt.key == pg.K_ESCAPE:
                    game_state = "paused"
                    menu_idx = 0
                    set_mouse_capture(False)
                elif evnt.key == pg.K_t:
                    cycle_theme(1)
                    say(f"THEME: {T['label']}", 2.0)
                elif evnt.key == pg.K_r:
                    seed = FIXED_SEED if game_mode == "delivery" else random.randint(10000, 9999999)
                    reset_world(seed)
                    say("NEW GALAXY GENERATED" if game_mode == "freeroam" else "RESTARTED")
                elif evnt.key == pg.K_SPACE and ending in ("none", "good", "quiet"):
                    story = None
                elif evnt.key == pg.K_TAB:
                    show_log = not show_log
                elif ending == "choice" and evnt.key in (pg.K_1, pg.K_2):
                    if evnt.key == pg.K_1:
                        ending = "good"
                        disc[:] = True
                        explored[:] = True
                        push_story(T["end_good_title"], T["end_good"], 40.0)
                    else:
                        ending = "quiet"
                        push_story(T["end_quiet_title"], T["end_quiet"], 40.0)

    if game_state == "menu":
        yaw += 0.12 * dt

    if game_state in ("play", "menu"):
        update_orbits(dt)
        refresh_positions()

    if game_state == "play":
        mission["t"] += dt
        msg_t = max(0.0, msg_t - dt)
        cooldown -= dt
        if story is not None and ending != "choice":
            story["t"] -= dt
            if story["t"] <= 0:
                story = None

    heights = wells_height(BP[:, 0], BP[:, 2])
    BC = BP.copy()
    BC[:, 1] = heights + np.where(ISHOLE, 1.5, 1.0 + BRV * 0.4)

    if game_state == "play":
        dxz = np.hypot(BP[:, 0] - ship_pos[0], BP[:, 2] - ship_pos[2])
        disc |= dxz < scan_r * np.where(ISSTAR, 1.6, 1.0)
        explored |= np.hypot(FOG_CX - ship_pos[0], FOG_CZ - ship_pos[2]) < scan_r * 1.2
        forward = np.array([np.sin(yaw), 0.0, np.cos(yaw)])
        right = np.array([np.cos(yaw), 0.0, -np.sin(yaw)])
        keys = pg.key.get_pressed()
        diff = BP - ship_pos
        diff[:, 1] = 0.0
        d2 = (diff * diff).sum(axis=1)
        dist = np.sqrt(d2) + 1e-6

        if mode == "fly":
            thrust = 22.0
            if keys[pg.K_w]:
                vel += forward * thrust * dt
            if keys[pg.K_s]:
                vel -= forward * thrust * dt
            if keys[pg.K_d]:
                vel += right * thrust * dt
            if keys[pg.K_a]:
                vel -= right * thrust * dt
            if cooldown <= 0:
                for i in np.nonzero(ISPLANET & (dist < BRAD + 3.5))[0]:
                    if np.linalg.norm(vel - bodies[i]["vel"]) < DOCK_SPEED:
                        C = BC[i]
                        A = ship_pos - C
                        rad0 = np.linalg.norm(A)
                        land = dict(
                            idx=int(i), t0=t_sec, timer=0.0, rad0=rad0,
                            az0=np.arctan2(A[2], A[0]),
                            el0=np.arcsin(np.clip(A[1] / rad0, -1, 1)),
                            head0=forward.copy()
                        )
                        mode = "landing"
                        break

        if mode == "fly":
            accel = G * BM / (d2 + BS2)
            pull = dist >= BRAD
            vel += ((diff / dist[:, None]) * (accel * pull)[:, None]).sum(axis=0) * dt
            for i in np.nonzero(~pull)[0]:
                normal = -diff[i] / max(dist[i], 0.001)
                ship_pos[0] = BP[i][0] + normal[0] * BRAD[i]
                ship_pos[2] = BP[i][2] + normal[2] * BRAD[i]
                vel *= 0.85
            if np.any(dist < HOR):
                ship_pos[0], ship_pos[2] = safe_pos[0], safe_pos[2]
                vel[:] = 0.0
                trail.clear()
                mission["t"] += 15.0
                say(T["spaghetti_msg"], 4.0)
            ship_pos += vel * dt
            ship_pos[1] = grid_height_at(ship_pos[0], ship_pos[2]) + HOVER_OFFSET
    else:
        diff = BP - ship_pos
        diff[:, 1] = 0.0
        dist = np.sqrt((diff * diff).sum(axis=1)) + 1e-6
        forward = np.array([np.sin(yaw), 0.0, np.cos(yaw)])
        keys = pg.key.get_pressed()

    hole_dists = dist[ISHOLE]
    min_hole_dist = float(hole_dists.min()) if len(hole_dists) else 9999.0
    hole_proximity = float(np.clip(1.0 - (min_hole_dist - 10.0) / 140.0, 0.0, 1.0))

    eps = 0.25
    h_ahead = grid_height_at(ship_pos[0] + forward[0] * eps, ship_pos[2] + forward[2] * eps)
    h_behind = grid_height_at(ship_pos[0] - forward[0] * eps, ship_pos[2] - forward[2] * eps)
    slope_pitch = -np.arctan2(h_ahead - h_behind, 2.0 * eps)
    bank_roll = 0.0
    if game_state == "play" and mode == "fly":
        if keys[pg.K_a]:
            bank_roll += 0.35
        if keys[pg.K_d]:
            bank_roll -= 0.35
    FM = m((0, 0, 0), (slope_pitch, yaw, bank_roll), (1, 1, 1))
    fly_b = (FM[0, :3].copy(), FM[1, :3].copy(), FM[2, :3].copy())
    ship_b = fly_b

    if mode != "fly":
        if game_state == "play":
            land["timer"] += dt
        tm = land["timer"]
        i = land["idx"]
        b = bodies[i]
        C = BC[i]
        r = b["radius"]
        spin_ang = SPIN * (t_sec - land["t0"])
        az = land["az0"] - spin_ang
        head = rot_y(land["head0"], spin_ang)
        u_land = np.array([np.cos(EL_LAND) * np.cos(az), np.sin(EL_LAND), np.cos(EL_LAND) * np.sin(az)])
        if mode == "landing":
            e = ease(min(tm / LAND_T, 1.0))
            el = land["el0"] + (EL_LAND - land["el0"]) * e
            rad = land["rad0"] + (r + 0.05 - land["rad0"]) * e
            pos = polar(C, az, el, rad)
            ship_b = blend_basis(fly_b, surface_basis(u_land, head), e)
            if game_state == "play" and tm >= LAND_T:
                mode, land["timer"] = "landed", 0.0
                if game_mode == "delivery" and mission["target"] is not None and i == mission["target"]:
                    k = mi
                    delivered += 1
                    scan_r += SCAN_PER_RELAY
                    relay_done.add(i)
                    reveal_system(b["parent"])
                    reveal_area(b["pos"][0], b["pos"][2], 450.0)
                    safe_pos = ship_pos.copy()
                    mi += 1
                    new_mission()
                    text = f'"{T["fragments"][k]}"'
                    if mission["target"] is not None:
                        text += "\n\n" + T["guild"][k]
                    push_story(f"DELIVERY {k + 1}/{len(relay_order)} DONE  -  recipient:", text, 16.0)
                    if mission["target"] is None:
                        ending = "choice"
                    say(f"DELIVERY {k + 1} DONE - fog lifted, scanners boosted", 4.0)
                else:
                    safe_pos = ship_pos.copy()
                    say(f"Touchdown on {b['name']}" + ("" if game_mode == "freeroam" else " (no target here)"), 2.5)
        elif mode == "landed":
            pos = C + u_land * (r + 0.05)
            ship_b = surface_basis(u_land, head)
            if game_state == "play" and tm >= STAY_T:
                mode, land["timer"] = "takeoff", 0.0
        else:
            e = ease(min(tm / TAKE_T, 1.0))
            el = EL_LAND * (1 - e)
            rad = (r + 0.05) + (r * 1.15 + 3.2 - (r + 0.05)) * e
            pos = polar(C, az, el, rad)
            pos[1] = (1 - e) * pos[1] + e * (grid_height_at(pos[0], pos[2]) + HOVER_OFFSET)
            u_cur = np.array([np.cos(el) * np.cos(az), np.sin(el), np.cos(el) * np.sin(az)])
            ship_b = blend_basis(surface_basis(u_cur, head), fly_b, e)
            if game_state == "play" and tm >= TAKE_T:
                vel = b["vel"] + np.array([np.cos(az), 0.0, np.sin(az)]) * 5.0
                mode, cooldown = "fly", 4.0
        ship_pos[:] = pos

    cam_target = 3.6 if mode == "fly" else 5.2
    if game_state == "play":
        cam_dist += (cam_target - cam_dist) * min(1.0, 3.0 * dt)
    cam_pos = np.array([
        ship_pos[0] - np.sin(yaw) * np.cos(pitch) * cam_dist,
        ship_pos[1] + np.sin(pitch) * cam_dist + 0.4,
        ship_pos[2] - np.cos(yaw) * np.cos(pitch) * cam_dist
    ])
    snap_x = np.floor(ship_pos[0] / GRID_STEP) * GRID_STEP
    snap_z = np.floor(ship_pos[2] / GRID_STEP) * GRID_STEP
    world_grid = base_grdvrts.copy()
    world_grid[:, 0] += snap_x
    world_grid[:, 2] += snap_z
    world_grid[:, 1] = wells_height(world_grid[:, 0], world_grid[:, 2])
    view_mat = v(cam_pos, (pitch, yaw, 0))
    scr.fill(T["bg"])
    draw_mesh(world_grid, grid_edjs, identity_mat, view_mat, proj_mat, T["grid"], 1, max_dist=48.0)

    tgt = mission["target"]
    PATCH = 52.0
    for i, b in enumerate(bodies):
        if b["parent"] < 0 or not disc[i]:
            continue
        P = bodies[b["parent"]]["pos"]
        R = b["orbit_r"]
        rel_x, rel_z = ship_pos[0] - P[0], ship_pos[2] - P[2]
        if abs(np.hypot(rel_x, rel_z) - R) > PATCH + 10:
            continue
        half = min(np.pi, (PATCH + 15) / R)
        dth = 1.5 / R
        k0 = int(np.floor(np.arctan2(rel_z, rel_x) / dth))
        kn = int(np.ceil(half / dth)) + 1
        angs = np.arange(k0 - kn, k0 + kn + 1) * dth
        n = len(angs)
        oxs = P[0] + R * np.cos(angs)
        ozs = P[2] + R * np.sin(angs)
        ohs = wells_height(oxs, ozs) + 0.1
        ov = np.stack([oxs, ohs, ozs, np.ones(n)], axis=1)
        oe = np.stack([np.arange(n - 1), np.arange(1, n)], axis=1)
        is_t = (i == tgt)
        bcol = themed_body_color(b)
        bg = T["bg"]
        col = T["accent"] if is_t else tuple(int(bg[c] + (bcol[c] - bg[c]) * 0.85) for c in range(3))
        draw_mesh(ov, oe, identity_mat, view_mat, proj_mat, col, 2, 48.0)

    for i in np.nonzero((dist < 650.0) & disc)[0]:
        b = bodies[i]
        r = b["radius"]
        C = BC[i]
        bcol = themed_body_color(b)
        if b["kind"] == "hole":
            draw_mesh(sphere_verts, sphere_edges, m(C, (0, 0, 0), (r, r, r)), view_mat, proj_mat, bcol, 2, 600.0)
            ring_cols = (T["hole_ring1"], T["hole_ring2"])
            for k, sc in enumerate((2.4, 3.4)):
                draw_mesh(
                    ring_verts, ring_edges, m(C, (0.25, t_sec * (1.5 - k), 0), (r * sc, r * sc, r * sc)),
                    view_mat, proj_mat, ring_cols[k], 2, 600.0
                )
        elif b["kind"] == "star":
            draw_mesh(sphere_verts, sphere_edges, m(C, (0, t_sec * SPIN, 0), (r, r, r)), view_mat, proj_mat, bcol, 2, 800.0)
            bg = T["bg"]
            dim = tuple(int(bg[c] + (bcol[c] - bg[c]) * 0.45) for c in range(3))
            draw_mesh(
                sphere_verts, sphere_edges, m(C, (0, -t_sec * 0.2, 0.3), (r * 1.3, r * 1.3, r * 1.3)),
                view_mat, proj_mat, dim, 1, 800.0
            )
        else:
            pcol = T["accent2"] if i in relay_done else bcol
            draw_mesh(sphere_verts, sphere_edges, m(C, (0, t_sec * SPIN, 0), (r, r, r)), view_mat, proj_mat, pcol, 2, 600.0)
            if b.get("ring"):
                bg = T["bg"]
                rcol = tuple(int(bg[c] + (bcol[c] - bg[c]) * 0.7) for c in range(3))
                draw_mesh(
                    ring_verts, ring_edges, m(C, (0.35, 0, 0.25), (r * 1.8, r * 1.8, r * 1.8)),
                    view_mat, proj_mat, rcol, 1, 600.0
                )
            if game_mode == "delivery" and b.get("relay") and i not in relay_done:
                top = C + np.array([0.0, r + 3.0, 0.0])
                draw_mesh(
                    octa_verts, octa_edges, m(top, (0, t_sec, 0), (0.5, 1.2, 0.5)),
                    view_mat, proj_mat, T["relay_beacon"], 1, 600.0
                )

    if tgt is not None and disc[tgt]:
        tb_ = bodies[tgt]
        tpos = BC[tgt].copy()
        tpos[1] += tb_["radius"] + 2.5 + np.sin(t_sec * 2) * 0.3
        draw_mesh(
            octa_verts, octa_edges, m(tpos, (0, t_sec * 1.2, 0), (0.9, 0.9, 0.9)),
            view_mat, proj_mat, T["accent"], 2, 800.0
        )

    if game_state == "play":
        trail_timer += dt
        if trail_timer >= 0.03:
            if mode == "fly":
                trail.append([ship_pos[0], ship_pos[1], ship_pos[2], 1.0])
            elif trail:
                trail.pop(0)
            if len(trail) > 60:
                trail.pop(0)
            trail_timer = 0.0

    if len(trail) > 1:
        pts = np.array(trail)
        clip = pts @ view_mat @ proj_mat
        bg_col = np.array(T["bg"], dtype=float)
        trail_col = np.array(T["trail"], dtype=float)
        num_segs = len(pts) - 1
        for i in range(num_segs):
            q1, q2 = clip[i], clip[i + 1]
            if q1[3] >= 0.1 and q2[3] >= 0.1:
                n1 = q1[:2] / q1[3]
                n2 = q2[:2] / q2[3]
                x1, y1 = (n1[0] + 1) * 0.5 * wid, (1 - n1[1]) * 0.5 * hig
                x2, y2 = (n2[0] + 1) * 0.5 * wid, (1 - n2[1]) * 0.5 * hig
                if max(abs(x1), abs(x2), abs(y1), abs(y2)) > 1e5:
                    continue
                fade = (i + 1) / num_segs
                col = tuple((bg_col + (trail_col - bg_col) * (fade ** 1.5)).astype(int).tolist())
                ln = max(np.hypot(x2 - x1, y2 - y1), 1e-6)
                nx_, ny_ = -(y2 - y1) / ln * 0.5, (x2 - x1) / ln * 0.5
                pg.draw.aaline(scr, col, (x1 + nx_, y1 + ny_), (x2 + nx_, y2 + ny_))
                pg.draw.aaline(scr, col, (x1 - nx_, y1 - ny_), (x2 - nx_, y2 - ny_))

    draw_mesh(
        ship_verts, ship_edges, basis_matrix(ship_b, ship_pos, SHIP_SCALE), view_mat, proj_mat,
        T["ship"], 2, max_dist=50.0
    )

    if game_state != "menu":
        speed_val = np.linalg.norm(vel) if mode == "fly" else 0.0
        scr.blit(font.render(
            f"SPEED: {speed_val:05.2f} u/s | POS: ({ship_pos[0]:.0f}, {ship_pos[2]:.0f}) | SCAN: {scan_r:.0f}",
            True, T["text"]
        ), (16, 16))
        if game_mode == "freeroam":
            scr.blit(font.render("MODE: FREE ROAM (RANDOM MAP)", True, T["accent2"]), (16, 38))
            scr.blit(font.render("[ESC] menu  [T] theme  [R] new map  [TAB] log", True, T["text_dim"]), (16, 60))
        elif tgt is not None:
            tb = bodies[tgt]
            known = bool(disc[tgt])
            aim = tb["pos"] if known else bodies[tb["parent"]]["pos"]
            tdist = np.hypot(aim[0] - ship_pos[0], aim[2] - ship_pos[2])
            rel_speed = np.linalg.norm(vel - tb["vel"]) if (mode == "fly" and known) else 0.0
            label = tb["name"] if known else f"unknown {T['planet_word']} (follow arrow)"
            scr.blit(font.render(
                f"DELIVERY {mi + 1}/{len(relay_order)}: {mission['cargo']}  ->  {label}",
                True, T["accent"]
            ), (16, 38))
            state_txt = {"fly": "", "landing": "   << LANDING", "landed": "   << LANDED", "takeoff": "   << TAKEOFF"}[mode]
            if mode == "fly" and known and tdist < tb["radius"] * 1.15 + 3.5 + 8:
                state_txt = "   << SLOW DOWN TO LAND"
            scr.blit(font.render(
                f"DIST: {tdist:6.0f}{'' if known else ' (approx)'}   REL SPEED: {rel_speed:4.1f} (land < {DOCK_SPEED:.0f})   TIME: {mission['t']:5.0f}s{state_txt}",
                True, T["text"]
            ), (16, 60))
            draw_arrow(aim[0], aim[2])
            scr.blit(font.render(
                f"DELIVERED: {delivered}/{len(relay_order)}   [ESC] pause  [T] theme  [TAB] log  [R] restart",
                True, T["text_dim"]
            ), (16, 82))
        else:
            scr.blit(font.render(
                "NO ORDERS - FREE FLIGHT" if ending != "choice" else "FINAL RECIPIENT WAITING",
                True, T["accent"]
            ), (16, 38))
            scr.blit(font.render(
                f"DELIVERED: {delivered}/{len(relay_order)}   [ESC] pause  [T] theme  [TAB] log  [R] restart",
                True, T["text_dim"]
            ), (16, 60))

    draw_minimap()
    if msg_t > 0:
        s_ = big_font.render(msg, True, T["warn"])
        scr.blit(s_, ((wid - s_.get_width()) // 2, 110))
    if game_state == "play":
        if show_log and log:
            draw_panel("LOG  [TAB to close]", "\n\n".join(f"{t}: {x}" for t, x in log[-3:]), T["warn"])
        elif ending == "choice":
            draw_panel(T["choice_title"], T["choice_txt"], T["warn"])
        elif story is not None:
            draw_panel(story["title"], story["text"])

    apply_glitch_fx(hole_proximity, t_sec)

    if game_state in ("menu", "paused"):
        btn_rects = draw_menu_overlay()

    pg.display.flip()

pg.quit()