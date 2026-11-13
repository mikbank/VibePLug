#!/usr/bin/env python3
"""Draw original generic migration icons; not an official NIRAS logo."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]/'plugin'

def icon(size, background):
    scale=4
    image=Image.new('RGBA',(size*scale,size*scale),background)
    draw=ImageDraw.Draw(image)
    def box(coords, radius, fill, outline=None, width=1):
        draw.rounded_rectangle(tuple(round(x*size*scale) for x in coords),
            radius=round(radius*size*scale),fill=fill,outline=outline,
            width=max(1,round(width*size*scale)))
    white=(255,255,255,255)
    if size==192:
        box((.04,.04,.96,.96),.19,(8,127,120,255))
        box((.18,.28,.43,.71),.045,None,white,.025)
        box((.57,.28,.82,.71),.045,None,white,.025)
        draw.line([(round(x*size*scale),round(y*size*scale)) for x,y in [(.29,.48),(.68,.48)]],fill=white,width=round(.035*size*scale))
        draw.polygon([(round(x*size*scale),round(y*size*scale)) for x,y in [(.61,.39),(.72,.48),(.61,.57)]],fill=white)
        draw.line([(round(x*size*scale),round(y*size*scale)) for x,y in [(.62,.62),(.66,.66),(.74,.57)]],fill=white,width=round(.024*size*scale))
    else:
        box((.10,.18,.38,.83),.04,None,white,.065)
        box((.62,.18,.90,.83),.04,None,white,.065)
        draw.line([(round(.25*size*scale),round(.49*size*scale)),(round(.75*size*scale),round(.49*size*scale))],fill=white,width=round(.08*size*scale))
        draw.polygon([(round(x*size*scale),round(y*size*scale)) for x,y in [(.62,.32),(.82,.49),(.62,.66)]],fill=white)
    return image.resize((size,size),Image.Resampling.LANCZOS)

ROOT.mkdir(parents=True,exist_ok=True)
icon(192,(0,0,0,0)).save(ROOT/'color.png')
outline=icon(32,(255,255,255,0))
# Keep white RGB even at antialiased edges; alpha supplies edge coverage.
white_outline=Image.new('RGBA',outline.size,(255,255,255,0))
white_outline.putalpha(outline.getchannel('A'))
outline=white_outline
outline.save(ROOT/'outline.png')
print('Generated color.png (192x192) and outline.png (32x32).')
