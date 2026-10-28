"""Blob Crew icon system: vivid flat blob characters with minimal black faces on a pale squircle tile.
Usage: python crew.py  -> renders every icon in CREW to png/<id>.png and sheet.png"""
import math, io, os, sys, resvg_py
from PIL import Image, ImageDraw
N=1024; INK="#111111"
def squircle(n=5,s=N):
    a=s/2;p=[]
    for i in range(400):
        t=2*math.pi*i/400;c,si=math.cos(t),math.sin(t)
        p.append(f"{a+a*math.copysign(abs(c)**(2/n),c):.1f},{a+a*math.copysign(abs(si)**(2/n),si):.1f}")
    return "M"+" L".join(p)+"Z"
def mix(h,t,k):
    h=h.lstrip('#');t=t.lstrip('#')
    a=[int(h[i:i+2],16) for i in (0,2,4)];b=[int(t[i:i+2],16) for i in (0,2,4)]
    return '#%02x%02x%02x'%tuple(round(x+(y-x)*k) for x,y in zip(a,b))
def tint(h,k=0.80): return mix(h,'#FFF9F0',k)
def roundpoly(pts,r):
    n=len(pts);d=''
    for i in range(n):
        p0,p1,p2=pts[i-1],pts[i],pts[(i+1)%n]
        def towards(a,b,k):
            dx,dy=b[0]-a[0],b[1]-a[1];L=math.hypot(dx,dy);k=min(k,L/2);return (a[0]+dx/L*k,a[1]+dy/L*k)
        a=towards(p1,p0,r);b=towards(p1,p2,r)
        d+=('M' if i==0 else 'L')+f'{a[0]:.1f},{a[1]:.1f} Q{p1[0]},{p1[1]} {b[0]:.1f},{b[1]:.1f} '
    return d+'Z'
# ---------- body shapes (local coords, ~radius 380, centred on 0,0) ----------
def body(kind,c,bg):
    rs=f'fill="{c}" stroke="{c}" stroke-linejoin="round"'
    if kind=='gummy':  return f'<path {rs} stroke-width="10" d="M0,-340 C230,-340 390,-60 390,170 C390,340 220,370 0,370 C-220,370 -390,340 -390,170 C-390,-60 -230,-340 0,-340Z"/>'
    if kind=='drop':   return f'<path {rs} stroke-width="10" d="M40,-460 C150,-280 370,-80 370,130 C370,330 210,410 10,410 C-200,410 -360,320 -360,120 C-360,-90 -100,-260 40,-460Z"/>'
    if kind=='nub':    return f'<circle {rs} r="360"/><circle {rs} cy="-362" r="62"/>'
    if kind=='scallop':
        s=f'<circle {rs} r="320"/>'
        for i in range(16):
            a=2*math.pi*i/16; s+=f'<circle {rs} cx="{335*math.cos(a):.0f}" cy="{335*math.sin(a):.0f}" r="78"/>'
        return s
    if kind=='bitten':
        return f'<path fill="{c}" d="M0,-370 L30,-120 L330,-380 L190,-100 L364,-64 A370,370 0 1 1 0,-370Z"/>'
    if kind=='box':    return f'<rect {rs} x="-380" y="-320" width="760" height="680" rx="210"/>'
    if kind=='shield': return f'<path fill="{c}" d="M-370,-250 Q-370,-330 -290,-345 Q0,-410 290,-345 Q370,-330 370,-250 L370,60 Q370,310 30,445 Q0,457 -30,445 Q-370,310 -370,60Z"/>'
    if kind=='bubble': return f'<circle {rs} r="350"/><path {rs} stroke-width="36" d="M-260,150 C-280,260 -340,330 -430,370 C-300,380 -190,350 -110,300 Z"/>'
    if kind=='ears':   return f'<circle {rs} cy="30" r="350"/><circle {rs} cx="-280" cy="-260" r="105"/><circle {rs} cx="280" cy="-260" r="105"/>'
    if kind=='play':   return f'<path fill="{c}" d="{roundpoly([(-370,-450),(500,0),(-370,450)],170)}"/>'
    if kind=='spiky':
        s='';pts=[]
        for i in range(24):
            a=2*math.pi*i/24; r=380 if i%2==0 else 320; pts.append((round(r*math.cos(a)),round(r*math.sin(a))))
        return f'<path fill="{c}" d="{roundpoly(pts,22)}"/>'
    raise KeyError(kind)
