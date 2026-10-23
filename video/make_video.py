#!/usr/bin/env python3
"""Genera el video del Track 2 (1920x1080, ~3 min): diapositivas + voz sintética + subtítulos.

Fuente única del texto: guion_v2.md (columna "Narración (EN)"). La voz es Piper (en_US-lessac-high, offline).
Salidas: hysa_track2_pitch.mp4 (subtítulos pegados) y hysa_track2_pitch.srt (para YouTube).
Uso: source ../env.sh && python3 make_video.py   (requiere piper-tts, Pillow, cairosvg en el venv; ffmpeg del sistema)
"""
import hashlib, io, os, re, subprocess, wave

import cairosvg
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
from piper import PiperVoice, SynthesisConfig

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(HERE, "..", "track2", "figures")
BUILD = os.path.join(HERE, "build")
for sub in ("frames", "tts"):
    os.makedirs(os.path.join(BUILD, sub), exist_ok=True)

VOICE = os.path.join(HERE, "voices", "en_US-lessac-high.onnx")
LENGTH_SCALE = 1.0           # ritmo nativo de la voz
W, H, FPS = 1920, 1080, 30
LEAD, GAP, SCENE_GAP, CARD_SECS = 0.6, 0.28, 0.65, 13.0

# ---------------------------------------------------------------- texto
md = open(os.path.join(HERE, "guion_v2.md"), encoding="utf-8").read()
ROWS = [l for l in md.splitlines() if re.match(r"\| [1-7] \|", l)]
NARR = [r.split("|")[3].strip() for r in ROWS]
SENT = [re.split(r"(?<=[.?!])\s+", t) for t in NARR]
SAY = [("BUB1B", "bub one B"), ("BUBR1", "bub R one"), ("BubR1", "bub R one"),
       ("aneuploidy", "an-yoo-ploidy"), ("aneuploid", "an-yoo-ploid"), ("riboside", "rybo-side"),
       ("fisetin", "fissetin"), ("telangiectasia", "telanjee-ectasia")]
def for_voice(s):
    for a, b in SAY:
        s = s.replace(a, b)
    return s

# ---------------------------------------------------------------- voz
voice = PiperVoice.load(VOICE)
cfg = SynthesisConfig(length_scale=LENGTH_SCALE)
def tts(text):
    key = hashlib.sha1(f"{LENGTH_SCALE}|{text}".encode()).hexdigest()[:16]
    path = os.path.join(BUILD, "tts", key + ".wav")
    if not os.path.exists(path):
        with wave.open(path, "wb") as wf:
            voice.synthesize_wav(for_voice(text), wf, syn_config=cfg)
    with wave.open(path) as wf:
        return path, wf.getnframes() / wf.getframerate(), wf.getframerate()

# línea de tiempo: cada oración con su inicio y fin reales
timeline, t = [], LEAD
for si, sents in enumerate(SENT):
    if si:
        t += SCENE_GAP - GAP
    for k, s in enumerate(sents):
        path, dur, rate = tts(s)
        timeline.append(dict(scene=si, k=k, text=s, wav=path, start=t, end=t + dur))
        t += dur + GAP
SPEECH_END = timeline[-1]["end"]
CARD_START = SPEECH_END + 0.9
TOTAL = CARD_START + CARD_SECS

# ---------------------------------------------------------------- diseño
def fc(pattern):
    return subprocess.run(["fc-match", "-f", "%{file}", pattern], capture_output=True, text=True).stdout
FONT = {"display": fc("Noto Serif Display:semibold"), "serif_it": fc("Noto Serif:italic"),
        "sans": fc("Noto Sans"), "sansb": fc("Noto Sans:bold"), "mono": fc("Noto Sans Mono")}
_cache = {}
def F(kind, size):
    if (kind, size) not in _cache:
        _cache[(kind, size)] = ImageFont.truetype(FONT[kind], size)
    return _cache[(kind, size)]


# símbolos que faltan en Noto (→ − ≥) se dibujan con DejaVu Sans, alineados a la misma línea base
from fontTools.ttLib import TTFont
FALLBACK = fc("DejaVu Sans")
_cmaps, _fb = {}, {}
def _has(font, ch):
    if font.path not in _cmaps:
        _cmaps[font.path] = TTFont(font.path, fontNumber=0).getBestCmap()
    return ch == " " or ord(ch) in _cmaps[font.path]
def _runs(text, font):
    out = []
    for ch in text:
        f = font if _has(font, ch) else _fb.setdefault(font.size, ImageFont.truetype(FALLBACK, font.size))
        if out and out[-1][1] is f:
            out[-1][0] += ch
        else:
            out.append([ch, f])
    return out
def tlen(text, font):
    return sum(f.getlength(t) for t, f in _runs(text, font))
def T(d, xy, text, font, fill):
    x, y = xy
    for t, f in _runs(text, font):
        dy = font.getmetrics()[0] - f.getmetrics()[0]
        d.text((x, y + dy), t, font=f, fill=fill)
        x += f.getlength(t)
    return x

