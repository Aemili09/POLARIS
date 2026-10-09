"""Draw the proposed POLARIS hardware as one auditable vector engineering sheet.

Optional rendering dependencies: cairosvg, Pillow. This is a wiring proposal,
not a claim that a physical prototype or acquisition firmware has been tested.
"""
from pathlib import Path
from html import escape
import math
import json
import cairosvg

ROOT = Path(__file__).resolve().parent
W, H = 4400, 3500
INK, TEAL, RED, PURPLE, GRAY, GOLD = '#17324d', '#087f8c', '#c54036', '#7044b3', '#526479', '#c68c12'
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="#087f8c"/></marker></defs>',
         '<rect width="100%" height="100%" fill="white"/>']

def line(x1,y1,x2,y2,color=INK,width=4,dash=None):
    extra=f' stroke-dasharray="{dash}"' if dash else ''
    parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{extra}/>')

def wire(points,color=TEAL,width=5):
    parts.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in points)}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"/>')

def dot(x,y,color=INK,r=7):
    parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')

def rect(x,y,w,h,fill='white',stroke='#c8d5df',radius=12,width=3):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')

def text(x,y,value,size=30,color=INK,bold=False,anchor='start',spacing=1.28):
    lines=value.split('\n')
    for i,t in enumerate(lines):
        parts.append(f'<text x="{x}" y="{y+i*size*spacing}" font-family="DejaVu Sans, sans-serif" font-size="{size}" font-weight="{"700" if bold else "400"}" fill="{color}" text-anchor="{anchor}">{escape(t)}</text>')

def panel(x,y,w,h,title,subtitle=None):
    rect(x,y,w,h,'#fbfdff')
    rect(x,y,w,68,'#eaf2f6',radius=12)
    text(x+22,y+46,title,34,bold=True)
    if subtitle:text(x+22,y+103,subtitle,26,GRAY)

def net(x,y,label,color=TEAL,anchor='start'):
    text(x,y-12,label,27,color,True,anchor)
    dot(x,y,color,5)

def ground(x,y):
    line(x,y,x,y+18,GRAY)
    for i,half in enumerate((26,17,8)):
        line(x-half,y+18+i*10,x+half,y+18+i*10,GRAY)

def resistor(x1,y1,x2,y2,label=None,label_side=1):
    if abs(x1-x2)<1:
        mid=(y1+y2)/2
        line(x1,y1,x1,mid-28)
        rect(x1-13,mid-28,26,56,'white',INK,0)
        line(x1,mid+28,x1,y2)
        if label:text(x1+23*label_side,mid+8,label,24,anchor='start' if label_side>0 else 'end')
    else:
        mid=(x1+x2)/2
        line(x1,y1,mid-38,y1)
        rect(mid-38,y1-13,76,26,'white',INK,0)
        line(mid+38,y1,x2,y2)
        if label:text(mid,y1-28,label,25,anchor='middle')

def capacitor(x,y,label,polar=False):
    line(x,y,x,y+28)
    line(x-23,y+28,x+23,y+28,width=5)
    line(x-23,y+43,x+23,y+43,width=5)
    line(x,y+43,x,y+73)
    if polar:text(x-43,y+23,'+',26,RED,True)
    text(x+35,y+43,label,24)
    ground(x,y+73)

