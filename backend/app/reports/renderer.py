"""Render a ReportSnapshot into a complete clinical report PDF (ADR-004).

A pure function of its input: no database session, no authorization, no I/O
beyond returning bytes. Mirrors how ``app/ai/`` stays database-free -- the
caller (``ReportService``) decides what to do with a rendering failure and
whether anything gets persisted.
"""

from datetime import timezone
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from app.schemas.report import ReportFindingSnapshot, ReportSnapshot


_STYLES = getSampleStyleSheet()

_TITLE = ParagraphStyle("ReportTitle", parent=_STYLES["Title"], fontSize=18)
_HEADING = ParagraphStyle(
    "ReportHeading", parent=_STYLES["Heading2"], spaceBefore=14, spaceAfter=6
)
_SUBHEADING = ParagraphStyle(
    "ReportSubheading", parent=_STYLES["Heading3"], spaceBefore=10, spaceAfter=2
)
_BODY = _STYLES["BodyText"]
_ITALIC = _STYLES["Italic"]
_NOTE = ParagraphStyle(
    "PipelineNote", parent=_STYLES["Italic"], textColor=colors.HexColor("#555555")
)
_DISCLAIMER = ParagraphStyle(
    "Disclaimer",
    parent=_STYLES["BodyText"],
    textColor=colors.HexColor("#7a1f1f"),
    borderColor=colors.HexColor("#7a1f1f"),
    borderWidth=0.5,
    borderPadding=6,
    backColor=colors.HexColor("#fbeaea"),
)
_FOOTER_FONT_SIZE = 7


def _safe(text: str | None) -> str:
    """Escape Platypus markup and fall back for characters base14 can't render.

    ADR-004 assumes bundled/base fonts, not an embedded Unicode font, so a
    character outside latin-1 is replaced rather than left to crash rendering.
    """

    if not text:
        return ""
    return escape(text).encode("latin-1", errors="replace").decode("latin-1")


def _p(text: str, style: ParagraphStyle = _BODY) -> Paragraph:
    return Paragraph(_safe(text), style)


def _finding_label(finding: ReportFindingSnapshot) -> str:
    category = "Early Watch" if finding.category == "early_watch" else "Differential"
    return f"{finding.rank + 1}. {finding.condition_name} -- {category}, {finding.likelihood_band} likelihood"


def _render_finding(story: list, finding: ReportFindingSnapshot) -> None:
    story.append(_p(_finding_label(finding), _SUBHEADING))
    story.append(_p(finding.explanation))

    if finding.supporting_findings:
        story.append(_p("Supporting: " + "; ".join(finding.supporting_findings)))
    if finding.contradicting_findings:
        story.append(_p("Contradicting: " + "; ".join(finding.contradicting_findings)))

    if finding.trend_basis:
        # Kept visually distinct from evidence[]: this traces the patient's
        # OWN history, never external literature (AGENTS.md section 8.2).
        story.append(_p("Patient history trend (own prior visits):", _ITALIC))
        for reference in finding.trend_basis:
            text = reference.get("observation") or str(reference)
            story.append(_p(f"- {text}", _ITALIC))

    story.append(_p("Evidence:"))
    for evidence in finding.evidence:
        citation = evidence.citation
        if evidence.source_tier:
            citation += f" [{evidence.source_tier}]"
        if evidence.published_year:
            citation += f", {evidence.published_year}"
        story.append(_p(f"- {evidence.source}: {citation}"))
        story.append(_p(evidence.relevant_passage, _ITALIC))

    story.append(Spacer(1, 10))


def _build_story(snapshot: ReportSnapshot) -> list:
    story: list = [
        _p("NeuroONE Clinical Report", _TITLE),
        _p(
            "Generated "
            f"{snapshot.generated_at.astimezone(timezone.utc):%Y-%m-%d %H:%M} UTC"
        ),
        Spacer(1, 8),
        Paragraph(_safe(snapshot.disclaimer), _DISCLAIMER),
        Spacer(1, 10),
    ]

    if snapshot.provider_mode == "simulated":
        story.append(_p(f"Note: {snapshot.pipeline_note}", _NOTE))
        story.append(Spacer(1, 10))

    story.append(_p("Patient", _HEADING))
    story.append(_p(f"Name: {snapshot.patient.full_name}"))
    if snapshot.patient.age_years is not None:
        story.append(_p(f"Age: {snapshot.patient.age_years}"))
    if snapshot.patient.gender:
        story.append(_p(f"Gender: {snapshot.patient.gender}"))

    story.append(_p("Clinical Case", _HEADING))
    story.append(_p(f"Visit date: {snapshot.visit.visit_date:%Y-%m-%d}"))
    story.append(_p(f"Chief complaint: {snapshot.visit.chief_complaint}"))
    if snapshot.visit.history:
        story.append(_p(f"Relevant history: {snapshot.visit.history}"))
    if snapshot.visit.notes:
        story.append(_p(f"Additional notes: {snapshot.visit.notes}"))

    story.append(_p("Reported Symptoms", _SUBHEADING))
    for symptom in snapshot.visit.symptoms:
        line = f"{symptom.symptom_name} -- severity {symptom.severity}/10"
        if symptom.duration_days is not None:
            line += f", {symptom.duration_days} day(s)"
        if symptom.onset:
            line += f", onset: {symptom.onset}"
        story.append(_p(line))
        if symptom.observation:
            story.append(_p(f"Observation: {symptom.observation}", _ITALIC))

    story.append(_p("Differential Diagnosis and Evidence", _HEADING))
    for finding in snapshot.findings:
        _render_finding(story, finding)

    story.append(Spacer(1, 8))
    story.append(_p("Disclaimer", _HEADING))
    story.append(Paragraph(_safe(snapshot.disclaimer), _DISCLAIMER))

    return story


def _draw_footer(canvas, doc, disclaimer: str) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", _FOOTER_FONT_SIZE)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawCentredString(
        doc.pagesize[0] / 2, 15 * mm, _safe(disclaimer)[:150]
    )
    canvas.drawCentredString(doc.pagesize[0] / 2, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def render(snapshot: ReportSnapshot) -> bytes:
    """Render a complete, multi-page clinical report PDF.

    Raises whatever ReportLab raises on an unrenderable layout. The caller
    treats any exception here as a report-generation failure: render happens
    before persistence (ADR-004), so nothing is ever half-saved.
    """

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        title="NeuroONE Clinical Report",
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=22 * mm,
    )

    def _on_page(canvas, doc_) -> None:
        _draw_footer(canvas, doc_, snapshot.disclaimer)

    doc.build(_build_story(snapshot), onFirstPage=_on_page, onLaterPages=_on_page)
    return buffer.getvalue()


__all__ = ["render"]
