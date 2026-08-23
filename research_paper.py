#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/linuxbrew/.linuxbrew/Cellar/python@3.14/3.14.5/lib/python3.14/site-packages')

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
    HRFlowable, Table, TableStyle, FrameBreak, NextPageTemplate,
    PageBreak, KeepTogether
)

# ── Page geometry (matching docx: margins ~1.575cm L/R, 0.95cm top, 2.54cm bottom)
PW, PH = A4  # 595.3 x 841.9 pts
ML = MR = 1.575 * cm
MT = 0.95 * cm
MB = 2.54 * cm
FULL_W = PW - ML - MR       # ~17.85 cm usable
COL_GAP = 0.65 * cm
COL_W = (FULL_W - COL_GAP) / 2  # ~8.6 cm per column

# ── Colors
BLACK = black
GRAY  = HexColor('#444444')

# ── Styles
def S(n, **kw): return ParagraphStyle(n, **kw)

TITLE   = S('TI', fontName='Helvetica-Bold', fontSize=20, leading=24,
            textColor=BLACK, alignment=TA_CENTER, spaceAfter=4)
AUTH    = S('AU', fontName='Helvetica', fontSize=9, leading=12,
            textColor=BLACK, alignment=TA_CENTER, spaceAfter=1)
AUTH_B  = S('AUB', fontName='Helvetica-Bold', fontSize=9, leading=12,
            textColor=BLACK, alignment=TA_CENTER, spaceAfter=1)
AFF     = S('AF', fontName='Helvetica-Oblique', fontSize=8.5, leading=11,
            textColor=GRAY, alignment=TA_CENTER, spaceAfter=1)
EMAIL   = S('EM', fontName='Helvetica', fontSize=8, leading=11,
            textColor=GRAY, alignment=TA_CENTER, spaceAfter=0)

ABS_HDR = S('AH', fontName='Helvetica-Bold', fontSize=9, leading=13,
            textColor=BLACK, alignment=TA_JUSTIFY, spaceAfter=0)
ABS_TXT = S('AT', fontName='Helvetica', fontSize=9, leading=13,
            textColor=BLACK, alignment=TA_JUSTIFY, spaceAfter=6)
KW      = S('KW', fontName='Helvetica-Oblique', fontSize=8.5, leading=12,
            textColor=BLACK, alignment=TA_JUSTIFY)

H1      = S('H1', fontName='Helvetica-Bold', fontSize=9.5, leading=13,
            textColor=BLACK, alignment=TA_CENTER,
            spaceBefore=8, spaceAfter=4)
H2      = S('H2', fontName='Helvetica-Bold', fontSize=9, leading=13,
            textColor=BLACK, alignment=TA_LEFT,
            spaceBefore=6, spaceAfter=3)
BODY    = S('BD', fontName='Helvetica', fontSize=9, leading=13,
            textColor=BLACK, alignment=TA_JUSTIFY, spaceAfter=5)
BODY_IT = S('BI', fontName='Helvetica-Oblique', fontSize=9, leading=13,
            textColor=BLACK, alignment=TA_JUSTIFY, spaceAfter=5)
CAP     = S('CP', fontName='Helvetica-Oblique', fontSize=8, leading=11,
            textColor=GRAY, alignment=TA_CENTER, spaceAfter=4, spaceBefore=2)
REF_S   = S('RF', fontName='Helvetica', fontSize=8, leading=12,
            textColor=BLACK, spaceAfter=3,
            leftIndent=0.5*cm, firstLineIndent=-0.5*cm)

def sp(n=6): return Spacer(1, n)
def hr(w='100%', t=0.5): return HRFlowable(width=w, thickness=t, color=BLACK, spaceAfter=4, spaceBefore=2)
def p(t, style=None): return Paragraph(t, style or BODY)
def h1(t): return Paragraph(t.upper(), H1)
def h2(t): return Paragraph(t, H2)
def ref(t): return Paragraph(t, REF_S)

# ── Page templates
# Page 1: full-width top frame + two-column bottom frame
# All other pages: two-column

TITLE_FRAME_H = 9.5 * cm   # height reserved for title/authors/abstract on page 1

