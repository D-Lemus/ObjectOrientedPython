# spacecraft.py
import os
import time
import random
from typing import Optional
from engineered_vehicle import EngineeredVehicle

class Spacecraft(EngineeredVehicle):
    """
    Requisitos:
    - combustible (fuel)
    - pertenece a un país
    - velocidad aumenta cada segundo
    - puede despegar (takeoff)
    - probabilidad muy baja de explotar
    - puede tener tripulantes o no
    - longitud mínima 100 m
    """
    MAX_SPEED = 28000           # km/h aprox. órbita baja (referencia)
    EXPLODE_PROB_TAKEOFF = 0.001   # 0.1% durante despegue
    EXPLODE_PROB_ACCEL = 0.0002    # 0.02% por “tick” al acelerar
    FUEL_BURN_RATE = 5             # consumo por “tick” (unidades arbitrarias)

    def __init__(
        self,
        country: str,
        length_m: float,
        fuel: float,
        has_crew: bool = True,
        crew_size: Optional[int] = None,
        name: str = "Unnamed Ship"
    ):
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
        if self.has_crew and self.crew_size < 0:
            raise ValueError("El tamaño de la tripulación no puede ser negativo.")
        self.name = name
        self._status = "on pad"  # en plataforma

    # -------- utilidades internas --------
    def _check_explosion(self, prob: float) -> bool:
        return random.random() < prob

    def _burn_fuel(self, amount: float) -> None:
        self.fuel = max(0.0, self.fuel - amount)
        if self.fuel == 0:
            self._status = "fuel depleted"

    # -------- info / estado --------
    def get_status(self) -> str:
        base = super().get_status()
        crew_txt = f"{self.crew_size} crew" if self.has_crew else "uncrewed"
        return (f"{self.name} [{self.country}] – {base} – fuel: {self.fuel:.1f} – "
                f"{crew_txt} – length: {self.length_m:.1f} m")

    # -------- operaciones --------
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

        # ascenso inicial corto
        for _ in range(3):
            if self.fuel <= 0 or self._status == "exploded":
                break
            self.speed += 200
            self._burn_fuel(self.FUEL_BURN_RATE * 2)
            print(f"[{self.name}] speed: {self.speed} km/h | fuel: {self.fuel:.1f}")
            time.sleep(1)

        if self._status != "exploded":
            self._status = "in flight"

    # ---- interfaz polimórfica ----
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

    def decelerate(self) -> None:
        if self._status == "exploded":
            print(f"[{self.name}] No puede frenar; estado: {self._status}")
            return

        self._status = "decelerating"
        while self.speed > 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.speed = max(0, self.speed - 800)  # retropropulsión / freno atmosférico
            self._burn_fuel(self.FUEL_BURN_RATE * 0.5)
            print(f"[{self.name}] status: {self._status} | speed: {self.speed} km/h | fuel: {self.fuel:.1f}")
            time.sleep(1)
        self.stop()
        print(f"[{self.name}] Detenida.")
