"""Build the NeuroONE backend architecture report as a styled DOCX."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports" / "NeuroONE_Backend_Architecture_Report.docx"

NAVY = "12314A"
BLUE = "236A96"
CYAN = "4FA3C7"
TEAL = "21867A"
GREEN = "4C956C"
GOLD = "D89B35"
RED = "B55252"
INK = "1C2730"
MUTED = "637381"
PALE_BLUE = "EAF3F8"
PALE_TEAL = "E8F4F1"
PALE_GOLD = "FFF6E4"
PALE_RED = "FBECEC"
LIGHT = "F4F7F9"
GRID = "CBD5DC"
WHITE = "FFFFFF"


def rgb(hex_color: str) -> RGBColor:
    return RGBColor.from_string(hex_color)


def set_run_font(
    run,
    *,
    name: str = "Calibri",
    size: float | None = None,
    color: str | None = None,
    bold: bool | None = None,
    italic: bool | None = None,
):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    if size is not None:
        run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = rgb(color)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    return run


def set_cell_shading(cell, fill: str):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=90, start=120, bottom=90, end=120):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def set_table_geometry(table, widths_dxa: list[int], indent_dxa: int = 120):
    total = sum(widths_dxa)
    table.autofit = False
    table.alignment = WD_TABLE_ALIGNMENT.LEFT

    tbl_pr = table._tbl.tblPr
    tbl_w = tbl_pr.find(qn("w:tblW"))
    if tbl_w is None:
        tbl_w = OxmlElement("w:tblW")
        tbl_pr.insert(0, tbl_w)
    tbl_w.set(qn("w:w"), str(total))
    tbl_w.set(qn("w:type"), "dxa")

    tbl_ind = tbl_pr.find(qn("w:tblInd"))
    if tbl_ind is None:
        tbl_ind = OxmlElement("w:tblInd")
        tbl_pr.append(tbl_ind)
    tbl_ind.set(qn("w:w"), str(indent_dxa))
    tbl_ind.set(qn("w:type"), "dxa")

    grid = table._tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for width in widths_dxa:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(width))
        grid.append(col)

    for row in table.rows:
        for index, (cell, width) in enumerate(zip(row.cells, widths_dxa)):
            tc_pr = cell._tc.get_or_add_tcPr()
            tc_w = tc_pr.find(qn("w:tcW"))
            if tc_w is None:
                tc_w = OxmlElement("w:tcW")
                tc_pr.append(tc_w)
            tc_w.set(qn("w:w"), str(width))
            tc_w.set(qn("w:type"), "dxa")
            cell.width = Inches(width / 1440)
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def style_table(table, widths_dxa: list[int], *, header_fill=PALE_BLUE, font_size=9):
    table.style = "Table Grid"
    set_table_geometry(table, widths_dxa)
    if table.rows:
        set_repeat_table_header(table.rows[0])
    for row_index, row in enumerate(table.rows):
        for cell in row.cells:
            if row_index == 0:
                set_cell_shading(cell, header_fill)
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.space_before = Pt(0)
                paragraph.paragraph_format.space_after = Pt(1.5)
                paragraph.paragraph_format.line_spacing = 1.0
                for run in paragraph.runs:
                    set_run_font(
                        run,
                        size=font_size,
                        color=NAVY if row_index == 0 else INK,
                        bold=True if row_index == 0 else None,
                    )


def add_table(doc, headers: list[str], rows: list[list[str]], widths_dxa: list[int], *, header_fill=PALE_BLUE, font_size=9):
    table = doc.add_table(rows=1, cols=len(headers))
    for index, header in enumerate(headers):
        table.rows[0].cells[index].text = header
    for row_data in rows:
        cells = table.add_row().cells
        for index, value in enumerate(row_data):
            cells[index].text = str(value)
    style_table(table, widths_dxa, header_fill=header_fill, font_size=font_size)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return table


def add_field(paragraph, instruction: str):
    run = paragraph.add_run()
    fld_char_begin = OxmlElement("w:fldChar")
    fld_char_begin.set(qn("w:fldCharType"), "begin")
    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = instruction
    fld_char_separate = OxmlElement("w:fldChar")
    fld_char_separate.set(qn("w:fldCharType"), "separate")
    fallback = OxmlElement("w:t")
    fallback.text = "1"
    fld_char_end = OxmlElement("w:fldChar")
    fld_char_end.set(qn("w:fldCharType"), "end")
    run._r.extend([fld_char_begin, instr_text, fld_char_separate, fallback, fld_char_end])


def configure_document(doc: Document):
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.header_distance = Inches(0.492)
    section.footer_distance = Inches(0.492)
    section.different_first_page_header_footer = True

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Calibri"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Calibri")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Calibri")
    normal.font.size = Pt(11)
    normal.font.color.rgb = rgb(INK)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.1

    heading_tokens = {
        "Heading 1": (16, BLUE, 16, 8),
        "Heading 2": (13, BLUE, 12, 6),
        "Heading 3": (12, NAVY, 8, 4),
    }
    for style_name, (size, color, before, after) in heading_tokens.items():
        style = styles[style_name]
        style.font.name = "Calibri Light"
        style._element.rPr.rFonts.set(qn("w:ascii"), "Calibri Light")
        style._element.rPr.rFonts.set(qn("w:hAnsi"), "Calibri Light")
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = rgb(color)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True

    for style_name in ("List Bullet", "List Number"):
        style = styles[style_name]
        style.font.name = "Calibri"
        style.font.size = Pt(11)
        style.paragraph_format.left_indent = Inches(0.5)
        style.paragraph_format.first_line_indent = Inches(-0.25)
        style.paragraph_format.space_after = Pt(4)
        style.paragraph_format.line_spacing = 1.1

    caption = styles["Caption"]
    caption.font.name = "Calibri"
    caption.font.size = Pt(8.5)
    caption.font.italic = True
    caption.font.color.rgb = rgb(MUTED)
    caption.paragraph_format.space_before = Pt(3)
    caption.paragraph_format.space_after = Pt(8)
    caption.paragraph_format.keep_with_next = False

    header = section.header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_after = Pt(0)
    set_run_font(p.add_run("NEUROONE  /  BACKEND ARCHITECTURE"), size=8.5, color=MUTED, bold=True)

    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    set_run_font(p.add_run("Internal Project Report   |   "), size=8, color=MUTED)
    add_field(p, "PAGE")


def add_kicker(doc, text: str, *, color=TEAL, align=WD_ALIGN_PARAGRAPH.LEFT, after=5):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(after)
    run = p.add_run(text.upper())
    set_run_font(run, name="Calibri", size=9, color=color, bold=True)
    run.font.all_caps = True
    return p


def add_lead(doc, text: str):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(9)
    set_run_font(p.add_run(text), name="Calibri", size=12, color=NAVY, bold=True)
    return p


def add_body(doc, text: str, *, bold_prefix: str | None = None):
    p = doc.add_paragraph()
    if bold_prefix and text.startswith(bold_prefix):
        set_run_font(p.add_run(bold_prefix), bold=True, color=INK)
        set_run_font(p.add_run(text[len(bold_prefix):]), color=INK)
    else:
        set_run_font(p.add_run(text), color=INK)
    return p


def add_bullets(doc, items: list[str]):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        set_run_font(p.add_run(item), size=11, color=INK)


def add_numbers(doc, items: list[str]):
    for item in items:
        p = doc.add_paragraph(style="List Number")
        set_run_font(p.add_run(item), size=11, color=INK)


def add_callout(doc, label: str, text: str, *, fill=PALE_BLUE, accent=BLUE):
    table = doc.add_table(rows=1, cols=1)
    set_table_geometry(table, [9360])
    table.style = "Table Grid"
    cell = table.cell(0, 0)
    set_cell_shading(cell, fill)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    set_run_font(p.add_run(f"{label}: "), size=10, color=accent, bold=True)
    set_run_font(p.add_run(text), size=10, color=INK)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def add_code(doc, code: str):
    table = doc.add_table(rows=1, cols=1)
    set_table_geometry(table, [9360])
    table.style = "Table Grid"
    cell = table.cell(0, 0)
    set_cell_shading(cell, "F7F9FA")
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    set_run_font(p.add_run(code), name="Consolas", size=8.4, color=NAVY)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def add_figure(doc, image_path: Path, caption: str, *, width=6.45):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.keep_with_next = True
    run = p.add_run()
    shape = run.add_picture(str(image_path), width=Inches(width))
    doc_pr = shape._inline.docPr
    doc_pr.set("descr", caption)
    cp = doc.add_paragraph(caption, style="Caption")
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER


def draw_box(ax, x, y, w, h, title, subtitle="", *, fill=PALE_BLUE, edge=BLUE, title_color=NAVY):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.025",
        linewidth=1.5,
        edgecolor=f"#{edge}",
        facecolor=f"#{fill}",
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h * 0.62, title, ha="center", va="center", fontsize=12, fontweight="bold", color=f"#{title_color}")
    if subtitle:
        ax.text(x + w / 2, y + h * 0.30, subtitle, ha="center", va="center", fontsize=8.5, color=f"#{MUTED}", wrap=True)


def arrow(ax, start, end, *, color=BLUE, style="-|>", lw=1.5):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=13, linewidth=lw, color=f"#{color}"))


def save_layer_diagram(path: Path):
    fig, ax = plt.subplots(figsize=(12, 7), dpi=180)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")
    layers = [
        ("ROUTERS", "HTTP paths and response models", PALE_BLUE, BLUE),
        ("DEPENDENCIES", "Sessions, identity and role gates", "E8F0FA", "4D79A8"),
        ("PYDANTIC SCHEMAS", "Validation and serialization contracts", PALE_TEAL, TEAL),
        ("SERVICES", "Business rules and orchestration", "EAF2E7", GREEN),
        ("REPOSITORIES", "Persistence operations and queries", PALE_GOLD, GOLD),
        ("SQLALCHEMY + POSTGRESQL", "Mapped entities, sessions and physical tables", "F3ECF7", "7A5A96"),
    ]
    y = 5.95
    for index, (title, subtitle, fill, edge) in enumerate(layers):
        draw_box(ax, 2.1, y, 7.8, 0.72, title, subtitle, fill=fill, edge=edge)
        if index < len(layers) - 1:
            arrow(ax, (6, y), (6, y - 0.24), color=MUTED)
        y -= 1.02
    ax.text(10.35, 4.35, "Cross-cutting", fontsize=9, fontweight="bold", color=f"#{MUTED}")
    for yy, label in [(3.85, "Security"), (3.30, "Exceptions"), (2.75, "Configuration")]:
        draw_box(ax, 10.25, yy, 1.45, 0.4, label, fill="F5F7F9", edge=GRID, title_color=MUTED)
    ax.text(6, 6.87, "NeuroONE backend separation of responsibilities", ha="center", fontsize=16, fontweight="bold", color=f"#{NAVY}")
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def save_erd(path: Path):
    fig, ax = plt.subplots(figsize=(13, 7.4), dpi=180)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.4)
    ax.axis("off")

    def entity(x, y, w, title, columns, color):
        row_h = 0.33
        h = 0.58 + len(columns) * row_h
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.035", facecolor="white", edgecolor=f"#{color}", linewidth=1.6))
        ax.add_patch(FancyBboxPatch((x, y + h - 0.58), w, 0.58, boxstyle="round,pad=0.01,rounding_size=0.035", facecolor=f"#{color}", edgecolor=f"#{color}", linewidth=1.2))
        ax.text(x + 0.18, y + h - 0.29, title, va="center", fontsize=12, fontweight="bold", color="white")
        for i, (marker, name, typ) in enumerate(columns):
            yy = y + h - 0.82 - i * row_h
            ax.text(x + 0.16, yy, marker, fontsize=7.5, fontweight="bold", color=f"#{color}", va="center")
            ax.text(x + 0.62, yy, name, fontsize=8.2, color=f"#{INK}", va="center")
            ax.text(x + w - 0.15, yy, typ, fontsize=7.4, color=f"#{MUTED}", ha="right", va="center")
        return h

    users = [
        ("PK", "id", "UUID"), ("UQ", "username", "varchar(50)"), ("UQ", "email", "varchar(255)"),
        ("", "hashed_password", "varchar(255)"), ("", "first_name / last_name", "varchar(100)"),
        ("", "role", "userrole enum"), ("", "is_active / is_verified", "boolean"),
        ("", "created_at / updated_at", "timestamptz"), ("", "is_deleted / deleted_at", "soft delete"),
    ]
    patients = [
        ("PK", "id", "UUID"), ("FK", "doctor_id", "UUID -> users.id"),
        ("", "first_name / last_name", "varchar(20)"), ("", "gender / dob", "char(1) / date"),
        ("UQ", "email", "varchar(20)"), ("", "address", "varchar(100)"),
        ("", "blood_group", "varchar(4)"), ("", "allergies", "varchar[]"),
        ("", "emergency_contact", "varchar(15)"), ("", "audit + soft-delete fields", "inherited"),
    ]
    phones = [("PK", "id", "integer"), ("FK", "patient_id", "UUID -> patients.id"), ("", "phone_number", "varchar(15)")]
    entity(0.35, 1.15, 3.75, "users", users, BLUE)
    entity(4.65, 0.9, 4.05, "patients", patients, TEAL)
    entity(9.35, 2.35, 3.25, "patient_phones", phones, GOLD)
    arrow(ax, (4.1, 3.45), (4.65, 3.45), color=BLUE, style="-")
    ax.text(4.22, 3.67, "1", fontsize=9, fontweight="bold", color=f"#{NAVY}")
    ax.text(4.53, 3.67, "many", fontsize=8, ha="right", color=f"#{NAVY}")
    arrow(ax, (8.7, 3.45), (9.35, 3.45), color=TEAL, style="-")
    ax.text(8.82, 3.67, "1", fontsize=9, fontweight="bold", color=f"#{NAVY}")
    ax.text(9.27, 3.67, "many", fontsize=8, ha="right", color=f"#{NAVY}")
    ax.text(6.5, 7.08, "Implemented PostgreSQL schema", ha="center", fontsize=16, fontweight="bold", color=f"#{NAVY}")
    ax.text(6.5, 6.72, "Three physical tables, two one-to-many relationships", ha="center", fontsize=9.5, color=f"#{MUTED}")
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def save_sqlalchemy_flow(path: Path):
    fig, ax = plt.subplots(figsize=(12, 5.2), dpi=180)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    items = [
        (0.25, "Typed Python model", "Mapped[T]\nmapped_column()", PALE_BLUE, BLUE),
        (2.65, "SQLAlchemy metadata", "tables, columns,\nkeys and indexes", PALE_TEAL, TEAL),
        (5.05, "Alembic", "autogenerate +\nversioned migration", PALE_GOLD, GOLD),
        (7.45, "PostgreSQL", "DDL, enum, array,\nconstraints", "F3ECF7", "7A5A96"),
        (9.85, "Session", "query, flush,\ncommit, refresh", "EAF2E7", GREEN),
    ]
    for idx, (x, title, sub, fill, edge) in enumerate(items):
        draw_box(ax, x, 2.1, 1.9, 1.22, title, sub, fill=fill, edge=edge)
        if idx < len(items) - 1:
            arrow(ax, (x + 1.9, 2.71), (x + 2.38, 2.71), color=MUTED)
    ax.text(6, 4.65, "How Python definitions become persistent database state", ha="center", fontsize=16, fontweight="bold", color=f"#{NAVY}")
    ax.text(6, 1.2, "Runtime path", fontsize=9, fontweight="bold", color=f"#{MUTED}", ha="center")
    arrow(ax, (10.8, 1.7), (8.45, 1.7), color=GREEN, style="<|-|>")
    ax.text(9.6, 1.42, "ORM reads and writes rows", fontsize=8.5, color=f"#{MUTED}", ha="center")
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def save_auth_flow(path: Path):
    fig, ax = plt.subplots(figsize=(12.5, 7), dpi=180)
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 7)
    ax.axis("off")
    ax.text(6.25, 6.62, "Authentication and protected-request lifecycle", ha="center", fontsize=16, fontweight="bold", color=f"#{NAVY}")
    columns = [(1.3, "REGISTER", TEAL), (4.9, "LOGIN", BLUE), (8.5, "PROTECTED REQUEST", GOLD)]
    for x, title, color in columns:
        ax.text(x + 1.35, 6.12, title, ha="center", fontsize=10, fontweight="bold", color=f"#{color}")
    flows = [
        (1.3, [("Validate schema", PALE_TEAL, TEAL), ("Check email + username", PALE_TEAL, TEAL), ("Hash password", PALE_TEAL, TEAL), ("Create user", PALE_TEAL, TEAL)]),
        (4.9, [("Find identity", PALE_BLUE, BLUE), ("Verify password", PALE_BLUE, BLUE), ("Check active", PALE_BLUE, BLUE), ("Issue signed JWT", PALE_BLUE, BLUE)]),
        (8.5, [("Read bearer token", PALE_GOLD, GOLD), ("Decode + validate JWT", PALE_GOLD, GOLD), ("Reload user", PALE_GOLD, GOLD), ("Check active + role", PALE_GOLD, GOLD)]),
    ]
    for x, steps in flows:
        y = 5.25
        for idx, (label, fill, edge) in enumerate(steps):
            draw_box(ax, x, y, 2.7, 0.66, label, fill=fill, edge=edge)
            if idx < len(steps) - 1:
                arrow(ax, (x + 1.35, y), (x + 1.35, y - 0.28), color=MUTED)
            y -= 1.03
    ax.text(6.25, 0.52, "AuthService orchestrates; core/security.py owns cryptographic operations; dependencies.py enforces request access.", ha="center", fontsize=9.2, color=f"#{MUTED}")
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def save_coverage_chart(path: Path):
    labels = ["Infrastructure", "Services", "Schemas", "Repositories", "Models", "API routers"]
    implemented = [6, 4, 4, 3, 4, 0]
    scaffolded = [0, 0, 0, 0, 5, 6]
    fig, ax = plt.subplots(figsize=(10.8, 5.2), dpi=180)
    y = range(len(labels))
    ax.barh(y, implemented, color=f"#{TEAL}", label="Implemented")
    ax.barh(y, scaffolded, left=implemented, color=f"#{GRID}", label="Scaffold / placeholder")
    ax.set_yticks(list(y), labels)
    ax.invert_yaxis()
    ax.set_xlabel("Module or mapped-class count")
    ax.set_title("Current backend implementation footprint", loc="left", fontsize=15, fontweight="bold", color=f"#{NAVY}", pad=14)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="x", alpha=0.18)
    ax.legend(frameon=False, loc="lower right")
    ax.tick_params(colors=f"#{MUTED}")
    for i, (done, todo) in enumerate(zip(implemented, scaffolded)):
        if done:
            ax.text(done - 0.12, i, str(done), ha="right", va="center", color="white", fontweight="bold", fontsize=9)
        if todo:
            ax.text(done + todo - 0.12, i, str(todo), ha="right", va="center", color=f"#{INK}", fontweight="bold", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def add_cover(doc: Document):
    for _ in range(4):
        doc.add_paragraph().paragraph_format.space_after = Pt(0)
    add_kicker(doc, "Technical Architecture Report", color=TEAL, align=WD_ALIGN_PARAGRAPH.CENTER, after=15)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(7)
    set_run_font(p.add_run("NeuroONE"), name="Calibri Light", size=35, color=NAVY, bold=True)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(6)
    set_run_font(p.add_run("Backend Architecture & Database Implementation"), name="Calibri Light", size=20, color=BLUE, bold=True)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(36)
    set_run_font(p.add_run("Models, schemas, repositories, services, security and SQLAlchemy persistence"), size=11.5, color=MUTED, italic=True)

    table = doc.add_table(rows=3, cols=2)
    set_table_geometry(table, [2400, 6960])
    rows = [("Project", "NeuroONE V1"), ("Scope", "Backend implementation as of 03 August 2026"), ("Audience", "Developers, reviewers, maintainers and project stakeholders")]
    for i, (label, value) in enumerate(rows):
        table.cell(i, 0).text = label
        table.cell(i, 1).text = value
        set_cell_shading(table.cell(i, 0), PALE_BLUE)
        for run in table.cell(i, 0).paragraphs[0].runs:
            set_run_font(run, size=9.5, color=NAVY, bold=True)
        for run in table.cell(i, 1).paragraphs[0].runs:
            set_run_font(run, size=9.5, color=INK)
    table.style = "Table Grid"

    doc.add_paragraph().paragraph_format.space_after = Pt(24)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run_font(p.add_run("FASTAPI  /  PYDANTIC  /  SQLALCHEMY  /  POSTGRESQL  /  ALEMBIC"), size=9, color=TEAL, bold=True)
    doc.add_page_break()


def build_report():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix="neuroone_backend_report_") as tmp:
        assets = Path(tmp)
        layer_diagram = assets / "layered_architecture.png"
        erd = assets / "database_erd.png"
        sqlalchemy_flow = assets / "sqlalchemy_flow.png"
        auth_flow = assets / "auth_flow.png"
        coverage = assets / "coverage.png"
        save_layer_diagram(layer_diagram)
        save_erd(erd)
        save_sqlalchemy_flow(sqlalchemy_flow)
        save_auth_flow(auth_flow)
        save_coverage_chart(coverage)

        doc = Document()
        configure_document(doc)
        props = doc.core_properties
        props.title = "NeuroONE Backend Architecture & Database Implementation"
        props.subject = "Technical project report covering the NeuroONE backend"
        props.author = "NeuroONE Engineering"
        props.keywords = "NeuroONE, FastAPI, SQLAlchemy, PostgreSQL, clean architecture"
        props.comments = "Generated from the backend implementation present on 03 August 2026."

        add_cover(doc)

        add_kicker(doc, "Executive orientation")
        doc.add_heading("Executive summary", level=1)
        add_lead(doc, "NeuroONE's backend is organized around a clean, layered flow: validated inputs enter services, services apply application rules, repositories own persistence, and SQLAlchemy maps Python entities to PostgreSQL tables.")
        add_body(doc, "The implemented core currently supports users, patients, patient phone numbers, authentication, JWT-based identity, reusable access-control dependencies and global exception handling. User and patient route files exist but are still placeholders, so the architecture is substantially ahead of the HTTP endpoint implementation.")
        add_callout(doc, "Current database scope", "The active Alembic schema contains three tables: users, patients and patient_phones. Visit, diagnosis, symptom, report and RAG models are design scaffolds only and do not yet create database tables.", fill=PALE_GOLD, accent=GOLD)

        doc.add_heading("Report scope", level=2)
        add_bullets(doc, [
            "Explain what models, schemas, repositories and services do independently.",
            "Show how those layers cooperate during real registration, login and patient-management flows.",
            "Document the implemented PostgreSQL structure, keys, relationships, indexes and soft-delete fields.",
            "Explain how SQLAlchemy sessions, mapped classes and Alembic migrations implement persistence.",
            "Record current limitations and practical next steps without presenting placeholders as completed features.",
        ])

        doc.add_heading("At-a-glance status", level=2)
        add_table(doc, ["Area", "Current state", "What is present"], [
            ["Data model", "Core implemented", "User, Patient, PhoneNumber and shared BaseModel"],
            ["Persistence", "Implemented", "Generic repository plus user/patient query repositories"],
            ["Application logic", "Implemented", "UserService, PatientService and AuthService"],
            ["Security", "Implemented", "bcrypt_sha256, legacy bcrypt verification, JWT encode/decode"],
            ["HTTP infrastructure", "Implemented", "DB dependency, bearer identity, active-user and role gates, handlers"],
            ["Feature routes", "Scaffolded", "Six APIRouter modules currently contain no endpoints"],
            ["Clinical domain", "Scaffolded", "Visit, diagnosis, symptom, report and RAG models contain no mapped fields"],
        ], [1750, 1550, 6060], font_size=8.7)
        add_figure(doc, coverage, "Figure 1. Implemented modules and deliberately scaffolded areas in the current backend.")

        doc.add_page_break()
        add_kicker(doc, "System design")
        doc.add_heading("1. Backend structure and clean architecture", level=1)
        add_body(doc, "The project separates delivery, validation, business logic and persistence. Each layer has a narrow reason to change: routers change with HTTP contracts, schemas with data contracts, services with business rules, repositories with persistence requirements, and models with stored domain state.")
        add_figure(doc, layer_diagram, "Figure 2. Layered backend architecture and cross-cutting infrastructure.")

        doc.add_heading("1.1 Directory map", level=2)
        add_code(doc, """backend/