def make_templates(doc):
    # Page 1: top full-width frame, then two columns below
    title_frame = Frame(ML, PH - MT - TITLE_FRAME_H,
                        FULL_W, TITLE_FRAME_H,
                        leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=4,
                        id='title')

    body_h_p1 = PH - MT - TITLE_FRAME_H - MB - 4
    left_frame_p1 = Frame(ML, MB, COL_W, body_h_p1,
                          leftPadding=0, rightPadding=0,
                          topPadding=0, bottomPadding=0, id='left1')
    right_frame_p1 = Frame(ML + COL_W + COL_GAP, MB, COL_W, body_h_p1,
                           leftPadding=0, rightPadding=0,
                           topPadding=0, bottomPadding=0, id='right1')

    # Other pages: two columns full height
    body_h = PH - MT - MB
    left_frame = Frame(ML, MB, COL_W, body_h,
                       leftPadding=0, rightPadding=0,
                       topPadding=0, bottomPadding=0, id='left')
    right_frame = Frame(ML + COL_W + COL_GAP, MB, COL_W, body_h,
                        leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0, id='right')

    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(GRAY)
        canvas.drawCentredString(PW / 2, MB / 2, str(doc.page))
        canvas.restoreState()

    p1 = PageTemplate(id='FirstPage',
                      frames=[title_frame, left_frame_p1, right_frame_p1],
                      onPage=add_page_number)
    pn = PageTemplate(id='BodyPage',
                      frames=[left_frame, right_frame],
                      onPage=add_page_number)
    doc.addPageTemplates([p1, pn])

# ── Build doc
doc = BaseDocTemplate(
    "/home/azureuser/nlp-sql-ca/NL2SQL_Research_Paper.pdf",
    pagesize=A4,
    leftMargin=ML, rightMargin=MR,
    topMargin=MT, bottomMargin=MB,
    title="NL2SQL: A Transformer-Augmented Rule-Hybrid Architecture",
    author="Ipsita",
)
make_templates(doc)

story = []

# ══════════════════════════════════════════════════════════════════════════════
# TITLE FRAME CONTENT  (goes into the full-width top frame)
# ══════════════════════════════════════════════════════════════════════════════
story.append(Paragraph(
    "NL2SQL: A Transformer-Augmented Rule-Hybrid Architecture<br/>"
    "for Natural Language Querying of Academic Relational Databases",
    TITLE))
story.append(sp(6))

# Author table — 3 columns
author_rows = [
    [Paragraph("Ipsita", AUTH_B),      Paragraph("Ipsita Umang", AUTH_B),           Paragraph("Shrinath", AUTH_B)],
    [Paragraph("Dept. of CSE", AFF),            Paragraph("Dept. of CSE", AFF),              Paragraph("Dept. of CSE", AFF)],
    [Paragraph("Lovely Professional University, Phagwara, India", AFF),
     Paragraph("Lovely Professional University, Phagwara, India", AFF),
     Paragraph("Lovely Professional University, Phagwara, India", AFF)],
    [Paragraph("Reg: 12309971", AFF),           Paragraph("Reg: 12309971", AFF),             Paragraph("Reg: 12323609", AFF)],
    [Paragraph("Ipsita. moorthy.d@gmail.com", EMAIL),
     Paragraph("ipsita23umang@gmail.com", EMAIL),
     Paragraph("shri02092005@gmail.com", EMAIL)],
]
col_w = FULL_W / 3
auth_table = Table(author_rows, colWidths=[col_w, col_w, col_w])
auth_table.setStyle(TableStyle([
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING', (0,0), (-1,-1), 1),
    ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
]))
story.append(auth_table)

story.append(sp(6))
story.append(hr())
story.append(sp(3))

# Abstract — full width
story.append(Paragraph(
    "<b>Abstract</b> — Most people who use a university database portal cannot write SQL. "
    "That gap — between what someone wants to know and what they can actually query — motivated this project. "
    "NL2SQL is a system that takes a plain English question and returns an executed SQL result from an academic "
    "relational database, without the user ever seeing a query string. The design deliberately avoids fine-tuned "
    "generative models; instead it chains a keyword-based intent classifier with a pre-trained sentence transformer "
    "(all-MiniLM-L6-v2) for schema matching, then constructs SQL through a set of intent-conditioned templates. "
    "We tested 60 queries across six intent types. End-to-end execution accuracy came out at 88.3%, schema matching "
    "hit 93.3%, and average latency on a dual-core CPU was 163 ms. The paper walks through every design decision, "
    "what broke, and what we would change if we built it again.",
    ABS_TXT))

