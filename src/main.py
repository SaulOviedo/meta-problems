# src/main.py

import random
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
            
            # Escribir todos los detalles del perfil de la persona
            for key, value in persona.items():
                # Formatear la clave para que sea legible
                formatted_key = key.replace('_', ' ').title()
                if formatted_key not in ['Name', 'Archetype']: # Evitar duplicados
                    f.write(f"**{formatted_key}:** {value}\n")
            f.write("\n")

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

    # 1. Generación de Contexto
    context = generate_context()
    print(f"Contexto seleccionado: Industria '{context['industry']}' en '{context['location']}'")

    # 2. Ejecución de la Simulación
    simulation_results = run_simulation(context)

    # 3. Guardar Resultados
    save_results_to_file(simulation_results, context)

    # 4. Mostrar Resultados en Consola
    identified_problems = simulation_results['high_value_problems']
    if identified_problems:
        print("\nProblemas de Alto Valor Identificados:")
        for i, problem in enumerate(identified_problems, 1):
            print(f"{i}. {problem}")
    else:
        print("\nNo se identificaron problemas de alto valor en esta simulación.")

    # 4. Guardar Resultados en Archivo
    save_results_to_file(simulation_results, context)

if __name__ == "__main__":
    main()