|-- app/
|   |-- api/          routers and reusable request dependencies
|   |-- core/         configuration, database engine and security helpers
|   |-- models/       SQLAlchemy mapped entities
|   |-- repositories/ database access and feature-specific queries
|   |-- schemas/      Pydantic request/response contracts
|   |-- services/     business rules and orchestration
|   `-- utils/        domain exceptions and HTTP exception handlers
`-- main.py           FastAPI application composition""")

        doc.add_heading("1.2 The layers on their own", level=2)
        add_table(doc, ["Layer", "Owns", "Must not own"], [
            ["Models", "Persistent entities, columns, relationships and database-facing defaults", "Request validation, HTTP status codes or workflow orchestration"],
            ["Schemas", "Input validation, PATCH optionality and safe response serialization", "SQL queries, commits or password hashing"],
            ["Repositories", "CRUD mechanics and SQLAlchemy query construction", "FastAPI behavior or cross-feature business policy"],
            ["Services", "Business decisions, entity construction and multi-step orchestration", "Raw SQL and HTTP response management"],
            ["Dependencies", "Request-scoped sessions, current identity and reusable authorization gates", "Clinical or persistence rules"],
            ["Handlers", "Mapping domain failures to consistent HTTP responses", "Raising service-level business decisions"],
        ], [1450, 3955, 3955], font_size=8.5)

        doc.add_heading("1.3 How the layers work together", level=2)
        add_numbers(doc, [
            "A router accepts an HTTP request and declares a Pydantic request schema.",
            "FastAPI validates the payload before service code runs and resolves dependencies such as the database session and current user.",
            "The service receives validated data, applies application rules and constructs or updates an ORM entity.",
            "The repository performs the SQLAlchemy operation against the provided Session.",
            "SQLAlchemy translates mapped operations into SQL for PostgreSQL and refreshes persisted entities.",
            "The router returns the ORM entity; a response_model can serialize it through a schema configured with from_attributes=True.",
            "If a domain exception is raised, a global handler converts it to a stable HTTP status and JSON error body.",
        ])

        doc.add_page_break()
        add_kicker(doc, "Domain and persistence")
        doc.add_heading("2. SQLAlchemy models", level=1)
        add_lead(doc, "Models are the durable shape of the domain. They tell SQLAlchemy which Python attributes correspond to database columns and how rows relate to one another.")

        doc.add_heading("2.1 Base and shared lifecycle fields", level=2)
        add_body(doc, "Base extends SQLAlchemy's DeclarativeBase and attaches a naming convention to metadata. That convention produces predictable names for indexes, unique constraints, checks, foreign keys and primary keys, which makes Alembic migrations easier to inspect and safer to reverse.")
        add_code(doc, """class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)

