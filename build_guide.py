#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/linuxbrew/.linuxbrew/Cellar/python@3.14/3.14.5/lib/python3.14/site-packages')

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

PW, PH = A4
DARK   = HexColor('#1a2e4a')
BLUE   = HexColor('#2c5282')
LBLUE  = HexColor('#ebf4ff')
GREEN  = HexColor('#1a4731')
LGREEN = HexColor('#f0fff4')
ORANGE = HexColor('#7b341e')
LORANGE= HexColor('#fffaf0')
PURPLE = HexColor('#44337a')
LPURPLE= HexColor('#faf5ff')
GRAY   = HexColor('#4a5568')
LGRAY  = HexColor('#f7fafc')
BORDER = HexColor('#cbd5e0')
CODE_BG= HexColor('#1e1e1e')
CODE_FG= HexColor('#d4d4d4')
YELLOW = HexColor('#744210')
LYELLOW= HexColor('#fffff0')

def S(n, **kw): return ParagraphStyle(n, **kw)

TITLE   = S('T',  fontName='Helvetica-Bold',        fontSize=22, leading=28, textColor=white,  alignment=TA_CENTER, spaceAfter=4)
SUBT    = S('ST', fontName='Helvetica',              fontSize=11, leading=15, textColor=LBLUE,  alignment=TA_CENTER, spaceAfter=0)
H1      = S('H1', fontName='Helvetica-Bold',         fontSize=14, leading=18, textColor=white,  spaceBefore=0, spaceAfter=0)
H2      = S('H2', fontName='Helvetica-Bold',         fontSize=11, leading=15, textColor=DARK,   spaceBefore=10, spaceAfter=4)
H3      = S('H3', fontName='Helvetica-BoldOblique',  fontSize=10, leading=14, textColor=BLUE,   spaceBefore=7,  spaceAfter=3)
BODY    = S('BD', fontName='Helvetica',              fontSize=10, leading=15, textColor=black,  alignment=TA_JUSTIFY, spaceAfter=6)
BODYL   = S('BL', fontName='Helvetica',              fontSize=10, leading=15, textColor=black,  alignment=TA_LEFT,    spaceAfter=6)
BUL     = S('BU', fontName='Helvetica',              fontSize=10, leading=15, textColor=black,  alignment=TA_JUSTIFY, leftIndent=0.6*cm, firstLineIndent=-0.4*cm, spaceAfter=4)
CODE    = S('CO', fontName='Courier',                fontSize=9,  leading=13, textColor=CODE_FG, backColor=CODE_BG, leftIndent=0.3*cm, rightIndent=0.3*cm, spaceBefore=3, spaceAfter=3)
NOTE    = S('NT', fontName='Helvetica-Oblique',      fontSize=9,  leading=13, textColor=GRAY,   alignment=TA_CENTER, spaceAfter=4)
CAP     = S('CP', fontName='Helvetica-Bold',         fontSize=9,  leading=12, textColor=GRAY,   alignment=TA_CENTER, spaceAfter=6)
LABEL   = S('LB', fontName='Helvetica-Bold',         fontSize=9,  leading=12, textColor=BLUE)
ANSWER  = S('AN', fontName='Helvetica',              fontSize=9.5,leading=14, textColor=black,  alignment=TA_JUSTIFY)

doc = SimpleDocTemplate(
    "/home/azureuser/nlp-sql-ca/NL2SQL_Teaching_Guide.pdf",
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
)

def sp(n=8):   return Spacer(1, n)
def hr():      return HRFlowable(width='100%', thickness=0.5, color=BORDER, spaceAfter=6, spaceBefore=4)
def p(t):      return Paragraph(t, BODY)
def pl(t):     return Paragraph(t, BODYL)
def bul(t):    return Paragraph(f'• &nbsp; {t}', BUL)
def code(t):   return Paragraph(t, CODE)
def note(t):   return Paragraph(t, NOTE)
def h2(t):     return Paragraph(t, H2)
def h3(t):     return Paragraph(t, H3)

W = doc.width

