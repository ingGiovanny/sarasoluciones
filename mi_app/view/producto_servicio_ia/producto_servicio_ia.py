import json
from django.http import JsonResponse
from django.conf import settings
from groq import Groq


#funcion para generar descripción de servicios de capacitación
def generar_descripcion_ia(request):
    if request.method == 'POST':
        try:
            # Recibimos el dato desde el frontend
            data = json.loads(request.body)
            nombre_item = data.get('nombre', '')

            if not nombre_item:
                return JsonResponse({'error': 'Falta el nombre del producto/servicio'}, status=400)

            # Inicializamos Groq con tu clave
            client = Groq(api_key=settings.GROQ_API_KEY)

            # El "Prompt" (Las instrucciones para la IA)
            prompt = f"Actúa como un experto en Seguridad y Salud en el Trabajo (SST). Crea una descripción profesional, comercial y atractiva para el siguiente producto o servicio de capacitación: '{nombre_item}'. REGLAS: 1. Máximo 3 líneas de texto (unas 40 palabras). 2. No incluyas saludos, introducciones ni comillas. 3. Entrega única y exclusivamente la descripción directa."
            # Llamamos al modelo Llama 3 (es súper rápido y gratis en Groq)
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            # Extraemos la respuesta
            descripcion_generada = chat_completion.choices[0].message.content
            
            return JsonResponse({'descripcion': descripcion_generada})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Método no permitido'}, status=405)



    #funcion para generar descripción de productos 
def generar_descripcion_producto_ia(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Recuerda que aquí viene "Nombre + Color + Modelo"
            nombre_item = data.get('nombre', '') 

            if not nombre_item:
                return JsonResponse({'error': 'Falta la información del producto'}, status=400)

            client = Groq(api_key=settings.GROQ_API_KEY)

            # PROMPT EXCLUSIVO PARA PRODUCTOS FÍSICOS
            prompt = f"Actúa como un experto en Equipos de Protección Personal (EPP) y artículos de Seguridad y Salud en el Trabajo (SST). Crea una descripción comercial, técnica y atractiva para este producto exacto: '{nombre_item}'. REGLAS: 1. Máximo 3 líneas. 2. Resalta la protección, el material y el confort. 3. No incluyas saludos ni comillas, solo la descripción directa."

            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant", 
            )
            
            return JsonResponse({'descripcion': chat_completion.choices[0].message.content})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Método no permitido'}, status=405)




# VISTA PARA DESCRIPCIÓN DETALLADA  DE CAPACITACIONES
def generar_descripcion_detallada_ia(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre_item = data.get('nombre', '')

            if not nombre_item:
                return JsonResponse({'error': 'Falta el nombre del servicio'}, status=400)

            from groq import Groq
            client = Groq(api_key=settings.GROQ_API_KEY)

            # PROMPT PARA EL TEXTO LARGO (TEMARIO/OBJETIVOS)
            prompt = f"Actúa como un experto en Seguridad y Salud en el Trabajo (SST). Escribe una descripción detallada y completa para la capacitación: '{nombre_item}'. Incluye los objetivos principales y a quién va dirigido. REGLAS: 1. Máximo 6 líneas (unas 80 palabras). 2. Usa un tono profesional y persuasivo. 3. No incluyas saludos ni frases de introducción."

            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant", 
            )
            
            return JsonResponse({'descripcion': chat_completion.choices[0].message.content})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Método no permitido'}, status=405)

