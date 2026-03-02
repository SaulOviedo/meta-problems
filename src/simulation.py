# src/simulation.py

from .personas import generate_personas
from .interviews import conduct_interview, extract_problem_from_answer
from .analysis import analyze_problems
from .config import PERSONA_ARCHETYPES

def run_simulation(context):
    """
    Runs the full simulation for a given context.
    Returns a dictionary with the full simulation data.
    """
    print(f"\nIniciando simulación para la industria: {context['industry']} en {context['location']}")

    # 1. Generación de Personas Sintéticas
    num_personas = len(PERSONA_ARCHETYPES)
    personas = generate_personas(context, list(PERSONA_ARCHETYPES.keys()), num_personas)
    print(f"Se generaron {len(personas)} personas sintéticas.")

    # 2. Entrevistas de Fricción
    interviews = []
    all_problems = []
    for persona in personas:
        print(f"\nEntrevistando a: {persona['name']} ({persona['archetype']})")
        interview_log = conduct_interview(persona, context)
        interviews.append({"persona": persona, "log": interview_log})
        
        # Extract problems from the interview log
        for entry in interview_log:
            problem = extract_problem_from_answer(entry['answer'])
            if problem:
                all_problems.append(problem)

    # 3. Análisis y Filtrado de Problemas
    high_value_problems = []
    if all_problems:
        print("\nAnalizando problemas identificados...")
        high_value_problems = analyze_problems(all_problems)
    
    return {
        "industry": context['industry'],
        "location": context['location'],
        "interviews": interviews,
        "high_value_problems": high_value_problems
    }