def section_header(title, subtitle=None, color=DARK):
    rows = [[Paragraph(title, H1)]]
    if subtitle:
        rows.append([Paragraph(subtitle, S('ss', fontName='Helvetica', fontSize=9, leading=12, textColor=HexColor('#90cdf4'), spaceAfter=0))])
    t = Table(rows, colWidths=[W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color),
        ('TOPPADDING',    (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING',   (0,0), (-1,-1), 14),
        ('RIGHTPADDING',  (0,0), (-1,-1), 14),
        ('ROUNDEDCORNERS', [4]),
    ]))
    return t

def info_box(text, color=LBLUE, border=BLUE):
    t = Table([[Paragraph(text, S('ib', fontName='Helvetica', fontSize=10, leading=15, textColor=black, alignment=TA_JUSTIFY))]], colWidths=[W])
    t.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.2, border),
        ('BACKGROUND', (0,0), (-1,-1), color),
        ('TOPPADDING',    (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING',   (0,0), (-1,-1), 12),
        ('RIGHTPADDING',  (0,0), (-1,-1), 12),
    ]))
    return t

def code_box(lines):
    text = '<br/>'.join(lines)
    t = Table([[Paragraph(text, CODE)]], colWidths=[W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('TOPPADDING',    (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING',   (0,0), (-1,-1), 14),
        ('RIGHTPADDING',  (0,0), (-1,-1), 14),
        ('BOX', (0,0), (-1,-1), 0.5, HexColor('#555555')),
    ]))
    return t

def qa_box(q, a):
    rows = [
        [Paragraph(f'Q: {q}', S('qq', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=PURPLE))],
        [Paragraph(f'A: {a}', ANSWER)],
    ]
    t = Table(rows, colWidths=[W])
    t.setStyle(TableStyle([
        ('BOX',        (0,0), (-1,-1), 0.8, PURPLE),
        ('BACKGROUND', (0,0), (0,0),   LPURPLE),
        ('BACKGROUND', (0,1), (0,1),   white),
        ('TOPPADDING',    (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('LINEBELOW', (0,0), (0,0), 0.5, BORDER),
    ]))
    return t

story = []

# ══════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════
cover = Table([
    [Paragraph("NL2SQL", S('cv', fontName='Helvetica-Bold', fontSize=42, leading=48, textColor=white, alignment=TA_CENTER))],
    [Paragraph("Project Teaching Guide", S('cv2', fontName='Helvetica', fontSize=16, leading=20, textColor=LBLUE, alignment=TA_CENTER))],
    [sp(8)],
    [Paragraph("Natural Language → SQL using Transformers + Rules", S('cv3', fontName='Helvetica-Oblique', fontSize=12, leading=16, textColor=HexColor('#90cdf4'), alignment=TA_CENTER))],
    [sp(6)],
    [Paragraph("CSE472 — Deep Learning for NLP | LPU", S('cv4', fontName='Helvetica', fontSize=10, leading=14, textColor=HexColor('#a0aec0'), alignment=TA_CENTER))],
], colWidths=[W])
cover.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), DARK),
    ('TOPPADDING',    (0,0), (-1,-1), 30),
    ('BOTTOMPADDING', (0,0), (-1,-1), 30),
    ('LEFTPADDING',   (0,0), (-1,-1), 20),
    ('RIGHTPADDING',  (0,0), (-1,-1), 20),
]))
story += [sp(30), cover, sp(20)]

story.append(info_box(
    "📖  This guide explains the NL2SQL project from scratch — what it does, how each component works, "
    "why design decisions were made, and what to say if a faculty asks you about it. "
    "Read it once end-to-end and you'll be able to explain the whole project confidently."
))

# ══════════════════════════════════════════════════════════════════════
# 1. BIG PICTURE
# ══════════════════════════════════════════════════════════════════════
story += [sp(16), section_header("1.  The Big Picture", "What does this project actually do?"), sp(10)]

story.append(p(
    "Databases store information in tables — student records, marks, courses. To get data out, you normally "
    "need to write SQL. Most people can't write SQL. NL2SQL solves this: you type a plain English question, "
    "and the system figures out the right SQL query and runs it for you."))

story.append(info_box(
    '🗣️  You type: "show top 5 students by cgpa"\n\n'
    '🤖  System returns: actual database rows — names, CGPAs, departments\n\n'
    '📝  SQL it ran behind the scenes: SELECT * FROM students ORDER BY cgpa DESC LIMIT 5',
    color=LGREEN, border=GREEN))

