"""Build the 100-page, A4, illustrated veterinary quick-reference ebook."""
from pathlib import Path
from textwrap import wrap
import math

from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT = Path(__file__).parent
OUT = ROOT / "output/pdf/atlas_visual_veterinaria_100_paginas.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
pdfmetrics.registerFont(TTFont("DejaVu", FONT))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", BOLD))
W, H = A4
INK = HexColor("#18382f")
DEEP = HexColor("#153c34")
CREAM = HexColor("#fbf8f0")
MUTED = HexColor("#5b6c64")
GOLD = HexColor("#d0a85c")
WHITE = HexColor("#ffffff")
COLORS = ["#9bcaa3", "#9fbece", "#e6ac8d", "#c4a6d5", "#e3c677", "#93c8bd", "#eaa4a4", "#a8b8e0", "#edb88c", "#a9c9a0"]
SOURCES = {
    "FUNDAMENTOS": "Merck: farmacocinética, farmacodinâmica e disposição de fármacos [1]",
    "SEMIOLOGIA": "Merck: triagem e atendimento inicial [2]",
    "HEMATOLOGIA": "Merck: hematologia clínica e leucograma [3]",
    "BIOQUÍMICA E URINA": "Merck: urinálise e patologia clínica [4]",
    "MICROBIOLOGIA": "ISCAID: diretrizes de antimicrobianos; Merck: otite externa [5]",
    "PARASITOLOGIA": "CAPC: diretrizes para cães e gatos [6]",
    "FARMACOLOGIA APLICADA": "Merck: analgésicos e AINEs; AAHA: anestesia [7]",
    "SISTEMAS CLÍNICOS": "Merck: clínica de pequenos animais; IRIS: rim [8]",
    "URGÊNCIAS": "Merck: triagem; AAHA: fluidos e anestesia [9]",
    "PREVENÇÃO E SAÚDE ÚNICA": "WSAVA: vacinação, nutrição e dor; CAPC [10]",
}
REFS = [
 ("1", "Merck Veterinary Manual, Pharmacokinetics / Pharmacodynamics", "https://www.merckvetmanual.com/pharmacology/pharmacology-introduction/pharmacokinetics"),
 ("2", "Merck, Initial Triage and Resuscitation of Small Animal Emergency Patients", "https://www.merckvetmanual.com/emergency-medicine-and-critical-care/evaluation-and-initial-treatment-of-small-animal-emergency-patients/initial-triage-and-resuscitation-of-small-animal-emergency-patients"),
 ("3", "Merck, Clinical Hematology / Leukogram Abnormalities", "https://www.merckvetmanual.com/clinical-pathology-and-procedures/diagnostic-procedures-for-the-private-practice-laboratory/clinical-hematology"),
 ("4", "Merck, Urinalysis", "https://www.merckvetmanual.com/clinical-pathology-and-procedures/diagnostic-procedures-for-the-private-practice-laboratory/urinalysis"),
 ("5", "ISCAID, Guidelines / Merck, Otitis Externa", "https://www.iscaid.org/guidelines"),
 ("6", "CAPC, General Guidelines for Dogs and Cats", "https://capcvet.org/guidelines/general-guidelines/"),
 ("7", "Merck, Analgesics Used in Animals / AAHA, Anesthesia", "https://www.merckvetmanual.com/therapeutics/pain-assessment-and-management/analgesics-used-in-animals"),
 ("8", "Merck Veterinary Manual, Small Animal Clinical Topics", "https://www.merckvetmanual.com/"),
 ("9", "AAHA, 2024 Fluid Therapy / 2020 Anesthesia Guidelines", "https://www.aaha.org/resources/2024-aaha-fluid-therapy-guidelines-for-dogs-and-cats/"),
 ("10", "WSAVA, Global Guidelines: Vaccination, Nutrition and Pain", "https://wsava.org/global-guidelines/"),
]