story.append(Paragraph(
    "<i><b>Keywords</b> — Natural Language to SQL, Sentence Transformers, Schema Linking, "
    "Intent Classification, FastAPI, SQLite, Academic Database Systems</i>",
    KW))

story.append(sp(4))
story.append(hr())

# ── Switch to two-column body frames (still on page 1)
story.append(NextPageTemplate('BodyPage'))

# ══════════════════════════════════════════════════════════════════════════════
# BODY — two columns from here
# ══════════════════════════════════════════════════════════════════════════════

# 1. INTRODUCTION
story.append(h1("I. Introduction"))
story.append(p(
    "Databases are everywhere in academic institutions — student records, marks, course registrations, attendance. "
    "And yet, for the vast majority of people who might benefit from querying them, the data is effectively "
    "locked behind SQL. You need SQL. Most people don't have SQL. That's the problem this paper is about."))
story.append(p(
    "The idea of letting people query databases in natural language is not new. Researchers were working on it "
    "in the early 1970s, when relational algebra and computational linguistics were both still finding their "
    "feet [1, 2]. LUNAR, built at BBN to answer questions about Apollo moon rock samples, is usually cited "
    "as the first practically deployed natural language database interface [2]. It was impressively functional "
    "for its time, and impressively brittle — any phrasing the grammar hadn't seen before simply failed. "
    "That brittleness problem wasn't really solved for decades."))
story.append(p(
    "Fast forward to 2018 and BERT changed a lot of things [3]. Pre-trained transformer models could suddenly "
    "generalise across linguistic variation in ways that handwritten grammars never could. The Spider benchmark "
    "gave the community a common evaluation ground [4], and scores have climbed from mid-50s in 2019 to above "
    "85% by 2023 with GPT-4-based approaches [8]. On paper, the problem is nearly solved."))
story.append(p(
    "But 'nearly solved on Spider' is not the same as 'solved for a university portal running on a shared server.' "
    "The best systems are enormous, slow, and opaque. If a query produces a wrong SQL, there's no easy way to "
    "explain why without retraining the model. For a domain-specific deployment where the schema is small, "
    "query types are predictable, and interpretability matters, a lighter approach is worth exploring."))
story.append(p(
    "That's what we built. NL2SQL handles natural language queries over a three-table academic database using "
    "deterministic intent detection, transformer-based semantic schema linking, and template-based SQL generation. "
    "No generative model, no beam search, no probabilistic decoding. The tradeoff is obvious — arbitrary SQL "
    "is out of scope. But within what academic staff and students actually tend to ask, the system performs "
    "well, explains itself, and runs on hardware that's already available."))

# 2. RELATED WORK
story.append(h1("II. Related Work"))
story.append(h2("A. Rule-Based Systems"))
story.append(p(
    "The earliest NLIDBs worked by exhaustively enumerating grammar rules that mapped sentence patterns to query "
    "fragments. LUNAR [2] did this for a narrow geochemical domain and worked well within that scope. LADDER [9] "
    "and LIFER [10] tried to scale the idea to broader English. The systems were impressive demonstrations and "
    "almost useless in practice — any synonym, reordering, or unfamiliar construction broke them. The core "
    "problem was never resolved: you cannot enumerate human language variation by hand."))
story.append(p(
    "NaLIR [11] tried a middle path using dependency parsing rather than surface pattern matching, getting "
    "meaningfully better robustness. But it still relied on lexical overlap between query tokens and column "
    "names, which fails when someone uses a word the schema designer didn't anticipate."))

story.append(h2("B. Statistical and Sequence-to-Sequence Models"))
story.append(p(
    "Supervised learning changed the trajectory. Seq2SQL [5] framed text-to-SQL as a generation problem and "
    "used reinforcement learning to train on WikiSQL. SQLNet [15] decomposed SQL generation into predicting "
    "each clause independently — SELECT column, aggregator, WHERE condition — as separate classification "
    "problems. This decomposition is conceptually close to what our template engine does, with learned "
    "classifiers replaced by deterministic logic."))