story += [sp(8), h2("The Full Pipeline (in order):"), sp(4)]

pipeline_rows = [
    ["Step", "Component", "What it does"],
    ["1", "FastAPI endpoint", "Receives your English question via HTTP POST"],
    ["2", "NLPreprocessor", "Cleans text, extracts keywords, detects intent (COUNT / TOP_N / etc.)"],
    ["3", "EmbeddingMatcher", "Uses AI to find which table + columns your question refers to"],
    ["4", "SQLGenerator", "Builds the SQL string from intent + table + columns"],
    ["5", "SQLExecutor", "Validates and runs the SQL, returns results as JSON"],
]
pt = Table(pipeline_rows, colWidths=[1.2*cm, 4.5*cm, W - 1.2*cm - 4.5*cm])
pt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK), ('TEXTCOLOR', (0,0), (-1,0), white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 9.5),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LGRAY]),
    ('GRID', (0,0), (-1,-1), 0.4, BORDER),
    ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 8), ('ALIGN', (0,0), (0,-1), 'CENTER'),
]))
story += [pt, sp(6)]

# ══════════════════════════════════════════════════════════════════════
# 2. PREPROCESSOR
# ══════════════════════════════════════════════════════════════════════
story += [sp(10), section_header("2.  The Preprocessor", "nlp/preprocessor.py — Cleans text + detects intent"), sp(10)]

story.append(p(
    "The preprocessor is the first thing that runs on your input. Its job is to take messy human text "
    "and extract structured information from it — specifically: what does the user want to do, and "
    "what numbers did they mention?"))

story += [h2("Step-by-step walkthrough:"), sp(4)]

steps = [
    ("Normalise", 'Convert to lowercase, strip punctuation, collapse spaces.\n"Show TOP 5 students!!" → "show top 5 students"'),
    ("Tokenise",  'Split on spaces → ["show", "top", "5", "students"]'),
    ("Extract keywords", 'Remove stopwords (the, a, show, get, list, display...) → ["top", "5", "students"]'),
    ("Detect intent", 'Match against trigger word lists → TOP_N'),
    ("Extract numbers", 'Find digits + word numbers → [5]'),
]
for name, desc in steps:
    row = [[
        Paragraph(name, S('sn', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=BLUE)),
        Paragraph(desc, S('sd', fontName='Helvetica', fontSize=9.5, leading=13, textColor=black)),
    ]]
    t = Table(row, colWidths=[3.5*cm, W - 3.5*cm])
    t.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, BORDER),
        ('BACKGROUND', (0,0), (0,0), LBLUE),
        ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('LINEAFTER', (0,0), (0,-1), 0.5, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story += [t, sp(3)]

story += [sp(8), h2("The 7 Intent Classes:"), sp(4)]

intents = [
    ["Intent",     "Trigger Words",                                    "SQL produced"],
    ["COUNT",      "how many, count, total number",                    "SELECT COUNT(*) FROM ..."],
    ["AVERAGE",    "average, avg, mean",                               "SELECT AVG(col) FROM ..."],
    ["TOP_N",      "top, highest, best, maximum, max",                 "ORDER BY col DESC LIMIT n"],
    ["BOTTOM_N",   "bottom, lowest, worst, minimum, min",              "ORDER BY col ASC LIMIT n"],
    ["FILTER_GT",  "above, greater than, more than, over",             "WHERE col > threshold"],
    ["FILTER_LT",  "below, less than, under, low",                     "WHERE col < threshold"],
    ["SELECT",     "(default — nothing matched)",                      "SELECT * FROM ... LIMIT 20"],
]
it = Table(intents, colWidths=[2.5*cm, 5.5*cm, W - 2.5*cm - 5.5*cm])
it.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK), ('TEXTCOLOR', (0,0), (-1,0), white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 9),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LGRAY]),
    ('GRID', (0,0), (-1,-1), 0.4, BORDER),
    ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 7),
]))
story += [it, sp(8)]

story.append(info_box(
    "💡  Why rule-based for intent? Because the 6-class label space is small and the trigger words are "
    "distinct enough. A machine learning classifier would give identical accuracy with extra complexity. "
    "Simple is better when it works.", color=LYELLOW, border=HexColor('#d69e2e')))