BG, INK, MUTED = (244, 246, 248), (24, 33, 43), (88, 102, 116)
ACCENT, ACCENT_SOFT, LINE, CARD = (43, 95, 138), (226, 236, 245), (210, 219, 228), (255, 255, 255)
WARM, WARM_SOFT, GREEN, GREEN_SOFT = (176, 82, 44), (249, 233, 224), (40, 120, 86), (223, 241, 232)
X0, X1, TOP, BOTTOM = 110, W - 110, 222, 872          # área útil; abajo quedan los subtítulos

def wrap(text, font, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if tlen(trial, font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur); cur = word
    if cur:
        lines.append(cur)
    return lines

def para(d, xy, text, font, fill, width, gap=1.32):
    x, y = xy
    for ln in wrap(text, font, width):
        T(d, (x, y), ln, font=font, fill=fill)
        y += int(font.size * gap)
    return y

def spaced(d, xy, text, font, fill, track=2.5):
    x, y = xy
    for ch in text:
        T(d, (x, y), ch, font=font, fill=fill)
        x += tlen(ch, font) + track
    return x

def slide(eyebrow, title):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    spaced(d, (X0, 74), eyebrow.upper(), F("sansb", 24), ACCENT)
    tag = "PROBAND01 · MVA HACKATHON 2026 · TRACK 2"
    f = F("sans", 22)
    spaced(d, (X1 - tlen(tag, f) - 2.0 * len(tag), 76), tag, f, MUTED, track=2.0)
    if title:
        T(d, (X0, 112), title, font=F("display", 60), fill=INK)
    return img, d

def card(d, box, fill=CARD, outline=LINE, radius=18, width=2):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def pill(d, xy, text, font, fg, bg, pad=(16, 7)):
    x, y = xy
    w = tlen(text, font)
    d.rounded_rectangle((x, y, x + w + 2 * pad[0], y + font.size + 2 * pad[1] + 4), radius=(font.size + 2 * pad[1]) // 2, fill=bg)
    T(d, (x + pad[0], y + pad[1]), text, font=font, fill=fg)
    return x + w + 2 * pad[0]

def load_fig(name, max_w, max_h, crop=None):
    """Devuelve (imagen, escala, origen). Las zonas se dan en coordenadas de la figura original (viewBox del SVG
    o píxeles del PNG); `crop` recorta una región en esas mismas coordenadas."""
    p = os.path.join(FIGS, name)
    if p.endswith(".svg"):
        src_w = float(re.search(r'viewBox="0 0 ([\d.]+)', open(p).read()).group(1))
        im = Image.open(io.BytesIO(cairosvg.svg2png(url=p, output_width=2400))).convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im); im = bg.convert("RGB")
    else:
        im = Image.open(p).convert("RGB"); src_w = im.width
    k = im.width / src_w                                 # píxeles por unidad de la figura original
    org = (0, 0)
    if crop:
        im = im.crop(tuple(int(v * k) for v in crop)); org = (crop[0], crop[1])
    s = min(max_w / im.width, max_h / im.height)
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    return im, k * s, org

def place_fig(img, d, fig, x, y):
    card(d, (x - 14, y - 14, x + fig.width + 14, y + fig.height + 14))
    img.paste(fig, (x, y))

def spot(img, fig, fx, fy, sc, org, boxes, color):
    """Atenúa la figura salvo las zonas marcadas (no tapa nada). El borde rodea la unión de las zonas,
    así nunca cruza texto aunque dos zonas se superpongan."""
    if not boxes:
        return img
    mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(mask)
    for b in boxes:
        md.rounded_rectangle((fx + (b[0] - org[0]) * sc - 6, fy + (b[1] - org[1]) * sc - 6,
                              fx + (b[2] - org[0]) * sc + 6, fy + (b[3] - org[1]) * sc + 6), radius=10, fill=255)
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(ov).rectangle((fx, fy, fx + fig.width, fy + fig.height), fill=(*BG, 150))
    ov.putalpha(ImageChops.multiply(ov.getchannel("A"), ImageChops.invert(mask)))
    out = img.convert("RGBA"); out.alpha_composite(ov); out = out.convert("RGB")
    ring = ImageChops.subtract(mask.filter(ImageFilter.MaxFilter(9)), mask)
    out.paste(Image.new("RGB", img.size, color), mask=ring)
    return out

def side_block(d, y, label, text, color, soft, x, width, lab=24, txt=31, after=22):
    """Bloque de texto con etiqueta de color (columna derecha o bloques a todo el ancho)."""
    f_lab, f_txt = F("sansb", lab), F("sans", txt)
    lines = wrap(text, f_txt, width - 56)
    lh = int(txt * 1.32)
    top = int(lab * 0.9)
    h = top + lab + 18 + len(lines) * lh + top
    card(d, (x, y, x + width, y + h), fill=soft, outline=soft, radius=14)
    d.rectangle((x, y + 14, x + 6, y + h - 14), fill=color)
    spaced(d, (x + 30, y + top), label.upper(), f_lab, color, track=2.0)
    yy = y + top + lab + 18
    for ln in lines:
        T(d, (x + 30, yy), ln, font=f_txt, fill=INK); yy += lh
    return y + h + after

# ---------------------------------------------------------------- escenas (cada una devuelve [(oración_disparo, imagen)])
def scene1():
    out = []
    for step in range(4):
        img, d = slide("Track 2 · Drug repurposing", None)
        T(d, (X0, 236), "One child.", font=F("display", 128), fill=INK)
        if step >= 1:
            T(d, (X0, 384), "One gene.", font=F("display", 128), fill=ACCENT)
        if step >= 2:
            para(d, (X0, 562), "Mosaic variegated aneuploidy (MVA): ultra-rare · very slow growth · high risk of childhood cancer",
                 F("sans", 34), MUTED, 860)
        if step >= 3:
            x = pill(d, (X0, 722), "PROBAND01", F("sansb", 28), CARD, ACCENT)
            pill(d, (x + 16, 722), "BUB1B · two faulty copies", F("sansb", 28), ACCENT, ACCENT_SOFT)
            T(d, (X0, 790), "c.2210T>G p.(Leu737Ter)", font=F("mono", 26), fill=MUTED)
            T(d, (X0, 828), "c.3006T>G p.(Asn1002Lys)   identified in Track 1", font=F("mono", 26), fill=MUTED)
        out.append(([0, 1, 2, 3][step], img))
    return out

# zonas de la Fig 1 (coordenadas del viewBox 920x600)
F1 = {"bub1b": (250, 44, 670, 96), "bubr1": (240, 126, 680, 182), "ax1": (40, 226, 420, 542),
      "ax2": (500, 226, 880, 542), "baker": (500, 390, 880, 456)}
def scene2():
    fig, sc, org = load_fig("fig1_mechanism.svg", 1040, BOTTOM - TOP - 30)
    fx, fy = X0 + 14, TOP + 26
    plan = [(0, ["bubr1"], 0), (1, ["bub1b"], 0), (2, ["ax1", "ax2"], 0), (3, ["ax1"], 1), (4, ["ax2"], 2), (5, ["baker"], 3)]
    cols = {"bub1b": ACCENT, "bubr1": ACCENT, "ax1": WARM, "ax2": GREEN, "baker": ACCENT}
    out = []
    for trig, marks, nside in plan:
        img, d = slide("The mechanism", "One defect, two axes")
        place_fig(img, d, fig, fx, fy)
        mcol = {cols[m] for m in marks}
        img = spot(img, fig, fx, fy, sc, org, [F1[m] for m in marks], mcol.pop() if len(mcol) == 1 else ACCENT)
        d = ImageDraw.Draw(img)
        x, w, y = X0 + fig.width + 70, X1 - (X0 + fig.width + 70), TOP + 12
        if nside >= 1:
            y = side_block(d, y, "Axis 1 · chromosomes", "Chromosomes gained and lost → raised cancer risk", WARM, WARM_SOFT, x, w)
        if nside >= 2:
            y = side_block(d, y, "Axis 2 · cell aging", "Cells age too early → linked to growth failure and muscle loss", GREEN, GREEN_SOFT, x, w)
        if nside >= 3:
            side_block(d, y, "Baker et al., Nature 2011", "First proof that clearing senescent cells delays age-related disease, in BubR1-low mice",
                       ACCENT, ACCENT_SOFT, x, w)
        out.append((trig, img))
    return out

# Fig 2 en dos tiempos (píxeles del PNG original 1987x1396): panel A agrandado, después panel B
F2_A, F2_B = (330, 0, 1600, 545), (0, 646, 1975, 1370)
F2 = {"bub1b": (345, 258, 1560, 300), "aurkb": (345, 96, 1560, 138), "ttk": (345, 314, 1560, 356),
      "ttk_note": (478, 314, 748, 410)}   # la nota "cytotoxic Aurora / MPS1 inhibitors"
def scene3():
    figA = load_fig("fig2_druggability.png", 1080, BOTTOM - TOP - 30, crop=F2_A)
    figB = load_fig("fig2_druggability.png", 1080, BOTTOM - TOP - 30, crop=F2_B)
    plan = [(0, figA, [], 0, ACCENT), (2, figA, ["bub1b"], 1, ACCENT), (3, figA, ["aurkb", "ttk", "ttk_note"], 2, WARM), (4, figB, [], 3, GREEN)]
    out = []
    for trig, (fig, sc, org), marks, nside, col in plan:
        img, d = slide("Why downstream", "The gene itself is not a drug target")
        fx, fy = X0 + 14, TOP + 26
        place_fig(img, d, fig, fx, fy)
        img = spot(img, fig, fx, fy, sc, org, [F2[m] for m in marks], col)
        d = ImageDraw.Draw(img)
        x = X0 + 1080 + 70; w, y = X1 - x, TOP + 12
        if nside >= 1:
            y = side_block(d, y, "DepMap · Open Targets", "Pan-essential in DepMap (median CRISPR effect −1.21) · 0 drugs or clinical candidates",
                           ACCENT, ACCENT_SOFT, x, w, lab=22, txt=29)
        if nside >= 2:
            y = side_block(d, y, "Nearby compounds", "Spindle poisons and chemotherapy → would weaken the checkpoint further",
                           WARM, WARM_SOFT, x, w, lab=22, txt=29)
        if nside >= 3:
            side_block(d, y, "So", "Search downstream, on the two consequences", GREEN, GREEN_SOFT, x, w, lab=22, txt=29)
        out.append((trig, img))
    return out

# filas de los tres candidatos propuestos en la Fig 4 (píxeles del PNG original 2447x1009)
F4_PROPOSED = (8, 124, 2440, 380)
def scene4():
    fig, sc, org = load_fig("fig4_convergence.png", X1 - X0 - 28, BOTTOM - TOP - 40)
    fx, fy = (W - fig.width) // 2, TOP + 26
    out = []
    for step, trig in enumerate([0, (0, 0.62), 1]):
        img, d = slide("The search", "Eleven independent lines of evidence")
        place_fig(img, d, fig, fx, fy)
        if step >= 1:
            img = spot(img, fig, fx, fy, sc, org, [F4_PROPOSED], GREEN)
            d = ImageDraw.Draw(img)
        if step >= 2:                                   # sello de verificación, arriba a la derecha junto al título
            f1, f2 = F("mono", 22), F("sansb", 26)
            label = "138 / 138 re-checked"
            wtot = tlen("audit_report.py", f1) + 32 + 14 + tlen(label, f2)
            x = X1 - wtot
            title_end = X0 + tlen("Eleven independent lines of evidence", F("display", 60))
            assert x > title_end + 30, "el sello se pisa con el título"
            x = pill(d, (x, 134), "audit_report.py", f1, CARD, ACCENT)
            T(d, (x + 14, 134), label, font=f2, fill=ACCENT)
        out.append((trig, img))
    return out

CANDS = [
    ("1", "Metformin", "APPROVED DRUG", ACCENT, ACCENT_SOFT,
     [("How", "AMPK activation: energy stress that aneuploid cells tolerate poorly"),
      ("In children", "Fanconi anemia trial: tested dose, no metabolic acidosis")], "Highest"),
    ("2", "Nicotinamide riboside", "SUPPLEMENT · VITAMIN B3", WARM, WARM_SOFT,
     [("How", "NAD⁺ → SIRT2 → BUBR1; an NAD⁺ precursor raised BubR1 in mice"),
      ("In children", "Ataxia-telangiectasia: 25 mg/kg/day, well tolerated")], "Moderate"),
    ("3", "Fisetin", "SUPPLEMENT", GREEN, GREEN_SOFT,
     [("How", "Senolytic: clears senescent cells (the aging axis)"),
      ("In children", "No data; adult trials only")], "Lowest clinically"),
]
def scene5():
    """Las tres tarjetas aparecen enseguida (nombre y tipo); el detalle de cada una entra cuando la voz la nombra."""
    out = []
    cw, gap = (X1 - X0 - 2 * 40) // 3, 40
    for step, trig in enumerate([0, 1, 3, 5]):
        img, d = slide("The candidates", "Ranked by evidence in children")
        T(d, (X0, 200), "One approved drug and two widely available supplements", font=F("sans", 32), fill=MUTED)
        for i, (rank, name, tag, col, soft, rows, conf) in enumerate(CANDS):
            x = X0 + i * (cw + gap); y0, y1 = 268, BOTTOM
            full = step >= i + 1
            card(d, (x, y0, x + cw, y1), fill=CARD if full else BG, outline=LINE if full else LINE, width=2 if full else 3)
            d.rectangle((x + 18, y0, x + cw - 18, y0 + 8), fill=col if full else LINE)
            T(d, (x + 30, y0 + 22), rank, font=F("display", 90), fill=col)
            yy = para(d, (x + 110, y0 + 40), name, F("display", 44), INK if full else MUTED, cw - 140, gap=1.15)
            pill(d, (x + 110, max(yy + 6, y0 + 100)), tag, F("sansb", 20), col, soft, pad=(12, 5))
            if not full:
                continue
            yy = y0 + 196
            for lab, txt in rows:
                spaced(d, (x + 30, yy), lab.upper(), F("sansb", 22), MUTED, track=2.0)
                yy = para(d, (x + 30, yy + 34), txt, F("sans", 32), INK, cw - 60) + 26
            d.line((x + 30, y1 - 78, x + cw - 30, y1 - 78), fill=LINE, width=2)
            xx = spaced(d, (x + 30, y1 - 56), "CONFIDENCE", F("sansb", 22), MUTED, track=2.0)
            T(d, (xx + 16, y1 - 62), conf, font=F("sansb", 30), fill=col)
        out.append((trig, img))
    return out

def scene6():
    blocks = [
        ("Pharmacogenes (research-grade)", "No barrier to the proposed agents · monitor kidney function on metformin", ACCENT, ACCENT_SOFT),
        ("Recommended for all MVA types", "Tumor surveillance: kidney ultrasound every 3 months, from birth to age 7 (Nakano et al. 2024)", GREEN, GREEN_SOFT),
        ("What this is", "A hypothesis for a supervised single-patient (n-of-1) trial, with biomarkers to judge response. Not a proven treatment.", WARM, WARM_SOFT),
    ]
    out = []
    for step, trig in enumerate([0, 1, 2]):
        img, d = slide("Safety and framing", "Ready to discuss, not yet proven")
        y = TOP + 10
        for i, (lab, txt, col, soft) in enumerate(blocks):
            if step >= i:
                y = side_block(d, y, lab, txt, col, soft, X0, X1 - X0, lab=28, txt=44, after=34)
        out.append((trig, img))
    return out

def scene7():
    out = []
    for step, trig in enumerate([0, 1]):
        img, d = slide("Scalability", "Reusable for the next child")
        y = TOP + 30
        for big, small in [("Public", "databases only — plus the gene found in Track 1"),
                           ("Laptop", "a dual-core laptop runs the whole pipeline"),
                           ("138 / 138", "checks re-run against their sources by a script")]:
            T(d, (X0, y), big, font=F("display", 64), fill=ACCENT)
            T(d, (X0 + 380, y + 22), small, font=F("sans", 34), fill=INK)
            y += 112
        T(d, (X0, y + 10), "github.com/hernanysa/mva-hackathon-2026-bub1b", font=F("mono", 32), fill=MUTED)
        if step >= 1:
            T(d, (X0, y + 100), "Thank you to the child and family behind PROBAND01.", font=F("serif_it", 46), fill=INK)
        out.append((trig, img))
    return out

ACK = ("This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, "
       "Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship "
       "from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and "
       "their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible.")
def final_card():
    img, d = slide("Acknowledgement", None)
    y = para(d, (X0, 190), ACK, F("sans", 38), INK, X1 - X0, gap=1.42)
    d.line((X0, y + 30, X1, y + 30), fill=LINE, width=2)
    y = para(d, (X0, y + 64), "Narration: synthetic voice (Piper TTS). Analysis and video prepared with AI assistance (Claude, Anthropic).",
             F("sans", 30), MUTED, X1 - X0)
    T(d, (X0, y + 12), "Code and report: github.com/hernanysa/mva-hackathon-2026-bub1b", font=F("mono", 30), fill=MUTED)
    return img

SCENES = [scene1, scene2, scene3, scene4, scene5, scene6, scene7]

# ---------------------------------------------------------------- diapositivas con su momento de entrada
def trig_time(spans, trig):
    if isinstance(trig, tuple):
        k, frac = trig
        return spans[k][0] + frac * (spans[k][1] - spans[k][0])
    return spans[trig][0]

shots = []                      # dict(img, start, scene, first)
for si, build in enumerate(SCENES):
    spans = {e["k"]: (e["start"], e["end"]) for e in timeline if e["scene"] == si}
    for n, (trig, img) in enumerate(build()):
        img.save(os.path.join(BUILD, "frames", f"s{si + 1}_{n}.png"))     # para revisar a ojo
        st = 0.0 if (si == 0 and n == 0) else max(0.0, trig_time(spans, trig) - (0.35 if n == 0 else 0.12))
        shots.append(dict(img=img, start=st, scene=si, first=(n == 0)))
card_img = final_card(); card_img.save(os.path.join(BUILD, "frames", "s8_card.png"))
shots.append(dict(img=card_img, start=CARD_START, scene=None, first=True))
SPAN = {}
for i, sh in enumerate(shots):
    if sh["first"] and sh["scene"] is not None:
        nxt = next((x["start"] for x in shots[i + 1:] if x["first"]), TOTAL)
        SPAN[sh["scene"]] = (sh["start"], nxt)

# ---------------------------------------------------------------- animación de la intro: una célula que separa mal un cromosoma
def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)
def lerp(a, b, u):
    return a + (b - a) * u
