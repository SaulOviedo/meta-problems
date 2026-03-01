# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration for LLM
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")

# Configuration for Simulation
INDUSTRY_NICHES = [
    "logística química",
    "seguros de carga",
    "minería de tierras raras",
    "gestión de residuos industriales",
    "agricultura de precisión"
]

# Configuration for Personas
PERSONA_ARCHETYPES = {
    "veterano_cinico": {
        "description": "Un experto de la industria con más de 20 años de experiencia, escéptico sobre las nuevas tecnologías y enfocado en la rentabilidad a corto plazo.",
        "bias": "Negativo hacia la innovación, prefiere soluciones probadas y de bajo costo."
    },
    "gerente_operativo_agobiado": {
        "description": "Responsable de las operaciones diarias, constantemente apagando incendios y lidiando con la presión de la eficiencia.",
        "bias": "Enfocado en soluciones que simplifiquen su trabajo y reduzcan la carga operativa."
    },
    "regulador_estricto": {
        "description": "Un funcionario gubernamental o de un organismo regulador, enfocado en el cumplimiento de normativas y la seguridad.",
        "bias": "Prioriza la seguridad y el cumplimiento por encima de la eficiencia o el costo."
    },
    "innovador_entusiasta": {
        "description": "Un joven profesional apasionado por la tecnología y la innovación, siempre buscando nuevas formas de optimizar procesos.",
        "bias": "Positivo hacia la tecnología, a veces subestimando los desafíos de la implementación."
    }
}