# ══════════════════════════════════════════════════════════════════════
# 3. EMBEDDING MATCHER
# ══════════════════════════════════════════════════════════════════════
story += [sp(14), section_header("3.  The Embedding Matcher", "nlp/embeddings.py — The AI brain of the system"), sp(10)]

story.append(p(
    "This is the most technically interesting component. Its job is schema linking — figuring out "
    "which database table and columns the user's question is about, even when they use completely "
    "different words from the column names."))

story.append(info_box(
    '🔴  The problem: User says "show me students with good academic score"\n'
    '        Column name in DB: cgpa\n\n'
    '✅  "academic score" and "cgpa" have zero words in common — but they mean the same thing.\n'
    '       A keyword matcher would fail. The transformer handles this.',
    color=HexColor('#fff5f5'), border=HexColor('#fc8181')))

story += [sp(10), h2("How it works — 3 stages:"), sp(6)]

story += [h3("Stage 1 — Synonym Expansion (before AI)"), sp(3)]
story.append(p(
    "A 54-entry dictionary replaces common domain variants with their schema equivalent. "
    "This handles the obvious cases cheaply, so the AI only needs to handle the hard cases."))
story.append(code_box([
    '"grade"      →  "marks"        |   "branch"    →  "department"',
    '"teacher"    →  "faculty"      |   "gpa"       →  "cgpa"',
    '"percentage" →  "attendance"   |   "professor" →  "faculty"',
    '"score"      →  "marks"        |   "kids"      →  "students"',
]))

story += [sp(8), h3("Stage 2 — Transformer Encoding"), sp(3)]
story.append(p(
    "The model used is <b>all-MiniLM-L6-v2</b> — a sentence transformer with 22 million parameters. "
    "It converts any text into a list of 384 numbers called an embedding vector. "
    "The key property: similar meaning = similar vectors."))
story.append(code_box([
    '"student academic score"          →  [0.21, -0.43, 0.87, 0.11, ...]  (384 numbers)',
    '"cumulative grade point average"  →  [0.19, -0.41, 0.85, 0.13, ...]  (384 numbers)',
    '                                                                        ↑ very similar!',
]))
story += [sp(4)]
story.append(info_box(
    "📌  Why 384 numbers? Each dimension captures some aspect of meaning — grammar, topic, sentiment, "
    "domain context. The model was trained on millions of sentence pairs to make semantically similar "
    "sentences have close vectors. We don't define what each dimension means — the model learns it.",
    color=LBLUE, border=BLUE))

story += [sp(8), h3("Stage 3 — Cosine Similarity"), sp(3)]
story.append(p(
    "Cosine similarity measures the angle between two vectors. If they point in the same direction "
    "(similar meaning), the score is close to 1.0 (100%). If unrelated, the score is near 0."))
story.append(code_box([
    'query = encode("show students with good academic score")',
    '',
    'cosine(query, students_embedding) = 0.847  ← 84.7%  ✅ WINNER',
    'cosine(query, marks_embedding)    = 0.612  ← 61.2%',
    'cosine(query, courses_embedding)  = 0.431  ← 43.1%',
    '',
    '→ Table selected: students',
]))

story += [sp(8), h3("At Startup vs At Query Time"), sp(3)]
timing_rows = [
    ["At Startup (once)", "At Query Time (every request)"],
    ["Load all-MiniLM-L6-v2 model (~1.2s)", "Run synonym expansion (~0ms)"],
    ["Encode all table descriptions", "Encode user's query (~91ms)"],
    ["Encode all column descriptions", "Cosine similarity vs tables"],
    ["Store in memory as numpy arrays", "Cosine similarity vs columns"],
    ["", "Return top table + top 5 columns"],
]
tt = Table(timing_rows, colWidths=[W/2, W/2])
tt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK), ('TEXTCOLOR', (0,0), (-1,0), white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 9),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [LGREEN, white]),
    ('GRID', (0,0), (-1,-1), 0.4, BORDER),
    ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 8), ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LINEBEFORE', (1,0), (1,-1), 1, BLUE),
]))
story += [tt, sp(6)]

# ══════════════════════════════════════════════════════════════════════
# 4. SQL GENERATOR
# ══════════════════════════════════════════════════════════════════════
story += [sp(14), section_header("4.  The SQL Generator", "sql_generator/generator.py — Builds SQL from intent + schema"), sp(10)]