# ---------- eyes ----------
def eyes(kind,gap=150,look=(0,0),bg='#fff'):
    lx,ly=look; L,R=-gap/2,gap/2; o=''
    if kind=='dot':
        for x in (L,R): o+=f'<circle cx="{x}" cy="0" r="40" fill="{INK}"/>'
    elif kind=='googly':
        for x,s in ((L-10,1),(R+10,.9)):
            o+=f'<ellipse cx="{x}" cy="0" rx="{80*s}" ry="{104*s}" fill="#fff" stroke="{INK}" stroke-width="22"/>'
        for x,s in ((L-10,1),(R+10,.9)):
            px,py=x+lx*30,ly*40
            o+=f'<ellipse cx="{px}" cy="{py}" rx="{40*s}" ry="{52*s}" fill="{INK}"/><ellipse cx="{px-12}" cy="{py-20}" rx="10" ry="13" fill="#fff"/>'
    elif kind=='pixel':
        for x in (L,R):
            o+=f'<rect x="{x-38}" y="-50" width="76" height="100" fill="#fff"/><rect x="{x-38+38*(lx>0)}" y="12" width="38" height="38" fill="{INK}"/>'
    elif kind=='shades':
        o+=f'<path fill="{INK}" d="M{L-150},-60 H{R+150} V-20 H{R+120} V30 H{R+90} V60 H{R-60} V30 H{R-90} V-20 H{L+90} V30 H{L+60} V60 H{L-90} V30 H{L-120} V-20 H{L-150}Z"/>'
        o+=f'<rect x="{L-60}" y="-10" width="30" height="20" fill="#fff"/><rect x="{R-60}" y="-10" width="30" height="20" fill="#fff"/>'
    elif kind=='heart':
        for x in (L,R): o+=f'<path fill="{INK}" transform="translate({x} 0) scale(2.2)" d="M0,22 C-30,2 -28,-22 -14,-22 C-6,-22 0,-15 0,-10 C0,-15 6,-22 14,-22 C28,-22 30,2 0,22Z"/>'
    elif kind=='x':
        for x in (L,R): o+=f'<path stroke="{INK}" stroke-width="30" stroke-linecap="round" d="M{x-36},-36 L{x+36},36 M{x+36},-36 L{x-36},36"/>'
    elif kind=='happy':
        for x in (L,R): o+=f'<path fill="none" stroke="{INK}" stroke-width="28" stroke-linecap="round" d="M{x-40},20 Q{x},-45 {x+40},20"/>'
    elif kind=='sleepy':
        for x in (L,R): o+=f'<path fill="none" stroke="{INK}" stroke-width="28" stroke-linecap="round" d="M{x-40},-5 Q{x},45 {x+40},-5"/>'
    elif kind=='wink':
        o+=f'<circle cx="{L}" cy="0" r="40" fill="{INK}"/><path fill="none" stroke="{INK}" stroke-width="28" stroke-linecap="round" stroke-linejoin="round" d="M{R+40},-38 L{R-30},0 L{R+40},38"/>'
    elif kind=='cyclops':
        o+=f'<rect x="-110" y="-62" width="220" height="30" rx="15" fill="{INK}"/><path fill="{INK}" d="M-80,-40 A80,80 0 0 0 80,-40Z"/>'
    elif kind=='mask':
        o+=f'<path fill="{INK}" d="M-250,80 C-250,-140 -130,-230 0,-230 C130,-230 250,-140 250,80 C250,170 160,190 110,140 C70,100 40,60 0,60 C-40,60 -70,100 -110,140 C-160,190 -250,170 -250,80Z"/>'
        o+=f'<circle cx="-150" cy="70" r="40" fill="{bg}"/><circle cx="150" cy="70" r="40" fill="{bg}"/><circle cx="0" cy="110" r="22" fill="{INK}"/>'
    return o
def mouth(kind,y=110):
    if kind in (None,'none'): return ''
    if kind=='smile': return f'<path fill="none" stroke="{INK}" stroke-width="26" stroke-linecap="round" d="M-45,{y} Q0,{y+45} 45,{y}"/>'
    if kind=='o':     return f'<ellipse cx="0" cy="{y+20}" rx="32" ry="42" fill="{INK}"/>'
    if kind=='flat':  return f'<rect x="-50" y="{y}" width="100" height="24" rx="12" fill="{INK}"/>'
    if kind=='teeth':
        s=f'<rect x="-110" y="{y-12}" width="220" height="16" fill="{INK}"/>'
        for i in range(5): s+=f'<path fill="{INK}" d="M{-110+i*44},{y} l22,32 l22,-32Z"/>'
        return s
    if kind=='grin':  return f'<path fill="{INK}" d="M-80,{y-10} H80 Q80,{y+80} 0,{y+80} Q-80,{y+80} -80,{y-10}Z"/>'
    raise KeyError(kind)
