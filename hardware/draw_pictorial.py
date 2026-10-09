"""Single-sheet physical-component wiring illustration, CC BY-SA 3.0.

Board graphics: Fritzing/fritzing-parts. Pin positions are taken from the
part connector metadata, not guessed from the rendered image.
"""
from pathlib import Path
import base64
from html import escape
import xml.etree.ElementTree as ET
import cairosvg

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'pictorial_assets'
W,H = 4200,2700
INK='#182c42'; GRAY='#667789'; GND='#353b45'; V5='#b92373'; V12='#d93632'
STEP='#b68500'; DIR='#e27918'; EN='#3763c2'; DT='#188450'; SCK='#078aa5'; HOME='#8b45b4'; LED='#99633d'
p=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
   '<rect width="100%" height="100%" fill="#ffffff"/>',
   '<defs><linearGradient id="metal"><stop stop-color="#909ba5"/><stop offset=".45" stop-color="#e2e7eb"/><stop offset="1" stop-color="#8b959f"/></linearGradient><linearGradient id="black"><stop stop-color="#414853"/><stop offset="1" stop-color="#12181f"/></linearGradient></defs>']
def text(x,y,s,size=29,col=INK,bold=False,anchor='start'):
    for i,line in enumerate(s.split('\n')):
        p.append(f'<text x="{x}" y="{y+i*size*1.28}" font-family="DejaVu Sans,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{col}" text-anchor="{anchor}">{escape(line)}</text>')
def rect(x,y,w,h,fill,stroke='none',rx=8):
    p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')
def circle(x,y,r,fill,stroke='none',sw=3):
    p.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def wire(pts,col=GND,w=8,dots=()):
    points=' '.join(f'{x:.2f},{y:.2f}' for x,y in pts)
    for c,ww in [('white',w+6),(col,w)]:
        p.append(f'<polyline points="{points}" fill="none" stroke="{c}" stroke-width="{ww}" stroke-linecap="round" stroke-linejoin="round"/>')
    for x,y in dots:circle(x,y,8,col)
def label(x,y,s,col=INK,size=25,anchor='start'):
    width=len(s)*size*.62+18
    xx=x if anchor=='start' else x-width if anchor=='end' else x-width/2
    rect(xx-5,y-size,width+10,size+10,'white',rx=3)
    text(x,y,s,size,col,True,anchor)
def badge(x,y,n,title):
    circle(x,y-11,25,INK);text(x,y-2,str(n),28,'white',True,'middle')
    text(x+40,y,title,35,INK,True)
def asset(name,x,y,w):
    b=(ASSETS/(name+'.svg')).read_bytes();r=ET.fromstring(b)
    vb=list(map(float,r.get('viewBox').split()));h=w*vb[3]/vb[2]
    data=base64.b64encode(b).decode()
    p.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" xlink:href="data:image/svg+xml;base64,{data}"/>')
    return lambda xx,yy:(x+xx*w/vb[2],y+yy*w/vb[2])
def resistor(x1,y1,x2,y2,value,name,vertical=False):
    wire([(x1,y1),(x2,y2)],'#9a9fa5',5)
    x=(x1+x2)/2;y=(y1+y2)/2
    if vertical:
        rect(x-15,y-42,30,84,'#decfa5','#a59a7e',13)
        colors=['#e5c43b','#8a3f94','#c9342f','#aa8e30'] if value=='4.7 kΩ' else ['#7a4326','#171717','#c95421','#aa8e30']
        for off,col in zip([-24,-12,0,27],colors):rect(x-15,y+off,30,6,col,rx=0)
        label(x-24 if name=='R3' else x+24,y-5,name+' '+value,INK,23,'end' if name=='R3' else 'start')
    else:
        rect(x-42,y-15,84,30,'#decfa5','#a59a7e',13)
        colors=['#7a4326','#171717','#c95421','#aa8e30'] if value=='10 kΩ' else ['#7a4326','#171717','#7a4326','#aa8e30']
        for off,col in zip([-24,-12,0,27],colors):rect(x+off,y-15,6,30,col,rx=0)
        label(x,y-29,name+' '+value,INK,24,'middle')