class BaseModel(Base):
    __abstract__ = True
    id: Mapped[UUID]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    is_deleted: Mapped[bool]
    deleted_at: Mapped[datetime | None]""")
        add_body(doc, "Every concrete BaseModel subclass inherits a UUID primary key, creation/update timestamps and soft-delete state. server_default=func.now() lets PostgreSQL create timestamps, while onupdate=func.now() refreshes updated_at on mapped updates.")

        doc.add_heading("2.2 User model", level=2)
        add_body(doc, "User represents staff identities. username and email are unique and indexed; hashed_password stores the password verifier, never plaintext. UserRole is a Python string enum exposed to application code and a PostgreSQL enum in the physical schema. is_active controls login/access, while is_verified records a separate verification state.")
        add_bullets(doc, [
            "MVP roles are clinician and admin; PostgreSQL stores enum member names CLINICIAN and ADMIN.",
            "Composite index ix_users_name supports surname/given-name lookup ordering.",
            "The patients relationship is the parent side of the doctor-to-patient association.",
        ])

        doc.add_heading("2.3 Patient and PhoneNumber models", level=2)
        add_body(doc, "Patient contains clinical registration and contact data. doctor_id is a non-null foreign key to users.id. SQLAlchemy relationship(..., back_populates=...) connects both Python objects, so patient.doctor and user.patients represent the same database association from opposite directions.")
        add_body(doc, "Phone numbers are normalized into patient_phones rather than stored as a single text field. The Patient.phone relationship uses cascade='all, delete-orphan', so replacing or removing child objects keeps the child table synchronized with the parent collection.")
        add_callout(doc, "PostgreSQL-specific type", "Patient.allergies uses ARRAY(String). This is convenient and expressive in PostgreSQL, but it couples this mapping and its migration to a database that supports array columns.", fill=PALE_TEAL, accent=TEAL)

        doc.add_heading("2.4 Scaffolded clinical models", level=2)
        add_body(doc, "Visit, Diagnosis, Symptom, Report and Rag classes describe intended future concepts in comments, but their classes currently contain pass and do not define usable table mappings. Several import BaseModel from a top-level base module instead of app.models.base, so they should be corrected before being imported into app.models or Alembic metadata.")
        add_table(doc, ["Scaffold", "Intended relationship", "Implementation status"], [
            ["Visit", "Patient -> visits", "No table name, columns or relationships"],
            ["Diagnosis", "Visit -> diagnosis", "No table name, columns or relationships"],
            ["Symptom", "Visit -> symptoms", "No table name, columns or relationships"],
            ["Report", "Diagnosis -> report", "No table name, columns or relationships"],
            ["Rag", "Report -> RAG sources", "Table name exists, but no mapped feature fields"],
        ], [1500, 3000, 4860], header_fill=PALE_GOLD, font_size=8.7)

        doc.add_page_break()
        add_kicker(doc, "Physical data design")
        doc.add_heading("3. Database structure", level=1)
        add_lead(doc, "The current migration creates a compact relational core: one staff user can own many patients, and one patient can have many phone-number rows.")
        add_figure(doc, erd, "Figure 3. Entity-relationship diagram for the implemented PostgreSQL schema.")

        doc.add_heading("3.1 users table", level=2)
        add_table(doc, ["Column group", "Database type", "Purpose and constraint"], [
            ["id", "UUID", "Primary key generated from uuid.uuid4"],
            ["username", "varchar(50)", "Required, unique and indexed login identity"],
            ["email", "varchar(255)", "Required, unique and indexed identity/contact field"],
            ["hashed_password", "varchar(255)", "Required password hash; excluded from response schemas"],
            ["first_name, last_name", "varchar(100)", "Required personal-name fields; composite name index"],
            ["role", "userrole enum", "Authorization category: CLINICIAN or ADMIN"],
            ["is_active, is_verified", "boolean", "Operational account states"],
            ["created_at, updated_at", "timestamp with time zone", "Server-generated audit timestamps"],
            ["is_deleted, deleted_at", "boolean, timestamp", "Logical deletion state and deletion timestamp"],
        ], [2000, 2250, 5110], font_size=8.3)

        doc.add_heading("3.2 patients table", level=2)
        add_table(doc, ["Column group", "Database type", "Purpose and constraint"], [
            ["id", "UUID", "Primary key inherited from BaseModel"],
            ["doctor_id", "UUID", "Required foreign key to users.id; indexed"],
            ["first_name, last_name", "varchar(20)", "Patient name; last_name may be null"],
            ["gender, dob", "varchar(1), date", "Core demographic fields"],
            ["email", "varchar(20)", "Required, unique and indexed"],
            ["address", "varchar(100)", "Required address text"],
            ["blood_group", "varchar(4)", "Required blood-group label"],
            ["allergies", "varchar[]", "Required PostgreSQL array of allergy strings"],
            ["emergency_contact", "varchar(15)", "Required contact value"],
            ["audit + deletion fields", "inherited", "Same timestamp and soft-delete fields as users"],
        ], [2000, 2250, 5110], font_size=8.3)

        doc.add_heading("3.3 patient_phones table", level=2)
        add_table(doc, ["Column", "Database type", "Purpose and constraint"], [
            ["id", "integer", "Primary key"],
            ["patient_id", "UUID", "Required foreign key to patients.id"],
            ["phone_number", "varchar(15)", "One normalized phone number; currently not unique"],
        ], [2000, 2250, 5110], font_size=8.5)

        doc.add_heading("3.4 Indexing strategy", level=2)
        add_bullets(doc, [
            "Unique indexes on users.username, users.email and patients.email enforce identity uniqueness at the database boundary.",
            "ix_users_name(last_name, first_name) supports ordered or filtered staff-name access patterns.",
            "ix_patients_doctor_name(doctor_id, first_name, last_name) supports listing and searching a doctor's patients.",
            "The standalone patients.doctor_id index supports foreign-key filtering and joins.",
        ])

        doc.add_page_break()
        add_kicker(doc, "ORM mechanics")
        doc.add_heading("4. How SQLAlchemy implements the database", level=1)
        add_figure(doc, sqlalchemy_flow, "Figure 4. Build-time and runtime path from typed model declarations to PostgreSQL state.")

        doc.add_heading("4.1 Declarative mapping", level=2)
        add_body(doc, "SQLAlchemy 2.0 typed mappings combine Mapped[T] annotations with mapped_column(). The type annotation informs both Python tooling and SQLAlchemy, while mapped_column supplies database behavior such as length, nullability, uniqueness, indexes, foreign keys and defaults.")
        add_code(doc, """doctor_id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("users.id"),
    nullable=False,
    index=True,
)""")

        doc.add_heading("4.2 Engine and sessions", level=2)
        add_body(doc, "core/database.py creates an Engine from DATABASE_URL and a SessionLocal factory with autocommit=False and autoflush=False. api/dependencies.py opens one Session per request, yields it to FastAPI and guarantees close() in a finally block.")
        add_body(doc, "Repositories receive the Session instead of creating one. This makes the request boundary responsible for resource lifetime and lets services/repositories participate in the same unit of work.")

        doc.add_heading("4.3 Repository transaction behavior", level=2)
        add_body(doc, "The current BaseRepository calls commit() in create, update and soft_delete, then refreshes created/updated objects. This works for one-operation methods, but it prevents a future service from atomically combining multiple repository operations under one commit.")
        add_callout(doc, "Recommended evolution", "Move commit/rollback ownership to the service or a unit-of-work boundary; let repositories add, flush and query. That allows patient creation plus audit logging to succeed or fail as one transaction.", fill=PALE_GOLD, accent=GOLD)

        doc.add_heading("4.4 Alembic migrations", level=2)
        add_body(doc, "alembic/env.py points target_metadata to Base.metadata and imports registered models, enabling Alembic autogeneration. The initial migration f1f7379b0c32 creates users, patients, patient_phones, their enum, keys and indexes. The following migration c1d5012eb1cd is an empty revision and performs no schema changes.")
        add_bullets(doc, [
            "upgrade() applies schema changes in revision order.",
            "downgrade() reverses the initial migration by dropping child tables and indexes before parent tables.",
            "Naming conventions produce deterministic constraint names such as pk_users and fk_patients_doctor_id_users.",
        ])

        doc.add_page_break()
        add_kicker(doc, "Data contracts")
        doc.add_heading("5. Pydantic schemas", level=1)
        add_lead(doc, "Schemas are the application's boundary contracts. They validate untrusted request data and control which fields leave the API, without becoming database entities themselves.")

        doc.add_heading("5.1 User schemas", level=2)
        add_table(doc, ["Schema", "Purpose", "Notable behavior"], [
            ["UserBase", "Shared identity/profile fields", "Validates names, username and EmailStr"],
            ["UserCreate", "Registration input", "Adds plaintext password; password never becomes an ORM response field"],
            ["UserUpdate", "Partial profile/admin update", "All fields optional; includes role and account-state fields"],
            ["UserResponse", "Public serialized user", "from_attributes=True; excludes hashed_password and password"],
        ], [1750, 2800, 4810], font_size=8.7)

        doc.add_heading("5.2 Patient schemas", level=2)
        add_body(doc, "PatientBase validates demographics, contact information, blood group, allergies and a non-empty list of phone schemas. PatientCreate adds doctor_id. PatientUpdate makes fields optional for PATCH behavior, and PatientResponse adds identifiers, timestamps and the related doctor response.")
        add_callout(doc, "Nested mapping", "Pydantic phone objects cannot be assigned as dictionaries to a SQLAlchemy relationship. PatientService explicitly converts each schema PhoneNumber into an ORM PhoneNumber instance.", fill=PALE_TEAL, accent=TEAL)

        doc.add_heading("5.3 Authentication and common schemas", level=2)
        add_table(doc, ["Schema", "Key fields", "Use"], [
            ["LoginRequest", "username, password", "Credential input; should later align with the service's username_or_email naming"],
            ["Token", "access_token, token_type", "Bearer token response"],
            ["TokenPayload", "sub, username, role, exp", "Validated JWT claims"],
            ["PaginationParams", "page, page_size", "Normalized offset/limit calculation"],
            ["PaginatedResponse[T]", "items, total, page, page_size, pages", "Generic collection response"],
        ], [1750, 2600, 5010], font_size=8.6)

        doc.add_heading("5.4 PATCH semantics", level=2)
        add_body(doc, "model_dump(exclude_unset=True) is central to partial updates. It includes only fields the caller actually supplied, so omitted fields remain unchanged. This differs from exclude_none=True: an explicitly supplied null is still a deliberate value unless separately prohibited by business rules.")
        add_code(doc, """update_data = user_data.model_dump(
    exclude_unset=True,
    exclude={"password"},
)