def prop(kind,c):
    if not kind: return ''
    if kind=='sparkle': return f'<path fill="{INK}" stroke="{INK}" stroke-width="30" stroke-linejoin="round" d="M0,-130 Q16,-16 130,0 Q16,16 0,130 Q-16,16 -130,0 Q-16,-16 0,-130Z"/>'
    if kind=='note':    return f'<path fill="{INK}" d="M-20,-130 h40 v170 a60,50 0 1 1 -40,-46Z M20,-130 q80,20 90,90 q-40,-40 -90,-40Z"/>'
    if kind=='arrow':   return f'<path fill="{INK}" stroke="{INK}" stroke-width="30" stroke-linejoin="round" d="M-40,-140 h80 v120 h70 l-110,130 l-110,-130 h70Z"/>'
    if kind=='cursor':  return f'<path fill="{INK}" stroke="{INK}" stroke-width="24" stroke-linejoin="round" d="M-70,-120 L90,30 L15,40 L60,120 L25,138 L-20,58 L-70,105Z"/>'
    if kind=='prompt':  return f'<path fill="none" stroke="{INK}" stroke-width="34" stroke-linecap="round" stroke-linejoin="round" d="M-110,-60 L-30,0 L-110,60 M10,70 H120"/>'
    if kind=='ripple':  return ''.join(f'<path fill="none" stroke="{INK}" stroke-width="28" stroke-linecap="round" d="M{-40+r*0.5:.0f},{-r*0.87:.0f} A{r},{r} 0 0 1 {-40+r*0.5:.0f},{r*0.87:.0f}"/>' for r in (60,115,170))
    if kind=='pin':     return f'<path fill="{INK}" d="M0,140 C-40,80 -90,30 -90,-30 A90,90 0 1 1 90,-30 C90,30 40,80 0,140Z"/><circle cy="-30" r="34" fill="{c}"/>'
    if kind=='zap':     return f'<path fill="{INK}" stroke="{INK}" stroke-width="20" stroke-linejoin="round" d="M30,-140 L-80,20 H0 L-30,140 L90,-30 H10Z"/>'
    raise KeyError(kind)
def icon(c,shape,eye,mth=None,look=(0,0),tilt=-8,pos=(512,560),scale=1.0,face=(0,-20),gap=170,pr=None,prop_at=(0,0),prop_rot=0,mouth_y=110,bg=None,ss=2,prop_col=None,flat_bg=False,deep=False):
    bg=bg or tint(c); top=bg if flat_bg else (mix(bg,'#FFFFFF',0.14) if deep else mix(bg,'#FFFFFF',0.45)); shade=mix(bg,c,0.16); rim=mix(c,'#FFFFFF',0.38)
    fx,fy=face; T=f'translate({pos[0]} {pos[1]}) rotate({tilt}) scale({scale})'
    g=f'<g filter="url(#s)" opacity="0.28"><g transform="translate({pos[0]} {pos[1]+26}) rotate({tilt}) scale({scale})">{body(shape,mix(c,"#000000",0.35) if not deep else "#000000",bg)}</g></g>'
    g+=f'<g transform="{T}">{body(shape,c,bg)}'
    g+=f'<g transform="translate({fx} {fy})">{eyes(eye,gap,look,c)}{mouth(mth,mouth_y)}</g></g>'
    if pr: g+=f'<g transform="translate({prop_at[0]} {prop_at[1]}) rotate({prop_rot})">{prop(pr,c).replace(INK,prop_col) if prop_col else prop(pr,c)}</g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{N*ss}" height="{N*ss}" viewBox="0 0 {N} {N}"><defs><clipPath id="t"><path d="{squircle()}"/></clipPath>'
            f'<filter id="s" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="26"/></filter><linearGradient id="g" x1="0" y1="0" x2="0.35" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bg}"/></linearGradient></defs>'
            f'<g clip-path="url(#t)"><rect width="{N}" height="{N}" fill="url(#g)"/>{g}</g></svg>')