story.append(p(
    "The SQL Generator is pure deterministic logic — no AI at all. It takes three inputs "
    "(intent, matched table, extracted numbers) and fills in a template. "
    "Every possible output is valid SQL by construction — no hallucination possible."))

story += [sp(6), h2("Templates by Intent:"), sp(4)]

templates = [
    ("COUNT",     "SELECT COUNT(*) AS total FROM {table}"),
    ("AVERAGE",   "SELECT AVG({col}) AS average_{col} FROM {table}"),
    ("TOP_N",     "SELECT * FROM {table} ORDER BY {col} DESC LIMIT {n}"),
    ("BOTTOM_N",  "SELECT * FROM {table} ORDER BY {col} ASC LIMIT {n}"),
    ("FILTER_GT", "SELECT * FROM {table} WHERE {col} > {threshold}"),
    ("FILTER_LT", "SELECT * FROM {table} WHERE {col} < {threshold}"),
    ("SELECT",    "SELECT * FROM {table} LIMIT 20   (or WHERE department='CSE' if dept detected)"),
]
for intent, tmpl in templates:
    row = [[
        Paragraph(intent, S('in', fontName='Courier-Bold', fontSize=9, leading=12, textColor=white, backColor=DARK)),
        Paragraph(tmpl,   S('tm', fontName='Courier',      fontSize=9, leading=12, textColor=CODE_FG, backColor=CODE_BG)),
    ]]
    t = Table(row, colWidths=[2.5*cm, W - 2.5*cm])
    t.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('LINEBEFORE', (1,0), (1,-1), 0.5, BORDER),
        ('BOX', (0,0), (-1,-1), 0.4, BORDER),
        ('LINEBELOW', (0,0), (-1,-1), 0.3, BORDER),
    ]))
    story += [t]

story += [sp(8), h2("Full Example — end to end:"), sp(4)]
story.append(code_box([
    'Input query:   "top 3 students by attendance"',
    '',
    'After preprocessing:',
    '  intent   = TOP_N',
    '  numbers  = [3]',
    '  keywords = ["students", "attendance"]',
    '',
    'After embedding match:',
    '  table    = "students"   (84.7% confidence)',
    '  top col  = "attendance" (matched by keyword)',
    '',
    'SQL generated:',
    '  SELECT * FROM students ORDER BY attendance DESC LIMIT 3',
    '',
    'Result: 3 rows — Anita C (95%), Priya K (91%), Karthik P (88%)',
]))

story += [sp(8)]
story.append(info_box(
    "💡  The explanation dict: alongside the SQL, the generator also returns a dictionary like "
    '{"intent": "TOP_N", "table": "students", "order_by": "attendance", "limit": 3}. '
    "This is returned in the API response so the frontend can show the user exactly why "
    "that query was constructed — full transparency.", color=LYELLOW, border=HexColor('#d69e2e')))

# ══════════════════════════════════════════════════════════════════════
# 5. EXECUTOR + DATABASE
# ══════════════════════════════════════════════════════════════════════
story += [sp(14), section_header("5.  Executor & Database", "database/executor.py + schema.py"), sp(10)]

story += [h2("SQLExecutor — Safety first"), sp(4)]
story.append(p(
    "Before any SQL touches the database, the executor runs a blocklist check. "
    "This prevents the system from ever modifying or deleting data, even if there's a bug "
    "somewhere in the generator."))

story.append(code_box([
    'BLOCKED = ["DROP", "DELETE", "INSERT", "UPDATE", "TRUNCATE", "ALTER", "CREATE", "EXEC"]',
    '',
    'if any blocked keyword found → reject with error message',
    'if SQL does not start with SELECT → reject',
    'else → run via pandas.read_sql() → return rows as JSON',
]))

story += [sp(8), h2("Database Schema (3 tables):"), sp(4)]

schema_rows = [
    ["Table",    "Columns",                                              "Records"],
    ["students", "id, name, department, cgpa, attendance, semester",     "10 rows"],
    ["marks",    "id, student_id (FK→students), subject, marks, semester", "50 rows (5 subjects × 10 students)"],
    ["courses",  "course_id, course_name, faculty, credits",             "5 rows"],
]
st = Table(schema_rows, colWidths=[2.2*cm, 9.5*cm, W - 2.2*cm - 9.5*cm])
st.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK), ('TEXTCOLOR', (0,0), (-1,0), white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 9),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LGRAY]),
    ('GRID', (0,0), (-1,-1), 0.4, BORDER),
    ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 8), ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story += [st, sp(8)]

