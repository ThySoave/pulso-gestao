"""
Gera logo, banner do Facebook e cards de post para o Pulso Negócios.
Uso:
  python3 gerar_marca.py logo
  python3 gerar_marca.py banner
  python3 gerar_marca.py card "Frase de impacto aqui"
  python3 gerar_marca.py todos
"""

import sys
import os
from PIL import Image, ImageDraw, ImageFont

# ── Cores da marca ────────────────────────────────────────────────────────────
AZUL    = "#1B2B4B"
DOURADO = "#E8A84C"
BRANCO  = "#FFFFFF"
CINZA   = "#B0B8C8"

FONTS_DIR = os.path.join(os.path.dirname(__file__), "fonts")
OUT_DIR   = os.path.join(os.path.dirname(__file__), "marca")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Fontes ────────────────────────────────────────────────────────────────────
FONT_BOLD   = "/usr/share/fonts/opentype/urw-base35/NimbusSans-Bold.otf"
FONT_REG    = "/usr/share/fonts/opentype/urw-base35/NimbusSans-Regular.otf"
FONT_NARROW = "/usr/share/fonts/opentype/urw-base35/NimbusSansNarrow-Bold.otf"

def _font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def _hex(cor):
    cor = cor.lstrip("#")
    return tuple(int(cor[i:i+2], 16) for i in (0, 2, 4))