import math
import numpy as np
CHROMO = [(46, 98, 150), WARM, (36, 128, 92), (124, 92, 168)]   # el cromosoma 1 (naranja) no se engancha
MBOX = (1000, 196, 1860, 872)
def _shade(c, k):
    return tuple(int(max(0, min(255, v * k))) for v in c)
def _bez(p0, c, p1, n=22):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1]) for t in (i / n for i in range(n + 1))]
def _rot(pt, c, ang):
    x, y = pt[0] - c[0], pt[1] - c[1]
    return (c[0] + x * math.cos(ang) - y * math.sin(ang), c[1] + x * math.sin(ang) + y * math.cos(ang))

def with_mitosis(base, p):
    """Mitosis con el defecto de MVA1: un cromosoma no se engancha, la señal de 'esperar' es débil (poco BUBR1)
    y la célula se divide igual → una hija con un cromosoma de menos y otra con uno de más."""
    SS = 2
    bw, bh = MBOX[2] - MBOX[0], MBOX[3] - MBOX[1]
    W2, H2 = bw * SS, bh * SS
    secs = p * (SPAN[0][1] - SPAN[0][0])
    A = lambda a: int(255 * max(0.0, min(1.0, a)))
    S = lambda v: v * SS
    Si = lambda v: max(1, int(round(v * SS)))
    cx, cy = bw / 2, bh / 2 - 22
    appear = ease(p / 0.07)
    spindle = ease((p - 0.03) / 0.12)
    meta = ease((p - 0.08) / 0.22)
    ana = ease((p - 0.47) / 0.18)
    ana_slow = ease((p - 0.50) / 0.22)
    cyto = ease((p - 0.62) / 0.16)
    lab = ease((p - 0.80) / 0.06)

    # --- célula: metaballs elípticas → el surco de división aparece solo al separarse los centros
    rx, ry = 177.0, 131.0
    dx = 238.0 * cyto
    yy, xx = np.mgrid[0:H2, 0:W2].astype(np.float32) / SS
    f = np.zeros_like(xx)
    for c0 in (cx - dx, cx + dx):
        f += 1.0 / (((xx - c0) / rx) ** 2 + ((yy - cy) / ry) ** 2 + 1e-3)
    inside = np.clip((f - 1.0) * 14.0 + 0.5, 0, 1)          # borde suave
    shade = np.clip((f - 1.0) / 1.6, 0, 1)[..., None]
    outer, inner = np.array([214, 228, 240], np.float32), np.array([243, 248, 252], np.float32)
    rgb = outer * (1 - shade) + inner * shade
    mem = np.clip(1 - np.abs(f - 1.0) / 0.055, 0, 1)        # membrana
    mem2 = np.clip(1 - np.abs(f - 1.22) / 0.03, 0, 1) * 0.35  # contorno interno tenue
    memc = np.array(ACCENT, np.float32)
    rgb = rgb * (1 - mem[..., None]) + memc * mem[..., None]
    rgb = rgb * (1 - mem2[..., None]) + np.array([255, 255, 255], np.float32) * mem2[..., None]
    alpha = np.maximum(inside, mem) * appear
    lay = Image.fromarray(np.dstack([rgb, alpha[..., None] * 255]).astype(np.uint8), "RGBA")
    d = ImageDraw.Draw(lay, "RGBA")

    # --- polos (centrosomas) y husos
    pl, pr = (cx - 196 - 60 * cyto, cy), (cx + 196 + 60 * cyto, cy)
    pole_a = spindle * (1 - cyto)
    mt_a = spindle * (1 - ease((p - 0.66) / 0.10))
    if mt_a > 0.02:
        for pole, sgn in ((pl, 1), (pr, -1)):
            for i in range(9):                                   # microtúbulos polares (forma de huso)
                ty = cy + (i - 4) * 30
                tx = cx + sgn * 26
                ctrl = ((pole[0] + tx) / 2, cy + (ty - cy) * 1.55)
                d.line([(S(x), S(y)) for x, y in _bez(pole, ctrl, (tx, ty))], fill=(*MUTED, A(0.22 * mt_a)), width=Si(1.4))
            for ang in (-60, -30, 0, 30, 60):                    # áster
                a_ = math.radians(ang + (180 if sgn == 1 else 0))
                d.line((S(pole[0]), S(pole[1]), S(pole[0] + 46 * math.cos(a_)), S(pole[1] + 46 * math.sin(a_))),
                       fill=(*MUTED, A(0.25 * mt_a)), width=Si(1.2))
    if pole_a > 0.02:
        for pole in (pl, pr):
            for r, al in ((26, 0.10), (18, 0.18), (11, 0.35)):
                d.ellipse((S(pole[0] - r), S(pole[1] - r), S(pole[0] + r), S(pole[1] + r)), fill=(*ACCENT, A(al * pole_a)))
            d.rounded_rectangle((S(pole[0] - 9), S(pole[1] - 3), S(pole[0] + 1), S(pole[1] + 3)), radius=S(2), fill=(*INK, A(pole_a)))
            d.rounded_rectangle((S(pole[0] + 1), S(pole[1] - 8), S(pole[0] + 7), S(pole[1] + 2)), radius=S(2), fill=(*INK, A(pole_a)))

    # --- cromosomas: X en metafase, V al separarse
    plate = [(cx, cy - 122), (cx + 122, cy - 98), (cx, cy - 6), (cx, cy + 108)]   # el naranja (1) no llega a la placa
    scat = [(cx - 112, cy - 58), (cx + 64, cy - 122), (cx - 38, cy + 96), (cx + 104, cy + 52)]
    rot0 = [0.62, -0.85, 1.15, -0.35]
    final_y = [cy - 92, cy - 44, cy + 2, cy + 94]
    halo_c = None
    for k in range(4):
        col = CHROMO[k]
        pc = (lerp(scat[k][0], plate[k][0], meta), lerp(scat[k][1], plate[k][1], meta))
        ang = rot0[k] * (1 - meta)
        if k == 1:
            ang = rot0[k] * (1 - meta) + 0.35 * meta            # queda torcido: un solo lado enganchado
        sisters = []
        for side in (-1, 1):
            u = ana_slow if (k == 1 and side == -1) else ana
            if k == 1:
                dest_x = cx + 175 + 63 * cyto + (52 if side == -1 else 82)     # las dos al polo derecho
            else:
                dest_x = cx + side * (175 + 63 * cyto) if True else 0
            dest = (dest_x, final_y[k] + (4 if (k == 1 and side == -1) else 0))
            cen0 = (pc[0] + side * 7, pc[1])
            cen = (lerp(cen0[0], dest[0], u), lerp(cen0[1], dest[1], u))
            move_dir = 1 if dest[0] > cen0[0] else -1
            tip = lerp(side * 9, -move_dir * 22, u)                # >< en metafase → V que arrastra los brazos
            tip = lerp(tip, -move_dir * 5, cyto)                   # al terminar se relajan a bastones
            arm = 1 - 0.26 * u
            pts = [(cen[0] + tip, cen[1] - 40 * arm), cen, (cen[0] + tip, cen[1] + 44 * arm)]
            if u < 0.02:
                pts = [_rot(q, pc, ang) for q in pts]
            sisters.append((side, pts, cen))
        # fibras de cinetocoro
        if mt_a > 0.02:
            for side, pts, cen in sisters:
                kin = pts[1]
                if k == 1 and side == -1:
                    halo_c = kin
                    continue                                       # este cinetocoro queda sin enganchar
                pole = pr if (k == 1 or side == 1) else pl
                ctrl = ((pole[0] + kin[0]) / 2, (pole[1] + kin[1]) / 2 + (kin[1] - pole[1]) * 0.18)
                fc_ = WARM if k == 1 else (70, 86, 102)
                d.line([(S(x), S(y)) for x, y in _bez(pole, ctrl, kin)], fill=(*fc_, A((0.85 if k == 1 else 0.55) * mt_a * meta)), width=Si(2.2))
        # cromátidas con borde, relleno y brillo
        for side, pts, cen in sisters:
            P = [(S(x), S(y)) for x, y in pts]
            for w, colr, off in ((17, _shade(col, 0.62), 0), (13, col, 0), (4, _shade(col, 1.45), -2.2)):
                Q = [(x + S(off), y + S(off)) for x, y in P]
                d.line(Q, fill=(*colr, A(appear)), width=Si(w), joint="curve")
                for x, y in (Q[0], Q[-1]):
                    d.ellipse((x - S(w) / 2, y - S(w) / 2, x + S(w) / 2, y + S(w) / 2), fill=(*colr, A(appear)))
            if ana < 0.3:
                kx, ky = pts[1]
                d.ellipse((S(kx - 4), S(ky - 4), S(kx + 4), S(ky + 4)), fill=(*INK, A(appear * (1 - ana / 0.3) * 0.85)))

    # --- cinetocoro sin enganchar: halo que titila y señal de "esperar" débil (poco BUBR1)
    sig = ease((p - 0.16) / 0.05) * (1 - ease((p - 0.45) / 0.04))
    if halo_c and sig > 0.02:
        hx, hy = halo_c
        pulse = 0.5 + 0.5 * math.sin(secs * 6.0)
        for r, al in ((22 + 6 * pulse, 0.18), (13 + 3 * pulse, 0.35)):
            d.ellipse((S(hx - r), S(hy - r), S(hx + r), S(hy + r)), outline=(*WARM, A(al * sig * 2)), width=Si(2.5))
        weak = 1 - ease((p - 0.33) / 0.10)                         # la señal se apaga
        for i in range(10):
            ph = (secs * 0.55 + i / 10) % 1.0
            angp = i * 2.4
            rr = 14 + 70 * ph
            px_, py_ = hx + rr * math.cos(angp), hy + rr * math.sin(angp)
            al = (1 - ph) * 0.8 * sig * weak * (0.35 if i % 3 else 1.0)
            if al > 0.02:
                d.ellipse((S(px_ - 3.2), S(py_ - 3.2), S(px_ + 3.2), S(py_ + 3.2)), fill=(*WARM, A(al)))

    # --- indicador del control (arriba): esperando → señal débil → sigue igual
    states = [("Checkpoint: waiting for every chromosome", (196, 146, 30), 0.10, 0.33),
              ("Low BUBR1: the 'wait' signal is too weak", WARM, 0.33, 0.47),
              ("Division proceeds anyway", (186, 52, 40), 0.47, 0.80)]
    for txt, dot, a0, a1 in states:
        al = ease((p - a0) / 0.025) * (1 - ease((p - (a1 - 0.025)) / 0.025))   # sin superponerse con el siguiente
        if al <= 0.02:
            continue
        f_ = F("sansb", 23 * SS)
        w = tlen(txt, f_)
        x0, y0 = S(bw / 2) - (w + S(52)) / 2, S(6)
        d.rounded_rectangle((x0, y0, x0 + w + S(52), y0 + S(44)), radius=S(22), fill=(255, 255, 255, A(al * 0.95)),
                            outline=(*_shade(dot, 1.0), A(al)), width=Si(2))
        d.ellipse((x0 + S(16), y0 + S(15), x0 + S(30), y0 + S(29)), fill=(*dot, A(al)))
        T(d, (x0 + S(40), y0 + S(9)), txt, font=f_, fill=(*INK, A(al)))
    # --- resultado
    if lab > 0.02:
        for c0, txt, colr in ((cx - 238, "one chromosome too few", MUTED), (cx + 238, "one chromosome too many", WARM)):
            f_ = F("sansb", 25 * SS)
            T(d, (S(c0) - tlen(txt, f_) / 2, S(cy + ry + 34)), txt, font=f_, fill=(*colr, A(lab)))
        f_ = F("sans", 25 * SS)
        cap = "Weak checkpoint → division starts too early → aneuploid cells"
        T(d, (S(bw / 2) - tlen(cap, f_) / 2, S(cy + ry + 84)), cap, font=f_, fill=(*INK, A(lab)))
    lay = lay.resize((bw, bh), Image.LANCZOS)
    out = base.convert("RGBA")
    out.alpha_composite(lay, (MBOX[0], MBOX[1]))
    return out.convert("RGB")

