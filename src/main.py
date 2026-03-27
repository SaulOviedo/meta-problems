# src/main.py

import os
from datetime import datetime
from .simulation import run_simulation
from .context import generate_context


def save_results_to_file(simulation_data, context):
    """
    Saves the full simulation data to a Markdown file in the data directory.
    """
    if not os.path.exists('data'):
        os.makedirs('data')

    industry = context['industry']
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/resultado_{industry.replace(' ', '_')}_{timestamp}.md"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# Simulación de Meta-Problemas: {industry} en {context['location']}\n\n")
        f.write(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## Entrevistas de Fricción\n\n")
        for interview in simulation_data['interviews']:
            persona = interview['persona']
            f.write(f"### Perfil: {persona.get('name', 'N/A')} ({persona.get('archetype', 'N/A')})\n\n")
            for key, value in persona.items():
                formatted_key = key.replace('_', ' ').title()
                if formatted_key not in ['Name', 'Archetype']:
                    f.write(f"**{formatted_key}:** {value}\n")
            f.write("\n")

            f.write("#### Registro de la Entrevista\n\n")
            for entry in interview['log']:
                f.write(f"**P:** {entry['question']}\n\n")
                f.write(f"**R:** {entry['answer']}\n\n")
            f.write("---\n\n")

        f.write("## Análisis de Problemas\n\n")
        analysis = simulation_data.get('analysis', {})
        if analysis:
            f.write(f"**Problema principal:** {analysis.get('main_problem', 'N/A')}\n\n")
            f.write(f"**Mercado objetivo:** {analysis.get('target_market', 'N/A')}\n\n")
            f.write(f"**Tamaño de mercado:** {analysis.get('market_size_estimate', 'N/A')}\n\n")
            f.write(f"**Panorama competitivo:** {analysis.get('competitive_landscape', 'N/A')}\n\n")
            f.write(f"**Modelo de monetización:** {analysis.get('monetization_model', 'N/A')}\n\n")

            risks = analysis.get('main_risks', [])
            if risks:
                f.write("**Principales riesgos:**\n")
                for r in risks:
                    f.write(f"- {r}\n")
                f.write("\n")

            solutions = analysis.get('solutions', [])
            if solutions:
                f.write("### Soluciones Propuestas\n\n")
                for i, s in enumerate(solutions, 1):
                    f.write(f"#### {i}. {s.get('title', 'N/A')} (dificultad: {s.get('mvp_difficulty', 'N/A')})\n\n")
                    f.write(f"{s.get('description', '')}\n\n")
                    f.write(f"**Tiempo estimado MVP:** {s.get('mvp_time_estimate', 'N/A')}\n\n")
                    f.write(f"**Justificación:** {s.get('rationale', '')}\n\n")
        else:
            f.write("No se generó análisis en esta simulación.\n")

    print(f"\nResultados completos de la simulación guardados en: {filename}")


def main():
    """
    Main function to run the Meta-Problems simulation.
    """
    print("Iniciando Meta-Problems...")

    # 1. Generación de Contexto
    context = generate_context()
    print(f"Contexto seleccionado: Industria '{context['industry']}' en '{context['location']}'")

    # 2. Ejecución de la Simulación
    simulation_results = run_simulation(context)

    # 3. Guardar Resultados
    save_results_to_file(simulation_results, context)

    # 4. Mostrar Resultados en Consola
    analysis = simulation_results.get('analysis', {})
    if analysis:
        print(f"\nProblema principal: {analysis.get('main_problem')}")
        print(f"Mercado objetivo:   {analysis.get('target_market')}")
        solutions = analysis.get('solutions', [])
        if solutions:
            print(f"\nSoluciones ({len(solutions)}):")
            for i, s in enumerate(solutions, 1):
                print(f"  {i}. [{s['mvp_difficulty'].upper()}] {s['title']} (~{s['mvp_time_estimate']})")
    else:
        print("\nNo se generó análisis en esta simulación.")


if __name__ == "__main__":
    main()
