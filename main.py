import numpy as np
import pygame as pg

pg.init()
wid,hig=1000,750
scr=pg.display.set_mode((wid, hig))
pg.display.set_caption('gem')

clk=pg.time.Clock()

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
    cox,six=np.cos(rx),np.sin(rx)
    coy,siy=np.cos(ry),np.sin(ry)
    coz,siz=np.cos(rz),np.sin(rz)
    XR=np.array([[-1,0,0,0],[0,-cox,-six,0],[0,six,-cox,0],[0,0,0,1]],dtype=float)
    YR=np.array([[-coy,0,siy,0],[0,-1,0,0],[-siy,0,-coy,0],[0,0,0,1]],dtype=float)
    ZR=np.array([[-coz,-siz,0,0],[siz,-coz,0,0],[0,0,1,0],[0,0,0,1]],dtype=float)
    R=XR@YR@ZR
    return R@T
def p(fov):
    pass

runig=True
while runig:
    dt=clk.tick(60)/1000
    for evnt in pg.event.get():
        if evnt.type == pg.QUIT:
            pg.quit()
    scr.fill((0,0,0))
    pg.display.flip()

pg.quit()