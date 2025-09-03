# test_spacecraft.py
# Script de prueba interactivo.
# Demuestra el POLIMORFISMO al invocar métodos definidos en la superclase
# (accelerate/decelerate) pero ejecutados por la implementación concreta de Spacecraft.
# También muestra la HERENCIA (Spacecraft hereda de EngineeredVehicle) y, al
# interior de Spacecraft, el ENCAPSULAMIENTO con métodos/atributos "protegidos".

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

    # Instanciamos la subclase Spacecraft:
    # - HERENCIA: Spacecraft extiende EngineeredVehicle.
    # - POLIMORFISMO: luego llamaremos accelerate/decelerate (misma interfaz).
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

    # Lógica específica de Spacecraft (no está en la base)
    print("\nDespegando…")
    ship.takeoff()

    # ===== POLIMORFISMO en acción =====
    # Estas llamadas usan la interfaz común definida en EngineeredVehicle,
    # pero ejecutan la implementación concreta de Spacecraft.
    print("\nAcelerando…")
    ship.accelerate()

    print("\nDesacelerando…")
    ship.decelerate()

    print("\nEstado final:")
    print(ship.get_status())
