import numpy as np
import pygame as pg
import itertools

pg.init()
wid, hig = 1000, 500
scr = pg.display.set_mode((wid, hig))
pg.display.set_caption('gem')
clk = pg.time.Clock()

verts_3d = list(itertools.product([-0.5, 0.5], repeat=3))
verts = np.array([list(v) + [1.0] for v in verts_3d], dtype=float)
edjs = np.array([[i, j] for i in range(len(verts)) for j in range(i + 1, len(verts)) if np.sum(verts[i] != verts[j]) == 1], dtype=int)

def make_grid(size=40, step=2.0, sub_divs=10, y_level=-1.5):
    grdvrts = []
    grid_edjs = []
    coords = np.arange(-size, size + step, step)
    segs = np.linspace(-size, size, sub_divs + 1)
    idx = 0
    for c in coords:
        for k in range(sub_divs):
            grdvrts.append([c, y_level, segs[k], 1.0])
            grdvrts.append([c, y_level, segs[k + 1], 1.0])
            grid_edjs.append([idx, idx + 1])
            idx += 2
            grdvrts.append([segs[k], y_level, c, 1.0])
            grdvrts.append([segs[k + 1], y_level, c, 1.0])
            grid_edjs.append([idx, idx + 1])
            idx += 2
    return np.array(grdvrts, dtype=float), np.array(grid_edjs, dtype=int)

grdvrts, grid_edjs = make_grid(size=40, step=2.0, sub_divs=10, y_level=-1.5)

def m(trn, rot, scl):
    tx, ty, tz = trn
    rx, ry, rz = rot
    sx, sy, sz = scl
    S = np.array([[sx,0,0,0], [0,sy,0,0], [0,0,sz,0], [0,0,0,1]], dtype=float)
    T = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0], [tx,ty,tz,1]], dtype=float)
    cox, six = np.cos(rx), np.sin(rx)
    coy, siy = np.cos(ry), np.sin(ry)
    coz, siz = np.cos(rz), np.sin(rz)
    XR = np.array([[1,0,0,0], [0,cox,six,0], [0,-six,cox,0], [0,0,0,1]], dtype=float)
    YR = np.array([[coy,0,-siy,0], [0,1,0,0], [siy,0,coy,0], [0,0,0,1]], dtype=float)
    ZR = np.array([[coz,siz,0,0], [-siz,coz,0,0], [0,0,1,0], [0,0,0,1]], dtype=float)
    return S @ (XR @ YR @ ZR) @ T

def v(trn, rot):
    tx, ty, tz = trn
    rx, ry, rz = rot
    T = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0], [-tx,-ty,-tz,1]], dtype=float)
    cox, six = np.cos(-rx), np.sin(-rx)
    coy, siy = np.cos(-ry), np.sin(-ry)
    coz, siz = np.cos(-rz), np.sin(-rz)
    XR = np.array([[1,0,0,0], [0,cox,six,0], [0,-six,cox,0], [0,0,0,1]], dtype=float)
    YR = np.array([[coy,0,-siy,0], [0,1,0,0], [siy,0,coy,0], [0,0,0,1]], dtype=float)
    ZR = np.array([[coz,siz,0,0], [-siz,coz,0,0], [0,0,1,0], [0,0,0,1]], dtype=float)
    return T @ (ZR @ YR @ XR)

def p(fov):
    rad = np.radians(fov)
    f = 1 / np.tan(rad / 2)
    ar = wid / hig
    nr, fr = 0.1, 100.0
    return np.array([
        [f/ar, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, fr/(fr-nr), 1],
        [0, 0, -(fr*nr)/(fr-nr), 0]
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
yaw, pitch = 0.0, 0.0
cam_pos = np.array([0.0, 0.0, 0.0])
sensitivity = 0.003
proj_mat = p(70)
runig = True

while runig:
    dt = clk.tick(60) / 1000
    for evnt in pg.event.get():
        if evnt.type == pg.QUIT:
            runig = False
        if evnt.type == pg.MOUSEMOTION:
            dx, dy = evnt.rel
            yaw += dx * sensitivity
            pitch = np.clip(pitch + dy * sensitivity, -1.5, 1.5)
        if evnt.type == pg.KEYDOWN and evnt.key == pg.K_ESCAPE:
            runig = False
    keys = pg.key.get_pressed()
    speed = 5.0 * dt
    forward = np.array([np.sin(yaw), 0, np.cos(yaw)])
    right = np.array([np.cos(yaw), 0, -np.sin(yaw)])
    if keys[pg.K_w]:
        cam_pos += forward * speed
    if keys[pg.K_s]:
        cam_pos -= forward * speed
    if keys[pg.K_d]:
        cam_pos += right * speed
    if keys[pg.K_a]:
        cam_pos -= right * speed
    step = 2.0
    snap_x = np.floor(cam_pos[0] / step) * step
    snap_z = np.floor(cam_pos[2] / step) * step
    view_mat = v(cam_pos, (pitch, yaw, 0))
    scr.fill((0, 0, 0))
    draw_mesh(grdvrts, grid_edjs, m((snap_x, 0, snap_z), (0, 0, 0), (1, 1, 1)), view_mat, proj_mat, (110, 130, 160), 1, max_dist=38.0)
    draw_mesh(verts, edjs, m((0, 0, 4), (pg.time.get_ticks()*0.001, yaw, 0), (1, 1, 1)), view_mat, proj_mat, (255, 255, 255), 2, max_dist=45.0)
    pg.display.flip()

pg.quit()