# ---------------------------------------------------------------- audio completo
with wave.open(timeline[0]["wav"]) as wf:
    rate = wf.getframerate()
total_frames = int(TOTAL * rate)
buf = bytearray(total_frames * 2)
for e in timeline:
    with wave.open(e["wav"]) as wf:
        data = wf.readframes(wf.getnframes())
    off = int(e["start"] * rate) * 2
    buf[off:off + len(data)] = data[: max(0, len(buf) - off)]
narr = os.path.join(BUILD, "narration.wav")
with wave.open(narr, "wb") as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(rate); wf.writeframes(bytes(buf))

# ---------------------------------------------------------------- subtítulos (trozos de hasta ~84 caracteres)
def chunks(sentence, limit=84):
    if len(sentence) <= limit:
        return [sentence]
    parts = re.split(r"(?<=[,;:])\s+", sentence)
    out, cur = [], ""
    for p in parts:
        if cur and len(cur) + 1 + len(p) > limit:
            out.append(cur); cur = p
        else:
            cur = (cur + " " + p).strip()
    out.append(cur)
    final = []
    for c in out:                                  # cortes por palabra si algún trozo sigue largo
        while len(c) > limit:
            cut = c.rfind(" ", 0, limit)
            final.append(c[:cut]); c = c[cut + 1:]
        final.append(c)
    return final
