# src/interviews.py

from openai import OpenAI
from config import LLM_API_KEY, LLM_MODEL

client = OpenAI(api_key=LLM_API_KEY)

def conduct_interview(persona, context, depth=3):
    """
    Conducts a recursive "5 Whys" style interview with a synthetic persona.
    Returns the full interview log.
    """
    interview_log = []
    initial_question = f"Hola {persona.get('name', 'N/A')}. Como {persona.get('current_position', 'un profesional')} en la industria de '{context['industry']}' en '{context['location']}', ¿cuáles son las mayores frustraciones o ineficiencias que enfrentas en tu día a día?"

    question = initial_question
    for i in range(depth):
        print(f"  Pregunta {i+1}: {question}")

        # Construir el perfil detallado para el system prompt
        profile_details = "**TU PERFIL:**\n"
        for key, value in persona.items():
            formatted_key = key.replace('_', ' ').title()
            profile_details += f"**{formatted_key}:** {value}\n"

        system_prompt = f"""
        Eres la persona con los datos provistos a continuación. No una copia, no una una versión, no una imitación. Eres la persona real con estos datos.
        Por favor, actua de acuerdo a tu perfil y responde a las preguntas de la mejor manera posible.

        {profile_details}
        """

        # Construct a more detailed context for the interview prompt
        detailed_context = f"""
        Responde a la siguiente pregunta desde tu perspectiva, reflejando tu rol,
        experiencia y sesgos. Sé específico y da ejemplos concretos.

        Pregunta: {question}
        Respuesta:
        """

        try:
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": detailed_context}
                ],
                max_tokens=200,
                n=1,
                stop=None,
            )
            answer = response.choices[0].message.content.strip()
            print(f"  Respuesta: {answer}")

            interview_log.append({"question": question, "answer": answer})

            # Extract problem and formulate next question
            problem = extract_problem_from_answer(answer)
            if problem:
                question = f"Interesante. ¿Y por qué crees que ocurre eso? ¿Cuál es la causa raíz de '{problem}'?"
            else:
                break  # End interview if no clear problem is identified

        except Exception as e:
            print(f"Error durante la entrevista: {e}")
            break

    return interview_log

def extract_problem_from_answer(answer):
    """
    A simple heuristic to extract a "problem" from the persona's answer.
    This could be improved with more sophisticated NLP.
    """
    # Look for sentences expressing frustration, inefficiency, or difficulty
    keywords = ["problema", "frustrante", "ineficiente", "difícil", "cuello de botella", "retraso"]
    sentences = answer.split('.')
    for sentence in sentences:
        for keyword in keywords:
            if keyword in sentence.lower():
                return sentence.strip()
    return None