def parse():
    module = ""
    entries = []
    for line in (ROOT / "content/topics.txt").read_text().splitlines():
        if line.startswith("## "):
            module = line[3:]
            continue
        if line.strip():
            fields = line.split("|")
            assert len(fields) == 5, (module, fields)
            entries.append((module, *fields))
    assert len(entries) == 98, f"Expected 98 illustrated entries, got {len(entries)}"
    return entries

def rounded(c, x, y, w, h, fill, r=14, stroke=None):
    c.setFillColor(HexColor(fill) if isinstance(fill, str) else fill)
    c.setStrokeColor(HexColor(stroke) if isinstance(stroke, str) else (stroke or c._fillColorObj))
    c.roundRect(x, y, w, h, r, fill=1, stroke=int(stroke is not None))

def para(c, text, x, top, width, size=10, leading=None, color=INK, bold=False, max_height=None):
    style = ParagraphStyle("t", fontName="DejaVu-Bold" if bold else "DejaVu", fontSize=size,
                           leading=leading or size * 1.42, textColor=color)
    p = Paragraph(text.replace("&", "&amp;"), style)
    w, h = p.wrap(width, 200)
    if max_height and h > max_height:
        raise ValueError(f"Text overflow: {text[:45]} ({h:.0f} > {max_height})")
    p.drawOn(c, x, top - h)
    return h

def label(c, s, x, y, size=9, color=INK):
    c.setFont("DejaVu-Bold", size)
    c.setFillColor(color)
    c.drawString(x, y, s)

def motif(c, cx, cy, scale, kind, accent):
    """Original vector symbols; no stock illustration or copied reference art."""
    c.saveState()
    c.translate(cx, cy)
    c.scale(scale, scale)
    c.setStrokeColor(INK); c.setLineWidth(2.5)
    c.setFillColor(HexColor(accent))
    k = kind % 10
    if k == 0:  # molecule
        for x, y, r in [(-28, 4, 11), (5, 30, 14), (29, -17, 12), (-14, -27, 7)]:
            c.circle(x, y, r, fill=1, stroke=1)
        for a,b,d,e in [(-18,9,-7,24),(12,18,22,-7),(-20,-4,-16,-19)]: c.line(a,b,d,e)
    elif k == 1:  # stethoscope
        c.arc(-31,-5,19,40,180,180); c.line(-31,17,-31,-6); c.line(19,17,19,-6)
        c.bezier(-31,-5,-30,-46,10,-43,12,-12); c.circle(20,-13,11,fill=1,stroke=1)
    elif k == 2:  # blood cells
        for x,y,r in [(-23,20,15),(23,18,11),(2,-22,18),(-26,-23,7)]:
            c.circle(x,y,r,fill=1,stroke=1); c.setFillColor(WHITE);c.circle(x,y,r*.42,fill=1,stroke=0);c.setFillColor(HexColor(accent))
    elif k == 3:  # flask
        p=c.beginPath();p.moveTo(-9,34);p.lineTo(9,34);p.lineTo(9,10);p.lineTo(29,-34);p.curveTo(32,-41,-32,-41,-29,-34);p.lineTo(-9,10);p.close()
        c.drawPath(p,fill=1,stroke=1);c.line(-26,-19,26,-19)
    elif k == 4:  # microscope
        c.circle(20,-12,10,fill=1,stroke=1);c.line(-16,27,4,38);c.line(4,38,12,24);c.line(12,24,-8,13)
        c.arc(-8,-23,25,10,180,170);c.line(-36,-33,33,-33);c.line(-24,-24,20,-24)
    elif k == 5:  # parasite
        c.ellipse(-15,-29,15,29,fill=1,stroke=1)
        for y in [-18,-3,12]:
            c.line(-15,y,-34,y+12);c.line(15,y,34,y+12)
        c.circle(-5,17,2,fill=1,stroke=0);c.circle(5,17,2,fill=1,stroke=0)
    elif k == 6:  # capsule
        c.rotate(34);rounded(c,-34,-13,68,26,accent,13,INK);c.line(0,-13,0,13)
    elif k == 7:  # heart
        p=c.beginPath();p.moveTo(0,-34);p.curveTo(-54,0,-31,38,0,16);p.curveTo(31,38,54,0,0,-34);p.close();c.drawPath(p,fill=1,stroke=1)
        c.setStrokeColor(WHITE);c.line(-24,0,-10,0);c.line(-10,0,-4,10);c.line(-4,10,5,-10);c.line(5,-10,13,1);c.line(13,1,25,1)
    elif k == 8:  # emergency cross
        rounded(c,-11,-37,22,74,accent,5,INK);rounded(c,-37,-11,74,22,accent,5,INK)
    else:  # paw
        c.ellipse(-21,-31,21,7,fill=1,stroke=1)
        for x,y in [(-29,23),(-10,34),(11,33),(30,21)]: c.ellipse(x-7,y-9,x+7,y+9,fill=1,stroke=1)
    c.restoreState()