def ceramic(x,y,name):
    wire([(x-23,y+25),(x-23,y+70)],'#9a9fa5',5)
    wire([(x+23,y+25),(x+23,y+70)],'#9a9fa5',5)
    p.append(f'<ellipse cx="{x}" cy="{y}" rx="43" ry="34" fill="#d8a153" stroke="#9a642f" stroke-width="3"/>')
    text(x,y+8,'104',18,'#5c381a',True,'middle');label(x,y-47,name+' 100 nF',INK,23,'middle')
    return (x-23,y+70),(x+23,y+70)

text(95,90,'POLARIS  |  COMPONENT-TO-COMPONENT WIRING',57,INK,True)
text(98,143,'Proposed prototype · component top views unless marked · pin names govern connections',29,GRAY)

# Actual Fritzing board / package graphics.
uno=asset('uno',700,620,1000)
drv=asset('a4988',2400,565,432)
hx=asset('hx711',1560,1830,510)
mos=asset('mosfet',2940,1810,190)
motor=asset('stepper',3440,625,410)
badge(760,210,1,'ARDUINO UNO R3')
text(800,244,'USB powered • Vin / barrel jack unused',24,GRAY)
badge(2395,1210,2,'A4988 CARRIER')
badge(3345,565,3,'NEMA 17 • 4-WIRE')
text(3370,609,'200 steps/rev • ≥0.60 A/phase',26,GRAY)
badge(1520,1775,8,'HX711 (OPTIONAL)')
badge(2880,1740,6,'FQP30N06L')
text(2920,1782,'Front / marked face',25,GRAY)

# Laptop and camera are physical illustrations; USB is a complete cable.
badge(160,380,4,'LAPTOP + USB CAMERA')
rect(120,580,420,245,'url(#black)','#697580',15)
rect(142,601,376,196,'#e9f4f8',rx=4)
text(330,691,'POLARIS',37,'#257e96',True,'middle')
text(330,737,'USB capture + control',23,GRAY,False,'middle')
p.append('<path d="M120 825 H540 L575 870 H85 Z" fill="url(#metal)" stroke="#77848d" stroke-width="3"/>')
rect(261,835,142,17,'#848e98')
wire([(540,745),(625,745),(625,859),(705,859)],'#52616f',15)
label(573,725,'USB → UNO USB-B',GRAY,22)
rect(120,1010,340,138,'url(#black)','#8994a0',28)
circle(290,1079,74,'#252d36','#6d7a84',9);circle(290,1079,52,'#142934','#9aabb3',4);circle(290,1079,30,'#073c53');circle(276,1063,12,'#416f7e')
rect(214,1153,154,30,'#606b75');rect(252,1120,76,44,'#343d48')
wire([(120,1075),(75,1075),(75,930),(500,930),(500,835)],'#52616f',13)
label(126,986,'USB camera → laptop USB',GRAY,25)
text(145,1225,'UVC camera • manual exposure',25,GRAY)

# Named coordinates match Fritzing connector metadata.
uc={}
for el in ET.parse(ASSETS/'uno.svg').getroot().iter():
    if el.tag.endswith('circle') and el.get('id','').startswith('connector'):
        uc[el.get('id')]=uno(float(el.get('cx')),float(el.get('cy')))
u={k:uc[f'connector{v}pin'] for k,v in {'D2':63,'D3':64,'D4':65,'D5':66,'D6':67,'D7':68,'D9':52,'5V':87,'GND':88}.items()}
dy=[3.449485,10.692488,17.935487,25.178486,32.421486,39.664489,46.907491,54.150492]
d={name:drv(3.178788,yy) for name,yy in zip(['EN','MS1','MS2','MS3','RST','SLP','STEP','DIR'],dy)}
d.update({name:drv(40.200503,yy) for name,yy in zip(['VMOT','GNDm','2B','2A','1A','1B','VDD','GNDl'],dy)})

# Controller signal cables: separate lanes, no electrical join at crossings.
for name,target,y,lane,col in [('D2','STEP',270,2000,STEP),('D3','DIR',322,1950,DIR),('D4','EN',374,1900,EN)]:
    a=u[name];b=d[target]
    wire([a,(a[0],y),(lane,y),(lane,b[1]),b],col)
    label(1710,y-14,name+' → '+target,col,27)
