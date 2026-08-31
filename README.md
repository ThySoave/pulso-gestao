# Pulso Gestão

Agência de sites e automação comercial para PMEs. Este repositório reúne as ferramentas de
diagnóstico e conteúdo da operação.

> O motor de prospecção outbound da agência — 7 agentes encadeados de scout, qualificação por
> score, enriquecimento, disparo por WhatsApp e CRM com kanban — não é publicado aqui: opera
> sobre base de leads reais e credenciais de sessão.

## O problema

Dono de PME sabe que "as vendas poderiam ser melhores", mas não sabe **onde** está o furo.
Consultoria tradicional cobra caro por semanas de levantamento e entrega um diagnóstico que
o cliente não consegue ler. E a maioria dessas empresas não tem presença digital nenhuma —
não porque não queira, mas porque publicar com constância exige um tempo que ninguém tem.

## O que existe aqui

### Sistema de diagnóstico comercial

Questionário estruturado que atravessa as áreas da operação comercial, pontua cada resposta
e gera um **relatório em PDF** com o retrato da empresa e recomendações priorizadas.

O que era conversa de duas semanas vira uma sessão, e o cliente sai com um documento que
consegue mostrar para o sócio.

```
app.py             aplicação Flask, fluxo do questionário
perguntas.py       banco de perguntas e regras de pontuação por área
pdf_relatorio.py   composição do relatório — layout, gráficos e recomendações
templates/         interface do questionário
```

**Stack:** Python, Flask, geração de PDF.

### Automação de conteúdo — `pulso_auto/`

Publicação programada no Instagram da consultoria. Gera o card com a identidade visual a
partir do texto, mantém uma fila editorial e publica pela API.

```
poster.py       fila, montagem e publicação
gerar_marca.py  geração do card com identidade visual
posts.json      fila editorial
```

**Stack:** Python, Pillow, Instagram Graph API.

### Site — `pulso_site/`

Landing page da consultoria, publicada em GitHub Pages com domínio próprio.

## Por que isso existe

A Pulso é uma operação enxuta que mantenho como laboratório prático: as ferramentas de
diagnóstico, conteúdo e automação que os times de SaaS vendem, eu construo e uso com
clientes reais. Vender CRM e automação depois de ter implementado os dois é uma conversa
diferente.

## Configuração

Credenciais ficam em `.env`, fora do versionamento. Veja `.env.example` para as chaves
necessárias.

---

Feito por [Thyago Soave](https://linkedin.com/in/thyago-soave-correa) · [pulso-negocios.com](https://pulso-negocios.com)
