# src/main.py

import random
from .simulation import run_simulation
from .config import INDUSTRY_NICHES

def main():
    """
    Main function to run the Meta-Problems simulation.
    """
    print("Iniciando Meta-Problems...")

    # 1. Selección de Nicho
    selected_niche = random.choice(INDUSTRY_NICHES)
    print(f"Nicho seleccionado: {selected_niche}")

    # 2. Ejecución de la Simulación
    identified_problems = run_simulation(selected_niche)

    # 3. Mostrar Resultados
    if identified_problems:
        print("\nProblemas de Alto Valor Identificados:")
        for i, problem in enumerate(identified_problems, 1):
            print(f"{i}. {problem}")
    else:
        print("\nNo se identificaron problemas de alto valor en esta simulación.")

if __name__ == "__main__":
    main()