for name,y,lane,col in [('D5',426,650,DT),('D6',478,600,SCK),('D7',530,550,HOME)]:
    a=u[name];wire([a,(a[0],y),(lane,y),(lane,1560 if name=='D5' else 1610 if name=='D6' else 1670)],col)
    label(725,y-13,name+(' → HX711 DT' if name=='D5' else ' → HX711 SCK' if name=='D6' else ' → HOME'),col,25)
a=u['D9'];wire([a,(a[0],582),(1770,582),(1770,1660),(2820,1660),(2820,2180)],LED)
label(1530,569,'D9 → LED gate',LED,24)

# Power buses are actual connected nets, with junction dots only at connections.
wire([(700,1430),(4100,1430)],GND,12)
wire([(700,1500),(3220,1500)],V5,12)
label(720,1405,'COMMON GND / 0 V',GND,28)
label(720,1540,'+5 V FROM UNO USB',V5,28)
wire([u['GND'],(u['GND'][0],1430)],GND,dots=[(u['GND'][0],1430)])
wire([u['5V'],(u['5V'][0],1500)],V5,dots=[(u['5V'][0],1500)])
label(u['GND'][0]+12,1349,'GND',GND,25)
label(u['5V'][0]-12,1390,'5V',V5,25,'end')

# Driver: left-hand mode pins all high. Enable has a pull-up; STEP/DIR pull-downs.
wire([(2300,495),(2300,1500)],V5,dots=[(2300,1500)])
for pin in ['MS1','MS2','MS3','RST','SLP']:
    xx,yy=d[pin];wire([(2300,yy),(xx,yy)],V5,dots=[(2300,yy)])
wire([(2160,d['EN'][1]),(2160,495)],EN,dots=[(2160,d['EN'][1])])
resistor(2160,495,2300,495,'10 kΩ','R1')
circle(2300,495,8,V5)
for pin,x,nam,col in [('STEP',2180,'R2',STEP),('DIR',2090,'R3',DIR)]:
    yy=d[pin][1];wire([(x,yy),(x,1240)],col,dots=[(x,yy)])
    resistor(x,1240,x,1370,'10 kΩ',nam,True)
    wire([(x,1370),(x,1430)],GND,dots=[(x,1430)])
wire([d['VDD'],(2870,d['VDD'][1]),(2870,1500)],V5,dots=[(2870,1500)])
wire([d['GNDl'],(2910,d['GNDl'][1]),(2910,1430)],GND,dots=[(2910,1430)])
wire([d['GNDm'],(2950,d['GNDm'][1]),(2950,1430)],GND,dots=[(2950,1430)])
ca,cb=ceramic(2660,1310,'C2')
wire([ca,(ca[0],1500)],V5,dots=[(ca[0],1500)])
wire([cb,(cb[0],1430)],GND,dots=[(cb[0],1430)])

# Motor outputs. Actual lead colors differ by vendor: use coil measurements.
ends=[motor(xx,249) for xx in [64,73,82,91]]
for pin,end,lane,route_y,col in zip(['1A','1B','2A','2B'],ends,[3090,3140,3190,3240],[1320,1350,1380,1410],['#2587bb','#1c5594','#d19814','#bd6923']):
    a=d[pin];wire([a,(lane,a[1]),(lane,route_y),(end[0],route_y),end],col)
    label(lane,1240,pin,col,23,'middle')
text(3465,1475,'1A–1B = coil A; 2A–2B = coil B',25,INK,True)
text(3465,1510,'Find pairs with meter; do not use wire colours.',23,GRAY)

# 12 V adapter, inline fuse and real rocker-switch illustration.
badge(3250,205,5,'12 V DC / 3 A ADAPTER')
rect(3540,255,420,145,'url(#black)','#58636d',22)
rect(3580,278,340,91,'#e3e7eb',rx=4)
text(3750,317,'12 V DC · 3 A',30,INK,True,'middle');text(3750,351,'isolated regulated supply',22,GRAY,False,'middle')
wire([(3540,300),(3430,300),(3430,270),(3370,270)],V12)
rect(3260,237,110,66,'#242b32','#636c76',7);rect(3283,244,62,50,'#be342c',rx=4);text(3314,280,'I',25,'white',True,'middle')
wire([(3260,270),(3195,270)],V12)
rect(3085,252,110,36,'#e6eaed','#9fa9b0',2);rect(3085,252,22,36,'#929da6',rx=1);rect(3173,252,22,36,'#929da6',rx=1)
label(3140,233,'F1 • 2 A',INK,24,'middle');label(3315,344,'SW1 • ≥3 A DC',INK,24,'middle')
wire([(3085,270),(3020,270),(3020,d['VMOT'][1]),d['VMOT']],V12)
wire([(3020,270),(3020,405),(4050,405),(4050,1880),(3870,1880)],V12,dots=[(3020,405)])
wire([(3540,365),(3490,365),(3490,445),(4120,445),(4120,1430),(4100,1430)],GND,dots=[(4100,1430)])
label(3870,392,'SWITCHED +12 V',V12,26,'end')

