"""Gerador de relatório PDF do diagnóstico — Pulso Gestão."""

import os
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String

AZUL     = colors.HexColor("#1B2B4B")
DOURADO  = colors.HexColor("#E8A84C")
VERMELHO = colors.HexColor("#e74c3c")
LARANJA  = colors.HexColor("#e67e22")
VERDE    = colors.HexColor("#2ecc71")
CINZA_BG = colors.HexColor("#F5F5F5")
CINZA_TX = colors.HexColor("#666666")
BRANCO   = colors.white


def _barra(score: int, largura: float = 12 * cm, altura: float = 1.0 * cm):
    from perguntas import nivel_saude
    _, cor_hex = nivel_saude(score)
    d = Drawing(largura, altura)
    d.add(Rect(0, 0, largura, altura,
               fillColor=colors.HexColor("#e0e0e0"), strokeColor=None))
    d.add(Rect(0, 0, largura * (score / 100), altura,
               fillColor=colors.HexColor(cor_hex), strokeColor=None))
    d.add(String(largura * (score / 100) + 5, altura * 0.25,
                 f"{score}/100", fontName="Helvetica-Bold",
                 fontSize=8, fillColor=colors.HexColor("#333333")))
    return d


def gerar_pdf(caminho, empresa, segmento, cidade,
              funcionarios, faturamento, resultado, observacao=""):

    doc = SimpleDocTemplate(caminho, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    story = []

    from perguntas import nivel_saude, BLOCOS
    saude_geral = resultado.get("_geral", 0)
    nivel_label, nivel_cor = nivel_saude(saude_geral)

    # ── Estilos ────────────────────────────────────────────────────────────────
    def st(name, **kw):
        return ParagraphStyle(name, **kw)

    s_titulo_sec = st("ts", fontSize=14, textColor=AZUL,
                      fontName="Helvetica-Bold", spaceAfter=8, spaceBefore=14)
    s_corpo      = st("co", fontSize=10, textColor=colors.HexColor("#333"),
                      spaceAfter=6, leading=16)
    s_critico    = st("cr", fontSize=10, textColor=VERMELHO,
                      fontName="Helvetica-Bold", spaceAfter=4)
    s_atencao    = st("at", fontSize=10, textColor=LARANJA, spaceAfter=4)
    s_ok         = st("ok", fontSize=10, textColor=VERDE,
                      fontName="Helvetica-Bold")
    s_center     = st("cen", alignment=TA_CENTER, fontSize=10,
                      textColor=CINZA_TX)

    # ══════════════════════════════════════════════════════════════════════════
    # CAPA
    # ══════════════════════════════════════════════════════════════════════════
    def p(text, **kw):
        return Paragraph(text, ParagraphStyle("_", **kw))

    capa = [
        [p("PULSO GESTAO", fontSize=24, textColor=DOURADO,
           fontName="Helvetica-Bold", alignment=TA_CENTER)],
        [p("Diagnostico Empresarial", fontSize=12, textColor=BRANCO,
           alignment=TA_CENTER)],
        [Spacer(1, 0.6*cm)],
        [p(empresa.upper(), fontSize=26, textColor=BRANCO,
           fontName="Helvetica-Bold", alignment=TA_CENTER)],
        [Spacer(1, 0.2*cm)],
        [p(f"{segmento}  •  {cidade}", fontSize=11, textColor=BRANCO,
           alignment=TA_CENTER)],
        [p(f"{funcionarios} funcionarios  •  {faturamento}", fontSize=11,
           textColor=BRANCO, alignment=TA_CENTER)],
        [Spacer(1, 0.8*cm)],
        [p("Pontuacao Geral de Saude", fontSize=11,
           textColor=colors.HexColor("#aaaaaa"), alignment=TA_CENTER)],
        [Spacer(1, 0.2*cm)],
        [p(str(saude_geral), fontSize=64, textColor=DOURADO,
           fontName="Helvetica-Bold", alignment=TA_CENTER, leading=70)],
        [Spacer(1, 0.15*cm)],
        [p(f"— {nivel_label} —", fontSize=15, textColor=DOURADO,
           fontName="Helvetica-Bold", alignment=TA_CENTER)],
        [Spacer(1, 0.8*cm)],
        [p(f"Diagnostico realizado em {date.today().strftime('%d/%m/%Y')}",
           fontSize=10, textColor=CINZA_TX, alignment=TA_CENTER)],
        [p("thyago.c@pulso-negocios.com  •  @pulso.gestao",
           fontSize=9, textColor=CINZA_TX, alignment=TA_CENTER)],
    ]
    t_capa = Table(capa, colWidths=[17*cm])
    t_capa.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), AZUL),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 20),
        ("RIGHTPADDING",  (0,0), (-1,-1), 20),
    ]))
    story += [t_capa, PageBreak()]

    # ══════════════════════════════════════════════════════════════════════════
    # RESUMO EXECUTIVO
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Resumo Executivo", s_titulo_sec))
    story.append(HRFlowable(width="100%", thickness=2, color=DOURADO))
    story.append(Spacer(1, 0.3*cm))

    total_crit = sum(
        1 for b in resultado.values()
        if isinstance(b, dict) and "problemas" in b
        for pr in b["problemas"] if pr["gravidade"] == "crítico"
    )
    total_aten = sum(
        1 for b in resultado.values()
        if isinstance(b, dict) and "problemas" in b
        for pr in b["problemas"] if pr["gravidade"] == "atenção"
    )
    story.append(Paragraph(
        f"O diagnostico da <b>{empresa}</b> identificou <b>{total_crit} problemas criticos</b> "
        f"e <b>{total_aten} pontos de atencao</b>. "
        f"Pontuacao geral: <b>{saude_geral}/100 — {nivel_label}</b>.",
        s_corpo))
    story.append(Spacer(1, 0.4*cm))

    # Tabela de áreas
    header = [
        p("<b>Area</b>", fontSize=9, textColor=BRANCO,
          fontName="Helvetica-Bold"),
        p("<b>Saude</b>", fontSize=9, textColor=BRANCO,
          fontName="Helvetica-Bold", alignment=TA_CENTER),
        p("<b>Situacao</b>", fontSize=9, textColor=BRANCO,
          fontName="Helvetica-Bold", alignment=TA_CENTER),
    ]
    rows = [header]
    COR_MAP = {"Saudável": "#2ecc71", "Atenção": "#f39c12",
               "Crítico": "#e74c3c", "Urgente": "#c0392b"}
    for bloco in BLOCOS:
        bd    = resultado.get(bloco["id"], {})
        saude = bd.get("saude", 0)
        lbl, _ = nivel_saude(saude)
        cor    = COR_MAP.get(lbl, "#999")
        rows.append([
            p(bloco["titulo"], fontSize=9, textColor=AZUL),
            p(f"<b>{saude}/100</b>", fontSize=9, textColor=AZUL,
              fontName="Helvetica-Bold", alignment=TA_CENTER),
            p(f"<b>{lbl}</b>", fontSize=9,
              textColor=colors.HexColor(cor),
              fontName="Helvetica-Bold", alignment=TA_CENTER),
        ])
    t = Table(rows, colWidths=[9*cm, 3*cm, 5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), AZUL),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [BRANCO, CINZA_BG]),
        ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ]))
    story += [t, PageBreak()]

    # ══════════════════════════════════════════════════════════════════════════
    # DETALHAMENTO
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Analise Detalhada por Area", s_titulo_sec))
    story.append(HRFlowable(width="100%", thickness=2, color=DOURADO))

    for bloco in BLOCOS:
        bd    = resultado.get(bloco["id"], {})
        saude = bd.get("saude", 0)
        probs = bd.get("problemas", [])
        lbl, _  = nivel_saude(saude)
        cor_hex = COR_MAP.get(lbl, "#999")

        story.append(Spacer(1, 0.5*cm))

        # Cabeçalho da área
        ah = Table([[
            p(f"<b>{bloco['titulo']}</b>", fontSize=12, textColor=BRANCO,
              fontName="Helvetica-Bold"),
            p(f"<b>{saude}/100 — {lbl}</b>", fontSize=11,
              textColor=DOURADO, fontName="Helvetica-Bold",
              alignment=TA_RIGHT),
        ]], colWidths=[11*cm, 6*cm])
        ah.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), AZUL),
            ("TOPPADDING",    (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING",   (0,0), (-1,-1), 12),
            ("RIGHTPADDING",  (0,0), (-1,-1), 12),
        ]))
        story.append(ah)
        story.append(Spacer(1, 0.1*cm))
        story.append(_barra(saude))
        story.append(Spacer(1, 0.3*cm))

        if not probs:
            story.append(Paragraph(
                "Nenhum problema critico identificado nesta area.", s_ok))
        else:
            for pr in probs:
                s = s_critico if pr["gravidade"] == "crítico" else s_atencao
                marcador = "[CRITICO]" if pr["gravidade"] == "crítico" else "[ATENCAO]"
                story.append(Paragraph(
                    f"{marcador}  <b>{pr['pergunta']}</b>", s))
                story.append(Paragraph(
                    f"&nbsp;&nbsp;&nbsp;Resposta: <i>{pr['resposta']}</i>",
                    s_corpo))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # OBSERVAÇÕES
    # ══════════════════════════════════════════════════════════════════════════
    if observacao and observacao.strip():
        story.append(Paragraph("Observacoes do Diagnostico", s_titulo_sec))
        story.append(HRFlowable(width="100%", thickness=2, color=DOURADO))
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph(observacao, s_corpo))
        story.append(Spacer(1, 0.5*cm))

    # ══════════════════════════════════════════════════════════════════════════
    # PROPOSTA
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph(
        "O que a Pulso Gestao pode fazer por voce", s_titulo_sec))
    story.append(HRFlowable(width="100%", thickness=2, color=DOURADO))
    story.append(Spacer(1, 0.3*cm))

    solucoes = [
        ("Retencao de Clientes",
         "Sistema que identifica clientes inativos e dispara mensagens automaticas no momento certo."),
        ("Pipeline de Vendas",
         "Controle de orcamentos com follow-up automatico e taxa de conversao em tempo real."),
        ("Gestao Financeira",
         "Painel de custos, margens reais, alertas de vencimento e controle de inadimplencia."),
        ("Pos-Venda Automatico",
         "Pesquisa de satisfacao (NPS), gestao de reclamacoes e solicitacao de indicacoes."),
        ("Automacao de Processos",
         "Reducao de tarefas manuais repetitivas, liberando sua equipe para o que importa."),
        ("Presenca Digital",
         "Conteudo automatico nas redes sociais focado em atrair clientes do seu segmento."),
    ]
    for titulo_s, desc_s in solucoes:
        row = Table([[
            p(f"<b>{titulo_s}</b>", fontSize=10, textColor=AZUL,
              fontName="Helvetica-Bold"),
            p(desc_s, fontSize=9, textColor=CINZA_TX),
        ]], colWidths=[5.5*cm, 11.5*cm])
        row.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), CINZA_BG),
            ("TOPPADDING",    (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING",   (0,0), (-1,-1), 10),
            ("GRID",          (0,0), (-1,-1), 0, BRANCO),
        ]))
        story.append(row)
        story.append(Spacer(1, 0.12*cm))

    story.append(Spacer(1, 0.8*cm))

    # CTA
    cta = Table([[p(
        "Pronto para transformar esses problemas em resultados?<br/>"
        "<b>thyago.c@pulso-negocios.com  •  @pulso.gestao</b>",
        fontSize=11, textColor=BRANCO, alignment=TA_CENTER, leading=20,
    )]], colWidths=[17*cm])
    cta.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), AZUL),
        ("TOPPADDING",    (0,0), (-1,-1), 20),
        ("BOTTOMPADDING", (0,0), (-1,-1), 20),
    ]))
    story.append(cta)

    doc.build(story)
