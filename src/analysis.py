# src/analysis.py

from openai import OpenAI
from config import LLM_API_KEY, LLM_MODEL

client = OpenAI(api_key=LLM_API_KEY)

def analyze_problems(problems):
    """
    Analyzes a list of identified problems to find high-value ones.
    This uses an LLM to score and filter the problems.
    """
    if not problems:
        return []

    problems_text = "\n".join([f"- {p}" for p in problems])

    prompt = f"""
    Eres un analista de negocios experto en identificar oportunidades de mercado.
    A continuación se presenta una lista de problemas y fricciones identificados
    en una industria a través de entrevistas simuladas.

    Problemas Identificados:
    {problems_text}

    Tu tarea es analizar estos problemas y filtrar aquellos que representan
    una oportunidad de negocio de alto valor. Considera los siguientes criterios:
    1.  **Dolor del Cliente**: ¿Es un problema agudo y recurrente?
    2.  **Disposición a Pagar**: ¿Las empresas estarían dispuestas a pagar por una solución?
    3.  **Escalabilidad**: ¿La solución podría aplicarse a gran escala?
    4.  **Viabilidad Técnica (MVP)**: ¿Es factible construir una solución inicial (MVP) con esfuerzo moderado?

    Devuelve una lista de los 3 problemas más prometedores, justificados brevemente.
    Si ninguno parece prometedor, indica que no se encontraron oportunidades claras.

    Formato de salida:
    1. [Problema 1]: [Breve justificación]
    2. [Problema 2]: [Breve justificación]
    3. [Problema 3]: [Breve justificación]
    """

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "Eres un analista de negocios experto."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.3,
        )
        analysis_result = response.choices[0].message.content.strip()

        # Simple parsing of the result
        high_value_problems = [line for line in analysis_result.split('\n') if line.strip()]
        return high_value_problems

    except Exception as e:
        print(f"Error en el análisis de problemas: {e}")
        return []