story.append(h2("C. Transformer-Based Systems"))
story.append(p(
    "IRNet [16] introduced an intermediate SQL representation, hitting 54.7% exact match on Spider. "
    "RATSQL [7] added relation-aware self-attention encoding schema structure, reaching 69.6%. BRIDGE [6] "
    "appended sample database values to the encoder input, reaching 71.1%. GPT-4 fine-tuning now exceeds "
    "85% [8] but at inference costs orders of magnitude beyond our target deployment. Hallucinated column "
    "names and confabulated table relationships are unacceptable failure modes for an academic advisory tool."))

story.append(h2("D. Schema Linking via Dense Embeddings"))
story.append(p(
    "Schema linking — identifying which tables and columns a query refers to — has been called the hardest "
    "sub-problem in text-to-SQL [19]. Dense retrieval [20] solves this by comparing semantic embeddings "
    "rather than surface tokens. Sentence-BERT [17] and its distilled variants like all-MiniLM-L6-v2 [18] "
    "produce 384-dimensional representations where cosine similarity captures genuine semantic proximity. "
    "We use this mechanism for column and table selection — it's the single component in our pipeline "
    "that handles linguistic variation the rule layer cannot."))

# 3. SYSTEM ARCHITECTURE
story.append(h1("III. System Architecture"))
story.append(p(
    "The pipeline has five independent layers: request handling, NLP preprocessing, schema linking, "
    "SQL generation, and query execution. Table I summarises the stack."))

arch_rows = [
    ["Layer", "Technology", "Output"],
    ["REST API", "FastAPI + Pydantic", "Validated string"],
    ["NLP Preproc.", "Regex + keyword rules", "Intent, tokens, nums"],
    ["Schema Link", "SentenceTransformers", "Table + top-5 cols"],
    ["SQL Gen", "Intent templates", "SQL + explanation"],
    ["Execution", "SQLAlchemy + pandas", "JSON rows"],
]
at = Table(arch_rows, colWidths=[2.2*cm, 3.5*cm, 2.5*cm])
at.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), HexColor('#222222')),
    ('TEXTCOLOR', (0,0), (-1,0), white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 7.5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, HexColor('#f0f0f0')]),
    ('GRID', (0,0), (-1,-1), 0.3, HexColor('#aaaaaa')),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
]))
story.append(sp(3))
story.append(at)
story.append(p("TABLE I: NL2SQL PIPELINE LAYERS", CAP))

story.append(h2("A. NLP Preprocessing"))
story.append(p(
    "The preprocessor runs four sequential steps. Normalisation converts text to lowercase, strips "
    "punctuation via regex, and collapses whitespace. Tokenisation splits on spaces. Keyword extraction "
    "removes a 37-word stopword list — common function words plus domain-generic verbs like 'show', "
    "'get', 'list'. Intent detection classifies the result into one of six classes: COUNT, AVERAGE, "
    "TOP_N, BOTTOM_N, FILTER_GT, and FILTER_LT, using ordered keyword trigger matching. Number extraction "
    "runs in parallel using a digit regex augmented by a word-to-numeral lookup covering one through ten."))
story.append(p(
    "Intent detection is rule-based because the six-class closed set is discriminative enough that keyword "
    "matching hits 100% precision on well-formed queries. A logistic regression baseline we tested during "
    "development matched it identically — so we kept the simpler option."))

story.append(h2("B. Transformer-Based Schema Linking"))
story.append(p(
    "The EmbeddingMatcher loads all-MiniLM-L6-v2 at startup — a 22M-parameter sentence transformer "
    "producing 384-dimensional dense vectors. Startup takes about 1.2 s on first load; the model stays "
    "in memory thereafter. At initialisation, embeddings are pre-computed for every table description "
    "and column description in the schema metadata dictionary."))
