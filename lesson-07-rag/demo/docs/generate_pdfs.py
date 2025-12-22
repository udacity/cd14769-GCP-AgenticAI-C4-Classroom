from fpdf import FPDF
import os

def create_pdf(filename, title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, title, ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=11)
    # Add legal disclaimer/intro
    intro = (
        "LEGAL NOTICE AND TERMS OF OPERATION\n"
        "THIS DOCUMENT CONSTITUTES A BINDING AGREEMENT GOVERNING THE SUBJECT MATTER HEREIN. "
        "PLEASE REVIEW THE FOLLOWING TECHNICAL SPECIFICATIONS AND LEGAL STIPULATIONS CAREFULLY. "
        "FAILURE TO COMPLY WITH THESE PROTOCOLS MAY RESULT IN NULLIFICATION OF SERVICE OBLIGATIONS.\n\n"
        "SECTION 1: DEFINITIONS AND INTERPRETATIONS\n"
        "For the purposes of this document, 'Vendor' refers to the operating entity, and 'Client' refers to the end-user. "
        "All timeframes are calculated in business days unless otherwise specified.\n\n"
        "SECTION 2: OPERATIONAL PROTOCOLS"
    )
    pdf.multi_cell(0, 5, intro)
    pdf.ln(5)
    
    # Add content
    pdf.multi_cell(0, 5, content)
    
    pdf.ln(5)
    # Add legal footer
    footer = (
        "\nSECTION 3: LIABILITY AND INDEMNIFICATION\n"
        "The Vendor assumes no liability for force majeure events, carrier delays, or data transmission errors. "
        "By engaging with these services, the Client agrees to indemnify the Vendor against incidental or consequential damages. "
        "This policy is subject to change without prior notice pending regulatory review.\n\n"
        "CONFIDENTIALITY: The information contained herein is proprietary to the Vendor."
    )
    pdf.multi_cell(0, 5, footer)
    
    pdf.output(filename)
    print(f"Generated {filename}")

# 1. Shipping Policy
shipping_content = (
    "SUBSECTION A: DOMESTIC LOGISTICS AND FULFILLMENT\n"
    "1. Standard Fulfillment Protocol:\n"
    "   - Tariff: A flat-rate logistics fee of $5.00 USD is applicable to all standard consignments.\n"
    "   - Transit Duration: Expected delivery windows range between 5 to 7 business days, subject to carrier availability.\n"
    "   - Incentive Threshold: Logistics fees are waived for order values exceeding $50.00 USD (pre-tax).\n\n"
    "2. Expedited Fulfillment Protocol:\n"
    "   - Tariff: A premium logistics fee of $10.00 USD applies.\n"
    "   - Transit Duration: Accelerated delivery is estimated at 2 to 3 business days.\n\n"
    "SUBSECTION B: INTERNATIONAL LOGISTICS\n"
    "3. Cross-Border Consignment:\n"
    "   - Tariff: International shipping incurs a flat fee of $20.00 USD, exclusive of import duties.\n"
    "   - Transit Duration: Global transit times are estimated between 10 to 15 business days, pending customs clearance."
)

# 2. Returns Policy
returns_content = (
    "SUBSECTION A: RETURN AUTHORIZATION WINDOWS\n"
    "The Client must initiate return protocols within the temporal bounds defined by the jurisdiction of the delivery address ('Situs').\n"
    "Schedule of Jurisdictional Periods:\n"
    "   - New York (NY) & California (CA): 90 calendar days.\n"
    "   - Texas (TX): 45 calendar days.\n"
    "   - All other United States jurisdictions: 30 calendar days.\n"
    "   - International Jurisdictions: 60 calendar days.\n\n"
    "SUBSECTION B: CONDITION AND RESTOCKING\n"
    "1. Asset Integrity: All returned merchandise must be in its original, unadulterated condition.\n"
    "2. Defective Merchandise: Return logistics costs are absorbed by the Vendor for verified manufacturing defects.\n"
    "3. Discretionary Returns: For returns not attributed to defect, a restocking levy of $5.00 USD will be deducted from the remittance."
)

# 3. Tracking Policy
tracking_content = (
    "SUBSECTION A: DIGITAL SURVEILLANCE OF PARCEL TRANSIT\n"
    "1. Identification Assignment: Upon transfer of custody to the logistics carrier, a unique alphanumeric Tracking Identifier will be generated and transmitted to the Client via electronic mail.\n"
    "2. Real-Time Monitoring: The Client may query the status of the consignment via the Vendor's web portal using the assigned Order Identification Number.\n"
    "3. Data Latency: Please verify carrier data synchronization intervals. The Vendor is not liable for real-time discrepancies in carrier reporting systems."
)

# 4. Privacy Policy (New)
privacy_content = (
    "SUBSECTION A: DATA ACQUISITION AND RETENTION\n"
    "1. Data Collection: We collect Personally Identifiable Information (PII) including but not limited to IP addresses, geolocation data, and contact details for the purpose of transactional fulfillment.\n"
    "2. Third-Party Dissemination: PII may be encrypted and transmitted to third-party payment processors (e.g., Stripe, PayPal) strictly for fiscal settlement.\n\n"
    "SUBSECTION B: DATA SUBJECT RIGHTS\n"
    "Pursuant to GDPR and CCPA frameworks, the Client retains the right to request the expungement of their data records from our servers, subject to mandatory fiscal retention laws (e.g., 7-year tax audit trails)."
)

# 5. Terms of Service (New)
tos_content = (
    "SUBSECTION A: ACCEPTABLE USE POLICY\n"
    "1. Account Responsibility: The Client is solely responsible for maintaining the confidentiality of their access credentials. Any unauthorized access must be reported immediately.\n"
    "2. Prohibited Conduct: Utilization of the Vendor's platform for fraudulent activities, reverse engineering, or data mining is strictly prohibited.\n\n"
    "SUBSECTION B: DISPUTE RESOLUTION\n"
    "1. Arbitration Agreement: All disputes arising from these Terms shall be resolved via binding arbitration. The Client explicitly waives the right to participate in class-action lawsuits.\n"
    "2. Termination: The Vendor reserves the right to terminate services unilaterally without cause upon written notice."
)

if __name__ == "__main__":
    output_dir = "lesson-07-rag/demo/docs"
    
    create_pdf(os.path.join(output_dir, "Shipping_Policy.pdf"), "Shipping & Logistics Policy", shipping_content)
    create_pdf(os.path.join(output_dir, "Returns_Policy.pdf"), "Merchandise Return Policy", returns_content)
    create_pdf(os.path.join(output_dir, "Tracking_Policy.pdf"), "Consignment Tracking Protocol", tracking_content)
    create_pdf(os.path.join(output_dir, "Privacy_Policy.pdf"), "Data Privacy & Security Policy", privacy_content)
    create_pdf(os.path.join(output_dir, "Terms_of_Service.pdf"), "Terms of Service Agreement", tos_content)