def base(c, number, module, color):
    c.setFillColor(CREAM);c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(DEEP);c.rect(0,H-10,W,10,fill=1,stroke=0)
    c.setStrokeColor(HexColor("#e6e9dc"));c.line(38,38,W-38,38)
    label(c,"OLA VET  /  RESUMOS VISUAIS",40,24,8,MUTED)
    c.setFont("DejaVu-Bold",8);c.drawRightString(W-40,24,f"{number:02d} / 100")
    rounded(c,40,H-60,220,25,color,10)
    label(c,module,52,H-52,8.3,DEEP)

def entry_page(c, n, e, m_index):
    module,title,lead,one,two,alert=e
    color=COLORS[m_index]
    base(c,n,module,color)
    title_size=23 if len(title)<29 else 20 if len(title)<37 else 17.5
    para(c,title.upper(),40,H-89,W-80,title_size,title_size*1.14,INK,True,max_height=60)
    para(c,lead,41,H-151,W-82,12,17,MUTED,max_height=57)
    # Infographic panel
    rounded(c,40,H-448,W-80,226,"#ffffff",17)
    rounded(c,55,H-249,142,27,DEEP,9)
    label(c,"MAPA VISUAL",67,H-241,9,WHITE)
    motif(c,W/2,H-332,1.1,m_index,color)
    # the diagram is a 3-step loop, with textual labels different for each subject
    for x,s in [(98,"OBSERVAR"),(W-100,"RELACIONAR")]:
        c.setStrokeColor(HexColor(color));c.setLineWidth(2);c.circle(x,H-331,42,stroke=1,fill=0)
        c.setFont("DejaVu-Bold",8);c.setFillColor(DEEP);c.drawCentredString(x,H-334,s)
    c.setStrokeColor(HexColor(color));c.line(142,H-331,W/2-61,H-331);c.line(W/2+61,H-331,W-144,H-331)
    c.setFillColor(HexColor("#f2f6ef"));c.roundRect(60,H-431,W-120,58,10,fill=1,stroke=0)
    # The small diagram repeats the page's own key concepts, never generic filler.
    phrases=[one.split(".")[0],two.split(".")[0],alert.split(".")[0]]
    labels=["CONCEITO", "APLICAÇÃO", "LIMITE"]
    third=(W-150)/3
    for j,(head,phrase) in enumerate(zip(labels,phrases)):
        x=75+j*third
        label(c,f"0{j+1}  {head}",x,H-389,7.4,DEEP)
        short=" ".join(phrase.split()[:6])
        para(c,short,x,H-397,third-10,7.1,10,MUTED,max_height=24)
    # two substantive information cards
    cards=[("ENTENDA",one),("NA PRÁTICA",two)]
    x0=40; gap=14; cw=(W-80-gap)/2
    for j,(head,body) in enumerate(cards):
        x=x0+j*(cw+gap)
        rounded(c,x,H-650,cw,188,"#ffffff",15)
        rounded(c,x+13,H-498,38,24,color,7)
        label(c,f"0{j+1}",x+23,H-490,9,DEEP)
        label(c,head,x+13,H-521,10,DEEP)
        para(c,body,x+13,H-537,cw-26,10.2,15,MUTED,max_height=101)
    # caution line
    rounded(c,40,H-742,W-80,77,"#ecf2e9",13)
    label(c,"ATENÇÃO CLÍNICA",55,H-685,9.3,DEEP)
    para(c,alert,55,H-699,W-110,9.6,14,INK,max_height=44)
    para(c,SOURCES[module],42,69,W-84,7.1,10,MUTED,max_height=22)
    c.showPage()