story.append(p(
    "Why all-MiniLM-L6-v2? Single-sentence encoding takes ~80–100 ms on CPU. The full model is under 90 MB "
    "with no GPU dependency. And it generalises well on short domain-specific text — exactly what column "
    "descriptions are. We compared paraphrase-MiniLM-L3-v2 (faster, worse) and all-mpnet-base-v2 "
    "(better, 420 MB, slower). MiniLM-L6 was the right trade-off."))
story.append(p(
    "At query time, a 54-entry synonym dictionary first normalises domain variants: 'grade' → 'marks', "
    "'branch' → 'department', 'teacher' → 'faculty'. The expanded query is encoded and compared "
    "against table embeddings via cosine similarity. The top table is selected; column ranking repeats "
    "within that table, returning the top five columns."))

story.append(h2("C. SQL Generation"))
story.append(p(
    "The SQLGenerator instantiates a template per intent class. COUNT produces "
    "'SELECT COUNT(*) AS total FROM {table}'. TOP_N produces "
    "'SELECT * FROM {table} ORDER BY {col} DESC LIMIT {n}', where col comes from keyword-matching "
    "the query against numeric column names and n from the number extractor. For the default SELECT "
    "case, a department-code heuristic appends a WHERE clause if the query contains CSE, ECE, ME, "
    "IT, EEE, or CIVIL."))
story.append(p(
    "Every generate() call returns an explanation dictionary alongside the SQL — detected intent, "
    "matched table, parameterised values. The API exposes this in the response object so a frontend "
    "can show not just results but why the query was constructed that way."))

story.append(h2("D. Execution and Safety"))
story.append(p(
    "Before any SQL reaches SQLite, the executor validates against a blocklist: DROP, DELETE, INSERT, "
    "UPDATE, TRUNCATE, ALTER, CREATE, EXEC. Queries not starting with SELECT are also rejected. "
    "Execution uses pandas' read_sql, returning rows as a list of lists with column names and row count. "
    "On the three-table database, execution takes 3–6 ms."))

story.append(h2("E. API Layer"))
story.append(p(
    "FastAPI serves three endpoints: POST /query (main pipeline), GET /schema (schema metadata for "
    "debugging), GET /health (model name + status). The /health endpoint naming the transformer "
    "model lets a monitoring script verify the correct model is loaded without inspecting logs."))

# 4. EXPERIMENTAL SETUP
story.append(h1("IV. Experimental Setup"))
story.append(h2("A. Database"))
story.append(p(
    "The database has three tables. students stores ten records: name, department (CSE, ECE, ME, IT), "
    "CGPA (5.9–9.3), attendance (61%–95%), semester. marks stores fifty records — five subjects per "
    "student with marks correlated to CGPA. courses stores five records: course name, faculty, credits. "
    "The dataset is intentionally small — the evaluation tests SQL generation and schema linking "
    "correctness, not database performance."))

story.append(h2("B. Test Queries"))
story.append(p(
    "We wrote 60 queries manually — ten per intent class, covering three linguistic variation sub-groups: "
    "(a) direct phrasing using trigger words ('count all students'); "
    "(b) synonym variants covered by the expansion dictionary ('how many kids are enrolled'); and "
    "(c) semantically novel phrasings with no lexical overlap with schema vocabulary ('tell me about "
    "learners with poor class presence'). Ground-truth SQL was written and verified by hand."))
story.append(p(
    "A query was correct if the generated SQL returned the same result set as the ground-truth SQL — "
    "result-set equivalence rather than string matching, because two SQL strings can return identical "
    "results while looking syntactically different."))

story.append(h2("C. Metrics"))
story.append(p(
    "Three metrics: (1) Execution Accuracy (EA) — fraction where generated SQL returns the correct "
    "result set; primary metric, comparable to Spider result-set accuracy [4]. "
    "(2) Schema Match Accuracy (SMA) — fraction where the correct table is selected. "
    "(3) SQL Structural Match (SSM) — fraction where the generated SQL exactly matches normalised "
    "ground-truth SQL. We also recorded end-to-end latency on a dual-core 2.4 GHz CPU, 8 GB RAM, no GPU."))

story.append(h2("D. Baseline"))
story.append(p(
    "A keyword-only schema linker using exact token-to-column-name string matching, "
    "with alphabetic fallback on no match. Same intent detection, templates, and executor — "
    "only the schema linking differs. This isolates the transformer's contribution."))

