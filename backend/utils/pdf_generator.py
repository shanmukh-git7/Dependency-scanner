from fpdf import FPDF
import json
from datetime import datetime
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Dependency Vulnerability Scan Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_scan_pdf(scan_data, user_name):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Report Meta
    pdf.cell(200, 10, txt=f"Generated for: {user_name}", ln=True)
    pdf.cell(200, 10, txt=f"Scan Date: {scan_data.scan_date.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(200, 10, txt=f"Filename: {scan_data.filename}", ln=True)
    
    pdf.ln(10)
    
    # Summary
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Summary:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Total Dependencies: {scan_data.total_dependencies}", ln=True)
    pdf.cell(200, 10, txt=f"Vulnerabilities Found: {scan_data.vulnerabilities_count}", ln=True)
    
    pdf.ln(10)

    # Details
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Vulnerability Details:", ln=True)
    pdf.set_font("Arial", size=10)
    
    try:
        details = json.loads(scan_data.details)
        if not details:
            pdf.cell(200, 10, txt="No vulnerabilities detected.", ln=True)
        else:
            for vuln in details:
                pdf.set_text_color(255, 0, 0)
                pdf.cell(200, 10, txt=f"[{vuln.get('severity', 'HIGH')}] {vuln.get('artifact_id', 'Unknown')} - {vuln.get('type', 'Unknown Type')}", ln=True)
                pdf.set_text_color(0, 0, 0)
                pdf.multi_cell(0, 10, txt=f"Description: {vuln.get('description', 'No description available')}")
                pdf.ln(5)
    except json.JSONDecodeError:
         pdf.cell(200, 10, txt="Error parsing vulnerability details.", ln=True)

    # Ensure reports directory exists
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        
    filename = f"reports/scan_report_{scan_data.id}.pdf"
    pdf.output(filename)
    return filename