story.append(info_box(
    "⚠️  Known limitation: The current system only handles single-table queries. "
    "A query like 'which students failed in Deep Learning' needs to JOIN students + marks "
    "— this is not supported yet and is the #1 failure mode (3 out of 7 wrong answers).",
    color=HexColor('#fff5f5'), border=HexColor('#fc8181')))

# ══════════════════════════════════════════════════════════════════════
# 6. RESULTS
# ══════════════════════════════════════════════════════════════════════
story += [sp(14), section_header("6.  Results & Numbers", "What to quote when asked about performance"), sp(10)]

story.append(p(
    "We tested 60 hand-written queries — 10 per intent class. Three variations per class: "
    "direct phrasing, synonym variants, and semantically novel phrasings."))

res_rows = [
    ["Intent",     "Queries", "Execution Acc.", "Schema Acc.", "SQL Match", "Avg Latency"],
    ["COUNT",      "10",      "100%",           "100%",        "100%",      "142 ms"],
    ["AVERAGE",    "10",      "90%",            "100%",        "90%",       "155 ms"],
    ["TOP_N",      "10",      "90%",            "90%",         "90%",       "168 ms"],
    ["BOTTOM_N",   "10",      "90%",            "100%",        "80%",       "171 ms"],
    ["FILTER_GT",  "10",      "80%",            "90%",         "80%",       "163 ms"],
    ["FILTER_LT",  "10",      "80%",            "80%",         "70%",       "177 ms"],
    ["TOTAL",      "60",      "88.3%",          "93.3%",       "85.0%",     "163 ms"],
]
rt = Table(res_rows, colWidths=[2.5*cm, 1.8*cm, 3.0*cm, 2.8*cm, 2.8*cm, W-2.5*cm-1.8*cm-3.0*cm-2.8*cm-2.8*cm])
rt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK), ('TEXTCOLOR', (0,0), (-1,0), white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (-1,-2), 'Helvetica'),
    ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
    ('BACKGROUND', (0,-1), (-1,-1), LBLUE),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('ROWBACKGROUNDS', (0,1), (-1,-2), [white, LGRAY]),
    ('GRID', (0,0), (-1,-1), 0.4, BORDER),
    ('ALIGN', (1,0), (-1,-1), 'CENTER'),
    ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
]))
story += [rt, sp(10)]

