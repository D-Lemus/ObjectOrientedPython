import os
import time
import random
from typing import Optional

# ======================
# SUPERCLASE
# ======================
class EngineeredVehicle:
    """
    Clase base (superclase) para demostrar HERENCIA y POLIMORFISMO.
    """
    MAX_SPEED = 9999

    def __init__(self):
        self.speed = 0
        self._status = "stopped"
        self._temperature = 20.0

    def get_status(self) -> str:
        return self._status

    def stop(self) -> None:
        self.speed = 0
        self._status = "stopped"

    # Métodos polimórficos a sobrescribir
    def accelerate(self) -> None:
        raise NotImplementedError

    def decelerate(self) -> None:
        raise NotImplementedError


# ======================
# SUBCLASE FORMULA ONE
# ======================
class FormulaOne(EngineeredVehicle):
    MAX_SPEED = 300
    MIN_SPEED = 0

    def __init__(self):
        super().__init__()
        self._degrees_right = 0
        self._degrees_left = 0
        self._rpms = 0
        self._wheel_status = 0

    def _get_wheel_status(self):
        return self._wheel_status

    def _set_wheel_status(self, new_wheel_status):
        self._wheel_status = new_wheel_status

    def _get_rpms(self):
        return self._rpms

    def _set_rpms(self, new_rpms):
        self._rpms = max(0, int(new_rpms))

    # POLIMORFISMO: redefine accelerate
    def accelerate(self) -> int:
        rpm = self._rpms
        while self.speed <= self.MAX_SPEED - 10:
            os.system('cls' if os.name == 'nt' else 'clear')
            if self.speed == 110:
                print('\nturn left? press "A" ')
                print('turn right? press "D" ')
                print('to continue accelerating just press ENTER')
                response = input("\nChoose: ").upper().strip()
                if response == 'A':
                    self.steer_left(self.speed)
                    input("press ENTER to continue accelerating")
                elif response == 'D':
                    self.steer_right(self.speed)
                    input("press ENTER to continue accelerating")
            self._status = "moving"
            self.speed += 10
            rpm += 100
            self._set_rpms(rpm)
            print(f"speed: {self.speed} km/h")
            print(f"RPMs: {self._get_rpms()}")
            print(f"Status: {self._status}")
            time.sleep(0.05)
        return rpm

    # POLIMORFISMO: redefine decelerate
    def decelerate(self, rpm: int | None = None):
        if rpm is not None:
            self._set_rpms(rpm)
        while self.speed > 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            if self.speed == 110:
                print('\nturn left? press "A" ')
                print('turn right? press "D" ')
                print('to continue decelerating just press ENTER')
                response = input("\nChoose: ").upper().strip()
                if response == 'A':
                    self.steer_left(self.speed)
                    input("press ENTER to continue decelerating")
                elif response == 'D':
                    self.steer_right(self.speed)
                    input("press ENTER to continue decelerating")
            self.speed = max(0, self.speed - 10)
            self._set_rpms(self._get_rpms() - 100)
            print(f"speed: {self.speed} km/h")
            print(f"RPMs: {self._get_rpms()}")
            if self.speed == 0:
                self._status = "stopped"
                print(f"Status: {self._status}")
            time.sleep(0.05)

    def steer_right(self, degrees_right: int):
        if self.speed <= 120:
            print(f"steering {degrees_right} degrees to the RIGHT")
        else:
            print("too fast. slow down.")

    def steer_left(self, degrees_left: int):
        if self.speed <= 120:
            print(f"steering {degrees_left} degrees to the LEFT")
        else:
            print("too fast. slow down.")


