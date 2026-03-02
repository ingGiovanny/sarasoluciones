from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse

# Borra la línea: from .utils import generar_pdf_universal
# Borra la función exportar_modulo_pdf de aquí (la moveremos a views.py)

def generar_pdf_universal(filename, titulo, encabezados, data_filas):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph(titulo, styles['Title']))
    elements.append(Spacer(1, 12))

    tabla_data = [encabezados] + data_filas
    tabla = Table(tabla_data)

    estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0, 0.6, 0.6)), 
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
    ])
    
    tabla.setStyle(estilo)
    elements.append(tabla)
    doc.build(elements)
    return response