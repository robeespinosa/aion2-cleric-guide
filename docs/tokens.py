"""Normaliza el CSS/estilos del sitio a los tokens de diseño (gap 8/16/24, pesos 400/600/800, escala de 8 px, primary solo en CTA)."""
import re
SIZES=[16,24,32,40,48,56,64,72,80]
def num(t):
    m=re.fullmatch(r'(-?\d*\.?\d+)(px|rem|em)?',t.strip())
    if not m:return None
    v=float(m.group(1));u=m.group(2)
    return v*16 if u in('rem','em') else v
def snap8(v):
    if abs(v)<4:return 0
    r=int(round(abs(v)/8.0+1e-9))*8;r=max(8,r);return -r if v<0 else r
def snap_font(v):
    return max(16,min(SIZES,key=lambda s:(abs(s-v),s)))
def snap_gap(v):
    return 8 if v<12 else 16 if v<20 else 24
def snap_rad(t):
    v=num(t)
    if v is None or t.strip().endswith('%') or v>44:return t
    return '%dpx'%(8 if v<=12 else 16 if v<=20 else 24 if v<=28 else 32)
def toks(v):
    out=[];d=0;cur=''
    for ch in v:
        if ch=='(':d+=1
        if ch==')':d-=1
        if ch==' ' and d==0:
            if cur:out.append(cur);cur=''
        else:cur+=ch
    if cur:out.append(cur)
    return out
def split_decls(b):
    out=[];cur='';d=0;q=None
    for ch in b:
        if q:
            cur+=ch
            if ch==q:q=None
            continue
        if ch in'"\'':q=ch;cur+=ch;continue
        if ch=='(':d+=1
        if ch==')':d-=1
        if ch==';' and d==0:out.append(cur);cur=''
        else:cur+=ch
    if cur.strip():out.append(cur)
    return out
W={'100':400,'200':400,'300':400,'400':400,'500':400,'600':600,'700':600,'800':800,'900':800,'normal':400,'bold':600,'bolder':800,'lighter':400}
def fs(val):
    val=val.strip()
    m=re.fullmatch(r'clamp\((.+?),(.+?),(.+)\)',val)
    if m:
        a,b,c=[x.strip() for x in m.groups()];A=num(a);C=num(c)
        if A is None or C is None:return val,None
        a2,c2=snap_font(A),snap_font(C);return 'clamp(%dpx,%s,%dpx)'%(a2,b,c2),c2
    v=num(val)
    if v is None:return val,None
    s=snap_font(v);return '%dpx'%s,s
def proc_block(body,inline=False):
    decls=split_decls(body);out=[];size=None;haslh=False;changed=False
    for d in decls:
        if ':' not in d:out.append(d);continue
        p,v=d.split(':',1);p=p.strip();v=v.strip()
        if p.startswith('--') or "'" in v and '+' in v or v.startswith('"') or v.startswith("'"):out.append(d);continue
        if p=='font-weight':v=str(W.get(v,v))
        elif p=='font-size':
            v,s=fs(v)
            if s:size=s
        elif p=='line-height':haslh=True
        elif p=='font':
            m=re.fullmatch(r'(?:(\d{3}|bold|normal)\s+)?([\d.]+(?:rem|px|em))(?:/([\d.]+(?:px|rem|em)?))?\s+(.+)',v)
            if m:
                w,sz,lh,fam=m.groups();s=snap_font(num(sz));out.append('font-weight:%d'%W.get(w or 'normal',400));out.append('font-size:%dpx'%s)
                out.append('line-height:%dpx'%(s+8));haslh=True
                out.append('font-family:%s'%fam);continue
            out.append(d);continue
        elif p in('gap','row-gap','column-gap'):
            v=' '.join('%dpx'%snap_gap(num(t)) if num(t) is not None and num(t)>0 else t for t in toks(v))
        elif p=='padding' or p=='margin' or re.fullmatch(r'(padding|margin)-(top|right|bottom|left)',p):
            v=' '.join(('%dpx'%snap8(num(t)) if num(t) is not None and '(' not in t and not t.endswith('%') and not t.endswith('vw') else t) for t in toks(v))
        elif p in('width','height','min-width','min-height'):
            n=num(v)
            if n is not None and 8<=n<=160:v='%dpx'%snap8(n)
        elif p=='border-radius':
            v=' '.join(snap_rad(t) for t in toks(v))
        elif p in('top','bottom','left','right'):
            n=num(v)
            if n is not None and 8<=abs(n)<=160:v='%dpx'%snap8(n)
        out.append(p+':'+v)
    if size and not haslh and not inline:out.append('line-height:%dpx'%(size+8))
    if size and not haslh and inline:out.append('line-height:%dpx'%(size+8))
    return ';'.join(x for x in out if x.strip())
