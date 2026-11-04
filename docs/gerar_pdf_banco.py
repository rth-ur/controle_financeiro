"""Generate the database handout: python docs/gerar_pdf_banco.py.

Requires reportlab (documentation tool, independent of the test suite).
"""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle

OUT = Path(__file__).with_name('FinTrack_Banco_Relacional.pdf')
W, H = A4
NAVY = colors.HexColor('#10263C')
GREEN = colors.HexColor('#087F70')
MUTED = colors.HexColor('#4B6073')
LIGHT = colors.HexColor('#EDF5F7')
c = canvas.Canvas(str(OUT), pagesize=A4)
c.setTitle('FinTrack | Banco de dados relacional')
c.setAuthor('Projeto FinTrack')


def text(x, y, value, size=11, color=NAVY, font='Helvetica'):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, y, value)


def paragraph(value, x, y, width=491, size=10.5, color=MUTED):
    p = Paragraph(value, ParagraphStyle('body', fontName='Helvetica', fontSize=size,
                                       leading=size * 1.5, textColor=color))
    _, height = p.wrap(width, 1000)
    p.drawOn(c, x, y - height)
    return y - height


def header(number, title, subtitle):
    c.setFillColor(NAVY)
    c.rect(0, H - 143, W, 143, fill=1, stroke=0)
    text(42, H - 38, 'FINTRACK / DOCUMENTAÇÃO TÉCNICA', 10, colors.HexColor('#7FDDD0'))
    text(42, H - 78, title, 25, colors.white, 'Helvetica-Bold')
    text(42, H - 107, subtitle, 10, colors.HexColor('#D0DEE7'))
    text(42, 26, '04/11/2026  |  Estrutura documentada no repositório', 8, MUTED)
    text(W - 67, 26, f'{number} / 2', 8, MUTED)


header(1, 'Banco de dados relacional', 'Modelo atual · PostgreSQL no Supabase · Visão para apresentação')
text(42, 665, '01  /  COMO OS DADOS SÃO ORGANIZADOS', 11, GREEN, 'Helvetica-Bold')
paragraph('O banco relacional documentado tem uma entidade: <b>transacoes</b>. '
          'Cada linha representa uma movimentação financeira, identificada por uma chave primária.', 42, 646)

# Vector entity diagram: a single table, with the documented constraints.
x, y, width, height = 90, 311, 415, 267
c.setFillColor(LIGHT)
c.roundRect(x, y, width, height, 10, fill=1, stroke=0)
c.setFillColor(GREEN)
c.roundRect(x, y + height - 45, width, 45, 10, fill=1, stroke=0)
c.rect(x, y + height - 45, width, 15, fill=1, stroke=0)
text(x + 18, y + height - 29, 'transacoes', 17, colors.white, 'Helvetica-Bold')
rows = [('PK', 'id', 'bigint · identity · obrigatório'),
        ('', 'desc', 'text · obrigatório'), ('', 'val', 'numeric · obrigatório'),
        ('', 'tipo', 'text · obrigatório'), ('', 'met', 'text · opcional'),
        ('', 'cat', 'text · opcional'), ('', 'data', 'date · obrigatório')]
for i, (key, field, details) in enumerate(rows):
    row_y = y + height - 72 - i * 27
    text(x + 16, row_y, key, 9, GREEN, 'Helvetica-Bold')
    text(x + 52, row_y, field, 12, NAVY, 'Helvetica-Bold')
    text(x + 143, row_y, details, 10, MUTED)

paragraph('<b>PK = chave primária.</b> O campo id é único e gerado automaticamente. '
          'O esquema documentado não declara chaves estrangeiras ou relações entre tabelas.', 90, 292, 415)
text(42, 222, '02  /  PERSISTÊNCIA DA APLICAÇÃO', 11, GREEN, 'Helvetica-Bold')
paragraph('<b>Transações:</b> aplicação JavaScript → SDK Supabase → tabela transacoes. '
          'O código realiza consulta, inserção, atualização e exclusão.', 42, 203)
paragraph('<b>Metas e eventos:</b> ficam no localStorage do navegador, junto com as preferências '
          'de tema e barra lateral. Não são tabelas PostgreSQL no modelo atual documentado.', 42, 155)
paragraph('<b>Escopo:</b> documento baseado em README.md (schema SQL) e src/script.js '
          '(acesso aos dados). Não foi feita inspeção direta do catálogo do banco remoto.', 42, 100, size=9)
c.showPage()

header(2, 'Campos e regras', 'Dicionário de dados · Restrições declaradas · SQL de referência')
text(42, 665, '03  /  DICIONÁRIO DE DADOS', 11, GREEN, 'Helvetica-Bold')
style = ParagraphStyle('cell', fontName='Helvetica', fontSize=9, leading=13, textColor=NAVY)
data = [['Campo / tipo', 'Obrigatório', 'Significado / exemplo'],
        ['id / bigint', 'Sim · PK', 'Identificador automático da transação.'],
        ['desc / text', 'Sim', 'Descrição da movimentação. Ex.: Salário.'],
        ['val / numeric', 'Sim', 'Valor monetário. Ex.: 1000.00.'],
        ['tipo / text', 'Sim', 'Tipo usado pela aplicação: receita ou despesa.'],
        ['met / text', 'Não', 'Método: pix, cartao, debito, dinheiro, boleto ou ted.'],
        ['cat / text', 'Não', 'Categoria. Ex.: moradia ou transporte.'],
        ['data / date', 'Sim', 'Data da movimentação. Ex.: 2026-11-04.']]
table = Table([[Paragraph(cell, style) for cell in row] for row in data],
              colWidths=[117, 91, 303])
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D8ECE9')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LIGHT, colors.white]),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
_, th = table.wrap(511, 1000)
table.drawOn(c, 42, 644 - th)
bottom = 644 - th
paragraph('<b>Atenção às regras:</b> os valores de tipo, met e cat são convenções do código. '
          'O SQL documentado usa text e não declara CHECK, ENUM ou tabelas de referência. '
          'O tipo numeric também não tem precisão ou escala explicitadas.', 42, bottom - 17, size=9)
sql_y = bottom - 93
text(42, sql_y, '04  /  SQL DOCUMENTADO', 11, GREEN, 'Helvetica-Bold')
sql = [
    'create table transacoes (',
    '  id bigint generated always as identity primary key,',
    '  "desc" text not null,',
    '  val numeric not null,',
    '  tipo text not null,',
    '  met text,',
    '  cat text,',
    '  data date not null',
    ');',
]
c.setFillColor(LIGHT)
c.roundRect(42, sql_y - 183, 511, 166, 8, fill=1, stroke=0)
for i, line in enumerate(sql):
    text(55, sql_y - 39 - i * 15, line, 9, NAVY, 'Courier')
paragraph('A descrição foi delimitada como "desc" no SQL acima. A documentação não '
          'informa índices adicionais, políticas RLS, usuários ou relacionamentos com autenticação.',
          42, sql_y - 197, size=9)
c.save()
print(OUT)
