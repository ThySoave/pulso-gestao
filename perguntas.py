"""
Perguntas, opções e pontuação do diagnóstico Pulso Gestão.
Pontuação: 0 = sem problema | 1-2 = atenção | 3 = crítico
"""

BLOCOS = [
    {
        "id": "clientes",
        "titulo": "Clientes e Retenção",
        "icone": "👥",
        "descricao": "Como você conhece e mantém sua base de clientes",
        "perguntas": [
            {
                "id": "q1",
                "texto": "Quantos clientes ativos você tem hoje?",
                "opcoes": [
                    ("Sei o número exato", 0),
                    ("Tenho uma ideia aproximada", 1),
                    ("Não sei", 3),
                ],
            },
            {
                "id": "q2",
                "texto": "Onde ficam registrados os dados dos seus clientes?",
                "opcoes": [
                    ("Sistema / software", 0),
                    ("Planilha", 1),
                    ("Papel / caderno", 2),
                    ("WhatsApp", 2),
                    ("Não registro", 3),
                ],
            },
            {
                "id": "q3",
                "texto": "Você sabe quais clientes não aparecem há mais de 60 dias?",
                "opcoes": [
                    ("Sim, consigo ver isso facilmente", 0),
                    ("Tenho ideia, mas não é preciso", 1),
                    ("Não tenho como saber", 3),
                ],
            },
            {
                "id": "q4",
                "texto": "O que você faz quando um cliente para de aparecer?",
                "opcoes": [
                    ("Entro em contato ativamente", 0),
                    ("Às vezes entro em contato", 2),
                    ("Espero ele voltar", 3),
                ],
            },
            {
                "id": "q5",
                "texto": "Você tem alguma forma de lembrar o cliente que está na hora de voltar?",
                "opcoes": [
                    ("Sim, tenho um processo para isso", 0),
                    ("Faço manualmente quando lembro", 2),
                    ("Não tenho nada", 3),
                ],
            },
            {
                "id": "q6",
                "texto": "Nos últimos 6 meses, quantos clientes você perdeu?",
                "opcoes": [
                    ("Sei o número exato", 0),
                    ("Tenho uma ideia", 1),
                    ("Não tenho como saber", 3),
                ],
            },
        ],
    },
    {
        "id": "vendas",
        "titulo": "Vendas e Orçamentos",
        "icone": "📊",
        "descricao": "Processo de venda, orçamentos e acompanhamento",
        "perguntas": [
            {
                "id": "q7",
                "texto": "Como você faz e envia um orçamento hoje?",
                "opcoes": [
                    ("Sistema que gera PDF automático", 0),
                    ("Planilha / Word", 1),
                    ("Mensagem no WhatsApp", 2),
                    ("Verbal / no papel", 3),
                ],
            },
            {
                "id": "q8",
                "texto": "Quanto tempo passa entre o pedido e o envio do orçamento?",
                "opcoes": [
                    ("Menos de 1 hora", 0),
                    ("Até 24 horas", 1),
                    ("2 a 3 dias", 2),
                    ("Mais de 3 dias", 3),
                ],
            },
            {
                "id": "q9",
                "texto": "Você acompanha os orçamentos que enviou e não tiveram resposta?",
                "opcoes": [
                    ("Sim, tenho controle de todos", 0),
                    ("Às vezes, quando lembro", 2),
                    ("Não faço follow-up", 3),
                ],
            },
            {
                "id": "q10",
                "texto": "Dos orçamentos enviados no último mês, quantos você fechou?",
                "opcoes": [
                    ("Sei a taxa exata", 0),
                    ("Tenho uma ideia", 1),
                    ("Não tenho controle disso", 3),
                ],
            },
            {
                "id": "q11",
                "texto": "Quem é responsável pelo follow-up de orçamentos?",
                "opcoes": [
                    ("Pessoa específica com processo definido", 0),
                    ("Eu mesmo, quando consigo", 2),
                    ("Ninguém faz isso sistematicamente", 3),
                ],
            },
        ],
    },
    {
        "id": "comunicacao",
        "titulo": "Comunicação Interna",
        "icone": "🔄",
        "descricao": "Como a informação flui dentro da empresa",
        "perguntas": [
            {
                "id": "q12",
                "texto": "Como as informações chegam até sua equipe?",
                "opcoes": [
                    ("Sistema centralizado", 0),
                    ("Grupo de WhatsApp", 1),
                    ("Verbal / pessoalmente", 2),
                    ("Cada um se vira", 3),
                ],
            },
            {
                "id": "q13",
                "texto": "Já aconteceu de um cliente ser mal atendido por falha de comunicação interna?",
                "opcoes": [
                    ("Nunca / raramente", 0),
                    ("Às vezes", 2),
                    ("Com frequência", 3),
                ],
            },
            {
                "id": "q14",
                "texto": "Se você ficasse 1 semana sem aparecer, o que travaria na empresa?",
                "opcoes": [
                    ("Quase nada — está tudo documentado", 0),
                    ("Algumas coisas, mas funcionaria", 1),
                    ("Muita coisa depende só de mim", 3),
                ],
            },
            {
                "id": "q15",
                "texto": "As tarefas da equipe têm responsável e prazo definido?",
                "opcoes": [
                    ("Sim, temos um processo claro", 0),
                    ("Parcialmente", 1),
                    ("Cada um sabe o que tem que fazer (na teoria)", 2),
                ],
            },
        ],
    },
    {
        "id": "financeiro",
        "titulo": "Financeiro",
        "icone": "💰",
        "descricao": "Controle de custos, margens e recebimentos",
        "perguntas": [
            {
                "id": "q16",
                "texto": "Você sabe qual é o seu custo operacional fixo mensal?",
                "opcoes": [
                    ("Sei o valor exato", 0),
                    ("Tenho uma ideia aproximada", 1),
                    ("Não sei ao certo", 3),
                ],
            },
            {
                "id": "q17",
                "texto": "Você sabe a margem de lucro real de cada serviço ou produto?",
                "opcoes": [
                    ("Sim, tenho calculado", 0),
                    ("Tenho uma estimativa", 1),
                    ("Não calculo dessa forma", 3),
                ],
            },
            {
                "id": "q18",
                "texto": "Como você controla o que tem a receber?",
                "opcoes": [
                    ("Sistema com alertas automáticos", 0),
                    ("Planilha / anotações", 1),
                    ("Na memória", 2),
                    ("Não controlo direito", 3),
                ],
            },
            {
                "id": "q19",
                "texto": "Já foi pego de surpresa por uma conta que venceu sem você lembrar?",
                "opcoes": [
                    ("Nunca", 0),
                    ("Raramente", 1),
                    ("Com frequência", 3),
                ],
            },
            {
                "id": "q20",
                "texto": "Tem clientes com pagamento atrasado? Sabe o valor total em aberto?",
                "opcoes": [
                    ("Sei o valor exato e faço cobrança ativa", 0),
                    ("Tenho ideia mas não cobro sistematicamente", 2),
                    ("Não tenho controle disso", 3),
                ],
            },
        ],
    },
    {
        "id": "posvenda",
        "titulo": "Pós-Venda",
        "icone": "⭐",
        "descricao": "O que acontece depois que o cliente compra",
        "perguntas": [
            {
                "id": "q21",
                "texto": "O que você faz depois que entrega um serviço ou produto?",
                "opcoes": [
                    ("Tenho um processo de acompanhamento", 0),
                    ("Às vezes mando mensagem perguntando", 2),
                    ("Nada — espero o cliente dar retorno", 3),
                ],
            },
            {
                "id": "q22",
                "texto": "Como o cliente te avisa quando tem um problema?",
                "opcoes": [
                    ("Temos um canal específico para isso", 0),
                    ("Me liga ou manda WhatsApp", 1),
                    ("Não tem processo — ele simplesmente não volta", 3),
                ],
            },
            {
                "id": "q23",
                "texto": "Você pede avaliação ou indicação para clientes satisfeitos?",
                "opcoes": [
                    ("Sim, tenho um processo para isso", 0),
                    ("Às vezes, quando lembro", 2),
                    ("Não peço", 3),
                ],
            },
            {
                "id": "q24",
                "texto": "Você sabe quantos clientes ficaram insatisfeitos nos últimos 6 meses?",
                "opcoes": [
                    ("Sim, registro e acompanho", 0),
                    ("Tenho ideia dos casos mais graves", 1),
                    ("Não tenho como saber", 3),
                ],
            },
        ],
    },
    {
        "id": "processos",
        "titulo": "Processos e Tempo",
        "icone": "⚙️",
        "descricao": "Eficiência operacional e dependência de pessoas",
        "perguntas": [
            {
                "id": "q25",
                "texto": "Quanto tempo por semana é gasto em tarefas repetitivas que poderiam ser automáticas?",
                "opcoes": [
                    ("Menos de 2 horas", 0),
                    ("2 a 5 horas", 1),
                    ("Mais de 5 horas", 2),
                    ("Não sei calcular", 2),
                ],
            },
            {
                "id": "q26",
                "texto": "Tem algum processo que só você (ou uma pessoa) sabe fazer?",
                "opcoes": [
                    ("Não — tudo está documentado", 0),
                    ("Alguns processos", 1),
                    ("Muita coisa depende de uma pessoa só", 3),
                ],
            },
            {
                "id": "q27",
                "texto": "Se um funcionário-chave sair hoje, o que você perde junto?",
                "opcoes": [
                    ("Quase nada — processo está documentado", 0),
                    ("Algum conhecimento, mas me viro", 1),
                    ("Vou ter um problema sério", 3),
                ],
            },
            {
                "id": "q28",
                "texto": "Você usa algum sistema de gestão hoje?",
                "opcoes": [
                    ("Sim, uso e funciona bem", 0),
                    ("Uso mas é limitado / não atende tudo", 1),
                    ("Planilhas / papel", 2),
                    ("Nenhum sistema", 3),
                ],
            },
        ],
    },
    {
        "id": "marketing",
        "titulo": "Marketing e Visibilidade",
        "icone": "📣",
        "descricao": "Como novos clientes chegam até você",
        "perguntas": [
            {
                "id": "q29",
                "texto": "De onde vieram a maioria dos seus clientes nos últimos 6 meses?",
                "opcoes": [
                    ("Vários canais — tenho controle", 0),
                    ("Indicação de clientes", 1),
                    ("Redes sociais ou Google", 1),
                    ("Não sei de onde vieram", 3),
                ],
            },
            {
                "id": "q30",
                "texto": "Você tem presença online ativa?",
                "opcoes": [
                    ("Sim, posto regularmente com estratégia", 0),
                    ("Tenho perfil mas não posto com frequência", 2),
                    ("Não tenho presença online", 3),
                ],
            },
            {
                "id": "q31",
                "texto": "Você tem alguma ação para atrair clientes novos toda semana?",
                "opcoes": [
                    ("Sim, tenho estratégia definida", 0),
                    ("Faço algo esporadicamente", 2),
                    ("Dependo só de indicações", 2),
                ],
            },
        ],
    },
]


