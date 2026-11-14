import numpy as np
import pygame as pg

pg.init()
wid,hig=1000,750
scr=pg.display.set_mode((wid, hig))
pg.display.set_caption('gem')

clk=pg.time.Clock()

runig=True
while runig:
    dt=clk.tick(60)/1000
    for evnt in pg.event.get():
        if evnt == pg.QUIT:
            pg.quit()
    scr.fill((0,0,0))
    pg.display.flip()

pg.quit()