def arrow(x1,y1,x2,y2,color=TEAL,width=6):
    parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" marker-end="url(#arrow)"/>')

text(65,78,'POLARIS · GROUP 18  |  PROPOSED V1 HARDWARE',59,bold=True)
text(67,131,'Transmission polariscope: motorized linear analyzer + USB image capture + optional measured load',35,GRAY)
rect(65,157,4270,55,'#fff7e6','#dfc889',8)
text(86,195,'DESIGN PROPOSAL — not bench-tested. This sheet is the wiring basis; hardware firmware, calibration and experimental validation remain to be completed.',28,INK,True)

# A — power, isolated low voltage only.
panel(60,245,1290,650,'A  |  EXTERNAL LOAD POWER')
text(90,365,'PS1: isolated, regulated 12 V DC / 3 A adapter',31,bold=True)
text(90,409,'Use an enclosed certified adapter; no mains wiring on this board.',26,GRAY)
rect(110,457,190,235,'#f0f4f8',INK)
text(205,515,'DC IN',33,bold=True,anchor='middle')
text(205,565,'+12 V',30,RED,True,'middle')
text(205,644,'0 V',30,GRAY,True,'middle')
wire([(300,545),(460,545)],RED)
rect(460,526,100,38,'white',RED,0)
line(470,545,550,545,RED)
text(510,494,'F1: 2 A fuse',27,anchor='middle')
wire([(560,545),(715,545)],RED)
dot(715,545,RED)
dot(855,545,RED)
line(715,545,828,502,RED,5)
text(785,465,'SW1: ≥3 A at 12 V DC',27,anchor='middle')
wire([(855,545),(1175,545)],RED)
net(1175,545,'+12_SW',RED,anchor='end')
text(925,596,'to A4988 VMOT\nand LED panel +',28,RED)
wire([(300,645),(630,645)],GRAY)
ground(630,645)
text(695,671,'GND / 0 V common',29,GRAY,True)
text(95,759,'Motor and LED return directly to the supply ground.',28,bold=True)
text(95,802,'Uno is powered only by laptop USB; leave Vin/barrel unused.',26)
text(95,844,'Never connect +12_SW to Uno 5V, USB, or an I/O pin.',27,RED,True)

# B — PC and camera: separate USB connections.
panel(60,935,1290,1080,'B  |  LAPTOP + CAMERA','The camera sends images to the laptop, not to Arduino GPIO.')
rect(125,1080,645,350,'#eff6fa',INK)
text(447,1140,'PC1  LAPTOP / USB HOST',32,bold=True,anchor='middle')
text(155,1196,'Python / OpenCV + serial control',29)
text(155,1244,'USB1: control commands ↔ Uno',28)
text(155,1292,'USB2: image frames ← camera',28)
text(155,1360,'Two USB ports or a powered USB hub',25,GRAY)
wire([(770,1207),(1210,1207)],TEAL)
net(1208,1207,'USB1 → UNO USB-B',TEAL,anchor='end')
wire([(770,1310),(1110,1310),(1110,1490)],TEAL)
rect(840,1490,440,285,'#eff6fa',INK)
text(1060,1542,'CAM1  UVC CAMERA',30,bold=True,anchor='middle')
text(870,1594,'USB power + video from PC',26)
text(870,1640,'Manual exposure / gain / WB',25)
text(870,1686,'Lens looks through P2',27)
text(870,1733,'No camera → Uno I/O wiring',24,RED,True)
text(120,1518,'CAMERA SELECTION',28,TEAL,True)
text(120,1570,'UVC USB camera with controllable\nexposure, gain and white balance.\nLock settings for an angle sweep.\nCalibrate response before using\nintensity for quantitative inversion.',28)
text(95,1855,'Capture protocol: command angle → wait for DONE → settle →',27,bold=True)
text(95,1900,'discard buffered frames → capture → save angle + measured force.',26)
text(95,1952,'Start with 300–500 ms settling; verify it on the assembled hardware.',25,GRAY)

# C — controller and all assigned GPIO nets.
panel(1390,245,1270,1770,'C  |  ARDUINO UNO R3 (5 V LOGIC)')
text(1420,368,'Read signal names, not a clone board’s physical orientation.',27,GRAY)
rect(1530,435,725,1160,'#eff7f4','#4c8172')
text(1888,493,'U1  UNO R3',42,bold=True,anchor='middle')
text(1888,545,'USB powered',30,TEAL,True,'middle')
line(1450,625,1530,625,TEAL,6)
text(1450,594,'USB1',26,TEAL,True)
text(1570,635,'USB-B socket',29)
pins=[('5V','+5_LOGIC',650,PURPLE),('GND','GND',735,GRAY),
      ('D2 OUT','STEP',850,TEAL),('D3 OUT','DIR',940,TEAL),('D4 OUT','EN',1030,TEAL),
      ('D5 IN','HX_DT',1120,TEAL),('D6 OUT','HX_SCK',1210,TEAL),
      ('D7 IN','HOME',1300,TEAL),('D9 OUT','LED_CTL',1390,TEAL)]
for pin,name,y,col in pins:
    text(2195,y+10,pin,31,col,True,'end')
    line(2255,y,2590,y,col,5)
    net(2590,y,name,col,'end')
text(1580,1495,'D0 / D1: reserve for USB serial',27)
text(1580,1540,'All grounds join GND / 0 V',27,GRAY,True)
text(1425,1647,'STARTUP BIAS RESISTORS (external)',29,bold=True)
net(1440,1722,'+5_LOGIC',PURPLE)
resistor(1630,1722,1800,1722,'R_EN 10 kΩ')
line(1440,1722,1630,1722,PURPLE)
line(1800,1722,1915,1722)
net(1915,1722,'EN',TEAL,'end')
net(2080,1722,'STEP',TEAL)
resistor(2080,1722,2080,1828,'10 kΩ')
ground(2080,1828)
net(2450,1722,'DIR',TEAL)
resistor(2450,1722,2450,1828,'10 kΩ')
ground(2450,1828)
text(1425,1900,'Boot: EN HIGH (disabled), STEP LOW, LED_CTL LOW.',27,bold=True)
text(1425,1944,'STEP high/low ≥5 µs; wait ≥1 ms after driver wake-up.',26)
text(1425,1980,'Repeated net labels are electrically connected.',25,TEAL,True)

# D — bipolar stepper and driver, with decoupling and explicit mode straps.
panel(2700,245,1640,1020,'D  |  MOTORIZED ANALYZER: A4988 + BIPOLAR STEPPER')
rect(3080,482,590,655,'#f1f5fa',INK)
text(3375,533,'U2  A4988 CARRIER',31,bold=True,anchor='middle')
net(3160,376,'+5_LOGIC',PURPLE)
wire([(3160,376),(3160,482)],PURPLE)
text(3190,466,'VDD',24,PURPLE)
dot(3160,412,PURPLE)
wire([(3160,412),(2950,412)],PURPLE)
capacitor(2950,412,'C2 100 nF')
net(3520,375,'+12_SW',RED)
wire([(3520,375),(3520,482)],RED)
text(3550,466,'VMOT',24,RED)
dot(3520,409,RED)
wire([(3520,409),(3870,409)],RED)
capacitor(3870,409,'C1 100 µF / 35 V',True)
text(3990,360,'C1 close to VMOT/GND',25,GRAY,anchor='middle')
for y,name in [(610,'STEP'),(695,'DIR'),(780,'EN')]:
    net(2780,y,name,TEAL)
    line(2780,y,3080,y,TEAL,5)
    text(3105,y+9,name if name!='EN' else 'ENABLE (LOW = on)',25,bold=True)
net(2825,905,'+5_LOGIC',PURPLE)
wire([(2825,905),(2825,1045)],PURPLE)
for y,name in [(945,'RESET'),(1045,'SLEEP')]:
    dot(2825,y,PURPLE)
    line(2825,y,3080,y,PURPLE,5)
    text(3105,y+9,name,28,bold=True)
for x,name in [(3180,'MS1'),(3290,'MS2'),(3400,'MS3')]:
    text(x,1114,name,24,anchor='middle')
    wire([(x,1137),(x,1200)],PURPLE)
    dot(x,1200,PURPLE)
line(3180,1200,3400,1200,PURPLE,5)
net(3240,1200,'+5_LOGIC',PURPLE)
text(2770,1234,'All MS pins HIGH → 1/16 microstep',27,bold=True)
text(3540,1090,'BOTH',22,GRAY,anchor='middle')
text(3540,1120,'GND pins',23,GRAY,anchor='middle')
line(3540,1137,3540,1170,GRAY)
ground(3540,1170)
parts.append('<rect x="3930" y="535" width="355" height="407" rx="12" fill="#f4f6f8" stroke="#a5b4c2" stroke-width="2" stroke-dasharray="9 9"/>')
text(4108,574,'M1  NEMA 17',28,bold=True,anchor='middle')
text(4108,612,'4-wire bipolar',26,anchor='middle')
for y,name in [(650,'1A'),(725,'1B'),(810,'2A'),(885,'2B')]:
    text(3640,y+9,name,28,bold=True,anchor='end')
    line(3667,y,3930,y,TEAL,5)
    dot(3930,y,TEAL)
text(4100,691,'Coil A',28,bold=True,anchor='middle')
text(4100,851,'Coil B',28,bold=True,anchor='middle')
for start_y in (650,810):
    parts.append(f'<path d="M3930 {start_y} H3980 c32 0 32 25 0 25 c32 0 32 25 0 25 c32 0 32 25 0 25 H3930" fill="none" stroke="{INK}" stroke-width="4"/>')
text(3755,995,'200 full steps/rev; rated ≥0.60 A/phase',25)
text(3755,1038,'Find coil pairs with an ohmmeter.',26,bold=True)
text(3755,1080,'Wire colors are NOT standardized.',25,GRAY)
text(3755,1145,'20T pulley → belt → 80T P2 ring',27,TEAL,True)
text(3755,1185,'Motor stays outside the light path.',26)
text(3755,1225,'P2 rotates on its own bearing.',26)

# E — low-side LED switch. Internal panel current limiting is a buying constraint.
panel(2700,1305,1640,710,'E  |  LED BACKLIGHT: DC ON/OFF, NOT PWM DURING CAPTURE')
text(2740,1420,'Q1: FQP30N06L logic-level N-MOSFET',31,bold=True)
text(2740,1464,'TO-220, front marking facing you: 1=G, 2=D/tab, 3=S.',27)
rect(3750,1530,510,162,'#fff8df',GOLD)
text(4005,1571,'L1: 12 V white LED panel',28,bold=True,anchor='middle')
text(4005,1614,'Built-in current limiting; ≤0.5 A',25,anchor='middle')
text(4005,1654,'Diffuser; illuminate entire field',25,anchor='middle')
net(4005,1498,'+12_SW',RED,anchor='middle')
line(4005,1498,4005,1530,RED,5)
text(4040,1524,'+',27,RED,True)
wire([(4005,1692),(4005,1740),(3510,1740),(3510,1775)],INK)
text(4040,1719,'−',27,bold=True)
net(2780,1830,'LED_CTL',TEAL)
line(2780,1830,3070,1830,TEAL,5)
resistor(3070,1830,3240,1830,'R_G 100 Ω')
line(3240,1830,3390,1830,TEAL,5)
dot(3290,1830)
resistor(3290,1830,3290,1930,'R_PD 10 kΩ',-1)
ground(3290,1930)
# Enhancement NMOS symbol; all three terminals are individually labelled.
line(3390,1785,3390,1875,INK,6)
for ya,yb in [(1782,1804),(1818,1840),(1854,1877)]:line(3432,ya,3432,yb,INK,6)
wire([(3510,1775),(3510,1795),(3432,1795)],INK)
wire([(3432,1866),(3510,1866),(3510,1930)],INK)
line(3432,1829,3480,1829,INK)
line(3480,1829,3480,1866,INK)
parts.append('<path d="M3453 1818 L3436 1829 L3453 1840 Z" fill="#17324d"/>')
text(3350,1772,'G (1)',25,bold=True,anchor='end')
text(3560,1784,'D (2/tab)',25,bold=True)
text(3560,1895,'S (3)',25,bold=True)
ground(3510,1930)
text(2750,2000,'LED_CTL HIGH = ON. Use a current-limited panel; never connect a bare power LED here.',26,bold=True)

# F — NC homing switch with pull-up and input filtering.
panel(60,2055,1290,450,'F  |  HOME / INDEX SWITCH FOR P2')
net(140,2190,'+5_LOGIC',PURPLE)
resistor(140,2190,140,2300,'R_H 4.7 kΩ')
wire([(140,2300),(825,2300)],TEAL)
dot(140,2300)
net(825,2300,'HOME → Uno D7',TEAL,anchor='end')
dot(490,2300)
capacitor(490,2300,'C_H 100 nF')
wire([(140,2300),(140,2375),(865,2375)],INK)
dot(865,2375)
dot(1060,2350)
line(865,2375,1060,2350,INK,5)
line(1060,2350,1150,2350)
ground(1150,2350)
text(850,2200,'SW2: NC contact',28,bold=True)
text(850,2244,'Opens at home index',27)
text(805,2432,'COM → GND; NC → HOME',25,bold=True)
text(95,2480,'Away = LOW; index/open wire = HIGH. Verify LOW on back-off; debounce + timeout.',24,GRAY)

# G — optional force acquisition.
panel(1390,2055,1400,450,'G  |  OPTIONAL FORCE MEASUREMENT (NOT MOTOR LOADING)')
rect(1710,2170,420,245,'#eef6f3',INK)
text(1920,2204,'U3  HX711 MODULE',28,bold=True,anchor='middle')
net(1780,2169,'+5_LOGIC → VCC',PURPLE)
line(1780,2169,1780,2170,PURPLE)
for y,name,pin in [(2270,'HX_DT','DT'),(2350,'HX_SCK','SCK')]:
    net(1430,y,name,TEAL)
    line(1430,y,1710,y,TEAL,5)
    text(1730,y+9,pin,26,bold=True)
text(1770,2400,'GND',24,GRAY)
line(1800,2415,1800,2425,GRAY)
ground(1800,2425)
rect(2420,2195,330,252,'#f4f6f8',INK)
text(2585,2228,'LC1: 4-wire',27,bold=True,anchor='middle')
text(2585,2266,'full-bridge cell',25,anchor='middle')
text(2585,2316,'Rated for fixture',24,anchor='middle')
text(2585,2355,'load, e.g. 2 kN',24,anchor='middle')
text(2585,2400,'In load path',25,bold=True,anchor='middle')
for y,label in [(2230,'E+'),(2280,'E−'),(2340,'A+'),(2390,'A−')]:
    text(2106,y+7,label,23,bold=True,anchor='end')
    line(2130,y,2420,y,TEAL,4)
    text(2290,y-9,label+' wire',22,anchor='middle')
text(1420,2490,'Match cell datasheet (not colors). Tare + calibrate in newtons. Channel B unused.',24,GRAY)

# H — driver setup and engineering limits.
panel(2830,2055,1510,450,'H  |  SET CURRENT BEFORE RUNNING THE MOTOR')
text(2865,2180,'Start I_TRIP = 0.60 A/phase; never exceed the motor rating.',28,bold=True)
text(2865,2227,'A4988: VREF = 8 × I_TRIP × R_S',32,PURPLE,True)
text(2865,2274,'R_S = 0.068 Ω → 0.326 V;  R_S = 0.10 Ω → 0.480 V.',28)
text(2865,2319,'Read actual sense resistors; clone carriers may use other values.',27)
text(2865,2364,'C1 polarity: + to VMOT, − to GND; mount close to the driver.',27)
text(2865,2409,'Fit a heatsink and check temperature; keep power returns short.',27)
text(2865,2464,'POWER OFF before connecting or disconnecting motor leads.',28,RED,True)

# I — optical/mechanical assembly. Separate from electrical wires.
panel(60,2545,4280,405,'I  |  OPTICAL PATH + ANALYZER MECHANICS','Optical arrows indicate the light path, not electrical wiring. The specimen is loaded by a separate manual fixture.')
optics=[(95,535,'L1 + DIFFUSER','Uniform white backlight\nDC illumination'),
        (675,500,'P1: FIXED LINEAR','Transmission axis sets 0°\nFilm covers the field'),
        (1220,660,'PMMA / PC SPECIMEN','Manual rated loading frame\nLC1 in series if force is recorded'),
        (1925,695,'P2: ROTATING LINEAR','Bearing-supported 80T ring\nNear camera lens; check vignetting'),
        (2665,570,'LENS + CAM1','Fixed camera; USB to PC\nNo camera rotation'),
        (3280,1015,'M1 → 20T : 80T BELT DRIVE','4:1 ratio; 200 × 16 × 4 = 12,800 pulses/rev\nTargets 0° / 45° / 90° / 135°: 0 / 1600 / 3200 / 4800')]
for idx,(x,w,title,desc) in enumerate(optics):
    rect(x,2700,w,153,'#fff8e6' if idx<5 else '#eef6f3',GOLD if idx<5 else TEAL,10)
    text(x+w/2,2740,title,29,bold=True,anchor='middle')
    text(x+w/2,2782,desc,25,anchor='middle')
    if idx<4:arrow(x+w+4,2776,optics[idx+1][0]-8,2776,GOLD)
text(95,2909,'Use LINEAR polarizers, not photographic circular/CPL filters. At 0°, P2 is parallel to P1; at 90°, crossed. Home SW2, then calibrate optical zero.',28,bold=True)

# J — the scientific correction and build sequence belong in the same image.
panel(60,2990,4280,405,'J  |  BUILD NOTES + CORRECTIONS TO THE PROJECT CLAIMS')
line(1455,3080,1455,3365,'#c8d5df',3)
line(2870,3080,2870,3365,'#c8d5df',3)
text(90,3110,'BUILD / CHECK',29,TEAL,True)
text(90,3155,'Common GND everywhere; +5_LOGIC is Uno USB 5 V.\nUse terminal wiring for motor/LED power.\nIdentify coils, set VREF, then home and verify direction.\nOne-direction approach reduces belt backlash.\n0.028125°/pulse is a command increment, not accuracy.',27)
text(1490,3110,'ACQUIRE / CALIBRATE',29,TEAL,True)
text(1490,3155,'Warm up the light; lock exposure, gain and white balance.\nRecord dark/flat references and angle-tagged images.\nCheck repeatable 0°, 45°, 90°, 135° positions.\nMeasure thickness and stress-optic coefficient C.\nUse a rated fixture; 1000 N in simulation is not a load command.',26)
text(2905,3110,'WHAT THIS V1 CAN CLAIM',29,TEAL,True)
text(2905,3155,'Initial output: qualitative polarization / stress-pattern images.\nWhite LED + RGB camera ≠ three monochromatic channels.\nQuantitative MPa needs spectral/camera/material calibration.\nCNN defect labels and pass/fail need labelled physical tests.\nThe current simulation is not a validated physical digital twin.',26)
text(65,3444,'NET LEGEND:  +12_SW (red) · +5_LOGIC (purple) · signals (teal) · GND (gray). Repeated labels connect; a dot marks a junction. Module pins are functional labels, not a PCB footprint.',26,GRAY)
parts.append('</svg>')

PIN_MAP={'D2':'A4988 STEP','D3':'A4988 DIR','D4':'A4988 ENABLE (active LOW)',
         'D5':'HX711 DT (optional)','D6':'HX711 SCK (optional)','D7':'HOME NC switch',
         'D9':'100 ohm -> Q1 gate','5V':'A4988 VDD + configuration straps + HX711 VCC + pull-ups',
         'GND':'PS1 negative + both A4988 grounds + Q1 source + HX711 ground + switch COM'}
assert len([x for x in PIN_MAP if x.startswith('D')])==7
assert (200*16*(80/20))/360*45==1600
assert abs(8*.6*.068-.3264)<1e-12
svg=ROOT/'POLARIS_V1_Circuit_and_Connections.svg'
svg.write_text('\n'.join(parts))
cairosvg.svg2png(url=str(svg),write_to=str(ROOT/'POLARIS_V1_Circuit_and_Connections.png'))
(ROOT/'pin_connections.json').write_text(json.dumps(PIN_MAP,indent=2))
print('Generated one 4400 × 3500 image plus its editable SVG source.')