# Bulk capacitor close to VMOT/GND; illustrated cylindrical electrolytic.
wire([(3130,535),(3130,594),(3020,594)],V12,dots=[(3020,594)])
wire([(3190,535),(3190,645),(2950,645),(2950,d['GNDm'][1])],GND,dots=[(2950,d['GNDm'][1])])
rect(3100,425,120,110,'url(#black)','#697580',12)
p.append('<ellipse cx="3160" cy="425" rx="60" ry="16" fill="#b7bfc5" stroke="#737f87" stroke-width="3"/>')
rect(3187,434,20,90,'#c8ced2',rx=1);text(3197,480,'−',26,INK,True,'middle')
text(3129,572,'+',25,V12,True,'middle');text(3190,572,'−',25,GND,True,'middle')
label(3227,473,'C1 100 µF',INK,24);label(3227,505,'35 V',INK,24)

# Home microswitch with NC contact, pull-up, and a bypass/filter capacitor.
badge(190,1795,7,'HOME SWITCH • NC')
rect(230,1850,260,120,'#292e35','#4a535c',12)
circle(264,1876,12,'#b8c1c8');circle(458,1876,12,'#b8c1c8')
p.append('<path d="M262 1850 L510 1808 L520 1821 L274 1864 Z" fill="url(#metal)" stroke="#68737d" stroke-width="2"/>')
for x,n in [(270,'COM'),(360,'NC'),(450,'NO')]:
    rect(x-8,1970,16,55,'#a5adb5',rx=1);label(x,2054,n,INK,24,'middle')
wire([(550,1670),(550,2100),(360,2100),(360,2025)],HOME)
wire([(270,2025),(170,2025),(170,1430),(700,1430)],GND,dots=[(700,1430)])
wire([(550,1950),(630,1950)],HOME,dots=[(550,1950)])
resistor(630,1950,630,1800,'4.7 kΩ','R4',True)
wire([(630,1800),(630,1500),(700,1500)],V5,dots=[(700,1500)])
ca,cb=ceramic(595,2200,'C3')
wire([ca,(572,2330),(170,2330),(170,2025)],GND,dots=[(170,2025)])
wire([cb,(700,cb[1]),(700,2100),(550,2100)],HOME,dots=[(550,2100)])
label(455,2011,'unused',GRAY,20)

# HX711 input header is on the right, load-cell header on left in this artwork.
hp={name:hx(77.021,yy) for name,yy in [('GND',13.093),('DT',20.293),('SCK',27.494),('VCC',34.694)]}
wire([(650,1560),(2190,1560),(2190,hp['DT'][1]),hp['DT']],DT)
wire([(600,1610),(2250,1610),(2250,hp['SCK'][1]),hp['SCK']],SCK)
wire([hp['GND'],(2130,hp['GND'][1]),(2130,1430)],GND,dots=[(2130,1430)])
wire([hp['VCC'],(2310,hp['VCC'][1]),(2310,1500)],V5,dots=[(2310,1500)])
for name,pos in hp.items():label(pos[0]-30,pos[1]+8,name,INK,23,'end')