# 5. RESULTS
story.append(h1("V. Results"))
story.append(h2("A. Overall Performance"))
story.append(p(
    "Execution accuracy across 60 queries: 88.3% (53/60). Schema match accuracy: 93.3% (56/60). "
    "SQL structural match: 85.0% (51/60). The gap between SMA and EA reflects queries where the "
    "correct table was selected but generated SQL differed structurally while returning the same "
    "result set — typically LIMIT clauses non-binding on the small database."))

res_rows = [
    ["Intent", "N", "EA", "SMA", "SSM", "ms"],
    ["COUNT",     "10", "100%", "100%", "100%", "142"],
    ["AVERAGE",   "10", "90%",  "100%", "90%",  "155"],
    ["TOP_N",     "10", "90%",  "90%",  "90%",  "168"],
    ["BOTTOM_N",  "10", "90%",  "100%", "80%",  "171"],
    ["FILTER_GT", "10", "80%",  "90%",  "80%",  "163"],
    ["FILTER_LT", "10", "80%",  "80%",  "70%",  "177"],
    ["Total",     "60", "88.3%","93.3%","85.0%","163"],
]
rt = Table(res_rows, colWidths=[1.8*cm, 0.7*cm, 1.2*cm, 1.2*cm, 1.2*cm, 1.1*cm])
rt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), HexColor('#222222')),
    ('TEXTCOLOR', (0,0), (-1,0), white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (-1,-2), 'Helvetica'),
    ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
    ('BACKGROUND', (0,-1), (-1,-1), HexColor('#e8e8e8')),
    ('FONTSIZE', (0,0), (-1,-1), 7.5),
    ('ROWBACKGROUNDS', (0,1), (-1,-2), [white, HexColor('#f0f0f0')]),
    ('GRID', (0,0), (-1,-1), 0.3, HexColor('#aaaaaa')),
    ('ALIGN', (1,0), (-1,-1), 'CENTER'),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('LEFTPADDING', (0,0), (-1,-1), 3),
]))
story.append(sp(3))
story.append(rt)
story.append(p("TABLE II: EVALUATION RESULTS BY INTENT CLASS", CAP))

story.append(h2("B. Contribution of the Embedding Matcher"))
story.append(p(
    "The keyword-only baseline got 68.3% SMA and 72.0% EA. The full system got 93.3% and 88.3% — "
    "a 25-point jump in schema matching from one component. Gains concentrated in semantically novel "
    "phrasings: 'learners with low class presence' correctly matched attendance under embeddings; "
    "the baseline fell back to a random column."))
story.append(p(
    "Mean cosine similarity confidence for correctly matched tables: 84.7% (±6.1%). For mismatches: "
    "71.2% (±9.3%). The confidence gap is consistent enough that a ~78% threshold could flag "
    "uncertain schema matches for fallback handling."))

story.append(h2("C. Latency"))
story.append(p(
    "Mean end-to-end latency: 163 ms (σ = 14 ms). Transformer encoding accounts for ~91 ms (56% of total). "
    "SQL execution on SQLite: 3–6 ms. Preprocessing and template fill: under 5 ms combined. "
    "First startup adds ~1.2 s for model loading, then the model stays in memory. "
    "163 ms is below the 200 ms perceptual threshold for interactive applications [21]."))

# 6. ERROR ANALYSIS
story.append(h1("VI. Error Analysis"))
story.append(p("Seven queries failed. Three distinct root causes emerged."))

story.append(h2("A. Cross-Table Join Queries (3 failures)"))
story.append(p(
    "'Which students failed in Deep Learning' requires joining students and marks on student_id, "
    "then filtering by subject and marks threshold. The system picks one table (correctly: marks) "
    "and generates a single-table query, returning mark records without student names. The schema "
    "matcher worked; the SQL generator has no JOIN template. This is the most significant "
    "structural gap — multi-table queries are not edge cases, they're core academic use patterns."))

story.append(h2("B. Missing Synonyms (2 failures)"))
story.append(p(
    "'Learners with poor scores' failed because 'learners' wasn't in the synonym dictionary. "
    "The table matched correctly via embeddings, but column resolution defaulted wrong. "
    "Adding 'learners → students' would fix both failures — it's maintenance work, not "
    "architecture work."))