for field, value in update_data.items():
    setattr(user, field, value)""")

        doc.add_page_break()
        add_kicker(doc, "Persistence boundary")
        doc.add_heading("6. Repositories", level=1)
        add_lead(doc, "Repositories isolate SQLAlchemy query construction and persistence mechanics from business logic. Services ask for domain-relevant operations instead of building database statements.")

        doc.add_heading("6.1 BaseRepository", level=2)
        add_table(doc, ["Method", "Behavior", "Current transaction effect"], [
            ["create", "add entity, persist and refresh", "Commits"],
            ["get_by_id", "retrieve first row matching UUID", "Read only"],
            ["get_or_404", "retrieve or raise shared EntityNotFoundError", "Read only"],
            ["get_all", "return all mapped rows", "Read only"],
            ["update", "persist in-memory entity changes and refresh", "Commits"],
            ["soft_delete", "call entity.soft_delete()", "Commits"],
            ["exists", "SQL EXISTS check by UUID", "Read only"],
        ], [1700, 4650, 3010], font_size=8.6)

        doc.add_heading("6.2 UserRepository", level=2)
        add_bullets(doc, [
            "get_by_email and get_by_username use SQLAlchemy select() and exclude soft-deleted users.",
            "exists_email and exists_username answer uniqueness questions using query/filter access.",
            "get_active_users filters both is_deleted=False and is_active=True, then applies offset/limit pagination.",
        ])

        doc.add_heading("6.3 PatientRepository", level=2)
        add_bullets(doc, [
            "get_by_doctor returns active patients assigned through doctor_id.",
            "search applies case-insensitive matching across first name, last name, email and related phone numbers.",
            "get_by_phone uses relationship any() to query the patient_phones collection.",
            "get_by_email and get_active_patients exclude logically deleted rows and support focused access patterns.",
        ])

        add_callout(doc, "Implementation discrepancy", "BaseRepository.get_by_id() and get_all() currently do not filter is_deleted, despite their docstrings describing active-only behavior; get_all() also ignores its skip/limit parameters. Specialized repositories perform the active filtering correctly. This should be standardized before routes rely on generic listing.", fill=PALE_RED, accent=RED)

        doc.add_page_break()
        add_kicker(doc, "Application rules")
        doc.add_heading("7. Services", level=1)
        add_lead(doc, "Services translate validated use-case input into domain actions. They depend on repositories through constructor injection, making business behavior easier to unit test with mock repositories.")

        doc.add_heading("7.1 BaseService", level=2)
        add_body(doc, "BaseService is a generic holder for an injected repository. It contains no persistence or HTTP behavior; its purpose is consistent dependency storage and typing across feature services.")

        doc.add_heading("7.2 UserService", level=2)
        add_body(doc, "UserService manages users without performing authentication. It creates ORM users from UserCreate, but requires a keyword-only hashed_password supplied by AuthService. This prevents accidental plaintext persistence while preserving the separation between user management and cryptography.")
        add_table(doc, ["Operation", "Service responsibility"], [
            ["create_user", "Exclude plaintext password, construct User with supplied hash, delegate create"],
            ["get/list", "Delegate identity or collection retrieval"],
            ["update_user", "Fetch, apply only supplied non-password fields, delegate update"],
            ["delete_user", "Fetch, delegate soft deletion and return success boolean"],
            ["email/username lookup", "Wrap repository identity queries for AuthService"],
        ], [2150, 7210], header_fill=PALE_TEAL, font_size=8.8)

        doc.add_heading("7.3 PatientService", level=2)
        add_body(doc, "PatientService creates patients, retrieves and lists them, applies PATCH updates, soft-deletes them and lists patients by doctor. Its most important mapping rule is conversion of nested phone schemas into ORM PhoneNumber children.")
        add_code(doc, """patient = Patient(
    **patient_data.model_dump(exclude={"phone"}),
    phone=[PhoneNumber(**phone.model_dump())
           for phone in patient_data.phone],
)""")
        add_body(doc, "On phone updates, the service replaces the relationship collection only when phone was explicitly supplied. SQLAlchemy's delete-orphan cascade then synchronizes removed child rows.")

        doc.add_heading("7.4 AuthService", level=2)
        add_body(doc, "AuthService depends on UserService, not UserRepository. Registration checks uniqueness, hashes the password through core/security.py and calls UserService.create_user. Login resolves username or email, verifies the password, rejects inactive accounts and creates a signed JWT.")
        add_figure(doc, auth_flow, "Figure 5. Registration, login and protected-request authentication paths.")

        doc.add_heading("7.5 Security helpers", level=2)
        add_bullets(doc, [
            "New passwords use passlib's bcrypt_sha256 scheme; legacy bcrypt hashes remain verifiable.",
            "JWT claims include user UUID in sub, username, lowercase role value and an expiration timestamp.",
            "decode_access_token verifies the signature, configured algorithm and expiration through python-jose.",
            "Malformed or expired tokens become AuthenticationError rather than leaking library exceptions.",
        ])

        doc.add_page_break()
        add_kicker(doc, "HTTP boundary")
        doc.add_heading("8. FastAPI dependencies and global errors", level=1)

        doc.add_heading("8.1 Request-scoped dependencies", level=2)
        add_table(doc, ["Dependency", "Responsibility", "Returns"], [
            ["get_db", "Open SessionLocal and close it in finally", "SQLAlchemy Session"],
            ["get_user_service", "Provide configured UserService", "UserService"],
            ["get_auth_service", "Construct AuthService from injected UserService", "AuthService"],
            ["get_current_user", "Read bearer token, validate claims, reload non-deleted user", "User ORM model"],
            ["get_current_active_user", "Reject inactive authenticated accounts", "Active User"],
            ["require_roles", "Generate a reusable role-check dependency", "Authorized User"],
            ["get_current_admin/doctor", "Preconfigured role-specific dependencies", "Authorized User"],
        ], [2150, 4810, 2400], font_size=8.4)

        add_code(doc, """@router.get("/patients")
