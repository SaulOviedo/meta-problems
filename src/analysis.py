# src/analysis.py

import json
import re
from openai import OpenAI
from config import LLM_API_KEY, LLM_MODEL

client = OpenAI(api_key=LLM_API_KEY)


def _build_transcript(log):
    lines = []
    for entry in log:
        lines.append(f"[{entry['phase']}]")
        lines.append(f"Q: {entry['question']}")
        lines.append(f"A: {entry['answer']}")
        lines.append("")
    return "\n".join(lines)


def analyze_interview(interview_data, founder_profile, time_months, capital,
                      solution_type, market_target, num_solutions):
    """
    Analyzes a full interview log and returns a structured opportunity assessment.
    """
    persona = interview_data.get("persona", {})
    log = interview_data.get("log", [])

    transcript = _build_transcript(log)

    persona_summary = ", ".join(
        f"{k}: {v}" for k, v in persona.items()
        if k in ("name", "archetype", "industry", "company", "title", "company_size", "company_arr")
    )

    market_target_label = market_target if market_target != "sin_preferencia" else "no preference (explore all)"
    solution_type_label = solution_type if solution_type != "sin_preferencia" else "no preference (explore all)"

    prompt = f"""Eres un analista experto en startups y evaluación de oportunidades de negocio.

A continuación se presenta la transcripción de una entrevista simulada con un profesional de la industria, seguida de las restricciones del fundador.

---
PERSONA: {persona_summary}

TRANSCRIPCIÓN DE LA ENTREVISTA:
{transcript}
---

PERFIL DEL FUNDADOR:
- Perfil técnico: {founder_profile}
- Tiempo disponible para construir el MVP: {time_months} meses
- Capital disponible: {capital}
- Tipo de solución preferida: {solution_type_label}
- Mercado objetivo preferido: {market_target_label}

---

Basándote en la entrevista, produce un análisis estructurado de la oportunidad. Genera exactamente {num_solutions} soluciones, ordenadas de más a menos prometedora según las restricciones del fundador.

Responde ÚNICAMENTE con un objeto JSON válido (sin markdown, sin explicaciones) que siga exactamente este esquema:

{{
  "main_problem": "One clear sentence describing the core pain point.",
  "target_market": "Description of who specifically has this problem (company size, role, industry).",
  "market_size_estimate": "Rough TAM/SAM estimate with reasoning.",
  "competitive_landscape": "Existing solutions and why they fall short.",
  "monetization_model": "How this could be monetized and expected deal size.",
  "main_risks": ["risk 1", "risk 2", "risk 3"],
  "solutions": [
    {{
      "title": "Solution name",
      "description": "What it does and how.",
      "mvp_difficulty": "low | medium | high",
      "mvp_time_estimate": "e.g. 6 weeks",
      "rationale": "Why this is a good fit for the founder's constraints."
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": "Eres un analista de startups. Responde únicamente con JSON válido."},
            {"role": "user", "content": prompt},
        ],
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown code block if present
    match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", raw)
    if match:
        raw = match.group(1)

    return json.loads(raw)


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Stage 4: Analyze interview and identify opportunities")
    parser.add_argument("--input", default="data/outputs/interviews_output.json",
                        help="Path to interviews output JSON (default: data/outputs/interviews_output.json)")
    parser.add_argument("--output", default="data/outputs/analysis_output.json",
                        help="Path to write the output JSON (default: data/outputs/analysis_output.json)")
    parser.add_argument("--founder-profile", choices=["tecnico", "no_tecnico"], default="tecnico",
                        help="Founder's technical background (default: tecnico)")
    parser.add_argument("--time-months", type=int, default=2,
                        help="Months available to build MVP (default: 2)")
    parser.add_argument("--capital", choices=["bootstrapped", "pre_seed", "seed"], default="bootstrapped",
                        help="Available capital (default: bootstrapped)")
    parser.add_argument("--solution-type",
                        choices=["saas", "marketplace", "servicio_manual", "sin_preferencia"],
                        default="sin_preferencia",
                        help="Preferred solution type (default: sin_preferencia)")
    parser.add_argument("--market-target",
                        choices=["b2b_pyme", "b2b_enterprise", "b2c", "sin_preferencia"],
                        default="sin_preferencia",
                        help="Target market preference (default: sin_preferencia)")
    parser.add_argument("--num-solutions", type=int, default=3,
                        help="Number of solutions to generate, ranked best to worst (default: 3)")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        interview_data = json.load(f)

    print(f"Analyzing interview for: {interview_data.get('persona', {}).get('name', 'unknown')}")
    print(f"Founder profile: {args.founder_profile} | {args.time_months}mo | {args.capital} | "
          f"{args.solution_type} | {args.market_target} | {args.num_solutions} solutions\n")

    result = analyze_interview(
        interview_data=interview_data,
        founder_profile=args.founder_profile,
        time_months=args.time_months,
        capital=args.capital,
        solution_type=args.solution_type,
        market_target=args.market_target,
        num_solutions=args.num_solutions,
    )

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Main problem:  {result.get('main_problem')}")
    print(f"Target market: {result.get('target_market')}")
    print(f"Market size:   {result.get('market_size_estimate')}")
    print(f"Monetization:  {result.get('monetization_model')}")
    print(f"\nSolutions ({len(result.get('solutions', []))}):")
    for i, s in enumerate(result.get("solutions", []), start=1):
        print(f"  {i}. [{s['mvp_difficulty'].upper()}] {s['title']} (~{s['mvp_time_estimate']})")
        print(f"     {s['rationale']}")
    print(f"\nMain risks:")
    for r in result.get("main_risks", []):
        print(f"  - {r}")
    print(f"\n✓ Output saved to {args.output}")