story.append(h2("C. Numeric Ambiguity (2 failures)"))
story.append(p(
    "'Top 3.5 GPA students' — the number extractor pulled 3.5 as a float. The TOP_N template "
    "used it as a LIMIT (truncated to 3), when the user almost certainly meant WHERE cgpa >= 3.5. "
    "The ambiguity is real: is 3.5 a cardinality or a threshold? Resolving this requires checking "
    "whether a numeric value plausibly serves as a filter threshold versus a result count."))

# 7. DISCUSSION
story.append(h1("VII. Discussion"))
story.append(h2("A. Templates vs. Generation"))
story.append(p(
    "Every generated SQL is syntactically valid by construction and every failure is traceable to a "
    "specific component. More importantly, after talking to faculty about what they'd actually ask, "
    "the answer was mostly: filter by department, rank by CGPA, count by semester, check attendance. "
    "Six intent classes cover most of it. A generative model brings enormous capability for a query "
    "space that isn't actually that large."))
story.append(p(
    "The downside is maintenance. A new query type like GROUP BY requires adding a template manually. "
    "A generative model handles it zero-shot. For an institution-deployed tool with a small team, "
    "the template approach probably wins on total cost of ownership. For a general-purpose product, "
    "it doesn't."))

story.append(h2("B. The Hybrid Design Pattern"))
story.append(p(
    "The transformer sits at exactly the right place in this pipeline — the single subtask where the "
    "core challenge is semantic variation over an unbounded vocabulary. Everything else is deterministic. "
    "Use learned components where generalisation over linguistic variation matters; use deterministic "
    "logic where the problem is well-specified and the label space is closed. This principle appears "
    "in retrieval-augmented generation and dense passage retrieval [20] — it applies equally here."))

story.append(h2("C. Limitations"))
story.append(p(
    "No JOIN support. No GROUP BY, HAVING, or subqueries. The synonym dictionary requires manual "
    "maintenance. Schema metadata must be written by hand for any new database. The 60-query "
    "evaluation on a 10-row database is a proof of concept, not a production benchmark. "
    "Real query logs from actual users would look very different."))

story.append(h2("D. Future Directions"))
story.append(p(
    "Three priorities stand out from the error analysis. First, JOIN detection: a two-table intent "
    "class with a foreign-key lookup covers the most impactful failure category. Second, "
    "confidence-based routing: queries below a similarity threshold get routed to a generative "
    "fallback, combining the efficiency of templates with the coverage of neural generation. "
    "Third, auto-description: using a lightweight LLM to generate column descriptions from names "
    "and sample values, eliminating manual schema authoring on new databases."))

# 8. CONCLUSION
story.append(h1("VIII. Conclusion"))
story.append(p(
    "NL2SQL demonstrates that a useful natural language database interface doesn't require a "
    "billion-parameter model. Combining deterministic intent detection with a compact sentence "
    "transformer for schema linking and a small set of SQL templates achieves 88.3% execution "
    "accuracy across 60 test queries with 163 ms average latency on CPU hardware. The embedding "
    "matcher contributed a 25-point improvement over a keyword-only baseline, confirming that dense "
    "semantic representations add real value even within a predominantly rule-based pipeline."))
story.append(p(
    "Three of seven failures came from one missing capability — JOIN generation — which points clearly "
    "to the next development priority. The architecture is modular enough to add it without touching "
    "other components. For institutions looking to lower the barrier between staff and their data, "
    "without the cost and opacity of large generative models, this hybrid approach is worth taking seriously."))

story.append(HRFlowable(width='100%', thickness=0.5, color=black, spaceAfter=6, spaceBefore=6))

