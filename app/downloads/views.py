from flask import render_template, Response
from fpdf import FPDF
from app.downloads import bp
from app.models import Farm, FundedFarm, User
import psycopg2

@bp.route('/admin/downloads')
def download_page():
    return render_template('download.html')

@bp.route('/report/farms/pdf', methods=('GET', 'POST'))
def download_farms():
    result = Farm.query.all()
    titles = ['Name', 'Price', 'Duration', 'Active', 'Units', 'Margin']

    # set up pdf page
    pdf = FPDF()
    pdf.add_page()
    page_width = pdf.w
    pdf.set_font('Times','B', 12.0)
    pdf.cell(page_width, 0.0, 'Farm Data', align='C')
    pdf.ln(10)
    col_width = page_width/len(titles)
    pdf.ln(1)

    th = pdf.font_size
    for title in titles:
        pdf.cell(col_width, th, title, border=1)
    pdf.ln(th)
    pdf.set_font('Courier', '', 10)
    for row in result:
        pdf.cell(col_width, th, str(row.name), border=1)
        pdf.cell(col_width, th, str(row.price), border=1)
        pdf.cell(col_width, th, str(row.duration), border=1)
        pdf.cell(col_width, th, str(row.active), border=1)
        pdf.cell(col_width, th, str(row.units), border=1)
        pdf.cell(col_width, th, str(row.margin), border=1)
        pdf.ln(th)
    pdf.ln(10)

    pdf.set_font('Times','',10.0)
    pdf.cell(page_width, 0.0, '- end of report -', align='C')

    return Response(pdf.output(dest='S').encode('latin-1'),
                    mimetype='application/pdf',
                    headers={'Content-Disposition':'attachment;filename=farms_report.pdf'})


@bp.route('/report/funded/pdf', methods=('GET', 'POST'))
def download_funded_farms():
    result = FundedFarm.query.all()
    titles = ['Name', 'Amount', 'Units', 'Payout', 'Funder']

    # set up pdf page
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(1,1,-1)
    page_width = pdf.w - 1 * pdf.l_margin
    pdf.set_font('Times','B', 12.0)
    pdf.cell(page_width, 0.0, 'Funded Farm Data', align='C')
    pdf.ln(10)
    col_width = page_width/len(titles)
    pdf.ln(1)

    th = pdf.font_size
    for title in titles:
        pdf.cell(col_width, th, title, border=1)
    pdf.ln(th)
    pdf.set_font('Courier', '', 10)
    for row in result:
        pdf.cell(col_width, th, str(row.name), border=1)
        pdf.cell(col_width, th, str(row.amount), border=1)
        pdf.cell(col_width, th, str(row.units), border=1)
        pdf.cell(col_width, th, str(row.payout), border=1)
        pdf.cell(col_width, th, str(row.funder), border=1)
        pdf.ln(th)
    pdf.ln(10)

    pdf.set_font('Times','',10.0)
    pdf.cell(page_width, 0.0, '- end of report -', align='C')

    return Response(pdf.output(dest='S').encode('latin-1'),
                    mimetype='application/pdf',
                    headers={'Content-Disposition':'attachment;filename=funded_farms_report.pdf'})

@bp.route('/report/users/pdf', methods=('GET', 'POST'))
def download_users():
    result = User.query.all()
    titles = ['ID', 'Email', 'First-Name', 'Last-Name','Role']

    # set up pdf page
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(1,1,-1)
    page_width = pdf.w - 1 * pdf.l_margin
    pdf.set_font('Times','B', 12.0)
    pdf.cell(page_width, 0.0, 'Users Data', align='C')
    pdf.ln(10)
    col_width = page_width/len(titles)
    pdf.ln(1)

    th = pdf.font_size
    for title in titles:
        if title == 'Email':
            pdf.cell(col_width+14, th, title, border=1)
        elif title == 'Role':
            pdf.cell(col_width-14, th, title, border=1)
        else:
            pdf.cell(col_width, th, title, border=1)
    pdf.ln(th)
    pdf.set_font('Courier', '', 10)
    for row in result:
        pdf.cell(col_width, th, str(row.id_num), border=1)
        pdf.cell(col_width+14, th, str(row.email), border=1)
        pdf.cell(col_width, th, str(row.first_name), border=1)
        pdf.cell(col_width, th, str(row.last_name), border=1)
        pdf.cell(col_width-14, th, str(row.role), border=1)
        pdf.ln(th)
    pdf.ln(10)

    pdf.set_font('Times','',10.0)
    pdf.cell(page_width, 0.0, '- end of report -', align='C')

    return Response(pdf.output(dest='S').encode('latin-1'),
                    mimetype='application/pdf',
                    headers={'Content-Disposition':'attachment;filename=users_report.pdf'})
