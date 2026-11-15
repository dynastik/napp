import random
from pathlib import Path

import numpy as np
import pygame as pg

pg.init()
sound_dir = Path(__file__).resolve().parent
glitch_sfx = pg.mixer.Sound(str(sound_dir / "glitch.wav"))
paper_crumple_sfx = pg.mixer.Sound(str(sound_dir / "papercrumple.wav"))
paper_uncrumple_sfx = pg.mixer.Sound(str(sound_dir / "paperunscrunch.wav"))
pencilwrite_sfx = pg.mixer.Sound(str(sound_dir / "pencilwrite.wav"))
glitch_channel = pg.mixer.Channel(0)
respawn_channel = pg.mixer.Channel(1)
spawn_channel = pg.mixer.Channel(2)
wid, hig = 1000, 500
scr = pg.display.set_mode((wid, hig))
pg.display.set_caption('gem')
clk = pg.time.Clock()

try:
    qG = pg.image.load("heheehe.png").convert_alpha()
    vz = pg.transform.smoothscale(qG, (wid, hig))
except Exception:
    vz = pg.Surface((wid, hig))
    vz.fill((0, 0, 0))


def load_fnt(xk, vh, qV=False):
    qJ = set(pg.font.get_fonts())
    for n in xk:
        key = n.lower().replace(" ", "")
        if key in qJ:
            return pg.font.SysFont(n, vh, bold=qV)
    return pg.font.SysFont(None, vh, bold=qV)


zx = {
    "default": (
        load_fnt(["consolas", "dejavusansmono", "monospace"], 16),
        load_fnt(["consolas", "dejavusansmono", "monospace"], 22),
        load_fnt(["consolas", "dejavusansmono", "monospace"], 36, qV=True),
    ),
    "glitch": (
        load_fnt(["fixedsys", "terminal", "couriernew", "lucidaconsole", "dejavusansmono"], 16, qV=True),
        load_fnt(["fixedsys", "terminal", "couriernew", "lucidaconsole", "dejavusansmono"], 22, qV=True),
        load_fnt(["fixedsys", "terminal", "couriernew", "lucidaconsole", "dejavusansmono"], 34, qV=True),
    ),
    "paper": (
        load_fnt(["georgia", "cambria", "timesnewroman", "dejavuserif", "consolas"], 16),
        load_fnt(["georgia", "cambria", "timesnewroman", "dejavuserif", "consolas"], 22),
        load_fnt(["georgia", "cambria", "timesnewroman", "dejavuserif", "consolas"], 34, qV=True),
    ),
}

xZ = pg.Surface((wid, hig), pg.SRCALPHA)
for _y in range(0, hig, 4):
    pg.draw.line(xZ, (0, 0, 0, 65), (0, _y), (wid, _y), 1)

