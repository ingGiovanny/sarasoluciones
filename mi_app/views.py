from django.shortcuts import render
from mi_app.templates import *  
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.apps import apps
from .utils import generar_pdf_universal # Esta es la única importación necesaria de utils
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def vista(request):
    return render(request, 'index.html',)


def vista1(request):
    return render(request, 'index.html')

def vista2(request):
    return render(request, 'aside/body.html') 

def vista3(request):
    return render(request, 'modulos/prueba.html')

def ayuda(request):
    return render(request, 'ayuda.html')

def exportar_modulo_pdf(request, nombre_modelo):
    try:
        Modelo = apps.get_model('mi_app', nombre_modelo)
    except LookupError:
        return HttpResponse("Modelo no encontrado", status=404)

    config = {
        'Administrador': {
            'titulo': 'Reporte de Administradores',
            'campos': ['id', 'nombres_completos', 'correo_electronico', 'cedula', 'telefono'],
            'headers': ['N°', 'Nombre', 'Correo', 'Cédula', 'Teléfono']
        },
        'Categoria': {
            'titulo': 'Reporte de Categorías',
            'campos': ['id', 'nombre_completo', 'numero_documento', 'correo_electronico'],
            'headers': ['ID', 'Nombre', 'Documento', 'Correo']
        },
        'Cliente': {
            'titulo': 'Reporte de Clientes',
            'campos': ['id', 'fecha', 'total'],
            'headers': ['ID', 'Fecha de Venta', 'Total ($)']
        },
        'Compra': {
            'titulo': 'Listado de Compras',
            'campos': ['id', 'nombre', 'color', 'modelo'],
            'headers': ['N°', 'Nombre', 'Color', 'Modelo']
        },
        'Factura': {
            'titulo': 'Listado de Marcas',
            'campos': ['id', 'nombre'],
            'headers': ['ID', 'Nombre']
        },
        'Garantia': {
            'titulo': 'Listado de Garantías',
            'campos': ['id', 'nombre'],
            'headers': ['ID', 'Nombre']
        },
        'Gestionservicio': {
            'titulo': 'Listado de Gestión de Servicios',
            'campos': ['id', 'nombre'],
            'headers': ['ID', 'Nombre']
        },
        'Marca': {
            'titulo': 'Listado de Marcas',
            'campos': ['id', 'nombre'],
            'headers': ['ID', 'Nombre']
        },
        'Pedido': {
            'titulo': 'Listado de Productos',
            'campos': ['id', 'nombre', 'precio'],
            'headers': ['ID', 'Nombre', 'Precio ($)']
        },
        'Presentacion': {
            'titulo': 'Listado de Servicios',
            'campos': ['id', 'nombre', 'descripcion', 'precio'],
            'headers': ['ID', 'Nombre', 'Descripción', 'Precio ($)']
        },
        'Proveedor': {
            'titulo': 'Listado de Proveedores',
            'campos': ['id', 'nombre', 'correo_electronico', 'telefono'],
            'headers': ['ID', 'Nombre', 'Correo', 'Teléfono']
        },
        'Producto': {
            'titulo': 'Listado de Productos',
            'campos': ['id', 'nombre', 'precio'],
            'headers': ['ID', 'Nombre', 'Precio ($)']
        },
        'Servicio': {
            'titulo': 'Listado de Servicios',   
            'campos': ['id', 'nombre', 'descripcion', 'precio'],
            'headers': ['ID', 'Nombre', 'Descripción', 'Precio ($)']
        },
        'ventas': {
            'titulo': 'Reporte de Ventas',
            'campos': ['id', 'fecha', 'total'],
            'headers': ['ID', 'Fecha de Venta', 'Total ($)']
        },

    }

    conf = config.get(nombre_modelo)
    if not conf:
        return HttpResponse("Configuración no encontrada", status=404)

    objetos = Modelo.objects.all()
    filas = []
    for obj in objetos:
        fila = [str(getattr(obj, campo)) for campo in conf['campos']]
        filas.append(fila)

    return generar_pdf_universal(
        filename=f"reporte_{nombre_modelo.lower()}",
        titulo=conf['titulo'],
        encabezados=conf['headers'],
        data_filas=filas
    )

def exportar_pdf_universal(request, modelo):
    """
    Vista para generar un PDF genérico basado en el modelo enviado.
    """
    # 1. Crear el objeto de respuesta con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_{modelo}.pdf"'

    # 2. Crear el objeto PDF usando ReportLab
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # 3. Título del documento
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, f"Reporte de {modelo.capitalize()}")

    # 4. Lógica para obtener datos (Ejemplo dinámico)
    try:
        # Buscamos el modelo dentro de tu app de forma dinámica
        ModelClass = apps.get_model('mi_app', modelo)
        objetos = ModelClass.objects.all()

        p.setFont("Helvetica", 12)
        y = height - 80
        
        for obj in objetos:
            # Asumiendo que el modelo tiene un atributo __str__ o nombre
            p.drawString(100, y, f"- {str(obj)}")
            y -= 20 # Espaciado hacia abajo
            if y < 50: # Salto de página simple
                p.showPage()
                y = height - 50

    except LookupError:
        p.drawString(100, height - 80, "Error: El modelo no existe.")

    # 5. Cerrar el PDF y devolver la respuesta
    p.showPage()
    p.save()
    
    return response