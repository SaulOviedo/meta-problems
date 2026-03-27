# src/interviews.py

from openai import OpenAI
from config import LLM_API_KEY, LLM_MODEL

client = OpenAI(api_key=LLM_API_KEY)

# Structured interview phases. Each phase has a label and a question template.
# {name}, {position}, {industry} are filled at runtime.
INTERVIEW_PHASES = [
    {
        "phase": "contexto_empresa",
        "question": (
            "Hola {name}, gracias por tu tiempo. Para comenzar: "
            "¿A qué se dedica exactamente la empresa donde trabajas? "
            "¿Qué productos o servicios ofrece principalmente y a quién va dirigido su negocio?"
        ),
    },
    {
        "phase": "rol_y_dia_a_dia",
        "question": (
            "Entendido. ¿Cuál es tu rol específico dentro de la empresa y cómo es un día típico en tu trabajo? "
            "¿Qué tareas realizas, con qué herramientas trabajas y con quién interactúas habitualmente?"
        ),
    },
    {
        "phase": "pain_points",
        "question": (
            "Pensando en tu día a día, ¿cuáles son los mayores problemas o fricciones que tú o tu equipo "
            "experimentan con más frecuencia? Por ejemplo: pérdidas de tiempo, tareas repetitivas, procesos "
            "manuales, falta de información, fallos de comunicación, cuellos de botella, etc."
        ),
    },
    {
        "phase": "profundidad_del_problema",
        "question": (
            "Gracias por compartir eso. ¿Podrías darme más contexto o ejemplos específicos de estos problemas? "
            "¿Con qué frecuencia ocurren, qué impacto tienen en términos de tiempo o dinero perdido, "
            "y por qué crees que todavía no se han resuelto?"
        ),
    },
    {
        "phase": "intentos_previos",
        "question": (
            "¿Han intentado resolver estos problemas antes de alguna forma? "
            "¿Qué soluciones o herramientas probaron y por qué no funcionaron o no fueron suficientes?"
        ),
    },
    {
        "phase": "alcance_sistemico",
        "question": (
            "¿Crees que este problema es exclusivo de tu empresa o es algo común en tu industria en general? "
            "¿Conoces a colegas o competidores que sufran el mismo problema?"
        ),
    },
    {
        "phase": "vision_de_solucion",
        "question": (
            "Si existiera una solución ideal para estos problemas, ¿cómo imaginas que sería? "
            "¿Sería algo digital (software, app, automatización) o algo físico (equipamiento, herramienta, máquina)? "
            "¿Qué características no podrían faltar?"
        ),
    },
    {
        "phase": "disposicion_a_pagar",
        "question": (
            "¿Crees que tu empresa estaría dispuesta a pagar por una solución así? "
            "¿Quién tomaría esa decisión de compra dentro de la organización, "
            "y qué rango de inversión considerarías razonable para resolver estos problemas?"
        ),
    },
]


def _build_system_prompt(persona):
    profile_details = "**TU PERFIL:**\n"
    for key, value in persona.items():
        formatted_key = key.replace('_', ' ').title()
        profile_details += f"**{formatted_key}:** {value}\n"

    return (
        "Eres la persona con los datos provistos a continuación. "
        "No una copia, no una versión, no una imitación. Eres esa persona real.\n"
        "Responde de forma auténtica, con el vocabulario, sesgos y nivel de detalle "
        "propios de tu perfil. Usa ejemplos concretos y específicos de tu industria.\n\n"
        f"{profile_details}"
    )


def _ask(persona, question, conversation_history):
    """Send a question, appending it to the running conversation history."""
    system_prompt = _build_system_prompt(persona)
    conversation_history.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "system", "content": system_prompt}] + conversation_history,
        max_tokens=300,
        n=1,
        stop=None,
    )
    answer = response.choices[0].message.content.strip()
    conversation_history.append({"role": "assistant", "content": answer})
    return answer


def conduct_interview(persona, context):
    """
    Conducts a structured interview with a synthetic persona.

    Flow:
      1. Fixed phases covering company context, role, pain points, solution vision and WTP.

    Returns the full interview log as a list of {phase, question, answer} dicts.
    """
    interview_log = []
    conversation_history = []  # maintains full dialogue context across turns

    name = persona.get('name', 'N/A')
    position = persona.get('current_position', 'profesional')
    industry = context.get('industry', 'tu industria')

    for i, phase_config in enumerate(INTERVIEW_PHASES, start=1):
        phase = phase_config["phase"]
        question = phase_config["question"].format(
            name=name, position=position, industry=industry
        )

        print(f"\n  [{i}] {question}")
        try:
            answer = _ask(persona, question, conversation_history)
            print(f"  Respuesta: {answer}")
            interview_log.append({"phase": phase, "question": question, "answer": answer})

        except Exception as e:
            print(f"  Error en fase '{phase}': {e}")
            break

    return interview_log


if __name__ == "__main__":
    import argparse
    import json
    import os

    parser = argparse.ArgumentParser(description="Stage 3: Conduct friction interview with a persona")
    parser.add_argument("--input", default="data/fixtures/personas.json",
                        help="Path to personas JSON (default: data/fixtures/personas.json)")
    parser.add_argument("--context", default="data/fixtures/context.json",
                        help="Path to context JSON (default: data/fixtures/context.json)")
    parser.add_argument("--persona-index", type=int, default=0,
                        help="Index of the persona to interview from the personas array (default: 0)")
    parser.add_argument("--output", default="data/outputs/interviews_output.json",
                        help="Path to write the output JSON (default: data/outputs/interviews_output.json)")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        personas = json.load(f)
    with open(args.context, encoding="utf-8") as f:
        context = json.load(f)

    persona = personas[args.persona_index]
    print(f"Interviewing: {persona.get('name')} ({persona.get('archetype')}) @ {persona.get('company')}")

    interview_log = conduct_interview(persona, context)

    result = {"persona": persona, "log": interview_log}

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\nInterview complete: {len(interview_log)} exchanges")
    print(f"\n✓ Output saved to {args.output}")