story += [h2("Key numbers to remember:"), sp(6)]
key_nums = [
    ["88.3%",    "Execution Accuracy — primary metric (53/60 queries correct)"],
    ["93.3%",    "Schema Match Accuracy — correct table selected (56/60)"],
    ["163 ms",   "Average end-to-end latency on CPU (no GPU)"],
    ["+25 pts",  "Improvement from adding transformer over keyword-only baseline"],
    ["84.7%",    "Average cosine similarity confidence for correct table matches"],
    ["22M",      "Parameters in all-MiniLM-L6-v2 (tiny vs GPT-4's ~1.8 trillion)"],
]
for num, desc in key_nums:
    row = [[
        Paragraph(num, S('kn', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=BLUE, alignment=TA_CENTER)),
        Paragraph(desc, BODY),
    ]]
    t = Table(row, colWidths=[2.5*cm, W - 2.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), LBLUE),
        ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 0.4, BORDER),
        ('LINEBELOW', (0,0), (-1,-1), 0.3, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story += [t]

# ══════════════════════════════════════════════════════════════════════
# 7. FAILURES
# ══════════════════════════════════════════════════════════════════════
story += [sp(14), section_header("7.  Where It Fails & Why", "7 wrong answers — what broke and why"), sp(10)]

story.append(p("7 out of 60 queries failed. Knowing exactly why is important — it shows you actually understand the system."))
story += [sp(6)]

failures = [
    ("❌  Failure 1 — Cross-Table JOIN (3 failures)", ORANGE, LORANGE,
     "Query: \"which students failed in Deep Learning\"\n\n"
     "Needs: JOIN students + marks ON student_id, then filter WHERE subject='Deep Learning' AND marks < 50\n\n"
     "What happened: System correctly picked the marks table but generated a single-table query. "
     "Returned mark records without student names.\n\n"
     "Root cause: No JOIN template exists in the generator. This is the biggest missing feature."),
    ("❌  Failure 2 — Missing Synonyms (2 failures)", ORANGE, LORANGE,
     "Query: \"learners with poor scores\"\n\n"
     "Problem: 'learners' was not in the 54-entry synonym dictionary.\n\n"
     "What happened: Embedding matcher still found the right table (students — semantically close), "
     "but column resolution defaulted to the wrong column.\n\n"
     "Fix: Just add 'learners → students' to the dictionary. No code change needed."),
    ("❌  Failure 3 — Numeric Ambiguity (2 failures)", ORANGE, LORANGE,
     "Query: \"top 3.5 GPA students\"\n\n"
     "Problem: Is 3.5 a count (top 3.5 students?) or a threshold (cgpa >= 3.5)?\n\n"
     "What happened: Number extractor pulled 3.5, TOP_N template used it as LIMIT (truncated to 3). "
     "User actually meant WHERE cgpa >= 3.5.\n\n"
     "Fix: Add logic to check if a float value plausibly serves as a filter threshold vs a result count."),
]
for title, border_col, bg_col, text in failures:
    t = Table([
        [Paragraph(title, S('ft', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=border_col))],
        [Paragraph(text,  S('fb', fontName='Helvetica',      fontSize=9.5, leading=14, textColor=black, alignment=TA_JUSTIFY))],
    ], colWidths=[W])
    t.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, border_col),
        ('BACKGROUND', (0,0), (0,0), bg_col),
        ('BACKGROUND', (0,1), (0,1), white),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12), ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('LINEBELOW', (0,0), (0,0), 0.5, BORDER),
    ]))
    story += [t, sp(6)]

# ══════════════════════════════════════════════════════════════════════
# 8. FAQ FOR FACULTY
# ══════════════════════════════════════════════════════════════════════
story += [sp(14), section_header("8.  Faculty Q&A", "What to say if you get asked these questions"), sp(10)]

qas = [
    ("Why not just use ChatGPT or GPT-4 to generate the SQL?",
     "Two reasons. First, cost and speed — GPT-4 API costs money per call and adds 1–3 seconds of latency. "
     "Our system runs on a regular CPU in 163ms. Second, transparency — if GPT-4 generates wrong SQL, "
     "you can't easily debug why. Our system is fully traceable: every decision maps to a specific "
     "component and you can see exactly why each SQL was produced."),

    ("Why use a transformer at all if most of it is rule-based?",
     "The transformer handles the one part where rules genuinely fail — schema linking with semantic variation. "
     "You cannot write a rule that maps 'academic score' to the cgpa column without a semantic model. "
     "The transformer gives us that generalisation cheaply (22M params, <90MB, no GPU) without needing "
     "to fine-tune a generative model."),

    ("Why templates instead of a sequence-to-sequence model for SQL generation?",
     "Templates guarantee syntactically valid SQL on every single call. A seq2seq model can hallucinate "
     "column names, forget closing parentheses, or generate semantically wrong queries in ways that are "
     "hard to catch. For a closed domain with six intent types, templates cover everything needed and "
     "are trivially auditable."),

    ("What is cosine similarity and why use it?",
     "Cosine similarity measures the angle between two vectors. If they point in the same direction, "
     "similarity is 1.0 (100%). If perpendicular, it's 0. We use it instead of dot product because "
     "it's magnitude-invariant — a long sentence and a short sentence with the same meaning get "
     "the same score, which is what we want when comparing variable-length descriptions."),

    ("What's the biggest limitation of this system?",
     "No support for multi-table JOIN queries. Three out of seven failures were caused by this. "
     "A query like 'which students failed in Deep Learning' needs to join the students and marks "
     "tables — the system can't do that yet. Adding a JOIN intent class with a two-table template "
     "is the highest priority next step."),

    ("How is this different from traditional keyword-based NLIDBs?",
     "Traditional systems like LADDER matched surface text patterns to query fragments — brittle and "
     "domain-locked. Our embedding matcher uses dense vector representations, so semantically similar "
     "text matches even without word overlap. We proved this with a baseline: the keyword-only version "
     "got 68.3% schema accuracy; adding the transformer got 93.3% — a 25-point improvement."),

    ("What is all-MiniLM-L6-v2 and why this model specifically?",
     "It's a distilled sentence transformer trained on natural language inference and paraphrase tasks. "
     "L6 means 6 transformer layers. It produces 384-dimensional embeddings. We chose it because: "
     "(1) 22M parameters — tiny compared to alternatives; (2) under 90MB model size; "
     "(3) ~91ms per sentence on CPU; (4) strong performance on semantic similarity benchmarks. "
     "Compared to all-mpnet-base-v2 which is better but 420MB and much slower — MiniLM-L6 was the "
     "right trade-off for a CPU deployment."),
]