def process_css(css):
    return re.sub(r'\{([^{}]*)\}',lambda m:'{'+proc_block(m.group(1))+'}',css)
LAYER='''
/* ===== Tokens de diseño (v6) ===== */
:root{--gap-1:8px;--gap-2:16px;--gap-3:24px;--fw-regular:400;--fw-semibold:600;--fw-bold:800;--fs-1:16px;--fs-2:24px;--fs-3:32px;--fs-4:40px;--fs-5:48px;--r-1:8px;--r-2:16px;--r-3:24px;
--primary:#0f766e;--on-primary:#fff;--acc:var(--ink);--acc2:var(--ink);--bg:#f2f5f7;--chip:rgba(127,127,127,.14);--o1:rgba(100,116,139,.28);--o2:rgba(71,85,105,.22);--o3:rgba(148,163,184,.25)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--primary:#2dd4bf;--on-primary:#04201c;--acc:var(--ink);--acc2:var(--ink);--bg:#0b1015;--chip:rgba(255,255,255,.1);--o1:rgba(100,116,139,.3);--o2:rgba(71,85,105,.3);--o3:rgba(148,163,184,.16)}}
:root[data-theme="dark"]{--primary:#2dd4bf;--on-primary:#04201c;--acc:var(--ink);--acc2:var(--ink);--bg:#0b1015;--chip:rgba(255,255,255,.1);--o1:rgba(100,116,139,.3);--o2:rgba(71,85,105,.3);--o3:rgba(148,163,184,.16)}
body{font-size:16px;line-height:24px;font-weight:400}
h1{font-size:48px;line-height:56px;font-weight:800}h2{font-size:32px;line-height:40px;font-weight:800}h3{font-size:24px;line-height:32px;font-weight:600}
b,strong,summary,th,button{font-weight:600}
@media(max-width:560px){h1{font-size:40px;line-height:48px}h2{font-size:24px;line-height:32px}h3{font-size:16px;line-height:24px}}
a:not(.btn){text-decoration:underline;text-underline-offset:4px}
/* primary: solo acciones principales de cada pantalla */
.btn.p,#trk .tb button.pri,.avact button:first-child{background:var(--primary)!important;color:var(--on-primary)!important;border:0!important;box-shadow:none!important}
.btn:not(.p),.avact button+button{background:var(--chip);color:var(--ink)}
.clsw button[aria-pressed=true],.pk[aria-pressed=true]:after,.ms2 span.nx,.tag{background:var(--ink)!important;color:var(--bg)!important}
#sp{background:var(--ink)}.msb i,.bar2 i{background:var(--ok)!important}.grad,.prog h1{background:none;color:var(--ink);-webkit-text-fill-color:currentColor}
'''
def process(html):
    # colores literales teal -> neutros (el primary queda solo en botones de acción)
    for a,b in [('rgba(45,212,191,','rgba(127,127,127,'),('rgba(120,230,225,','rgba(255,255,255,'),('rgba(8,32,40,','rgba(17,24,31,'),('rgba(10,44,52,','rgba(20,28,36,'),('rgba(34,211,238,','rgba(127,127,127,'),('rgba(20,184,166,','rgba(127,127,127,'),('rgba(14,116,144,','rgba(127,127,127,'),('radial-gradient(circle,#2dd4bf,#0e7490)','radial-gradient(circle,#cbd5e1,#64748b)'),('<button data-t="\'+t[0]+\'" data-d="1">+1</button>','<button class="pri" data-t="\'+t[0]+\'" data-d="1">+1</button>')]:
        html=html.replace(a,b)
    html=re.sub(r'<style>(.*?)</style>',lambda m:'<style>'+process_css(m.group(1))+LAYER+'</style>',html,count=1,flags=re.S)
    html=re.sub(r'style="([^"]*)"',lambda m:'style="'+proc_block(m.group(1),True)+'"' if "'" not in m.group(1) else m.group(0),html)
    return html
