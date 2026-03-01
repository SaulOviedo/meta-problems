# src/simulation.py

from .personas import generate_personas
from .interviews import conduct_interview
from .analysis import analyze_problems
from .config import PERSONA_ARCHETYPES

def run_simulation(niche):
    """
    Runs the full simulation for a given industry niche.
    """
    print(f"\nIniciando simulación para la industria: {niche}")

    # 1. Generación de Personas Sintéticas
    num_personas = len(PERSONA_ARCHETYPES)
    personas = generate_personas(niche, list(PERSONA_ARCHETYPES.keys()), num_personas)
    print(f"Se generaron {len(personas)} personas sintéticas.")

    # 2. Entrevistas de Fricción
    all_problems = []
    for persona in personas:
        print(f"\nEntrevistando a: {persona['name']} ({persona['archetype']})")
        problems = conduct_interview(persona, niche)
        all_problems.extend(problems)

    # 3. Análisis y Filtrado de Problemas
    if all_problems:
        print("\nAnalizando problemas identificados...")
        high_value_problems = analyze_problems(all_problems)
        return high_value_problems
    else:
        return []
