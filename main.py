import numpy as np
import pygame as pg
import itertools

pg.init()
wid,hig=1000,500
scr=pg.display.set_mode((wid, hig))
pg.display.set_caption('gem')

clk=pg.time.Clock()

verts_3d = list(itertools.product([-0.5, 0.5], repeat=3))
verts = np.array([list(v) + [1.0] for v in verts_3d], dtype=float)

edjs=[[i, j]
    for i in range(len(verts))
    for j in range(i + 1, len(verts))
    if np.sum(verts[i] != verts[j]) == 1]

def m(trn,rot,scl):
    tx,ty,tz=trn
    rx,ry,rz=rot
    sx,sy,sz=scl
    S=np.array([[sx,0,0,0],[0,sy,0,0],[0,0,sz,0],[0,0,0,1]],dtype=float)
    T=np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[tx,ty,tz,1]],dtype=float)
    cox,six=np.cos(rx),np.sin(rx)
    coy,siy=np.cos(ry),np.sin(ry)
    coz,siz=np.cos(rz),np.sin(rz)
    XR=np.array([[1,0,0,0],[0,cox,six,0],[0,-six,cox,0],[0,0,0,1]],dtype=float)
    YR=np.array([[coy,0,-siy,0],[0,1,0,0],[siy,0,coy,0],[0,0,0,1]],dtype=float)
    ZR=np.array([[coz,siz,0,0],[-siz,coz,0,0],[0,0,1,0],[0,0,0,1]],dtype=float)
    R=XR@YR@ZR
    return S@R@T
def v(trn,rot):
    tx,ty,tz=trn
    rx,ry,rz=rot
    T=np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[-tx,-ty,-tz,1]],dtype=float)
    cox,six=np.cos(-rx),np.sin(-rx)
    coy,siy=np.cos(-ry),np.sin(-ry)
    coz,siz=np.cos(-rz),np.sin(-rz)
    XR=np.array([[1,0,0,0],[0,cox,six,0],[0,-six,cox,0],[0,0,0,1]],dtype=float)
    YR=np.array([[coy,0,-siy,0],[0,1,0,0],[siy,0,coy,0],[0,0,0,1]],dtype=float)
    ZR=np.array([[coz,siz,0,0],[-siz,coz,0,0],[0,0,1,0],[0,0,0,1]],dtype=float)
    R=ZR@YR@XR
    return T@R
def p(fov):
    rad=np.radians(fov)
    f=1/np.tan(rad/2)
    ar=(wid/hig)
    fr,nr=0.1,100
    return np.array([[f/ar,0,0,0],[0,f,0,0],[0,0,fr/(fr-nr),1],[0,0,-(fr*nr)/(fr-nr),1]],dtype=float)

pg.event.set_grab(True)
pg.mouse.set_visible(False)

yaw, pitch = 0.0, 0.0
sensitivity = 0.003

def rendr(rot=(0, 0, 0)):
    proj = p(70)
    proj[3, 3] = 0.0
    
    trix = verts @ m((0, 0, 3), rot, (1, 1, 1)) @ v((0, 0, 0), (0, 0, 0)) @ proj
    
    w = trix[:, 3:4]
    ndc = trix[:, :2] / w
    pts = np.column_stack([
        (ndc[:, 0] + 1) * 0.5 * wid,
        (1 - ndc[:, 1]) * 0.5 * hig
    ]).astype(int)
    
    for i, j in edjs:
        if w[i, 0] > 0 and w[j, 0] > 0:
            pg.draw.line(scr, (255, 255, 255), pts[i], pts[j], 2)

runig=True
while runig:
    dt=clk.tick(60)/1000
    for evnt in pg.event.get():
        if evnt.type == pg.QUIT:
            runig=False
        if evnt.type == pg.MOUSEMOTION:
            dx, dy = evnt.rel
            yaw += dx * sensitivity
            pitch = np.clip(pitch + dy * sensitivity, -1.5, 1.5)
        if evnt.type == pg.KEYDOWN:
            if evnt.key==pg.K_ESCAPE:
                pg.mouse.set_visible(True)

    scr.fill((0,0,0))
    rendr((pitch,yaw,0))
    pg.display.flip()

pg.quit()