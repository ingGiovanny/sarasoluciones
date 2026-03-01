# utils.py
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse

def exportar_a_pdf(titulo, encabezados, datos):
    html_string = render_to_string('modulos/reporte_general/reporte_general.html', {
        'titulo': titulo,
        'encabezados': encabezados,
        'datos': datos,
    })
    html = HTML(string=html_string)
    pdf = html.write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_{titulo}.pdf"'
    return response