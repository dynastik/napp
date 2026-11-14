import numpy as np
import pygame as pg

pg.init()
wid, hig = 1000, 500
scr = pg.display.set_mode((wid, hig))
pg.display.set_caption('gem')
clk = pg.time.Clock()
font = pg.font.SysFont('consolas', 16)

def make_sphere(radius=1.0, lat_divs=8, lon_divs=12):
    verts = []
    edges = []
    for i in range(lat_divs + 1):
        lat = np.pi * (-0.5 + i / lat_divs)
        y = radius * np.sin(lat)
        r = radius * np.cos(lat)
        for j in range(lon_divs):
            lon = 2 * np.pi * j / lon_divs
            x = r * np.cos(lon)
            z = r * np.sin(lon)
            verts.append([x, y, z, 1.0])
    for i in range(lat_divs + 1):
        for j in range(lon_divs):
            curr = i * lon_divs + j
            nxt = i * lon_divs + (j + 1) % lon_divs
            edges.append([curr, nxt])
            if i < lat_divs:
                below = (i + 1) * lon_divs + j
                edges.append([curr, below])
    return np.array(verts, dtype=float), np.array(edges, dtype=int)

def make_ship():
    verts = np.array([
        [ 0.00,  0.00,  0.55, 1.0], 
        [-0.32, -0.05, -0.35, 1.0], 
        [ 0.32, -0.05, -0.35, 1.0], 
        [ 0.00,  0.14, -0.25, 1.0], 
    ], dtype=float)
    edges = np.array([
        [0, 1], [0, 2], [0, 3],
        [1, 2], [1, 3], [2, 3]
    ], dtype=int)
    return verts, edges

def make_grid(size=38, step=2.0, sub_divs=14):
    grdvrts = []
    grid_edjs = []
    coords = np.arange(-size, size + step, step)
    segs = np.linspace(-size, size, sub_divs + 1)
    idx = 0
    for c in coords:
        for k in range(sub_divs):
            grdvrts.append([c, 0.0, segs[k], 1.0])
            grdvrts.append([c, 0.0, segs[k + 1], 1.0])
            grid_edjs.append([idx, idx + 1])
            idx += 2
            grdvrts.append([segs[k], 0.0, c, 1.0])
            grdvrts.append([segs[k + 1], 0.0, c, 1.0])
            grid_edjs.append([idx, idx + 1])
            idx += 2
    return np.array(grdvrts, dtype=float), np.array(grid_edjs, dtype=int)

base_grdvrts, grid_edjs = make_grid(size=38, step=2.0, sub_divs=14)
sphere_verts, sphere_edges = make_sphere(radius=1.0, lat_divs=8, lon_divs=14)
ship_verts, ship_edges = make_ship()

bodies = [
    {
        "name": "SUN",
        "pos": np.array([0.0, 0.0, 25.0]),
        "radius": 3.0,
        "mass": 90.0,
        "well_depth": 45.0,  
        "soft": 9.0,        
        "color": (255, 210, 80),
        "orbit_r": 0.0,
        "speed": 0.0,
        "angle": 0.0,
    },
    {
        "name": "TERRA",
        "pos": np.array([18.0, 0.0, 25.0]),
        "radius": 1.1,
        "mass": 20.0,
        "well_depth": 18.0, 
        "soft": 4.5,       
        "color": (90, 190, 255),
        "orbit_r": 18.0,
        "speed": 0.35,
        "angle": 0.0,
    },
    {
        "name": "JOVE",
        "pos": np.array([34.0, 0.0, 25.0]),
        "radius": 1.8,
        "mass": 40.0,
        "well_depth": 30.0, 
        "soft": 6.5,       
        "color": (255, 130, 90),
        "orbit_r": 34.0,
        "speed": 0.20,
        "angle": 2.2,
    },
]

def grid_height_at(x, z):
    y = -2.0
    for b in bodies:
        dx = x - b["pos"][0]
        dz = z - b["pos"][2]
        r_sq = dx * dx + dz * dz
        y -= b["well_depth"] / np.sqrt(r_sq + b["soft"] ** 2)
    return y

