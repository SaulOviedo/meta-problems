# src/main.py

import random
import os
from datetime import datetime
from .simulation import run_simulation
from .config import INDUSTRY_NICHES

def save_results_to_file(simulation_data):
    """
    Saves the full simulation data to a Markdown file in the data directory.
    """
    if not os.path.exists('data'):
        os.makedirs('data')

    niche = simulation_data['niche']
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/resultado_{niche.replace(' ', '_')}_{timestamp}.md"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# Simulación de Meta-Problemas: {niche}\n\n")
        f.write(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Entrevistas de Fricción\n\n")
        for interview in simulation_data['interviews']:
            persona = interview['persona']
            f.write(f"### Perfil: {persona['name']} ({persona['archetype']})\n\n")
            f.write(f"**Rol:** {persona['title']}\n\n")
            f.write(f"**Bio:** {persona['bio']}\n\n")
            
            f.write("#### Registro de la Entrevista\n\n")
            for entry in interview['log']:
                f.write(f"**P:** {entry['question']}\n\n")
                f.write(f"**R:** {entry['answer']}\n\n")
            f.write("---\n\n")

        f.write("## Análisis de Problemas\n\n")
        problems = simulation_data['high_value_problems']
        if problems:
            f.write("### Problemas de Alto Valor Identificados\n\n")
            for i, problem in enumerate(problems, 1):
                f.write(f"{i}. {problem}\n")
        else:
            f.write("No se identificaron problemas de alto valor en esta simulación.\n")
    
    print(f"\nResultados completos de la simulación guardados en: {filename}")

def main():
    """
    Main function to run the Meta-Problems simulation.
    """
    print("Iniciando Meta-Problems...")

    # 1. Selección de Nicho
    selected_niche = random.choice(INDUSTRY_NICHES)
    print(f"Nicho seleccionado: {selected_niche}")

    # 2. Ejecución de la Simulación
    simulation_results = run_simulation(selected_niche)

    # 3. Mostrar Resultados
    identified_problems = simulation_results['high_value_problems']
    if identified_problems:
        print("\nProblemas de Alto Valor Identificados:")
        for i, problem in enumerate(identified_problems, 1):
            print(f"{i}. {problem}")
    else:
        print("\nNo se identificaron problemas de alto valor en esta simulación.")

    # 4. Guardar Resultados en Archivo
    save_results_to_file(simulation_results)

if __name__ == "__main__":
    main()