cues = []
for e in timeline:
    parts = chunks(e["text"])
    tot = sum(len(p) for p in parts); t0 = e["start"]
    for p in parts:
        dt = (e["end"] - e["start"]) * len(p) / tot
        cues.append((t0, t0 + dt, p)); t0 += dt
def ts(x, sep):
    h, m, s = int(x // 3600), int(x % 3600 // 60), x % 60
    return f"{h:02d}:{m:02d}:{int(s):02d}{sep}{min(999, int(round((s - int(s)) * 1000))):03d}"
with open(os.path.join(HERE, "hysa_track2_pitch.srt"), "w", encoding="utf-8") as fh:
    for i, (a, b, txt) in enumerate(cues, 1):
        fh.write(f"{i}\n{ts(a, ',')} --> {ts(b, ',')}\n{txt}\n\n")
ass = os.path.join(BUILD, "subs.ass")
with open(ass, "w", encoding="utf-8") as fh:
    fh.write("[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nWrapStyle: 0\n\n"
             "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
             "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
             "Style: Sub,Noto Sans,44,&H00FFFFFF,&H00FFFFFF,&H33241A12,&H00000000,0,0,0,0,100,100,0,0,3,14,0,2,260,260,42,1\n\n"
             "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    for a, b, txt in cues:
        fh.write(f"Dialogue: 0,{ts(a, '.')[1:-1]},{ts(b, '.')[1:-1]},Sub,,0,0,0,,{txt}\n")

if os.environ.get("PREVIEW"):                                 # PREVIEW=1: solo cuadros de muestra, sin video
    for pp in (0.06, 0.24, 0.40, 0.55, 0.72, 0.92):
        with_mitosis(shots[3]["img"], pp).save(os.path.join(BUILD, f"preview_mitosis_{pp}.png"))
    raise SystemExit("preview listo")

# ---------------------------------------------------------------- render cuadro por cuadro
TR_STEP, TR_SCENE, ZOOM = 0.35, 0.55, 0.035
def frame_of(j, t):
    sh = shots[j]
    img = sh["img"]
    if sh["scene"] == 0:
        a, b = SPAN[0]
        img = with_mitosis(img, (t - a) / (b - a))
    if sh["scene"] is None:
        return img
    a, b = SPAN[sh["scene"]]
    z = 1 + ZOOM * max(0.0, min(1.0, (t - a) / (b - a)))
    cw, ch = W / z, H / z
    return img.resize((W, H), Image.BICUBIC, box=((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2))

out = os.path.join(HERE, "hysa_track2_pitch.mp4")
vf = f"subtitles={ass},format=yuv420p,fade=t=in:st=0:d=0.6,fade=t=out:st={TOTAL - 0.9:.2f}:d=0.9"
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
       "-i", narr, "-vf", vf, "-af", f"afade=t=out:st={TOTAL - 0.9:.2f}:d=0.9",
       "-c:v", "libx264", "-preset", "fast", "-crf", "21", "-c:a", "aac", "-b:a", "128k",
       "-t", f"{TOTAL:.2f}", "-movflags", "+faststart", out]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
nframes, j, last_static = int(TOTAL * FPS), 0, None
for fi in range(nframes):
    t = fi / FPS
    while j + 1 < len(shots) and shots[j + 1]["start"] <= t:
        j += 1
    sh = shots[j]
    tr = TR_SCENE if sh["first"] else TR_STEP
    if sh["scene"] is None and t - sh["start"] >= tr:          # placa final quieta: se reutiliza el cuadro
        if last_static is None:
            last_static = sh["img"].tobytes()
        proc.stdin.write(last_static)
        continue
    cur = frame_of(j, t)
    if j > 0 and t - sh["start"] < tr:
        cur = Image.blend(frame_of(j - 1, t), cur, ease((t - sh["start"]) / tr))
    proc.stdin.write(cur.tobytes())
proc.stdin.close()
if proc.wait() != 0:
    raise SystemExit("ffmpeg falló")
print(f"OK -> {out}  ({TOTAL:.1f} s; voz hasta {SPEECH_END:.1f} s; {len(timeline)} oraciones; {len(cues)} subtítulos)")
