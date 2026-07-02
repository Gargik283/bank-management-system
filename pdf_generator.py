from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def generate_bank_statement(
    filename,
    account,
    logs,
    total_deposits,
    total_withdrawals
):
    styles = getSampleStyleSheet()

    pdf = SimpleDocTemplate(filename)

    elements = []

    elements.append(
        Paragraph("<b><font size=18>Bank Management System</font></b>", styles["Title"])
    )

    elements.append(
        Paragraph("<b>Account Statement</b>", styles["Heading2"])
    )

    elements.append(
        Paragraph(f"Account Number : {account.get_account_number()}", styles["Normal"])
    )

    elements.append(
        Paragraph(f"Customer Name : {account.get_name()}", styles["Normal"])
    )

    elements.append(
        Paragraph(
            f"Current Balance : ₹{account.get_balance():,.2f}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(f"Total Deposits : ₹{total_deposits:,.2f}", styles["Normal"])
    )

    elements.append(
        Paragraph(f"Total Withdrawals : ₹{total_withdrawals:,.2f}", styles["Normal"])
    )

    elements.append(Paragraph("<br/>", styles["Normal"]))

    data = [["Action", "Amount", "Date & Time"]]

    for row in logs:
        data.append([
            row[3],
            str(row[4]),
            str(row[5])
        ])

    table = Table(data, colWidths=[2*inch, 2*inch, 2.5*inch])

    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),1,colors.black),
        ("BACKGROUND",(0,1),(-1,-1),colors.beige),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("BOTTOMPADDING",(0,0),(-1,0),10),
    ]))

    elements.append(table)

    pdf.build(elements)