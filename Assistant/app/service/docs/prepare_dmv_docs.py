
async def prepare_dmv_doc(doc: dict) -> str:
    """Prepare DMV document"""
    return 'document_path'

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from app.utils.logging import logger

async def generate_contract_pdf(data, file_path='customer_contract.pdf'):
    # Create a PDF document
    try:
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        elements = []

        # Styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        normal_style = styles['Normal']

        # Add title
        elements.append(Paragraph("Customer Contract", title_style))
        elements.append(Spacer(1, 0.5 * inch))

        # Customer Details
        elements.append(Paragraph(f"Full Name: {data['full_name']}", normal_style))
        elements.append(Paragraph(f"Contact: {data['phone_or_address']}", normal_style))
        elements.append(Paragraph(f"SSN: {data['ssn']}", normal_style))
        elements.append(Spacer(1, 0.2 * inch))

        # Policy Information
        elements.append(Paragraph("Policy Information:", styles['Heading2']))
        elements.append(Paragraph(f"Policy No: {data['policy']['policy_no']}", normal_style))
        elements.append(Paragraph(f"Provider: {data['policy']['provider']}", normal_style))
        elements.append(Paragraph(f"Effective Date: {data['policy']['effective_date']}", normal_style))
        elements.append(Paragraph(f"Expiry Date: {data['policy']['expiry_date']}", normal_style))
        elements.append(Spacer(1, 0.2 * inch))

        # Vehicle Information
        elements.append(Paragraph("Vehicle Information:", styles['Heading2']))
        elements.append(Paragraph(f"VIN: {data['vehicle']['vin']}", normal_style))
        elements.append(Paragraph(f"Trim: {data['vehicle']['trim']}", normal_style))
        elements.append(Paragraph(f"Miles: {data['vehicle']['miles']}", normal_style))
        elements.append(Paragraph(f"Color: {data['vehicle']['color']}", normal_style))
        elements.append(Spacer(1, 0.2 * inch))

        # Trade Vehicle Information
        elements.append(Paragraph("Trade Vehicle Information:", styles['Heading2']))
        elements.append(Paragraph(f"VIN: {data['trade_vehicle']['vin']}", normal_style))
        elements.append(Paragraph(f"Trim: {data['trade_vehicle']['trim']}", normal_style))
        elements.append(Paragraph(f"Miles: {data['trade_vehicle']['miles']}", normal_style))
        elements.append(Paragraph(f"Color: {data['trade_vehicle']['color']}", normal_style))
        elements.append(Spacer(1, 0.2 * inch))

        # Financial Information
        elements.append(Paragraph("Financial Information:", styles['Heading2']))
        elements.append(Paragraph(f"Sale Price: {data['sale_price']}", normal_style))
        elements.append(Paragraph(f"Rebate: {data['rebate']}", normal_style))
        elements.append(Paragraph(f"Dealer Fees: {data['dealer_fees']}", normal_style))
        elements.append(Paragraph(f"Trade Value: {data['trade_value']}", normal_style))
        elements.append(Paragraph(f"Trade Payoff: {data['trade_payoff']}", normal_style))
        elements.append(Paragraph(f"Tax Rate: {data['tax_rate'] * 100}%", normal_style))
        elements.append(Spacer(1, 0.2 * inch))

        # Customer Residential Information
        elements.append(Paragraph("Customer Residential Information:", styles['Heading2']))
        elements.append(Paragraph(f"Duration of Living: {data['customer_resdiential_info']['duration_of_living']} years", normal_style))
        elements.append(Paragraph(f"Residence Type: {data['customer_resdiential_info']['residence_type']}", normal_style))
        elements.append(Paragraph(f"Rent: {data['customer_resdiential_info']['rent']}", normal_style))
        elements.append(Spacer(1, 0.2 * inch))

        # Employment Information
        elements.append(Paragraph("Employment Information:", styles['Heading2']))
        elements.append(Paragraph(f"Employment Type: {data['employee_info']['employment_type']}", normal_style))
        elements.append(Paragraph(f"Duration of Employment: {data['employee_info']['duration_of_employment']} years", normal_style))
        elements.append(Paragraph(f"Organization: {data['employee_info']['organization']}", normal_style))
        elements.append(Spacer(1, 0.2 * inch))

        # Monthly Income
        elements.append(Paragraph(f"Monthly Income: {data['monthly_income']}", normal_style))
        elements.append(Spacer(1, 0.2 * inch))

        # Agreement
        elements.append(Paragraph("Agreement:", styles['Heading2']))
        elements.append(Paragraph(data['agreement'], normal_style))
        elements.append(Spacer(1, 0.5 * inch))

        # # Document URL and Signing Status
        # elements.append(Paragraph(f"Document URL: {data['document_url']}", normal_style))
        # elements.append(Paragraph(f"Signing Status: {data['signing_status']}", normal_style))

        # Build the PDF
        doc.build(elements)
        logger.info(f"PDF saved at: {file_path}")

        return file_path
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        return None