CREW={
 'media-grabber':      dict(c='#2F6BFF',shape='drop',eye='googly',mth='o',look=(.6,.7),tilt=10,pos=(470,600),face=(0,80),pr='arrow',prop_at=(820,230),prop_rot=10),
 'pack-any-cli':       dict(c='#FFD60A',shape='box',eye='pixel',mth='flat',look=(1,0),tilt=-6,pos=(540,600),face=(0,-20),pr='prompt',prop_at=(250,200)),
 'creative-components':dict(c='#FF5FC8',shape='scallop',eye='dot',mth='smile',tilt=8,pos=(512,580),face=(0,-10),mouth_y=70),
 'ai-engineering-skills':dict(c='#19D47A',shape='bitten',eye='shades',tilt=-4,pos=(480,560),face=(-60,40),gap=200),
 'vibecoding-skills':  dict(c='#9B5CFF',shape='gummy',eye='heart',mth='grin',tilt=-10,pos=(512,620),face=(0,30),gap=190),
 'design-skill':       dict(c='#FF6A1A',shape='nub',eye='cyclops',mth='teeth',tilt=6,pos=(512,590),face=(0,0),mouth_y=90,pr='cursor',prop_at=(810,800),prop_rot=-10),
 'tapix':              dict(c='#FF4D5E',shape='gummy',eye='wink',mth='smile',tilt=8,pos=(500,640),face=(0,40),pr='sparkle',prop_at=(800,220),prop_rot=10),
 'verse-studio':       dict(c='#14CFE0',shape='ears',eye='sleepy',mth='o',tilt=-6,pos=(480,620),face=(0,30),pr='note',prop_at=(840,170),prop_rot=12),
 'formecho':           dict(c='#A6E31B',shape='bubble',eye='happy',mth='o',tilt=-8,pos=(540,540),face=(0,-10),pr='ripple',prop_at=(850,520)),
 'video-editing-agent':dict(c='#FF3B30',shape='play',eye='x',mth='flat',tilt=-4,pos=(470,512),face=(-40,-20),gap=160),
 'geo-seo-agent':      dict(c='#3AA8FF',shape='spiky',eye='googly',mth='smile',look=(-.5,-.7),tilt=10,pos=(530,580),face=(0,0),pr='pin',prop_at=(800,780),prop_rot=-8,mouth_y=150),
 'claudeguard':        dict(c='#8C93A3',shape='shield',eye='mask',tilt=-6,pos=(512,600),face=(0,-30)),
}

# ---------- background themes ----------
DEEP={'media-grabber':'#FFD23F','pack-any-cli':'#4B2BB5','creative-components':'#004A44','ai-engineering-skills':'#3B0F5C',
'vibecoding-skills':'#C8F25A','design-skill':'#2A1E8C','tapix':'#102A6E','verse-studio':'#7A0F4A','formecho':'#5A1E9E',
'video-editing-agent':'#0E1A33','geo-seo-agent':'#FF7A1A','claudeguard':'#17171C'}
ANA={'media-grabber':'#D9D3FF','pack-any-cli':'#FFE2B8','creative-components':'#F2D6FF','ai-engineering-skills':'#DDF5B8',
'vibecoding-skills':'#F6D3F2','design-skill':'#FFE6B0','tapix':'#FFD9C2','verse-studio':'#CDE9FF','formecho':'#F2F5B8',
'video-editing-agent':'#FFD6CC','geo-seo-agent':'#CFF0F5','claudeguard':'#E4E6EC'}
def themed(k,theme='tint'):
    cfg=dict(CREW[k]); c=cfg['c']
    if theme=='deep':   # vivid character on a deep jewel tone of a contrasting hue; props in a light tint of the body
        cfg.update(bg=DEEP[k],deep=True,prop_col=mix(c,'#FFFFFF',0.45))
    elif theme=='analog': cfg.update(bg=ANA[k])
    elif theme=='cream':  cfg.update(bg='#F6F0E4')
    elif theme=='black':  cfg.update(bg='#16161A',prop_col='#F6F0E4',flat_bg=True)
    return cfg
THEMES=['tint','deep','analog','cream','black']
def render(cfg):
    return Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_string=icon(**cfg))))).convert('RGBA').resize((N,N),Image.LANCZOS)
if __name__=='__main__':
    theme=sys.argv[1] if len(sys.argv)>1 else 'tint'
    out=f'png/{theme}'; os.makedirs(out,exist_ok=True); ims=[]
    for k in CREW:
        cfg=themed(k,theme); im=render(cfg); im.save(f'{out}/{k}.png'); open(f'{out}/{k}.svg','w').write(icon(**dict(cfg,ss=1))); ims.append((k,im))
    cols=6; S=200; W=40+cols*(S+16); rows=(len(ims)+cols-1)//cols
    sh=Image.new('RGB',(W,40+rows*(S+16)),'#f4f3ef')
    for i,(k,im) in enumerate(ims):
        b=im.resize((S,S),Image.LANCZOS); sh.paste(b,(20+(i%cols)*(S+16),20+(i//cols)*(S+16)),b)
    sh.save(f'sheet-{theme}.png')
