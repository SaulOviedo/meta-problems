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

# After the pain_points phase, we drill down with "5 Whys" before continuing.
WHYS_DRILL_DEPTH = 2


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


def conduct_interview(persona, context, whys_depth=WHYS_DRILL_DEPTH):
    """
    Conducts a structured interview with a synthetic persona.

    Flow:
      1. Fixed phases covering company context, role, pain points, solution vision and WTP.
      2. After the pain_points phase, runs a recursive "5 Whys" drill-down before continuing.

    Returns the full interview log as a list of {phase, question, answer} dicts.
    """
    interview_log = []
    conversation_history = []  # maintains full dialogue context across turns

    name = persona.get('name', 'N/A')
    position = persona.get('current_position', 'profesional')
    industry = context.get('industry', 'tu industria')

    question_number = 1

    for phase_config in INTERVIEW_PHASES:
        phase = phase_config["phase"]
        question = phase_config["question"].format(
            name=name, position=position, industry=industry
        )

        print(f"\n  [{question_number}] {question}")
        try:
            answer = _ask(persona, question, conversation_history)
            print(f"  Respuesta: {answer}")
            interview_log.append({"phase": phase, "question": question, "answer": answer})
            question_number += 1

            # After identifying pain points, drill down with "5 Whys" before moving on
            if phase == "pain_points":
                problem = extract_problem_from_answer(answer)
                for i in range(whys_depth):
                    if not problem:
                        break
                    why_question = (
                        f"Interesante. ¿Y por qué crees que ocurre eso? "
                        f"¿Cuál es la causa raíz de '{problem[:120]}'?"
                    )
                    print(f"\n  [{question_number}] {why_question}")
                    why_answer = _ask(persona, why_question, conversation_history)
                    print(f"  Respuesta: {why_answer}")
                    interview_log.append({
                        "phase": f"why_{i+1}",
                        "question": why_question,
                        "answer": why_answer,
                    })
                    question_number += 1
                    problem = extract_problem_from_answer(why_answer)

        except Exception as e:
            print(f"  Error en fase '{phase}': {e}")
            break

    return interview_log


def extract_problem_from_answer(answer):
    """
    Heuristic to extract a core problem sentence from a persona's answer.
    """
    keywords = [
        "problema", "frustrante", "ineficiente", "difícil", "cuello de botella",
        "retraso", "pérdida", "falla", "error", "manual", "tedioso", "lento",
    ]
    sentences = answer.split('.')
    for sentence in sentences:
        for keyword in keywords:
            if keyword in sentence.lower():
                return sentence.strip()
    return None
