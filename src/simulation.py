# src/simulation.py

from .personas import generate_personas
from .interviews import conduct_interview
from .analysis import analyze_interviews
from .config import PERSONA_ARCHETYPES


def run_simulation(context, founder_profile="tecnico", time_months=2,
                   capital="bootstrapped", solution_type="sin_preferencia",
                   market_target="sin_preferencia", num_solutions=3,
                   event_callback=None):
    """
    Runs the full simulation for a given context.
    Returns a dictionary with the full simulation data.

    event_callback(event_type: str, data: dict) is called at key points
    during execution to emit progress events. Pass None to disable.
    """
    def emit(event_type, data):
        if event_callback:
            event_callback(event_type, data)

    print(f"\nIniciando simulación para la industria: {context['industry']} en {context['location']}")

    # 1. Generación de Personas Sintéticas
    emit("stage_start", {"stage": "personas"})
    personas = generate_personas(
        context, list(PERSONA_ARCHETYPES.keys()), len(PERSONA_ARCHETYPES),
        event_callback=event_callback,
    )
    print(f"Se generaron {len(personas)} personas sintéticas.")
    emit("stage_complete", {"stage": "personas"})

    # 2. Entrevistas de Fricción
    emit("stage_start", {"stage": "interviews"})
    interviews = []
    for i, persona in enumerate(personas):
        print(f"\nEntrevistando a: {persona['name']} ({persona['archetype']})")
        emit("interview_start", {
            "persona_index": i,
            "persona_name": persona.get("name", ""),
            "archetype": persona.get("archetype", ""),
        })
        log = conduct_interview(persona, context, event_callback=event_callback, persona_index=i)
        interviews.append({"persona": persona, "log": log})
        emit("interview_complete", {
            "persona_index": i,
            "persona_name": persona.get("name", ""),
            "phases_completed": len(log),
        })
    emit("stage_complete", {"stage": "interviews"})

    # 3. Análisis de Entrevistas
    analysis = {}
    if interviews:
        print("\nAnalizando problemas identificados...")
        emit("stage_start", {"stage": "analysis"})
        emit("analysis_start", {})
        analysis = analyze_interviews(
            interviews_list=interviews,
            founder_profile=founder_profile,
            time_months=time_months,
            capital=capital,
            solution_type=solution_type,
            market_target=market_target,
            num_solutions=num_solutions,
            event_callback=event_callback,
        )
        emit("stage_complete", {"stage": "analysis"})

    return {
        "industry": context['industry'],
        "location": context['location'],
        "interviews": interviews,
        "analysis": analysis,
    }
