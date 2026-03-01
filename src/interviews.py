# src/interviews.py

from openai import OpenAI
from config import LLM_API_KEY, LLM_MODEL

client = OpenAI(api_key=LLM_API_KEY)

def conduct_interview(persona, niche, depth=3):
    """
    Conducts a recursive "5 Whys" style interview with a synthetic persona.
    """
    problems = []
    initial_question = f"Hola {persona['name']}. Como {persona['title']} en la industria de '{niche}', ¿cuáles son las mayores frustraciones o ineficiencias que enfrentas en tu día a día?"

    question = initial_question
    for i in range(depth):
        print(f"  Pregunta {i+1}: {question}")
        prompt = f"""
        Eres {persona['name']}, un {persona['title']} en la industria de '{niche}'.
        Tu biografía es: {persona['bio']}
        Tu arquetipo es: {persona['archetype']}

        Responde a la siguiente pregunta desde tu perspectiva, reflejando tu rol,
        experiencia y sesgos. Sé específico y da ejemplos concretos.

        Pregunta: {question}
        Respuesta:
        """

        try:
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": f"Eres {persona['name']}, un {persona['title']} en la industria de '{niche}'."},
                    {"role": "user", "content": question}
                ],
                max_tokens=200,
                n=1,
                stop=None,
                temperature=0.5,
            )
            answer = response.choices[0].message.content.strip()
            print(f"  Respuesta: {answer}")

            # Extract problem and formulate next question
            problem = extract_problem_from_answer(answer)
            if problem:
                problems.append(problem)
                question = f"Interesante. ¿Y por qué crees que ocurre eso? ¿Cuál es la causa raíz de '{problem}'?"
            else:
                break  # End interview if no clear problem is identified

        except Exception as e:
            print(f"Error durante la entrevista: {e}")
            break

    return problems

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
