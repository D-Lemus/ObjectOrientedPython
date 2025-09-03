# testSpacecraft.py
# DIEGO LEMUS SEPULVEDA
# NESTOR EDUARDO PEREZ AVALOS

from spacecraft import Spacecraft

def ask_float(prompt: str, min_value: float = None) -> float:
    while True:
        try:
            value = float(input(prompt).strip())
            if min_value is not None and value < min_value:
                print(f"Debe ser >= {min_value}. Intenta de nuevo.")
                continue
            return value
        except ValueError:
            print("Valor inválido. Intenta de nuevo.")

def ask_int(prompt: str, min_value: int = None) -> int:
    while True:
        try:
            value = int(input(prompt).strip())
            if min_value is not None and value < min_value:
                print(f"Debe ser >= {min_value}. Intenta de nuevo.")
                continue
            return value
        except ValueError:
            print("Valor inválido. Intenta de nuevo.")

def ask_yes_no(prompt: str) -> bool:
    while True:
        ans = input(prompt + " [s/n]: ").strip().lower()
        if ans in ("s", "si", "sí", "y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Responde con s/n.")

if __name__ == "__main__":
    print("=== Configuración de Spacecraft ===")
    name = input("Nombre de la nave (opcional): ").strip() or "Unnamed Ship"
    country = input("País al que pertenece: ").strip() or "Unknown"
    length_m = ask_float("Longitud (m) (mínimo 100): ", min_value=100.0)
    fuel = ask_float("Combustible inicial (unidades): ", min_value=0.0)
    has_crew = ask_yes_no("¿Tiene tripulación?")
    crew_size = 0
    if has_crew:
        crew_size = ask_int("Tamaño de la tripulación: ", min_value=0)

    # Crear instancia
    ship = Spacecraft(
        country=country,
        length_m=length_m,
        fuel=fuel,
        has_crew=has_crew,
        crew_size=crew_size,
        name=name
    )

    print("\nEstado inicial:")
    print(ship.get_status())

    # Flujo simple de demostración
    print("\nDespegando…")
    ship.takeoff()

    print("\nAcelerando…")
    ship.accelerate()

    print("\nDesacelerando…")
    ship.decelerate()

    print("\nEstado final:")
    print(ship.get_status())