# Representative four-wire S-beam load cell; terminals are assigned by datasheet.
badge(860,1775,9,'4-WIRE LOAD CELL')
p.append('<path d="M940 1860 H1250 V1950 H1100 V2040 H1250 V2130 H940 V2040 H1090 V1950 H940 Z" fill="url(#metal)" stroke="#717e89" stroke-width="5"/>')
circle(1095,1895,20,'#586874','#9ba5ad');circle(1095,2090,20,'#586874','#9ba5ad')
rect(968,1970,105,65,'#3f454e',rx=3)
for i,(name,yy,col) in enumerate([('E+',5.693,V12),('E−',12.894,GND),('A+',20.093,'#32945d'),('A−',27.293,'#2687bb')]):
    a=hx(4.12,yy);wire([(1250,1890+i*65),(1390+i*32,1890+i*65),(1390+i*32,a[1]),a],col)
    label(a[0]+30,a[1]+8,name,INK,23)
    label(1282,1877+i*65,name,col,22)
text(880,2210,'Rated for fixture (e.g. 2 kN) • match E± / A±',24,GRAY)
text(1640,2180,'B+ / B− unused',24,GRAY)

# White LED panel (internally current limited), MOSFET and gate resistors.
badge(3350,1738,10,'12 V WHITE LED PANEL')
rect(3400,1800,470,245,'#e4e6e5','#879399',12)
for xx in range(3440,3830,65):
    for yy in range(1838,2020,55):
        rect(xx,yy,30,25,'#f3d773','#c4b369',2);rect(xx+5,yy+4,20,17,'#fff3b1',rx=1)
text(3410,2100,'Built-in current limiting • ≤0.5 A',26,GRAY)
label(3890,1885,'+',V12,31);label(3890,1990,'−',GND,31)
gate=mos(9.001,62.23);drain=mos(18.999,62.23);source=mos(28.997,62.23)
wire([(2820,2180),(2860,2180)],LED)
resistor(2860,2180,gate[0],2180,'100 Ω','R5')
wire([(gate[0],2180),gate],LED)
wire([(3870,1980),(3960,1980),(3960,2300),(drain[0],2300),drain],GND)
wire([source,(source[0],2210),(3240,2210),(3240,1430)],GND,dots=[(3240,1430)])
wire([(gate[0],2180),(gate[0],2220),(2820,2220),(2820,2240)],LED,dots=[(gate[0],2180)])
resistor(2820,2240,2820,2390,'10 kΩ','R6',True)
wire([(2820,2390),(3240,2390),(3240,2210)],GND,dots=[(3240,2210)])
text(2940,2355,'Tab = drain (2)',24,GRAY)

# Pin labels on driver placed atop the actual board near the correct pads.
for name in ['EN','MS1','MS2','MS3','RST','SLP','STEP','DIR']:
    xx,yy=d[name];label(xx+32,yy+9,name,INK,24)
for name in ['VMOT','GNDm','2B','2A','1A','1B','VDD','GNDl']:
    xx,yy=d[name];label(xx-32,yy+9,'GND' if name.startswith('GND') else name,INK,24,'end')
for name,pos in u.items():
    if name.startswith('D'):
        circle(*pos,7,{'D2':STEP,'D3':DIR,'D4':EN,'D5':DT,'D6':SCK,'D7':HOME,'D9':LED}[name])
        text(pos[0],pos[1]+62,name,20,'white',True,'middle')
for pos,t in [(gate,'1 G'),(drain,'2 D'),(source,'3 S')]:
    rect(pos[0]-22,pos[1]+18,44,32,'white',rx=2)
    text(pos[0],pos[1]+43,t,21,INK,True,'middle')

# Concise build-specific connection notes, no theory panels.
rect(90,2475,4020,117,'#f2f5f8',rx=12)
text(120,2517,'Dots = connected junctions; crossings without dots are separate wires.  12 V must never connect to UNO 5V / I/O.',27,INK,True)
text(120,2562,'A4988: MS1/MS2/MS3 + RESET/SLEEP → 5 V; 1/16 steps. Set I ≤ 0.60 A: VREF = 8 × I × Rs (read carrier Rs). Power OFF before changing motor wires.',25,INK)
text(100,2640,'Component artwork: Fritzing (CC BY-SA 3.0) + custom illustrations. Proposed wiring, not bench-tested. Verify purchased module labels; pictures are representative.',24,GRAY)
p.append('</svg>')
out=ROOT/'POLARIS_Pictorial_Wiring.svg'
out.write_text('\n'.join(p))
cairosvg.svg2png(url=str(out),write_to=str(ROOT/'POLARIS_Pictorial_Wiring.png'))
print('Created 4200 × 2700 pictorial wiring PNG and SVG.')