vO = {
    "glitch": {
        "label": "404: PARCEL NOT FOUND",
        "fnt_key": "glitch",
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
        "fnt_key": "paper",
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
        "fnt_key": "paper",
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

xv = ["glitch", "blueprint", "parchment"]
vM = 0
vN = xv[vM]
T = vO[vN]
fnt, qT, vS = zx[T["fnt_key"]]


def set_theme(xo):
    global vN, vM, T, fnt, qT, vS
    vN = xo
    vM = xv.index(xo)
    T = vO[vN]
    fnt, qT, vS = zx[T["fnt_key"]]

    vt = 0
    zS = 0
    zh = ""
    xC = 0
    for b in qU:
        if b["kind"] == "hole":
            zS += 1
            b["name"] = f"{T['hole_prefix']}-{zS}"
        elif b["kind"] == "star":
            vt += 1
            xC = 0
            zh = f"{T['star_prefix']}-{vt}"
            b["name"] = zh
        elif b["kind"] == "planet":
            b["name"] = f"{zh}{'bcde'[xC % 4]}"
            xC += 1

    if xe and xe.get("target") is not None:
        q9 = T["cargos"]
        xe["cargo"] = q9[min(mi, len(q9) - 1)]

    if vx is not None:
        if zj == 0 and zq == "none":
            if zB == "freeroam":
                vx["title"] = "FREE ROAM"
                vx["text"] = T["free_intro"]
            else:
                vx["title"] = T["menu_title"]
                vx["text"] = T["intro"]
        elif zq == "good":
            vx["title"] = T["end_good_title"]
            vx["text"] = T["end_good"]
        elif zq == "quiet":
            vx["title"] = T["end_quiet_title"]
            vx["text"] = T["end_quiet"]


qj = 1600.0
qo = 1350.0
qw = 8
qv = 6
qi = 3.0
G = 45.0
qp = 1.0
qu = 900.0
qb = 10.0


def make_sphere(xH=1.0, z4=8, z6=12):
    v2, zp = [], []
    for i in range(z4 + 1):
        lat = np.pi * (-0.5 + i / z4)
        y = xH * np.sin(lat)
        r = xH * np.cos(lat)
        for j in range(z6):
            lon = 2 * np.pi * j / z6
            v2.append([r * np.cos(lon), y, r * np.sin(lon), 1.0])
    for i in range(z4 + 1):
        for j in range(z6):
            zi = i * z6 + j
            nxt = i * z6 + (j + 1) % z6
            zp.append([zi, nxt])
            if i < z4:
                zp.append([zi, (i + 1) * z6 + j])
    return np.array(v2, dtype=float), np.array(zp, dtype=int)


def make_ship():
    v2 = np.array([
        [0.00, 0.00, 0.55, 1.0],
        [-0.32, -0.05, -0.35, 1.0],
        [0.32, -0.05, -0.35, 1.0],
        [0.00, 0.14, -0.25, 1.0],
    ], dtype=float)
    zp = np.array([[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]], dtype=int)
    return v2, zp


def make_ring(n=72):
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    v2 = np.stack([np.cos(a), np.zeros(n), np.sin(a), np.ones(n)], axis=1)
    zp = np.array([[i, (i + 1) % n] for i in range(n)], dtype=int)
    return v2, zp


def make_octa():
    v2 = np.array([
        [1, 0, 0, 1], [-1, 0, 0, 1], [0, 1, 0, 1],
        [0, -1, 0, 1], [0, 0, 1, 1], [0, 0, -1, 1]
    ], dtype=float)
    zp = np.array([
        [0, 2], [0, 3], [0, 4], [0, 5], [1, 2], [1, 3],
        [1, 4], [1, 5], [2, 4], [2, 5], [3, 4], [3, 5]
    ], dtype=int)
    return v2, zp


def make_grid(vh=48.0, vw=qi):
    zg = np.arange(-vh, vh + vw / 2, vw)
    v2, zp = [], []
    idx = 0
    for c in zg:
        for k in range(len(zg) - 1):
            v2.append([c, 0.0, zg[k], 1.0])
            v2.append([c, 0.0, zg[k + 1], 1.0])
            zp.append([idx, idx + 1])
            idx += 2
            v2.append([zg[k], 0.0, c, 1.0])
            v2.append([zg[k + 1], 0.0, c, 1.0])
            zp.append([idx, idx + 1])
            idx += 2
    return np.array(v2, dtype=float), np.array(zp, dtype=int)


qN, zE = make_grid()
vp, vo = make_sphere(1.0, 8, 14)
vd, vb = make_ship()
xT, xS = make_ring()
xt, xr = make_octa()


def hsv(h, s=65, v=100):
    c = pg.Color(0, 0, 0)
    c.hsva = (h % 360, s, v, 100)
    return (c.r, c.g, c.b)


def themed_body_color(b):
    if b["kind"] == "hole":
        return T["hole_core"]
    if vN == "glitch":
        return (120, 255, 150) if b["kind"] == "star" else (55, 225, 100)
    if vN == "blueprint":
        return (255, 240, 145) if b["kind"] == "star" else (210, 232, 255)
    if vN == "parchment":
        return (180, 95, 20) if b["kind"] == "star" else (35, 55, 95)
    return b["color"]


def gen_galaxy(x4):
    rng = np.random.default_rng(x4)
    qU = []
    vg = [(0.0, 0.0, 120.0)]

    for k in range(qv):
        a = 2 * np.pi * k / qv + 0.3
        x, z = qo * np.cos(a), qo * np.sin(a)
        vg.append((x, z, 90.0))
        qU.append(dict(
            name=f"{T['hole_prefix']}-{k + 1}", kind="hole", pos=np.array([x, 0.0, z]),
            vel=np.zeros(3), radius=4.0, mass=320.0, well_depth=600.0,
            soft=10.0, color=(170, 90, 255), parent=-1,
            orbit_r=0.0, speed=0.0, angle=0.0
        ))

    zb, xB, vX = 330.0, 0, 0
    while xB < qw and vX < 9000:
        vX += 1
        if vX % 1500 == 0:
            zb -= 25.0
        x, z = rng.uniform(-qj * 0.9, qj * 0.9, 2)
        if not all(np.hypot(x - sx, z - sz) > zb + sr for sx, sz, sr in vg):
            continue
        vg.append((x, z, zb))
        xB += 1
        vD = rng.uniform(2.0, 4.0)
        vC = vD * 60.0
        vB = len(qU)
        vj = f"{T['star_prefix']}-{xB}"
        qU.append(dict(
            name=vj, kind="star", pos=np.array([x, 0.0, z]),
            vel=np.zeros(3), radius=vD * 5.0, mass=vC,
            well_depth=vC * 4.0, soft=vD * 10.0,
            color=hsv(rng.uniform(20, 60), 70, 100), parent=-1,
            orbit_r=0.0, speed=0.0, angle=0.0
        ))
        xj = int(rng.integers(1, 5))
        for i in range(xj):
            orb = 90.0 + i * 55.0 + rng.uniform(0, 15)
            pr = rng.uniform(0.7, 1.8)
            pm = pr * 18.0
            vf = 1.0 if rng.random() < 0.8 else -1.0
            qU.append(dict(
                name=f"{vj}{'bcde'[i]}", kind="planet", pos=np.array([x, 0.0, z]),
                vel=np.zeros(3), radius=pr * 2.5, ring=bool(rng.random() < 0.3),
                mass=pm, well_depth=pm * 1.5, soft=6.0 + pr * 3.0,
                color=hsv(rng.uniform(0, 360), 60, 100), parent=vB, orbit_r=orb,
                speed=vf * np.sqrt(G * vC / ((orb ** 2 + (vD * 10.0) ** 2) * orb)) * rng.uniform(0.9, 1.1),
                angle=rng.uniform(0, 2 * np.pi), relay=False
            ))
        qU[vB + 1 + int(rng.integers(xj))]["relay"] = True
    return qU


def update_orbits(dt):
    for b in qU:
        if b["parent"] >= 0:
            P = qU[b["parent"]]["pos"]
            b["angle"] += b["speed"] * dt
            ca, sa = np.cos(b["angle"]), np.sin(b["angle"])
            b["pos"][0] = P[0] + ca * b["orbit_r"]
            b["pos"][2] = P[2] + sa * b["orbit_r"]
            b["vel"] = np.array([-sa * b["orbit_r"] * b["speed"], 0.0, ca * b["orbit_r"] * b["speed"]])


def rebuild_static():
    global BM, BS2, BWD, qa, HOR, BRV, qq, qr
    BM = np.array([b["mass"] for b in qU])
    BS2 = np.array([b["soft"] ** 2 for b in qU])
    BWD = np.array([b["well_depth"] for b in qU])
    qa = np.array([0.0 if b["kind"] == "hole" else b["radius"] * 1.15 for b in qU])
    HOR = np.array([b["radius"] if b["kind"] == "hole" else 0.0 for b in qU])
    BRV = np.array([b["radius"] for b in qU])
    qq = np.array([b["kind"] == "hole" for b in qU])
    qr = np.array([b["kind"] == "planet" for b in qU])


def refresh_positions():
    global BP
    BP = np.array([b["pos"] for b in qU])


def wells_height(xs, zs):
    dx = xs[:, None] - BP[None, :, 0]
    dz = zs[:, None] - BP[None, :, 2]
    return -2.0 - (BWD / np.sqrt(dx * dx + dz * dz + BS2)).sum(axis=1)


def grid_height_at(x, z):
    return wells_height(np.array([x]), np.array([z]))[0]


qE = True


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


def draw_mesh(v1, zp, xg, v3, xE, zd, v4=1, z8=38.0):
    zc = v1 @ xg @ v3 @ xE
    xn = 0.1
    qM = np.array(zd, dtype=float)
    qQ = np.array(T["bg"], dtype=float)
    p1 = zc[zp[:, 0]]
    p2 = zc[zp[:, 1]]
    w1, w2 = p1[:, 3], p2[:, 3]
    v0 = (w1 >= xn) | (w2 >= xn)
    p1, p2, w1, w2 = p1[v0], p2[v0], w1[v0], w2[v0]
    c1 = w1 < xn
    if np.any(c1):
        t1 = ((xn - w1[c1]) / (w2[c1] - w1[c1]))[:, None]
        p1[c1] = p1[c1] + t1 * (p2[c1] - p1[c1])
    c2 = w2 < xn
    if np.any(c2):
        t2 = ((xn - w2[c2]) / (w1[c2] - w2[c2]))[:, None]
        p2[c2] = p2[c2] + t2 * (p1[c2] - p2[c2])
    qK = 0.5 * (p1[:, 3] + p2[:, 3])
    zY = qK < z8
    p1, p2, qK = p1[zY], p2[zY], qK[zY]
    qZ = np.clip(1.0 - (qK / z8), 0.0, 1.0)[:, None]
    ze = (qQ + (qM - qQ) * qZ).astype(int)
    xl = p1[:, :2] / p1[:, 3:4]
    xm = p2[:, :2] / p2[:, 3:4]
    x1 = (xl[:, 0] + 1) * 0.5 * wid
    y1 = (1 - xl[:, 1]) * 0.5 * hig
    x2 = (xm[:, 0] + 1) * 0.5 * wid
    y2 = (1 - xm[:, 1]) * 0.5 * hig
    pad = 30.0
    vis = ~(((x1 < -pad) & (x2 < -pad)) | ((x1 > wid + pad) & (x2 > wid + pad)) |
            ((y1 < -pad) & (y2 < -pad)) | ((y1 > hig + pad) & (y2 > hig + pad)))
    vis &= (np.abs(x1) < 1e5) & (np.abs(x2) < 1e5) & (np.abs(y1) < 1e5) & (np.abs(y2) < 1e5)
    x1, y1, x2, y2, ze = x1[vis], y1[vis], x2[vis], y2[vis], ze[vis]
    X1, Y1, X2, Y2, CL = x1.tolist(), y1.tolist(), x2.tolist(), y2.tolist(), ze.tolist()
    if not qE or vN == "glitch":
        for i in range(len(X1)):
            pg.draw.line(scr, CL[i], (round(X1[i]), round(Y1[i])), (round(X2[i]), round(Y2[i])), v4)
    elif v4 <= 1:
        for i in range(len(X1)):
            pg.draw.aaline(scr, CL[i], (X1[i], Y1[i]), (X2[i], Y2[i]))
    else:
        d = np.hypot(x2 - x1, y2 - y1) + 1e-6
        NX, NY = (-(y2 - y1) / d).tolist(), ((x2 - x1) / d).tolist()
        xu = [k - (v4 - 1) / 2 for k in range(v4)]
        for i in range(len(X1)):
            for o in xu:
                pg.draw.aaline(
                    scr, CL[i],
                    (X1[i] + NX[i] * o, Y1[i] + NY[i] * o),
                    (X2[i] + NX[i] * o, Y2[i] + NY[i] * o)
                )


qd = 1337
qA = 0.5
qt, qC, qD = 2.4, 2.2, 1.8
qc = np.radians(60)
qB = 0.4
qy = 150.0
qz = 20.0
qh = 32
qe = 2 * qj / qh
_cc = -qj + (np.arange(qh) + 0.5) * qe
qf, qg = np.meshgrid(_cc, _cc, indexing="ij")

zC = "menu"
zB = "delivery"
xc = 0


def set_mouse_capture(q8):
    pg.event.set_grab(q8)
    pg.mouse.set_visible(not q8)
    pg.mouse.get_rel()


def new_mission():
    global xe
    if zB == "freeroam" or mi >= len(xO):
        xe = dict(target=None, cargo="", t=0.0)
    else:
        q9 = T["cargos"]
        xe = dict(target=xO[mi], cargo=q9[min(mi, len(q9) - 1)], t=0.0)


def reset_world(x5):
    global qU, vc, vel, vU, xW, xf, z3, zf
    global zm, zt, xY, mi, xO, xN, qs
    global vx, log, zq, zj, ve, qL
    qU = gen_galaxy(x5)
    rebuild_static()
    refresh_positions()
    qs = np.array([b["kind"] == "star" for b in qU])
    vc = np.array([0.0, grid_height_at(0.0, 0.0) + qp, 0.0])
    xW = np.array([0.0, 0.0, 0.0])
    vel = np.zeros(3)
    vU = []
    xf, z3, zf = "fly", None, 0.0
    qL = 0.0
    zm = np.zeros(len(qU), dtype=bool)
    zt = np.zeros((qh, qh), dtype=bool)
    xY = qy
    xP = [i for i, b in enumerate(qU) if b.get("relay")]
    xO = sorted(xP, key=lambda i: np.hypot(*qU[qU[i]["parent"]]["pos"][[0, 2]]))
    xN = set()
    mi, zj, zq, ve = 0, 0, "none", False
    log = []
    vx = None
    if zB == "freeroam":
        zm[:] = True
        zt[:] = True
        new_mission()
        push_story("FREE ROAM", T["free_intro"], 10.0)
    else:
        new_mission()
        push_story(T["menu_title"], T["intro"], 16.0)
    if vN in ("blueprint", "parchment"):
        spawn_channel.play(pencilwrite_sfx)


def start_mode(x7):
    global zB, zC, xc
    zB = x7
    x4 = qd if zB == "delivery" else random.randint(10000, 9999999)
    reset_world(x4)
    zC = "play"
    xc = 0
    set_mouse_capture(True)


def push_story(vR, vK, x0=12.0):
    global vx
    vx = dict(title=vR, text=vK, t=x0)
    log.append((vR, vK))


qU = []
vc = np.zeros(3)
vel = np.zeros(3)
vU = []
xW = np.zeros(3)
xe = {}
xf, z3, zf = "fly", None, 0.0
msg, xh = "", 0.0
zm = np.zeros(0, dtype=bool)
zt = np.zeros((qh, qh), dtype=bool)
xY, mi, xO, xN = qy, 0, [], set()
qs = np.zeros(0, dtype=bool)
vx, log, zq, zj, ve = None, [], "none", 0, False

reset_world(qd)
vx = None
set_mouse_capture(False)
yaw, xA, qL = 0.0, 0.35, 0.0
x8 = 0.003
xE = p(70)
zV = np.eye(4)
vW = 0.0
q5 = 3.6
xU = True


def say(vK, x0=3.0):
    global msg, xh
    msg, xh = vK, x0


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


def surface_basis(u, zK):
    fw = zK - u * np.dot(zK, u)
    if np.linalg.norm(fw) < 1e-3:
        fw = np.cross(u, np.array([0.0, 0.0, 1.0]))
    fw = unit(fw)
    return np.cross(u, fw), u, fw


def reveal_system(vs):
    for j, b in enumerate(qU):
        if j == vs or b["parent"] == vs:
            zm[j] = True


def reveal_area(x, z, rad):
    global zt
    zt |= np.hypot(qf - x, qg - z) < rad
    zm[np.hypot(BP[:, 0] - x, BP[:, 2] - z) < rad] = True


def wrap_text(vK, fnt, xb):
    z5 = []
    for xx in vK.split("\n"):
        cur = ""
        for w in xx.split(" "):
            t = (cur + " " + w).strip()
            if fnt.size(t)[0] <= xb:
                cur = t
            else:
                z5.append(cur)
                cur = w
        z5.append(cur)
    return z5


def draw_panel(vR, vK, vQ=None):
    if vQ is None:
        vQ = T["accent"]
    z5 = wrap_text(vK, fnt, wid - 160)
    h = 46 + 20 * len(z5)
    top = hig - h - 16
    vE = pg.Surface((wid - 120, h), pg.SRCALPHA)
    vE.fill(T["panel_bg"])
    scr.blit(vE, (60, top))
    pg.draw.rect(scr, vQ, (60, top, wid - 120, h), 1)
    scr.blit(fnt.render(vR, True, vQ), (76, top + 8))
    for k, l in enumerate(z5):
        scr.blit(fnt.render(l, True, T["panel_text"]), (76, top + 34 + 20 * k))


def draw_arrow(tx, tz):
    dx, dz = tx - vc[0], tz - vc[2]
    f = dx * np.sin(yaw) + dz * np.cos(yaw)
    r = dx * np.cos(yaw) - dz * np.sin(yaw)
    d = np.array([r, -f])
    d = d / max(np.linalg.norm(d), 1e-6)
    c = np.array([wid / 2, 70.0])
    tip, vH = c + d * 26, c - d * 14
    xz = np.array([-d[1], d[0]])
    col = T["accent"]
    pg.draw.line(scr, col, vH, tip, 3)
    pg.draw.line(scr, col, tip, tip - d * 12 + xz * 8, 3)
    pg.draw.line(scr, col, tip, tip - d * 12 - xz * 8, 3)


qm = 78
qn = qm * 2
qk = [
    (qm + qm * np.cos(np.radians(60 * i)),
     qm + qm * np.sin(np.radians(60 * i)))
    for i in range(6)
]
ql = pg.Surface((qn, qn), pg.SRCALPHA)
pg.draw.polygon(ql, (255, 255, 255, 255), qk)


def clamp_to_hex(px, py, cx, cy, z9):
    dx, dy = px - cx, py - cy
    ang = np.arctan2(dy, dx)
    x3 = (ang + np.pi) % (np.pi / 3) - (np.pi / 6)
    zO = (z9 * np.cos(np.pi / 6)) / max(np.cos(x3), 1e-5)
    zo = np.hypot(dx, dy)
    if zo > zO:
        xX = zO / zo
        return int(cx + dx * xX), int(cy + dy * xX)
    return int(px), int(py)


def draw_minimap():
    rx, ry = wid - qn - 16, 12
    cx, cy = rx + qm, ry + qm
    img = np.where(zt[:, :, None], np.array(T["fog_explored"]), np.array(T["fog_unexplored"])).astype(np.uint8)
    zy = pg.Surface((qh, qh))
    pg.surfarray.blit_array(zy, np.ascontiguousarray(img[:, ::-1]))
    z7 = pg.transform.smoothscale(zy, (qn, qn)).convert_alpha()
    vm = qj * 2.0

    if vN in ("blueprint", "parchment"):
        zD = (150, 185, 235, 55) if vN == "blueprint" else (70, 75, 85, 45)
        zJ = (180, 210, 250, 75) if vN == "blueprint" else (120, 125, 135, 70)
        for g in range(0, qn, 16):
            pg.draw.line(z7, zD, (g, 0), (g, qn), 1)
            pg.draw.line(z7, zD, (0, g), (qn, g), 1)
        za = qn / qh
        for ix in range(qh):
            for iz in range(qh):
                if not zt[ix, iz]:
                    px0 = int(ix * za)
                    py0 = int((qh - 1 - iz) * za)
                    pg.draw.line(z7, zJ, (px0, py0), (px0 + int(za), py0 + int(za)), 1)

    def tomap_local(x, z):
        return int((x + qj) / vm * qn), int((1 - (z + qj) / vm) * qn)

    zU = [qU[i] for i in range(len(qU)) if qU[i]["kind"] == "hole"]
    if zq == "good":
        pg.draw.lines(z7, T["map_hole"], True, [tomap_local(h["pos"][0], h["pos"][2]) for h in zU], 1)
    for i, b in enumerate(qU):
        if not zm[i]:
            continue
        pt = tomap_local(b["pos"][0], b["pos"][2])
        if b["kind"] == "star":
            pg.draw.circle(z7, T["map_star"], pt, 3)
        elif b["kind"] == "hole":
            pg.draw.circle(z7, T["map_hole"], pt, 3, 1)
        elif i in xN:
            pg.draw.circle(z7, T["accent2"], pt, 3, 1)
        else:
            pg.draw.circle(z7, themed_body_color(b), pt, 1)

    z7.blit(ql, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
    scr.blit(z7, (rx, ry))
    zP = [(rx + x, ry + y) for x, y in qk]
    pg.draw.polygon(scr, T["accent"], zP, 2)

    tgt = xe["target"]
    if tgt is not None:
        if zm[tgt]:
            tx, ty = tomap_local(qU[tgt]["pos"][0], qU[tgt]["pos"][2])
            pg.draw.circle(scr, T["accent"], clamp_to_hex(rx + tx, ry + ty, cx, cy, qm - 4), 6, 1)
        else:
            vr = qU[qU[tgt]["parent"]]["pos"]
            sx, sy = tomap_local(vr[0], vr[2])
            pg.draw.circle(scr, T["accent"], clamp_to_hex(rx + sx, ry + sy, cx, cy, qm - 6), 11, 1)
    px, py = tomap_local(vc[0], vc[2])
    pg.draw.circle(scr, T["accent2"], clamp_to_hex(rx + px, ry + py, cx, cy, qm - 3), 3)


def apply_glitch_fx(zT):
    if vN != "glitch":
        return
    scr.blit(xZ, (0, 0))
    if zT > 0.0:
        if random.random() < 0.25 + 0.55 * zT:
            vy = 1 + int(zT * 5)
            xa = int(12 + 30 * zT)
            for _ in range(vy):
                sh = random.randint(4, 18)
                sy = random.randint(0, hig - sh)
                x9 = random.randint(-xa, xa)
                row = scr.subsurface((0, sy, wid, sh)).copy()
                scr.blit(row, (x9, sy))
        if random.random() < 0.12 * zT:
            zv = pg.Surface((wid, hig), pg.SRCALPHA)
            zv.fill((255, 30, 30, int(35 * zT)))
            scr.blit(zv, (0, 0))


def get_menu_items():
    vL = f"Active: {T['label']}  (Click or LEFT/RIGHT to switch)"
    if zC == "paused":
        return [
            ("RESUME FLIGHT", "Return to active cockpit"),
            ("SET DELIVERY", "Start story campaign (fixed galaxy)"),
            ("FREE ROAM", "Generate a random galaxy to explore"),
            ("THEME", vL),
            ("QUIT", "Exit to desktop"),
        ]
    return [
        ("SET DELIVERY", "8-stop story campaign in a fixed galaxy"),
        ("FREE ROAM", "Explore a freshly generated random galaxy"),
        ("THEME", vL),
        ("QUIT", "Exit to desktop"),
    ]


def cycle_theme(vw=1):
    nxt = xv[(vM + vw) % len(xv)]
    set_theme(nxt)


def execute_menu_option(z2):
    global zC, xU
    if z2 == "RESUME FLIGHT":
        zC = "play"
        set_mouse_capture(True)
    elif z2 == "SET DELIVERY":
        start_mode("delivery")
    elif z2 == "FREE ROAM":
        start_mode("freeroam")
    elif z2 == "THEME":
        cycle_theme(1)
    elif z2 == "QUIT":
        xU = False


def draw_menu_overlay():
    xw = pg.Surface((wid, hig), pg.SRCALPHA)
    qS, qR, qP = T["bg"]
    xw.fill((qS, qR, qP, 195))
    scr.blit(xw, (0, 0))

    zX = get_menu_items()
    xi = len(zX)
    q3 = 42 if xi <= 4 else 38
    q0 = 6
    zL = 84
    zz = 30
    qY = 620
    qX = zL + xi * (q3 + q0) - q0 + zz
    bx = (wid - qY) // 2
    by = max(8, (hig - qX) // 2)

    pg.draw.rect(scr, T["menu_bg"], (bx, by, qY, qX))
    pg.draw.rect(scr, T["accent"], (bx, by, qY, qX), 2)

    zM = "SYSTEM PAUSED" if zC == "paused" else T["menu_title"]
    sub = f"ACTIVE MODE: {zB.upper()}" if zC == "paused" else T["menu_sub"]
    vG = vS.render(zM, True, T["accent"])
    xV = fnt.render(sub, True, T["text"])
    scr.blit(vG, (wid // 2 - vG.get_width() // 2, by + 12))
    scr.blit(xV, (wid // 2 - xV.get_width() // 2, by + 52))

    q4 = []
    vu = by + zL
    for idx, (z2, zk) in enumerate(zX):
        xJ = pg.Rect(bx + 28, vu + idx * (q3 + q0), qY - 56, q3)
        q4.append((xJ, z2, idx))
        x6 = (idx == xc)
        bg = T["btn_sel"] if x6 else T["btn_bg"]
        qW = T["accent2"] if x6 else T["btn_border"]
        pg.draw.rect(scr, bg, xJ)
        pg.draw.rect(scr, qW, xJ, 2 if x6 else 1)
        xD = "> " if x6 else "  "
        zn = f"THEME: < {T['label']} >" if z2 == "THEME" else z2
        z1 = T["accent2"] if x6 else T["text"]
        scr.blit(qT.render(xD + zn, True, z1), (xJ.x + 10, xJ.y + 1))
        scr.blit(fnt.render(zk, True, T["text_dim"]), (xJ.x + 32, xJ.y + q3 - 19))

    zQ = "UP/DOWN or MOUSE select  |  LEFT/RIGHT theme  |  ENTER/CLICK confirm"
    if zC == "paused":
        zQ += "  |  ESC resume"
    zH = fnt.render(zQ, True, T["text_dim"])
    scr.blit(zH, (wid // 2 - zH.get_width() // 2, by + qX - 22))
    return q4


q4 = []
vA=True
while xU:
    dt = min(clk.tick(60) / 1000.0, 0.05)
    vF = pg.time.get_ticks() * 0.001
    for zr in pg.event.get():
        if zr.type == pg.QUIT:
            xU = False
        elif vA and (
            (zr.type == pg.KEYDOWN and zr.key in (pg.K_RETURN, pg.K_SPACE, pg.K_ESCAPE))
            or (zr.type == pg.MOUSEBUTTONDOWN and zr.button == 1)
        ):
            vA = False
        elif zC in ("menu", "paused") and not vA:
            zX = get_menu_items()
            if zr.type == pg.MOUSEMOTION:
                for xJ, _, idx in q4:
                    if xJ.collidepoint(zr.pos):
                        xc = idx
            elif zr.type == pg.MOUSEBUTTONDOWN and zr.button == 1:
                for xJ, z2, idx in q4:
                    if xJ.collidepoint(zr.pos):
                        xc = idx
                        execute_menu_option(z2)
            elif zr.type == pg.KEYDOWN:
                if zr.key in (pg.K_UP, pg.K_w):
                    xc = (xc - 1) % len(zX)
                elif zr.key in (pg.K_DOWN, pg.K_s):
                    xc = (xc + 1) % len(zX)
                elif zr.key in (pg.K_LEFT, pg.K_a):
                    cycle_theme(-1)
                elif zr.key in (pg.K_RIGHT, pg.K_d, pg.K_t):
                    cycle_theme(1)
                elif zr.key in (pg.K_RETURN, pg.K_SPACE):
                    execute_menu_option(zX[xc][0])
                elif zr.key == pg.K_ESCAPE and zC == "paused":
                    zC = "play"
                    set_mouse_capture(True)
        elif zC == "play":
            if zr.type == pg.MOUSEMOTION:
                dx, dy = zr.rel
                yaw += dx * x8
                xA = np.clip(xA + dy * x8, 0.05, 1.35)
            elif zr.type == pg.KEYDOWN:
                if zr.key == pg.K_ESCAPE:
                    zC = "paused"
                    xc = 0
                    set_mouse_capture(False)
                elif zr.key == pg.K_t:
                    cycle_theme(1)
                    say(f"THEME: {T['label']}", 2.0)
                elif zr.key == pg.K_r:
                    x4 = qd if zB == "delivery" else random.randint(10000, 9999999)
                    reset_world(x4)
                    say("NEW GALAXY GENERATED" if zB == "freeroam" else "RESTARTED")
                elif zr.key == pg.K_SPACE and zq in ("none", "good", "quiet"):
                    vx = None
                elif zr.key == pg.K_TAB:
                    ve = not ve
                elif zq == "choice" and zr.key in (pg.K_1, pg.K_2):
                    if zr.key == pg.K_1:
                        zq = "good"
                        zm[:] = True
                        zt[:] = True
                        push_story(T["end_good_title"], T["end_good"], 40.0)
                    else:
                        zq = "quiet"
                        push_story(T["end_quiet_title"], T["end_quiet"], 40.0)

    if zC == "menu":
        yaw += 0.12 * dt

    if zC in ("play", "menu"):
        update_orbits(dt)
        refresh_positions()

    if zC == "play":
        xe["t"] += dt
        xh = max(0.0, xh - dt)
        zf -= dt
        if vx is not None and zq != "choice":
            vx["t"] -= dt
            if vx["t"] <= 0:
                vx = None

    zN = wells_height(BP[:, 0], BP[:, 2])
    BC = BP.copy()
    BC[:, 1] = zN + np.where(qq, 1.5, 1.0 + BRV * 0.4)

    if zC == "play":
        dxz = np.hypot(BP[:, 0] - vc[0], BP[:, 2] - vc[2])
        zm |= dxz < xY * np.where(qs, 1.6, 1.0)
        zt |= np.hypot(qf - vc[0], qg - vc[2]) < xY * 1.2
        zA = np.array([np.sin(yaw), 0.0, np.cos(yaw)])
        xQ = np.array([np.cos(yaw), 0.0, -np.sin(yaw)])
        zZ = pg.key.get_pressed()
        zl = BP - vc
        zl[:, 1] = 0.0
        d2 = (zl * zl).sum(axis=1)
        zo = np.sqrt(d2) + 1e-6

        if xf == "fly":
            vP = 22.0
            if zZ[pg.K_w]:
                vel += zA * vP * dt
            if zZ[pg.K_s]:
                vel -= zA * vP * dt
            if zZ[pg.K_d]:
                vel += xQ * vP * dt
            if zZ[pg.K_a]:
                vel -= xQ * vP * dt
            if zf <= 0:
                for i in np.nonzero(qr & (zo < qa + 3.5))[0]:
                    if np.linalg.norm(vel - qU[i]["vel"]) < qb:
                        C = BC[i]
                        A = vc - C
                        xG = max(float(np.linalg.norm(A)), 1e-4)
                        z3 = dict(
                            idx=int(i), t0=vF, timer=0.0, rad0=xG,
                            az0=np.arctan2(A[2], A[0]),
                            el0=np.arcsin(np.clip(A[1] / xG, -1.0, 1.0)),
                            head0=zA.copy()
                        )
                        xf = "landing"
                        break

        if xf == "fly":
            qH = G * BM / (d2 + BS2)
            xF = zo >= qa
            vel += ((zl / zo[:, None]) * (qH * xF)[:, None]).sum(axis=0) * dt
            for i in np.nonzero(~xF)[0]:
                xp = -zl[i] / max(zo[i], 0.001)
                vc[0] = BP[i][0] + xp[0] * qa[i]
                vc[2] = BP[i][2] + xp[2] * qa[i]
                vel *= 0.85
            if np.any(zo < HOR):
                if vN in ("blueprint", "parchment"):
                    respawn_channel.play(paper_crumple_sfx)
                    respawn_channel.queue(paper_uncrumple_sfx)
                else:
                    respawn_channel.play(paper_uncrumple_sfx)
                vc[0], vc[2] = xW[0], xW[2]
                vel[:] = 0.0
                vU.clear()
                xe["t"] += 15.0
                say(T["spaghetti_msg"], 4.0)
            vc += vel * dt
            vc[1] = grid_height_at(vc[0], vc[2]) + qp
    else:
        zl = BP - vc
        zl[:, 1] = 0.0
        zo = np.sqrt((zl * zl).sum(axis=1)) + 1e-6
        zA = np.array([np.sin(yaw), 0.0, np.cos(yaw)])
        zZ = pg.key.get_pressed()

    zR = zo[qq]
    xd = float(zR.min()) if len(zR) else 9999.0
    zT = float(np.clip(1.0 - (xd - 10.0) / 140.0, 0.0, 1.0))
    if zC == "play" and vN == "glitch" and zT > 0.0:
        glitch_channel.set_volume(min(0.65, zT))
        if not glitch_channel.get_busy():
            glitch_channel.play(glitch_sfx)
    else:
        glitch_channel.stop()

    eps = 0.25
    zF = grid_height_at(vc[0] + zA[0] * eps, vc[2] + zA[2] * eps)
    zG = grid_height_at(vc[0] - zA[0] * eps, vc[2] - zA[2] * eps)
    vi = -np.arctan2(zF - zG, 2.0 * eps)
    vI = 0.0
    if zC == "play" and xf == "fly":
        if zZ[pg.K_a]:
            vI += 0.45
        if zZ[pg.K_d]:
            vI -= 0.45
    qL += (vI - qL) * min(1.0, 10.0 * dt)
    _cr, _sr = np.cos(qL), np.sin(qL)
    _cp, _sp = np.cos(vi), np.sin(vi)
    _cy, _sy = np.cos(yaw), np.sin(yaw)
    _ZR = np.array([[_cr, _sr, 0, 0], [-_sr, _cr, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=float)
    _XR = np.array([[1, 0, 0, 0], [0, _cp, _sp, 0], [0, -_sp, _cp, 0], [0, 0, 0, 1]], dtype=float)
    _YR = np.array([[_cy, 0, -_sy, 0], [0, 1, 0, 0], [_sy, 0, _cy, 0], [0, 0, 0, 1]], dtype=float)
    FM = _ZR @ _XR @ _YR
    zw = (FM[0, :3].copy(), FM[1, :3].copy(), FM[2, :3].copy())
    va = zw

    if xf != "fly":
        if zC == "play":
            z3["timer"] += dt
        tm = z3["timer"]
        i = z3["idx"]
        b = qU[i]
        C = BC[i]
        r = b["radius"]
        vq = qB * (vF - z3["t0"])
        az = z3["az0"] - vq
        zK = rot_y(z3["head0"], vq)
        vZ = np.array([np.cos(qc) * np.cos(az), np.sin(qc), np.cos(qc) * np.sin(az)])
        if xf == "landing":
            e = ease(min(tm / qt, 1.0))
            el = z3["el0"] + (qc - z3["el0"]) * e
            rad = z3["rad0"] + (r + 0.05 - z3["rad0"]) * e
            pos = polar(C, az, el, rad)
            va = blend_basis(zw, surface_basis(vZ, zK), e)
            if zC == "play" and tm >= qt:
                xf, z3["timer"] = "landed", 0.0
                if zB == "delivery" and xe["target"] is not None and i == xe["target"]:
                    k = mi
                    zj += 1
                    xY += qz
                    xN.add(i)
                    reveal_system(b["parent"])
                    reveal_area(b["pos"][0], b["pos"][2], 450.0)
                    xW = vc.copy()
                    mi += 1
                    new_mission()
                    vK = f'"{T["fragments"][k]}"'
                    if xe["target"] is not None:
                        vK += "\n\n" + T["guild"][k]
                    push_story(f"DELIVERY {k + 1}/{len(xO)} DONE  -  recipient:", vK, 16.0)
                    if xe["target"] is None:
                        zq = "choice"
                    say(f"DELIVERY {k + 1} DONE - fog lifted, scanners boosted", 4.0)
                else:
                    xW = vc.copy()
                    say(f"Touchdown on {b['name']}" + ("" if zB == "freeroam" else " (no target here)"), 2.5)
        elif xf == "landed":
            pos = C + vZ * (r + 0.05)
            va = surface_basis(vZ, zK)
            if zC == "play" and tm >= qC:
                xf, z3["timer"] = "takeoff", 0.0
        else:
            e = ease(min(tm / qD, 1.0))
            el = qc * (1 - e)
            rad = (r + 0.05) + (r * 1.15 + 3.2 - (r + 0.05)) * e
            pos = polar(C, az, el, rad)
            pos[1] = (1 - e) * pos[1] + e * (grid_height_at(pos[0], pos[2]) + qp)
            vY = np.array([np.cos(el) * np.cos(az), np.sin(el), np.cos(el) * np.sin(az)])
            va = blend_basis(surface_basis(vY, zK), zw, e)
            if zC == "play" and tm >= qD:
                vel = b["vel"] + np.array([np.cos(az), 0.0, np.sin(az)]) * 5.0
                xf, zf = "fly", 4.0
        vc[:] = pos

    q7 = 3.6 if xf == "fly" else 5.2
    if zC == "play":
        q5 += (q7 - q5) * min(1.0, 3.0 * dt)
    q6 = np.array([
        vc[0] - np.sin(yaw) * np.cos(xA) * q5,
        vc[1] + np.sin(xA) * q5 + 0.4,
        vc[2] - np.cos(yaw) * np.cos(xA) * q5
    ])
    vk = np.floor(vc[0] / qi) * qi
    vl = np.floor(vc[2] / qi) * qi
    v5 = qN.copy()
    v5[:, 0] += vk
    v5[:, 2] += vl
    v5[:, 1] = wells_height(v5[:, 0], v5[:, 2])
    v3 = v(q6, (xA, yaw, 0))
    scr.fill(T["bg"])
    draw_mesh(v5, zE, zV, v3, xE, T["grid"], 1, z8=48.0)

    tgt = xe["target"]
    qx = 52.0
    for i, b in enumerate(qU):
        if b["parent"] < 0 or not zm[i]:
            continue
        P = qU[b["parent"]]["pos"]
        R = b["orbit_r"]
        xL, xM = vc[0] - P[0], vc[2] - P[2]
        if abs(np.hypot(xL, xM) - R) > qx + 10:
            continue
        zI = min(np.pi, (qx + 15) / R)
        dth = 1.5 / R
        k0 = int(np.floor(np.arctan2(xM, xL) / dth))
        kn = int(np.ceil(zI / dth)) + 1
        qI = np.arange(k0 - kn, k0 + kn + 1) * dth
        n = len(qI)
        oxs = P[0] + R * np.cos(qI)
        ozs = P[2] + R * np.sin(qI)
        ohs = wells_height(oxs, ozs) + 0.1
        ov = np.stack([oxs, ohs, ozs, np.ones(n)], axis=1)
        oe = np.stack([np.arange(n - 1), np.arange(1, n)], axis=1)
        zW = (i == tgt)
        qO = themed_body_color(b)
        bg = T["bg"]
        col = T["accent"] if zW else tuple(int(bg[c] + (qO[c] - bg[c]) * 0.85) for c in range(3))
        draw_mesh(ov, oe, zV, v3, xE, col, 2, 48.0)

    for i in np.nonzero((zo < 650.0) & zm)[0]:
        b = qU[i]
        r = b["radius"]
        C = BC[i]
        qO = themed_body_color(b)
        if b["kind"] == "hole":
            draw_mesh(vp, vo, m(C, (0, 0, 0), (r, r, r)), v3, xE, qO, 2, 600.0)
            xR = (T["hole_ring1"], T["hole_ring2"])
            for k, sc in enumerate((2.4, 3.4)):
                draw_mesh(
                    xT, xS, m(C, (0.25, vF * (1.5 - k), 0), (r * sc, r * sc, r * sc)),
                    v3, xE, xR[k], 2, 600.0
                )
        elif b["kind"] == "star":
            draw_mesh(vp, vo, m(C, (0, vF * qB, 0), (r, r, r)), v3, xE, qO, 2, 800.0)
            bg = T["bg"]
            dim = tuple(int(bg[c] + (qO[c] - bg[c]) * 0.45) for c in range(3))
            draw_mesh(
                vp, vo, m(C, (0, -vF * 0.2, 0.3), (r * 1.3, r * 1.3, r * 1.3)),
                v3, xE, dim, 1, 800.0
            )
        else:
            xy = T["accent2"] if i in xN else qO
            draw_mesh(vp, vo, m(C, (0, vF * qB, 0), (r, r, r)), v3, xE, xy, 2, 600.0)
            if b.get("ring"):
                bg = T["bg"]
                xI = tuple(int(bg[c] + (qO[c] - bg[c]) * 0.7) for c in range(3))
                draw_mesh(
                    xT, xS, m(C, (0.35, 0, 0.25), (r * 1.8, r * 1.8, r * 1.8)),
                    v3, xE, xI, 1, 600.0
                )
            if zB == "delivery" and b.get("relay") and i not in xN:
                top = C + np.array([0.0, r + 3.0, 0.0])
                draw_mesh(
                    xt, xr, m(top, (0, vF, 0), (0.5, 1.2, 0.5)),
                    v3, xE, T["relay_beacon"], 1, 600.0
                )

    if tgt is not None and zm[tgt]:
        tb_ = qU[tgt]
        vT = BC[tgt].copy()
        vT[1] += tb_["radius"] + 2.5 + np.sin(vF * 2) * 0.3
        draw_mesh(
            xt, xr, m(vT, (0, vF * 1.2, 0), (0.9, 0.9, 0.9)),
            v3, xE, T["accent"], 2, 800.0
        )

    if zC == "play":
        vW += dt
        if vW >= 0.03:
            if xf == "fly":
                vU.append([vc[0], vc[1], vc[2], 1.0])
            elif vU:
                vU.pop(0)
            if len(vU) > 60:
                vU.pop(0)
            vW = 0.0

    if len(vU) > 1:
        pts = np.array(vU)
        zc = pts @ v3 @ xE
        qQ = np.array(T["bg"], dtype=float)
        vV = np.array(T["trail"], dtype=float)
        xq = len(pts) - 1
        for i in range(xq):
            q1, q2 = zc[i], zc[i + 1]
            if q1[3] >= 0.1 and q2[3] >= 0.1:
                n1 = q1[:2] / q1[3]
                n2 = q2[:2] / q2[3]
                x1, y1 = (n1[0] + 1) * 0.5 * wid, (1 - n1[1]) * 0.5 * hig
                x2, y2 = (n2[0] + 1) * 0.5 * wid, (1 - n2[1]) * 0.5 * hig
                if max(abs(x1), abs(x2), abs(y1), abs(y2)) > 1e5:
                    continue
                zu = (i + 1) / xq
                col = tuple((qQ + (vV - qQ) * (zu ** 1.5)).astype(int).tolist())
                ln = max(np.hypot(x2 - x1, y2 - y1), 1e-6)
                nx_, ny_ = -(y2 - y1) / ln * 0.5, (x2 - x1) / ln * 0.5
                pg.draw.aaline(scr, col, (x1 + nx_, y1 + ny_), (x2 + nx_, y2 + ny_))
                pg.draw.aaline(scr, col, (x1 - nx_, y1 - ny_), (x2 - nx_, y2 - ny_))

    draw_mesh(
        vd, vb, basis_matrix(va, vc, qA), v3, xE,
        T["ship"], 2, z8=50.0
    )

    if zC != "menu":
        vn = np.linalg.norm(vel) if xf == "fly" else 0.0
        scr.blit(fnt.render(
            f"SPEED: {vn:05.2f} u/s | POS: ({vc[0]:.0f}, {vc[2]:.0f}) | SCAN: {xY:.0f}",
            True, T["text"]
        ), (16, 16))
        if zB == "freeroam":
            scr.blit(fnt.render("MODE: FREE ROAM (RANDOM MAP)", True, T["accent2"]), (16, 38))
            scr.blit(fnt.render("[ESC] menu  [T] theme  [R] new map  [TAB] log", True, T["text_dim"]), (16, 60))
        elif tgt is not None:
            tb = qU[tgt]
            z0 = bool(zm[tgt])
            aim = tb["pos"] if z0 else qU[tb["parent"]]["pos"]
            vJ = np.hypot(aim[0] - vc[0], aim[2] - vc[2])
            xK = np.linalg.norm(vel - tb["vel"]) if (xf == "fly" and z0) else 0.0
            z2 = tb["name"] if z0 else f"unknown {T['planet_word']} (follow arrow)"
            scr.blit(fnt.render(
                f"DELIVERY {mi + 1}/{len(xO)}: {xe['cargo']}  ->  {z2}",
                True, T["accent"]
            ), (16, 38))
            vv = {"fly": "", "landing": "   << LANDING", "landed": "   << LANDED", "takeoff": "   << TAKEOFF"}[xf]
            if xf == "fly" and z0 and vJ < tb["radius"] * 1.15 + 3.5 + 8:
                vv = "   << SLOW DOWN TO LAND"
            scr.blit(fnt.render(
                f"DIST: {vJ:6.0f}{'' if z0 else ' (approx)'}   REL SPEED: {xK:4.1f} (land < {qb:.0f})   TIME: {xe['t']:5.0f}s{vv}",
                True, T["text"]
            ), (16, 60))
            draw_arrow(aim[0], aim[2])
            scr.blit(fnt.render(
                f"DELIVERED: {zj}/{len(xO)}   [ESC] pause  [T] theme  [TAB] log  [R] restart",
                True, T["text_dim"]
            ), (16, 82))
        else:
            scr.blit(fnt.render(
                "NO ORDERS - FREE FLIGHT" if zq != "choice" else "FINAL RECIPIENT WAITING",
                True, T["accent"]
            ), (16, 38))
            scr.blit(fnt.render(
                f"DELIVERED: {zj}/{len(xO)}   [ESC] pause  [T] theme  [TAB] log  [R] restart",
                True, T["text_dim"]
            ), (16, 60))

    draw_minimap()
    if xh > 0:
        s_ = qT.render(msg, True, T["warn"])
        scr.blit(s_, ((wid - s_.get_width()) // 2, 110))
    if zC == "play":
        if ve and log:
            draw_panel("LOG  [TAB to close]", "\n\n".join(f"{t}: {x}" for t, x in log[-3:]), T["warn"])
        elif zq == "choice":
            draw_panel(T["choice_title"], T["choice_txt"], T["warn"])
        elif vx is not None:
            draw_panel(vx["title"], vx["text"])

    apply_glitch_fx(zT)

    if zC in ("menu", "paused"):
        q4 = draw_menu_overlay()

    if vA:
        scr.blit(vz, (0, 0))
        if int(vF * 2) % 2 == 0:
            qF = fnt.render("[ PRESS ENTER / SPACE OR CLICK TO START ]", True, (220, 220, 220))
            scr.blit(qF, ((wid - qF.get_width()) // 2, hig - 36))

    pg.display.flip()

pg.quit() 