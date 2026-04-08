from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

import os
from datetime import datetime


def generate_pdf_report(scan_data, username):
    filename = f"report_{username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join("reports", filename)

    os.makedirs("reports", exist_ok=True)

    doc = SimpleDocTemplate(filepath, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    elements.append(Paragraph("Dependency Vulnerability Scan Report", styles["Title"]))
    elements.append(Spacer(1, 0.5 * inch))

    elements.append(Paragraph(f"User: {username}", styles["Normal"]))
    elements.append(Paragraph(f"Scan Date: {datetime.now()}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(f"Total Dependencies: {scan_data['total_dependencies']}", styles["Normal"]))
    elements.append(Paragraph(f"Vulnerabilities Found: {scan_data['vulnerabilities_found']}", styles["Normal"]))
    elements.append(Spacer(1, 0.5 * inch))

    if scan_data["vulnerabilities"]:
        elements.append(Paragraph("Vulnerability Details:", styles["Heading2"]))
        elements.append(Spacer(1, 0.3 * inch))

        vuln_list = []
        for vuln in scan_data["vulnerabilities"]:
            text = f"{vuln.get('dependency')} - {vuln.get('cve')} - Severity: {vuln.get('severity')}"
            vuln_list.append(ListItem(Paragraph(text, styles["Normal"])))

        elements.append(ListFlowable(vuln_list, bulletType="bullet"))

    doc.build(elements)

    return filepath
