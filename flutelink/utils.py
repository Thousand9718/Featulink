import math
from .models import UsuarioDisciplinaTipo, Cantante, Instrumentista, Bailarin, Productor, Grafitero
from django.contrib.auth.models import User

import math

def haversine_distance(lat1, lng1, lat2, lng2):
    # Fórmula de Haversine:
    # Sirve para calcular la distancia más corta sobre la superficie de una esfera (como la Tierra)
    # entre dos puntos dados por su latitud y longitud en grados.

    R = 6371  # Radio medio de la Tierra en km

    # Convertimos las coordenadas de grados a radianes
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lng2 - lng1)

    # Fórmula de Haversine
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Resultado: distancia entre los dos puntos en kilómetros


def calcular_compatibilidad(obj1, obj2):
    compatibilidad = 100

    # Ubicación
    if obj1.ubicacion_lat and obj1.ubicacion_lng and obj2.ubicacion_lat and obj2.ubicacion_lng:
        distancia = haversine_distance(obj1.ubicacion_lat, obj1.ubicacion_lng, obj2.ubicacion_lat, obj2.ubicacion_lng)
        if distancia > 50:  # Ajusta el umbral si quieres
            compatibilidad -= 30
        elif distancia > 20:
            compatibilidad -= 15

    # Género (si lo tienen ambos)
    if hasattr(obj1, 'genero') and hasattr(obj2, 'genero'):
        if obj1.genero != obj2.genero:
            compatibilidad -= 20

    # Experiencia (diferencia muy alta)
    if hasattr(obj1, 'experiencia') and hasattr(obj2, 'experiencia'):
        diferencia = abs(obj1.experiencia - obj2.experiencia)
        if diferencia > 5:
            compatibilidad -= 15
        elif diferencia > 2:
            compatibilidad -= 7

    return max(compatibilidad, 0)


def obtener_modelo_por_tipo(tipo):
    mapa_modelos = {
        'cantante': Cantante,
        'instrumentista': Instrumentista,
        'breaker': Bailarin,
        'productor': Productor,
        'grafitero': Grafitero,
    }
    return mapa_modelos.get(tipo)