def calcular_pontuacao(respostas: dict) -> dict:
    """
    respostas = {"q1": 0, "q2": 2, ...}  (índice da opção escolhida)
    Retorna pontuação por bloco e geral (0-100, quanto maior melhor).
    """
    resultado = {}
    total_pontos  = 0
    total_max     = 0

    for bloco in BLOCOS:
        pontos_bloco = 0
        max_bloco    = 0
        problemas    = []

        for perg in bloco["perguntas"]:
            qid = perg["id"]
            idx = respostas.get(qid)
            if idx is None:
                continue
            try:
                _, pontos = perg["opcoes"][int(idx)]
            except (IndexError, ValueError):
                continue

            pontos_bloco += pontos
            max_bloco    += 3          # pior cenário sempre é 3

            if pontos >= 2:
                texto_opcao = perg["opcoes"][int(idx)][0]
                problemas.append({
                    "pergunta": perg["texto"],
                    "resposta": texto_opcao,
                    "gravidade": "crítico" if pontos == 3 else "atenção",
                })

        saude = round((1 - pontos_bloco / max_bloco) * 100) if max_bloco else 100
        resultado[bloco["id"]] = {
            "titulo":   bloco["titulo"],
            "icone":    bloco["icone"],
            "saude":    saude,
            "problemas": problemas,
        }
        total_pontos += pontos_bloco
        total_max    += max_bloco

    saude_geral = round((1 - total_pontos / total_max) * 100) if total_max else 100
    resultado["_geral"] = saude_geral
    return resultado


def nivel_saude(score: int) -> tuple:
    """Retorna (label, cor_hex) baseado no score."""
    if score >= 75:
        return "Saudável",   "#2ecc71"
    if score >= 50:
        return "Atenção",    "#f39c12"
    if score >= 25:
        return "Crítico",    "#e74c3c"
    return "Urgente",        "#c0392b"