def m(trn, rot, scl):
    tx, ty, tz = trn
    rx, ry, rz = rot
    sx, sy, sz = scl
    S = np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ], dtype=float)
    T = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [tx, ty, tz, 1]
    ], dtype=float)
    cox, six = np.cos(rx), np.sin(rx)
    coy, siy = np.cos(ry), np.sin(ry)
    coz, siz = np.cos(rz), np.sin(rz)
    XR = np.array([
        [1, 0, 0, 0],
        [0, cox, six, 0],
        [0, -six, cox, 0],
        [0, 0, 0, 1]
    ], dtype=float)
    YR = np.array([
        [coy, 0, -siy, 0],
        [0, 1, 0, 0],
        [siy, 0, coy, 0],
        [0, 0, 0, 1]
    ], dtype=float)
    ZR = np.array([
        [coz, siz, 0, 0],
        [-siz, coz, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=float)
    return S @ (XR @ YR @ ZR) @ T

def v(trn, rot):
    tx, ty, tz = trn
    rx, ry, rz = rot
    T = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [-tx, -ty, -tz, 1]
    ], dtype=float)
    cox, six = np.cos(-rx), np.sin(-rx)
    coy, siy = np.cos(-ry), np.sin(-ry)
    coz, siz = np.cos(-rz), np.sin(-rz)
    XR = np.array([
        [1, 0, 0, 0],
        [0, cox, six, 0],
        [0, -six, cox, 0],
        [0, 0, 0, 1]
    ], dtype=float)
    YR = np.array([
        [coy, 0, -siy, 0],
        [0, 1, 0, 0],
        [siy, 0, coy, 0],
        [0, 0, 0, 1]
    ], dtype=float)
    ZR = np.array([
        [coz, siz, 0, 0],
        [-siz, coz, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=float)
    return T @ (ZR @ YR @ XR)

def p(fov):
    rad = np.radians(fov)
    f = 1.0 / np.tan(rad / 2.0)
    ar = wid / hig
    nr, fr = 0.1, 120.0
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
    cols = (base_col * brightness).astype(int)
    ndc1 = p1[:, :2] / p1[:, 3:4]
    ndc2 = p2[:, :2] / p2[:, 3:4]
    x1 = ((ndc1[:, 0] + 1) * 0.5 * wid).astype(int)
    y1 = ((1 - ndc1[:, 1]) * 0.5 * hig).astype(int)
    x2 = ((ndc2[:, 0] + 1) * 0.5 * wid).astype(int)
    y2 = ((1 - ndc2[:, 1]) * 0.5 * hig).astype(int)
    for i in range(len(x1)):
        pg.draw.line(scr, cols[i], (x1[i], y1[i]), (x2[i], y2[i]), width)

pg.event.set_grab(True)
pg.mouse.set_visible(False)

HOVER_OFFSET = 1 
yaw, pitch = 0.0, 0.35
ship_pos = np.array([0.0, grid_height_at(0.0, 0.0) + HOVER_OFFSET, 0.0])
vel = np.array([0.0, 0.0, 0.0])
sensitivity = 0.003
proj_mat = p(70)
identity_mat = np.eye(4)
trail = []
trail_timer = 0.0
runig = True

while runig:
    dt = min(clk.tick(60) / 1000.0, 0.05)
    t_sec = pg.time.get_ticks() * 0.001

    for evnt in pg.event.get():
        if evnt.type == pg.QUIT:
            runig = False
        if evnt.type == pg.MOUSEMOTION:
            dx, dy = evnt.rel
            yaw += dx * sensitivity
            pitch = np.clip(pitch + dy * sensitivity, 0.05, 1.35)
        if evnt.type == pg.KEYDOWN and evnt.key == pg.K_ESCAPE:
            runig = False

    sun_pos = bodies[0]["pos"]
    for b in bodies[1:]:
        b["angle"] += b["speed"] * dt
        b["pos"][0] = sun_pos[0] + np.cos(b["angle"]) * b["orbit_r"]
        b["pos"][2] = sun_pos[2] + np.sin(b["angle"]) * b["orbit_r"]

    forward = np.array([np.sin(yaw), 0.0, np.cos(yaw)])
    right = np.array([np.cos(yaw), 0.0, -np.sin(yaw)])

    keys = pg.key.get_pressed()
    thrust = 22.0
    if keys[pg.K_w]:
        vel += forward * thrust * dt
    if keys[pg.K_s]:
        vel -= forward * thrust * dt
    if keys[pg.K_d]:
        vel += right * thrust * dt
    if keys[pg.K_a]:
        vel -= right * thrust * dt

    G = 45.0  
    for b in bodies:
        diff = np.array([b["pos"][0] - ship_pos[0], 0.0, b["pos"][2] - ship_pos[2]])
        dist_sq = np.dot(diff, diff)
        dist = np.sqrt(dist_sq)
        if dist > b["radius"] * 1.15:
            accel = (G * b["mass"]) / (dist_sq + b["soft"] ** 2)
            vel += (diff / dist) * accel * dt
        else:
            normal = -diff / max(dist, 0.001)
            ship_pos[0] = b["pos"][0] + normal[0] * (b["radius"] * 1.15)
            ship_pos[2] = b["pos"][2] + normal[2] * (b["radius"] * 1.15)
            vel *= 0.85

    ship_pos += vel * dt
    ship_pos[1] = grid_height_at(ship_pos[0], ship_pos[2]) + HOVER_OFFSET

    eps = 0.25
    h_ahead = grid_height_at(ship_pos[0] + forward[0] * eps, ship_pos[2] + forward[2] * eps)
    h_behind = grid_height_at(ship_pos[0] - forward[0] * eps, ship_pos[2] - forward[2] * eps)
    slope_pitch = -np.arctan2(h_ahead - h_behind, 2.0 * eps)

    bank_roll = 0.0
    if keys[pg.K_a]:
        bank_roll += 0.35
    if keys[pg.K_d]:
        bank_roll -= 0.35

    cam_dist = 3.2
    cam_pos = np.array([
        ship_pos[0] - np.sin(yaw) * np.cos(pitch) * cam_dist,
        ship_pos[1] + np.sin(pitch) * cam_dist + 0.4,
        ship_pos[2] - np.cos(yaw) * np.cos(pitch) * cam_dist
    ])

    step = 2.0
    snap_x = np.floor(ship_pos[0] / step) * step
    snap_z = np.floor(ship_pos[2] / step) * step

    world_grid = base_grdvrts.copy()
    world_grid[:, 0] += snap_x
    world_grid[:, 2] += snap_z
    world_grid[:, 1] = -2.0

    for b in bodies:
        dx = world_grid[:, 0] - b["pos"][0]
        dz = world_grid[:, 2] - b["pos"][2]
        r_sq = dx * dx + dz * dz
        world_grid[:, 1] -= b["well_depth"] / np.sqrt(r_sq + b["soft"] ** 2)

    view_mat = v(cam_pos, (pitch, yaw, 0))
    scr.fill((4, 6, 12))

    draw_mesh(world_grid, grid_edjs, identity_mat, view_mat, proj_mat, (80, 120, 175), 1, max_dist=38.0)

    for b in bodies:
        r = b["radius"]
        ground_y = grid_height_at(b["pos"][0], b["pos"][2]) + r * 0.5
        draw_pos = np.array([b["pos"][0], ground_y+3, b["pos"][2]])
        draw_mesh(sphere_verts, sphere_edges, m(draw_pos, (0, t_sec * 0.4, 0.2), (r, r, r)), view_mat, proj_mat, b["color"], 2, max_dist=75.0)

    trail_timer += dt
    if trail_timer >= 0.03:
        trail.append([ship_pos[0], ship_pos[1], ship_pos[2], 1.0])
        if len(trail) > 60:
            trail.pop(0)
        trail_timer = 0.0

    if len(trail) > 1:
        pts = np.array(trail)
        clip = pts @ view_mat @ proj_mat
        bg_col = np.array([4, 6, 12], dtype=float)
        trail_col = np.array([120, 255, 190], dtype=float)
        num_segs = len(pts) - 1

        for i in range(num_segs):
            p1, p2 = clip[i], clip[i + 1]
            if p1[3] >= 0.1 and p2[3] >= 0.1:
                ndc1 = p1[:2] / p1[3]
                ndc2 = p2[:2] / p2[3]
                x1, y1 = int((ndc1[0] + 1) * 0.5 * wid), int((1 - ndc1[1]) * 0.5 * hig)
                x2, y2 = int((ndc2[0] + 1) * 0.5 * wid), int((1 - ndc2[1]) * 0.5 * hig)

                fade = (i + 1) / num_segs
                col = (bg_col + (trail_col - bg_col) * (fade ** 1.5)).astype(int)
                pg.draw.line(scr, col, (x1, y1), (x2, y2), 2)

    ship_mat = m(ship_pos, (slope_pitch, yaw, bank_roll), (1.0, 1.0, 1.0))
    draw_mesh(ship_verts, ship_edges, ship_mat, view_mat, proj_mat, (120, 255, 190), 2, max_dist=50.0)

    speed_val = np.linalg.norm(vel)
    hud_text = font.render(
        f"SPEED: {speed_val:05.2f} u/s | POS: ({ship_pos[0]:.1f}, {ship_pos[1]:.1f}, {ship_pos[2]:.1f})",
        True,
        (180, 220, 255)
    )
    scr.blit(hud_text, (16, 16))

    pg.display.flip()

pg.quit()