def cover(c):
    c.setFillColor(DEEP);c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(HexColor("#224c3f"));c.circle(W-60,H-60,230,fill=1,stroke=0)
    c.setStrokeColor(GOLD);c.setLineWidth(2);c.circle(W/2,H-410,195,stroke=1,fill=0)
    rounded(c,42,H-94,148,30,"#b4d1a6",11)
    label(c,"OLA VET  •  2026",56,H-83,9,DEEP)
    label(c,"RESUMOS VISUAIS",44,H-170,15,GOLD)
    para(c,"VETERINÁRIA",42,H-188,W-84,37,47,WHITE,True)
    para(c,"100 páginas para conectar sinais, exames e decisões",44,H-258,440,15,23,HexColor("#dfecdf"))
    for i,(x,y) in enumerate([(W/2,H-405),(W/2-113,H-483),(W/2+113,H-483)]):
        c.setFillColor(HexColor("#f9f4e9"));c.circle(x,y,59 if i==0 else 46,fill=1,stroke=0)
        motif(c,x,y,.75 if i==0 else .52,[9,4,6][i],["#c5d8c0","#eccdb5","#abcdd5"][i])
    rounded(c,42,93,W-84,78,"#f9f4e9",14)
    para(c,"Cães e gatos  •  Fundamentos  •  Hematologia  •  Farmacologia  •  Clínica  •  Urgências",59,151,W-118,11,17,DEEP,True)
    label(c,"Material educativo para estudantes e profissionais",45,52,9,HexColor("#d9e4db"))
    c.showPage()

def references(c):
    base(c,100,"FONTES E LEITURA",COLORS[0])
    para(c,"FONTES E USO RESPONSÁVEL",40,H-96,W-80,23,29,INK,True)
    para(c,"Este atlas é um apoio visual para estudo e revisão. Cada ficha resume um conceito; os links abaixo levam às fontes técnicas para aprofundamento e atualização.",40,H-146,W-80,10.5,15,MUTED)
    y=H-218
    for code,name,url in REFS:
        rounded(c,40,y-39,W-80,47,"#ffffff",9)
        rounded(c,49,y-31,31,30,COLORS[(int(code)-1)%10],7)
        label(c,code,59,y-22,10,DEEP)
        para(c,name,89,y-2,W-146,8.2,11,INK,True,max_height=24)
        c.linkURL(url,(40,y-39,W-40,y+8),relative=0)
        y-=52
    para(c,"Fontes consultadas em setembro de 2026. Diretrizes, produtos e indicações mudam. Antes de aplicar uma conduta, verifique a fonte atual, a legislação local e as características do paciente.",42,75,W-84,8,11,MUTED,max_height=33)
    c.showPage()

def main():
    entries=parse()
    c=canvas.Canvas(str(OUT),pagesize=A4,pageCompression=1)
    c.setTitle("Ola Vet | Resumos Visuais de Veterinária | 100 páginas")
    c.setAuthor("Ola Vet")
    cover(c)
    modules=list(dict.fromkeys(e[0] for e in entries))
    for n,e in enumerate(entries,start=2):
        if n == 2 or entries[n-3][0] != e[0]:
            key=f"module_{modules.index(e[0])+1}"
            c.bookmarkPage(key)
            c.addOutlineEntry(e[0].title(),key,level=0)
        entry_page(c,n,e,modules.index(e[0]))
    references(c)
    c.save()
    print(f"Created {OUT} with 100 pages ({len(entries)} illustrated topics)")

if __name__ == "__main__": main()