def _pulso_line(draw, x, y, w, h, cor, espessura=3):
    """Desenha linha de pulso (ECG) estilizada."""
    pts = [
        (x,              y + h//2),
        (x + w*0.20,     y + h//2),
        (x + w*0.30,     y + h//2),
        (x + w*0.38,     y + h*0.15),
        (x + w*0.46,     y + h*0.85),
        (x + w*0.54,     y + h*0.10),
        (x + w*0.62,     y + h//2),
        (x + w*0.70,     y + h//2),
        (x + w,          y + h//2),
    ]
    for i in range(len(pts)-1):
        draw.line([pts[i], pts[i+1]], fill=cor, width=espessura)

# ── LOGO (600×200 px, fundo transparente) ─────────────────────────────────────
def gerar_logo():
    W, H = 600, 200
    img  = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Fundo arredondado
    draw.rounded_rectangle([0, 0, W-1, H-1], radius=18,
                            fill=_hex(AZUL) + (255,))

    # Linha de pulso dourada
    _pulso_line(draw, 30, 30, 200, 80, _hex(DOURADO), espessura=5)

    # Texto PULSO
    f_titulo = _font(FONT_BOLD, 72)
    draw.text((250, 28), "PULSO", font=f_titulo, fill=_hex(DOURADO))

    # Texto NEGÓCIOS
    f_sub = _font(FONT_REG, 32)
    draw.text((253, 110), "NEGÓCIOS", font=f_sub, fill=_hex(BRANCO))

    # Linha separadora dourada abaixo de NEGÓCIOS
    draw.rectangle([252, 150, 570, 153], fill=_hex(DOURADO))

    # Tagline
    f_tag = _font(FONT_REG, 18)
    draw.text((253, 160), "Diagnóstico · Sistema · Resultado", font=f_tag,
              fill=_hex(CINZA))

    path = os.path.join(OUT_DIR, "logo.png")
    img.save(path)
    print(f"✅ Logo salvo: {path}")
    return path

# ── BANNER FACEBOOK (851×315 px) ─────────────────────────────────────────────
def gerar_banner():
    W, H = 851, 315
    img  = Image.new("RGB", (W, H), _hex(AZUL))
    draw = ImageDraw.Draw(img)

    # Faixas decorativas douradas (canto direito)
    for i, alpha in enumerate([40, 25, 15]):
        offset = i * 40
        draw.polygon(
            [(W - 200 + offset, 0), (W, 0), (W, H), (W - 350 + offset, H)],
            fill=(*_hex(DOURADO), alpha)
        )

    # Linha de pulso grande (fundo decorativo)
    _pulso_line(draw, 0, 60, W, 200, (*_hex(DOURADO), 30) if False else _hex(DOURADO),
                espessura=2)

    # Logo na esquerda
    logo_path = os.path.join(OUT_DIR, "logo.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo = logo.resize((360, 120), Image.LANCZOS)
        img.paste(logo, (50, 50), logo)
    else:
        f = _font(FONT_BOLD, 60)
        draw.text((50, 60), "PULSO", font=f, fill=_hex(DOURADO))
        f2 = _font(FONT_REG, 28)
        draw.text((53, 130), "NEGÓCIOS", font=f2, fill=_hex(BRANCO))

    # Tagline central
    f_tag  = _font(FONT_BOLD, 28)
    f_sub  = _font(FONT_REG, 20)
    draw.text((50, 195), "Seu negócio tem mais potencial do que você vê.",
              font=f_tag, fill=_hex(BRANCO))
    draw.text((50, 235), "Diagnóstico gratuito · Sistema sob medida · Resultado real",
              font=f_sub, fill=_hex(CINZA))

    # Site
    f_site = _font(FONT_BOLD, 22)
    draw.text((50, 275), "pulso-negocios.com", font=f_site, fill=_hex(DOURADO))

    path = os.path.join(OUT_DIR, "banner_facebook.png")
    img.save(path, quality=95)
    print(f"✅ Banner salvo: {path}")
    return path

# ── CARD DE POST INSTAGRAM (1080×1080 px) ─────────────────────────────────────
def gerar_card(frase, nome_arquivo="card.png"):
    W, H = 1080, 1080
    img  = Image.new("RGB", (W, H), _hex(AZUL))
    draw = ImageDraw.Draw(img)

    # Bordas douradas
    draw.rectangle([0, 0, W-1, H-1], outline=_hex(DOURADO), width=8)
    draw.rectangle([16, 16, W-17, H-17], outline=(*_hex(DOURADO)[:3],), width=2)

    # Linha de pulso decorativa (topo)
    _pulso_line(draw, 60, 80, 960, 100, _hex(DOURADO), espessura=3)

    # Linha separadora
    draw.rectangle([60, 200, W-60, 203], fill=_hex(DOURADO))

    # Frase principal (quebra automática)
    f_frase = _font(FONT_BOLD, 68)
    palavras = frase.split()
    linhas, linha_atual = [], ""
    for palavra in palavras:
        teste = (linha_atual + " " + palavra).strip()
        bbox  = draw.textbbox((0, 0), teste, font=f_frase)
        if bbox[2] - bbox[0] > 940:
            if linha_atual:
                linhas.append(linha_atual)
            linha_atual = palavra
        else:
            linha_atual = teste
    if linha_atual:
        linhas.append(linha_atual)

    # Centralizar o bloco de texto verticalmente
    altura_total = len(linhas) * 85
    y_start = (H - altura_total) // 2 - 40
    for linha in linhas:
        bbox = draw.textbbox((0, 0), linha, font=f_frase)
        x = (W - (bbox[2] - bbox[0])) // 2
        draw.text((x, y_start), linha, font=f_frase, fill=_hex(DOURADO))
        y_start += 85

    # Linha separadora (rodapé)
    draw.rectangle([60, H-200, W-60, H-197], fill=_hex(DOURADO))

    # Logo no rodapé
    logo_path = os.path.join(OUT_DIR, "logo.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo = logo.resize((300, 100), Image.LANCZOS)
        img.paste(logo, ((W - 300)//2, H - 180), logo)
    else:
        f_logo = _font(FONT_BOLD, 36)
        draw.text((W//2, H-160), "PULSO NEGÓCIOS", font=f_logo,
                  fill=_hex(DOURADO), anchor="mm")

    # @pulsonegocios
    f_at = _font(FONT_REG, 28)
    draw.text((W//2, H - 55), "@pulsonegocios", font=f_at,
              fill=_hex(CINZA), anchor="mm")

    path = os.path.join(OUT_DIR, nome_arquivo)
    img.save(path, quality=95)
    print(f"✅ Card salvo: {path}")
    return path

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "todos"

    if cmd == "logo":
        gerar_logo()
    elif cmd == "banner":
        gerar_logo()
        gerar_banner()
    elif cmd == "card":
        frase = sys.argv[2] if len(sys.argv) > 2 else "Seu negócio está perdendo dinheiro sem você saber."
        gerar_card(frase)
    elif cmd == "todos":
        gerar_logo()
        gerar_banner()
        gerar_card("Seu negócio está perdendo dinheiro sem você saber.", "card_exemplo.png")
        print("\n📁 Tudo em:", OUT_DIR)