def list_patients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_clinician),
):
    ...""")

        doc.add_heading("8.2 Domain exceptions", level=2)
        add_body(doc, "Services and repositories raise application-specific exceptions without importing FastAPI. This keeps business logic reusable outside HTTP and makes error semantics testable.")
        add_table(doc, ["Domain exception", "HTTP mapping", "Meaning"], [
            ["EntityNotFoundError", "404 Not Found", "Requested entity is absent"],
            ["UserAlreadyExistsError", "409 Conflict", "Email or username conflicts"],
            ["AuthenticationError", "401 Unauthorized", "Identity is missing, invalid, expired or inactive"],
            ["InvalidCredentialsError", "401 Unauthorized", "Login credentials are invalid"],
            ["AuthorizationError", "403 Forbidden", "Authenticated identity lacks the required role"],
            ["Request/Pydantic ValidationError", "422 Unprocessable Entity", "Input does not satisfy schema rules"],
        ], [2500, 2250, 4610], header_fill=PALE_GOLD, font_size=8.5)
        add_body(doc, "register_exception_handlers(app) is called during application composition. Authentication responses include WWW-Authenticate: Bearer, while validation responses serialize detailed field errors under a consistent detail key.")

        doc.add_heading("8.3 Application composition", level=2)
        add_body(doc, "main.py creates FastAPI, registers exception handlers and mounts api_router under /api/v1. The router currently mounts auth, patients, visits, diagnosis, RAG and reports subrouters. Root and database health endpoints are the only implemented HTTP operations at present.")

        doc.add_page_break()
        add_kicker(doc, "End-to-end behavior")
        doc.add_heading("9. Representative workflows", level=1)

        doc.add_heading("9.1 Register a user", level=2)
        add_numbers(doc, [
            "FastAPI validates names, username, email and password into UserCreate.",
            "AuthService asks UserService whether the email and username already exist.",
            "core/security.py hashes the plaintext password with bcrypt_sha256.",
            "UserService removes password from the schema dump, adds hashed_password and creates a User ORM entity.",
            "UserRepository/BaseRepository adds, commits and refreshes the entity.",
            "AuthService returns UserResponse, which excludes all password material.",
        ])

        doc.add_heading("9.2 Login and access a protected endpoint", level=2)
        add_numbers(doc, [
            "AuthService chooses email or username lookup based on the supplied identity.",
            "The stored password hash is verified and inactive accounts are rejected with the same generic credentials error.",
            "A JWT is signed with sub, username, role and exp claims.",
            "OAuth2PasswordBearer extracts the token from a later Authorization: Bearer header.",
            "get_current_user validates the JWT and reloads the user from the database, preventing deleted accounts from relying only on old claims.",
            "get_current_active_user and require_roles enforce account and authorization state before the router runs.",
        ])

        doc.add_heading("9.3 Create and update a patient", level=2)
        add_numbers(doc, [
            "PatientCreate validates doctor_id, demographic/contact fields and at least one structured phone number.",
            "PatientService separates the phone list from scalar data, builds PhoneNumber child entities and constructs Patient.",
            "The repository persists the parent and children; the ORM relationship supplies patient_id to child rows.",
            "For PATCH, PatientUpdate records which fields were actually supplied.",
            "PatientService updates those attributes and replaces the phone collection only when phone appears in model_fields_set.",
            "The repository commits and refreshes the updated patient.",
        ])

        doc.add_heading("9.4 Soft deletion", level=2)
        add_body(doc, "Deletion does not issue SQL DELETE for BaseModel entities. The model's soft_delete() method sets is_deleted=True and the repository commits it. Specialized active queries filter out those rows, preserving history and foreign-key continuity.")
        add_callout(doc, "Important limitation", "soft_delete() does not currently assign deleted_at. Generic get_by_id/get_all also do not consistently hide deleted rows. Both behaviors should be corrected together so the logical-deletion contract is reliable.", fill=PALE_RED, accent=RED)

        doc.add_page_break()
        add_kicker(doc, "Engineering assessment")
        doc.add_heading("10. Strengths, gaps and recommended roadmap", level=1)

        doc.add_heading("10.1 Architectural strengths", level=2)
        add_bullets(doc, [
            "Clear separation among validation, business logic, persistence and HTTP delivery.",
            "Constructor injection for repositories and service-to-service orchestration improves unit-testability.",
            "Typed SQLAlchemy 2.0 mappings and Pydantic v2 schemas provide strong editor/runtime contracts.",
            "Central password/JWT utilities keep cryptography out of use-case services.",
            "Request dependencies centralize session lifetime, identity freshness, active-account checks and roles.",
            "Global exception handlers keep domain services independent of HTTP status codes.",
            "Normalized phone numbers and explicit ORM relationships establish a sound relational foundation.",
        ])

        doc.add_heading("10.2 Current implementation gaps", level=2)
        add_table(doc, ["Priority", "Gap", "Why it matters"], [
            ["High", "Feature routers contain no endpoints", "Implemented services are not yet accessible through the API"],
            ["High", "No automated tests in backend/tests", "Security and persistence regressions have no repeatable safety net"],
            ["High", "Generic repository ignores soft-delete and pagination contract", "Deleted records may reappear and list behavior is misleading"],
            ["High", "Repository-level commits", "Multi-write service workflows cannot be atomic"],
            ["Medium", "Clinical models are placeholders", "Visits, diagnoses, symptoms, reports and RAG cannot persist"],
            ["Medium", "deleted_at is never assigned", "Deletion timing cannot be audited"],
            ["Medium", "LoginRequest naming differs from login service", "Future auth route needs an explicit username-or-email contract"],
            ["Low", "Engine echo=True", "Production logs may be noisy and expose query details"],
            ["Low", "Health failure still returns a normal JSON response", "Monitoring may interpret a database failure as HTTP success"],
        ], [900, 3440, 5020], header_fill=PALE_RED, font_size=8.2)

        doc.add_heading("10.3 Recommended delivery sequence", level=2)
        add_numbers(doc, [
            "Add focused unit tests for AuthService, UserService, PatientService and repository filters using injected mocks and a test database.",
            "Maintain public login, authenticated identity, and ADMIN-only user-provisioning routes.",
            "Implement user/patient routes with response models, pagination and doctor/admin access rules.",
            "Correct generic soft-delete filtering, set deleted_at, and align get_all with skip/limit.",
            "Move transaction control to services or introduce a unit-of-work abstraction with rollback behavior.",
            "Complete each clinical model one bounded feature at a time, including schema, migration, repository, service, route and tests.",
            "Add audit logging and database integrity rules for workflows involving sensitive clinical information.",
            "Harden production configuration: disable SQL echo, return meaningful health status codes and manage secrets outside source control.",
        ])

        doc.add_heading("10.4 Definition of done for the next feature", level=2)
        add_bullets(doc, [
            "Mapped entity and reviewed Alembic migration.",
            "Create/update/response schemas with field-level validation.",
            "Repository queries that consistently exclude soft-deleted rows.",
            "Service business rules with explicit transaction behavior.",
            "Protected routes with response models and role dependencies.",
            "Domain exceptions mapped through the global handler registry.",
            "Unit, integration and authorization tests covering success and failure paths.",
        ])

        doc.add_page_break()
        add_kicker(doc, "Reference")
        doc.add_heading("Appendix A. Responsibility matrix", level=1)
        add_table(doc, ["Concern", "Primary owner", "Collaborators"], [
            ["Stored state and relationships", "SQLAlchemy models", "Alembic migrations, PostgreSQL"],
            ["Request validation", "Pydantic schemas", "FastAPI router"],
            ["Entity serialization", "Response schemas", "Router response_model"],
            ["Query construction", "Repositories", "SQLAlchemy Session"],
            ["Business decisions", "Services", "Schemas and repositories"],
            ["Password and JWT primitives", "core/security.py", "AuthService"],
            ["Current identity and roles", "api/dependencies.py", "AuthService, UserService"],
            ["HTTP error translation", "utils/handlers.py", "Domain exceptions"],
            ["Application composition", "main.py and api/router.py", "All route modules"],
        ], [2780, 3060, 3520], font_size=8.6)

        doc.add_heading("Appendix B. Key implementation files", level=1)
        add_table(doc, ["Path", "Role"], [
            ["app/models/base.py", "Declarative base, naming conventions and shared lifecycle fields"],
            ["app/models/user.py", "Staff identity and authorization mapping"],
            ["app/models/patient.py", "Patient and normalized phone mappings"],
            ["app/schemas/*.py", "Pydantic request, response, token and pagination contracts"],
            ["app/repositories/base_repository.py", "Generic CRUD persistence"],
            ["app/repositories/user_repository.py", "User identity and active-account queries"],
            ["app/repositories/patient_repository.py", "Patient search, doctor, email and phone queries"],
            ["app/services/user_service.py", "User-management orchestration"],
            ["app/services/patient_service.py", "Patient-management and nested-phone mapping"],
            ["app/services/auth_service.py", "Registration, login and token orchestration"],
            ["app/core/security.py", "Password hashing/verification and JWT primitives"],
            ["app/api/dependencies.py", "Sessions, identity freshness and role gates"],
            ["app/utils/exceptions.py", "Framework-independent domain failures"],
            ["app/utils/handlers.py", "Global HTTP exception mappings"],
            ["alembic/versions/f1f7379b0c32_initial_schema.py", "Implemented physical schema migration"],
        ], [3900, 5460], font_size=8.2)

        doc.add_heading("Appendix C. Glossary", level=1)
        add_table(doc, ["Term", "Meaning in NeuroONE"], [
            ["ORM", "Object-relational mapper translating Python entity operations to relational SQL"],
            ["Mapped entity", "A Python class whose attributes correspond to database columns/relationships"],
            ["Schema", "A Pydantic validation or serialization contract, not a database table"],
            ["Repository", "Persistence adapter that owns SQLAlchemy queries and CRUD mechanics"],
            ["Service", "Use-case layer that applies rules and coordinates repositories/services"],
            ["Dependency", "FastAPI-resolved reusable function for sessions, identity or authorization"],
            ["Soft delete", "Marking a row deleted without physically removing it"],
            ["JWT", "Signed token carrying identity/role claims and an expiration time"],
            ["Alembic revision", "Versioned, ordered database schema change"],
            ["Unit of work", "Transaction boundary that commits or rolls back a group of operations together"],
        ], [2350, 7010], font_size=8.5)

        add_callout(doc, "Report basis", "This document reflects the source present in backend/app and backend/alembic on 03 August 2026. It describes implemented behavior separately from commented plans and placeholder modules.", fill=LIGHT, accent=MUTED)

        settings = doc.settings._element
        update_fields = settings.find(qn("w:updateFields"))
        if update_fields is None:
            update_fields = OxmlElement("w:updateFields")
            settings.append(update_fields)
        update_fields.set(qn("w:val"), "true")
        doc.save(OUTPUT)
        print(OUTPUT)


if __name__ == "__main__":
    build_report()
