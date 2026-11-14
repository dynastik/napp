import numpy as np
import pygame as pg
import itertools

pg.init()
wid,hig=1000,750
scr=pg.display.set_mode((wid, hig))
pg.display.set_caption('gem')

clk=pg.time.Clock()

verts=np.array(list(itertools.product([-0.5, 0.5], repeat=3)))
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

def rendr():
    trix=p(70)@v((0,0,0),(0,0,0))@m((0,0,0),(0,0,0),(1,1,1))@verts
    fnl=trix[:,3]

runig=True
while runig:
    dt=clk.tick(60)/1000
    for evnt in pg.event.get():
        if evnt.type == pg.QUIT:
            runig=False
    scr.fill((0,0,0))
    pg.display.flip()

pg.quit()