# ======================
# SUBCLASE SPACECRAFT
# ======================
class Spacecraft(EngineeredVehicle):
    MAX_SPEED = 28000
    EXPLODE_PROB_TAKEOFF = 0.001
    EXPLODE_PROB_ACCEL = 0.0002
    FUEL_BURN_RATE = 5

    def __init__(self, country: str, length_m: float, fuel: float,
                 has_crew: bool = True, crew_size: Optional[int] = None,
                 name: str = "Unnamed Ship"):
        super().__init__()
        if length_m < 100:
            raise ValueError("La nave debe medir al menos 100 metros de longitud.")
        if fuel < 0:
            raise ValueError("El combustible no puede ser negativo.")

        self.country = country.strip() or "Unknown"
        self.length_m = float(length_m)
        self.fuel = float(fuel)
        self.has_crew = bool(has_crew)
        self.crew_size = (int(crew_size) if (has_crew and crew_size) else 0)
        self.name = name
        self._status = "on pad"

    def _check_explosion(self, prob: float) -> bool:
        return random.random() < prob

    def _burn_fuel(self, amount: float) -> None:
        self.fuel = max(0.0, self.fuel - amount)
        if self.fuel == 0:
            self._status = "fuel depleted"

    def get_status(self) -> str:
        base = super().get_status()
        crew_txt = f"{self.crew_size} crew" if self.has_crew else "uncrewed"
        return (f"{self.name} [{self.country}] – {base} – fuel: {self.fuel:.1f} – "
                f"{crew_txt} – length: {self.length_m:.1f} m")

    def takeoff(self, countdown: int = 3) -> None:
        if self.fuel <= 0:
            print(f"[{self.name}] Sin combustible para despegar.")
            return
        if self._status not in ("on pad", "stopped"):
            print(f"[{self.name}] No se puede despegar; estado actual: {self._status}")
            return
        for t in range(countdown, 0, -1):
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"[{self.name}] T-{t}…")
            time.sleep(1)
        if self._check_explosion(self.EXPLODE_PROB_TAKEOFF):
            self._status = "exploded"
            self.speed = 0
            print(f"[{self.name}] 💥 ¡Explosión durante el despegue!")
            return
        self._status = "ascending"
        print(f"[{self.name}] 🚀 Despegue exitoso. Ascendiendo…")
        for _ in range(3):
            if self.fuel <= 0 or self._status == "exploded":
                break
            self.speed += 200
            self._burn_fuel(self.FUEL_BURN_RATE * 2)
            print(f"[{self.name}] speed: {self.speed} km/h | fuel: {self.fuel:.1f}")
            time.sleep(1)
        if self._status != "exploded":
            self._status = "in flight"

    # POLIMORFISMO: redefine accelerate
    def accelerate(self) -> None:
        if self._status in ("on pad", "stopped"):
            print(f"[{self.name}] Llama a takeoff() antes de acelerar.")
            return
        if self._status in ("exploded", "fuel depleted"):
            print(f"[{self.name}] No puede acelerar; estado: {self._status}")
            return
        self._status = "accelerating"
        print(f"[{self.name}] Acelerando… (Ctrl+C para abortar)")
        try:
            while self.fuel > 0 and self.speed < self.MAX_SPEED:
                os.system('cls' if os.name == 'nt' else 'clear')
                if self._check_explosion(self.EXPLODE_PROB_ACCEL):
                    self._status = "exploded"
                    self.speed = 0
                    print(f"[{self.name}] 💥 ¡Falla catastrófica en vuelo!")
                    break
                self.speed += 500
                self._burn_fuel(self.FUEL_BURN_RATE)
                self._temperature += 1.5
                print(f"[{self.name}] status: {self._status} | speed: {self.speed} km/h | "
                      f"fuel: {self.fuel:.1f} | temp: {self._temperature:.1f} °C")
                time.sleep(1)
            if self._status not in ("exploded", "fuel depleted"):
                self._status = "coasting"
                print(f"[{self.name}] Vuelo en inercia. Velocidad: {self.speed} km/h")
        except KeyboardInterrupt:
            self._status = "manual hold"
            print(f"[{self.name}] Aceleración interrumpida manualmente.")

    # POLIMORFISMO: redefine decelerate
    def decelerate(self) -> None:
        if self._status == "exploded":
            print(f"[{self.name}] No puede frenar; estado: {self._status}")
            return
        self._status = "decelerating"
        while self.speed > 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.speed = max(0, self.speed - 800)
            self._burn_fuel(self.FUEL_BURN_RATE * 0.5)
            print(f"[{self.name}] status: {self._status} | speed: {self.speed} km/h | fuel: {self.fuel:.1f}")
            time.sleep(1)
        self.stop()
        print(f"[{self.name}] Detenida.")


# ======================
# MAIN DEMO POLIMÓRFICA
# ======================
def ask_float(prompt: str, min_value: float | None = None) -> float:
    while True:
        try:
            val = float(input(prompt).strip())
            if min_value is not None and val < min_value:
                print(f"Debe ser >= {min_value}. Intenta de nuevo.")
                continue
            return val
        except ValueError:
            print("Valor inválido. Intenta de nuevo.")

def ask_int(prompt: str, min_value: int | None = None) -> int:
    while True:
        try:
            val = int(input(prompt).strip())
            if min_value is not None and val < min_value:
                print(f"Debe ser >= {min_value}. Intenta de nuevo.")
                continue
            return val
        except ValueError:
            print("Valor inválido. Intenta de nuevo.")

def ask_yes_no(prompt: str) -> bool:
    while True:
        ans = input(prompt + " [s/n]: ").strip().lower()
        if ans in ("s","si","sí","y","yes"): return True
        if ans in ("n","no"): return False
        print("Responde con s/n.")

if __name__ == "__main__":
    print("=== Demo Polimórfica ===")
    print("1) Formula One")
    print("2) Spacecraft")
    choice = input("Elige vehículo [1/2]: ").strip()

    if choice == "1":
        car = FormulaOne()
        print("\n== DEMO F1 ==")
        rpm = car.accelerate()
        input("press ENTER to decelerate")
        car.decelerate(rpm if rpm is not None else 3000)
        print("Estado final:", car.get_status())

    elif choice == "2":
        print("\n== CONFIGURACIÓN SPACECRAFT ==")
        name = input("Nombre de la nave (opcional): ").strip() or "Unnamed Ship"
        country = input("País al que pertenece: ").strip() or "Unknown"
        length_m = ask_float("Longitud (m) (mínimo 100): ", min_value=100.0)
        fuel = ask_float("Combustible inicial (unidades): ", min_value=0.0)
        has_crew = ask_yes_no("¿Tiene tripulación?")
        crew_size = ask_int("Tamaño de la tripulación: ", min_value=0) if has_crew else 0

        ship = Spacecraft(country=country, length_m=length_m, fuel=fuel,
                          has_crew=has_crew, crew_size=crew_size, name=name)

        print("\nEstado inicial:")
        print(ship.get_status())
        print("\nDespegando…")
        ship.takeoff()
        print("\nAcelerando…")
        ship.accelerate()
        print("\nDesacelerando…")
        ship.decelerate()
        print("\nEstado final:")
        print(ship.get_status())

    else:
        print("Opción no válida.")