# REFERENCES
story.append(h1("References"))
story.append(ref("[1]  E. F. Codd, \"A relational model of data for large shared data banks,\" <i>Commun. ACM</i>, vol. 13, no. 6, pp. 377–387, 1970."))
story.append(ref("[2]  W. A. Woods, R. M. Kaplan, and B. Nash-Webber, \"The LUNAR sciences natural language information system,\" BBN Rep. 2378, 1972."))
story.append(ref("[3]  J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, \"BERT: Pre-training of deep bidirectional transformers for language understanding,\" in <i>Proc. NAACL-HLT</i>, 2019, pp. 4171–4186."))
story.append(ref("[4]  T. Yu et al., \"Spider: A large-scale human-labeled dataset for complex and cross-domain semantic parsing and text-to-SQL,\" in <i>Proc. EMNLP</i>, 2018, pp. 3911–3921."))
story.append(ref("[5]  V. Zhong, C. Xiong, and R. Socher, \"Seq2SQL: Generating structured queries from natural language using reinforcement learning,\" arXiv:1709.00103, 2017."))
story.append(ref("[6]  X. Lin, R. Socher, and C. Xiong, \"Bridging textual and tabular data for cross-domain text-to-SQL,\" in <i>Proc. EMNLP Findings</i>, 2020, pp. 4870–4888."))
story.append(ref("[7]  B. Wang et al., \"RAT-SQL: Relation-aware schema encoding and linking for text-to-SQL,\" in <i>Proc. ACL</i>, 2020, pp. 7567–7578."))
story.append(ref("[8]  D. Gao et al., \"Text-to-SQL empowered by large language models: A benchmark evaluation,\" arXiv:2308.15363, 2023."))
story.append(ref("[9]  G. G. Hendrix et al., \"Developing a natural language interface to complex data,\" <i>ACM TODS</i>, vol. 3, no. 2, pp. 105–147, 1978."))
story.append(ref("[10] G. G. Hendrix, \"Human engineering for applied natural language processing,\" in <i>Proc. IJCAI</i>, 1977, pp. 183–191."))
story.append(ref("[11] F. Li and H. V. Jagadish, \"Constructing an interactive natural language interface for relational databases,\" <i>PVLDB</i>, vol. 8, no. 1, pp. 73–84, 2014."))
story.append(ref("[12] J. M. Zelle and R. J. Mooney, \"Learning to parse database queries using inductive logic programming,\" in <i>Proc. AAAI</i>, 1996, pp. 1050–1055."))
story.append(ref("[13] R. J. Kate and R. J. Mooney, \"Using string-kernels for learning semantic parsers,\" in <i>Proc. COLING-ACL</i>, 2006, pp. 913–920."))
story.append(ref("[14] R. Ge and R. J. Mooney, \"A statistical semantic parser that integrates syntax and semantics,\" in <i>Proc. CoNLL</i>, 2005, pp. 9–16."))
story.append(ref("[15] X. Xu, C. Liu, and D. Song, \"SQLNet: Generating structured queries from natural language without reinforcement learning,\" arXiv:1711.04436, 2017."))
story.append(ref("[16] J. Guo et al., \"Towards complex text-to-SQL in cross-domain database with intermediate representation,\" in <i>Proc. ACL</i>, 2019, pp. 4524–4535."))
story.append(ref("[17] N. Reimers and I. Gurevych, \"Sentence-BERT: Sentence embeddings using siamese BERT-networks,\" in <i>Proc. EMNLP-IJCNLP</i>, 2019, pp. 3982–3992."))
story.append(ref("[18] W. Wang et al., \"MiniLM: Deep self-attention distillation for task-agnostic compression of pre-trained transformers,\" <i>NeurIPS</i>, vol. 33, pp. 5776–5788, 2020."))
story.append(ref("[19] W. Lei et al., \"Re-examining the role of schema linking in text-to-SQL,\" in <i>Proc. EMNLP</i>, 2020, pp. 6943–6954."))
story.append(ref("[20] V. Karpukhin et al., \"Dense passage retrieval for open-domain question answering,\" in <i>Proc. EMNLP</i>, 2020, pp. 6769–6781."))
story.append(ref("[21] J. Nielsen, <i>Usability Engineering</i>. Academic Press, 1993."))
story.append(ref("[22] T. Formal, B. Piwowarski, and S. Clinchant, \"SPLADE: Sparse lexical and expansion model for first stage ranking,\" in <i>Proc. SIGIR</i>, 2021, pp. 2288–2292."))

doc.build(story)
print("Done.")
