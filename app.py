#!/usr/bin/env python3
"""
Pulso Gestão — Sistema de Diagnóstico Empresarial
Roda localmente no celular/notebook durante a visita.
"""

import os
import json
import tempfile
from datetime import date
from flask import Flask, render_template, request, send_file, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "pulso-diagnostico-2026"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return render_template("inicio.html")


@app.route("/diagnostico", methods=["GET", "POST"])
def diagnostico():
    from perguntas import BLOCOS
    if request.method == "POST":
        dados = {k: v for k, v in request.form.items()}
        session["dados_empresa"] = {
            "empresa":      dados.get("empresa", ""),
            "segmento":     dados.get("segmento", ""),
            "cidade":       dados.get("cidade", ""),
            "funcionarios": dados.get("funcionarios", ""),
            "faturamento":  dados.get("faturamento", ""),
        }
        session["bloco_atual"] = 0
        session["respostas"]   = {}
        return redirect(url_for("bloco", idx=0))
    return render_template("diagnostico_inicio.html")


@app.route("/bloco/<int:idx>", methods=["GET", "POST"])
def bloco(idx):
    from perguntas import BLOCOS
    if "dados_empresa" not in session:
        return redirect(url_for("diagnostico"))

    if request.method == "POST":
        respostas = session.get("respostas", {})
        bloco_atual = BLOCOS[idx]
        for perg in bloco_atual["perguntas"]:
            val = request.form.get(perg["id"])
            if val is not None:
                respostas[perg["id"]] = int(val)
        session["respostas"] = respostas

        proximo = idx + 1
        if proximo < len(BLOCOS):
            return redirect(url_for("bloco", idx=proximo))
        else:
            return redirect(url_for("observacao"))

    bloco_data = BLOCOS[idx]
    total      = len(BLOCOS)
    progresso  = round((idx / total) * 100)
    return render_template("bloco.html",
        bloco=bloco_data,
        idx=idx,
        total=total,
        progresso=progresso,
        empresa=session["dados_empresa"]["empresa"],
    )


@app.route("/observacao", methods=["GET", "POST"])
def observacao():
    if "respostas" not in session:
        return redirect(url_for("diagnostico"))
    if request.method == "POST":
        session["observacao"] = request.form.get("observacao", "")
        return redirect(url_for("resultado"))
    return render_template("observacao.html",
        empresa=session["dados_empresa"]["empresa"])


@app.route("/resultado")
def resultado():
    if "respostas" not in session:
        return redirect(url_for("diagnostico"))
    from perguntas import calcular_pontuacao, nivel_saude, BLOCOS
    resultado = calcular_pontuacao(session["respostas"])
    saude_geral = resultado["_geral"]
    nivel_label, nivel_cor = nivel_saude(saude_geral)
    return render_template("resultado.html",
        empresa=session["dados_empresa"]["empresa"],
        resultado=resultado,
        saude_geral=saude_geral,
        nivel_label=nivel_label,
        nivel_cor=nivel_cor,
        blocos=BLOCOS,
    )


@app.route("/gerar-pdf")
def gerar_pdf():
    if "respostas" not in session:
        return redirect(url_for("diagnostico"))

    from perguntas import calcular_pontuacao
    from pdf_relatorio import gerar_pdf as _gerar

    resultado   = calcular_pontuacao(session["respostas"])
    dados       = session["dados_empresa"]
    observacao  = session.get("observacao", "")
    empresa     = dados["empresa"] or "Empresa"

    nome_arq = f"diagnostico_{empresa.replace(' ', '_')}_{date.today().strftime('%Y%m%d')}.pdf"
    caminho  = os.path.join(BASE_DIR, "relatorios", nome_arq)
    os.makedirs(os.path.join(BASE_DIR, "relatorios"), exist_ok=True)

    _gerar(
        caminho=caminho,
        empresa=empresa,
        segmento=dados.get("segmento", ""),
        cidade=dados.get("cidade", ""),
        funcionarios=dados.get("funcionarios", ""),
        faturamento=dados.get("faturamento", ""),
        resultado=resultado,
        observacao=observacao,
    )
    return send_file(caminho, as_attachment=True, download_name=nome_arq)


@app.route("/novo")
def novo():
    session.clear()
    return redirect(url_for("diagnostico"))


if __name__ == "__main__":
    print("\n  Pulso Gestão — Sistema de Diagnóstico")
    print("  Acesse no celular: http://SEU_IP:5001\n")
    app.run(host="0.0.0.0", port=5001, debug=False)