for q, a in qas:
    story += [qa_box(q, a), sp(8)]

# ══════════════════════════════════════════════════════════════════════
# 9. CHEAT SHEET
# ══════════════════════════════════════════════════════════════════════
story += [sp(10), section_header("9.  Quick Cheat Sheet", "Everything you need to remember on one page"), sp(10)]

cheat = Table([
    [Paragraph("Component", S('ch', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=white)),
     Paragraph("What it does", S('ch', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=white)),
     Paragraph("Tech used", S('ch', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=white))],
    [pl("NLPreprocessor"), pl("Normalise → tokenise → extract keywords → detect intent → extract numbers"), pl("Python regex + keyword rules")],
    [pl("EmbeddingMatcher"), pl("Synonym expand → encode query → cosine similarity vs table/col embeddings → pick best match"), pl("all-MiniLM-L6-v2, scikit-learn cosine_similarity")],
    [pl("SQLGenerator"), pl("Intent + table + numbers → fill SQL template → return SQL + explanation dict"), pl("Pure Python string formatting")],
    [pl("SQLExecutor"), pl("Blocklist check → run SQL → return rows + columns + row_count as JSON"), pl("SQLAlchemy, pandas read_sql")],
    [pl("FastAPI app"), pl("POST /query, GET /schema, GET /health"), pl("FastAPI, Pydantic, CORS middleware")],
    [pl("Database"), pl("students (10), marks (50), courses (5) — SQLite file"), pl("SQLAlchemy ORM, SQLite")],
], colWidths=[3.2*cm, 8.5*cm, W - 3.2*cm - 8.5*cm])
cheat.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK), ('TEXTCOLOR', (0,0), (-1,0), white),
    ('FONTSIZE', (0,0), (-1,-1), 9), ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LGRAY]),
    ('GRID', (0,0), (-1,-1), 0.4, BORDER),
    ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 7), ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story += [cheat, sp(12)]

nums_box = Table([[
    Table([
        [Paragraph("Key Numbers", S('kh', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=white))],
        [Paragraph("88.3% Execution Accuracy", BODY)],
        [Paragraph("93.3% Schema Match Accuracy", BODY)],
        [Paragraph("163 ms avg latency (CPU)", BODY)],
        [Paragraph("+25 pts over keyword baseline", BODY)],
        [Paragraph("22M params, <90MB model", BODY)],
        [Paragraph("60 test queries, 6 intent classes", BODY)],
    ], colWidths=[(W-1*cm)/2 - 0.5*cm]),
    Table([
        [Paragraph("Failure Modes (7 total)", S('kh', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=white))],
        [Paragraph("3 × JOIN queries (no template)", BODY)],
        [Paragraph("2 × Missing synonyms (easy fix)", BODY)],
        [Paragraph("2 × Numeric ambiguity", BODY)],
        [Paragraph(" ", BODY)],
        [Paragraph("Next step: add JOIN support", S('nx', fontName='Helvetica-BoldOblique', fontSize=10, leading=13, textColor=BLUE))],
        [Paragraph(" ", BODY)],
    ], colWidths=[(W-1*cm)/2 - 0.5*cm]),
]], colWidths=[(W-1*cm)/2, (W-1*cm)/2])
nums_box.setStyle(TableStyle([
    ('BOX', (0,0), (-1,-1), 1, BLUE),
    ('LINEBEFORE', (1,0), (1,-1), 0.5, BORDER),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
]))
story.append(nums_box)

doc.build(story)
print("Done.")
