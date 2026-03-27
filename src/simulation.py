# src/simulation.py

from .personas import generate_personas
from .interviews import conduct_interview
from .analysis import analyze_interviews
from .config import PERSONA_ARCHETYPES


def run_simulation(context, founder_profile="tecnico", time_months=2,
                   capital="bootstrapped", solution_type="sin_preferencia",
                   market_target="sin_preferencia", num_solutions=3):
    """
    Runs the full simulation for a given context.
    Returns a dictionary with the full simulation data.
    """
    print(f"\nIniciando simulación para la industria: {context['industry']} en {context['location']}")

    # 1. Generación de Personas Sintéticas
    personas = generate_personas(context, list(PERSONA_ARCHETYPES.keys()), len(PERSONA_ARCHETYPES))
    print(f"Se generaron {len(personas)} personas sintéticas.")

    # 2. Entrevistas de Fricción
    interviews = []
    for persona in personas:
        print(f"\nEntrevistando a: {persona['name']} ({persona['archetype']})")
        log = conduct_interview(persona, context)
        interviews.append({"persona": persona, "log": log})

    # 3. Análisis de Entrevistas
    analysis = {}
    if interviews:
        print("\nAnalizando problemas identificados...")
        analysis = analyze_interviews(
            interviews_list=interviews,
            founder_profile=founder_profile,
            time_months=time_months,
            capital=capital,
            solution_type=solution_type,
            market_target=market_target,
            num_solutions=num_solutions,
        )

    return {
        "industry": context['industry'],
        "location": context['location'],
        "interviews": interviews,
        "analysis": analysis,
    }
