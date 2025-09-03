# spacecraft.py
# Nestor Eduardo Perez Avalos
import os
import time
import random
from typing import Optional
from engineered_vehicle import EngineeredVehicle

class Spacecraft(EngineeredVehicle):
    """
    Subclase concreta que DEMUESTRA HERENCIA + POLIMORFISMO.

    HERENCIA:
      - 'Spacecraft' hereda de 'EngineeredVehicle' -> reutiliza y/o extiende
        atributos y métodos base (por ejemplo, usa stop(), get_status()).
      - Llama a super().__init__() para inicializar la parte "vehículo".

    POLIMORFISMO:
      - Sobrescribe accelerate() y decelerate() con su propia lógica,
        pero conserva la MISMA interfaz que 'EngineeredVehicle'.
        Así, un cliente que maneje 'EngineeredVehicle' puede invocar
        accelerate() sin importar si la instancia es Spacecraft u otra subclase.

    ENCAPSULAMIENTO:
      - Métodos internos con guion bajo (_check_explosion, _burn_fuel) y
        atributos "protegidos" por convención (_status, _temperature)
        encapsulan la lógica/estado interno para no ser manipulados desde fuera.
    """
    # Constantes específicas de Spacecraft (pueden diferir de la superclase)
    MAX_SPEED = 28000              # ~km/h (referencia a velocidad orbital baja)
    EXPLODE_PROB_TAKEOFF = 0.001   # 0.1% de probabilidad durante despegue
    EXPLODE_PROB_ACCEL   = 0.0002  # 0.02% por "tick" mientras acelera
    FUEL_BURN_RATE       = 5       # Consumo por "tick" (unidades arbitrarias)

    def __init__(
        self,
        country: str,
        length_m: float,
        fuel: float,
        has_crew: bool = True,
        crew_size: Optional[int] = None,
        name: str = "Unnamed Ship"
    ):
        # Llamada al constructor de la superclase -> HERENCIA
        super().__init__()

        # Validaciones propias de Spacecraft
        if length_m < 100:
            raise ValueError("La nave debe medir al menos 100 metros de longitud.")
        if fuel < 0:
            raise ValueError("El combustible no puede ser negativo.")

        # Atributos públicos y "protegidos"
        self.country = country.strip() or "Unknown"
        self.length_m = float(length_m)
        self.fuel = float(fuel)
        self.has_crew = bool(has_crew)
        self.crew_size = (int(crew_size) if (has_crew and crew_size) else 0)
        if self.has_crew and self.crew_size < 0:
            raise ValueError("El tamaño de la tripulación no puede ser negativo.")
        self.name = name

        # Estado inicial (protegido por convención) -> ENCAPSULAMIENTO suave
        self._status = "on pad"

    # ====== Métodos internos (encapsulan detalles) -> ENCAPSULAMIENTO ======
    def _check_explosion(self, prob: float) -> bool:
        """Evento aleatorio poco probable. No debería invocarse externamente."""
        return random.random() < prob

    def _burn_fuel(self, amount: float) -> None:
        """Modifica el estado interno de combustible y status; uso interno."""
        self.fuel = max(0.0, self.fuel - amount)
        if self.fuel == 0:
            self._status = "fuel depleted"

    # ====== Información/estado (puede extender get_status de la superclase) ======
    def get_status(self) -> str:
        """
        Extiende el get_status() heredado con info adicional del Spacecraft.
        Usa super().get_status() para reutilizar la base -> HERENCIA.
        """
        base = super().get_status()
        crew_txt = f"{self.crew_size} crew" if self.has_crew else "uncrewed"
        return (f"{self.name} [{self.country}] – {base} – fuel: {self.fuel:.1f} – "
                f"{crew_txt} – length: {self.length_m:.1f} m")

    # ====== Operación específica de Spacecraft ======
    def takeoff(self, countdown: int = 3) -> None:
        """
        Lógica de despegue propia de la nave. No existe en la superclase.
        Cambia estado interno y valida condiciones (combustible/estado).
        """
        if self.fuel <= 0:
            print(f"[{self.name}] Sin combustible para despegar.")
            return
        if self._status not in ("on pad", "stopped"):
            print(f"[{self.name}] No se puede despegar; estado actual: {self._status}")
            return

        # Cuenta regresiva (simulación)
        for t in range(countdown, 0, -1):
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"[{self.name}] T-{t}…")
            time.sleep(1)

        # Riesgo pequeño de explosión durante despegue (uso de método interno)
        if self._check_explosion(self.EXPLODE_PROB_TAKEOFF):
            self._status = "exploded"
            self.speed = 0
            print(f"[{self.name}] 💥 ¡Explosión durante el despegue!")
            return

        self._status = "ascending"
        print(f"[{self.name}] 🚀 Despegue exitoso. Ascendiendo…")

        # Ascenso inicial (consumo y cambio de estado interno)
        for _ in range(3):
            if self.fuel <= 0 or self._status == "exploded":
                break
            self.speed += 200
            self._burn_fuel(self.FUEL_BURN_RATE * 2)
            print(f"[{self.name}] speed: {self.speed} km/h | fuel: {self.fuel:.1f}")
            time.sleep(1)

        if self._status != "exploded":
            self._status = "in flight"

    # ====== Interfaz polimórfica (sobrescribe métodos abstractos) ======
    def accelerate(self) -> None:
        """
        POLIMORFISMO: implementación concreta de accelerate() para Spacecraft.
        Un cliente puede llamar ship.accelerate() sin saber si es un EngineeredVehicle,
        un Spacecraft u otra subclase; se ejecuta la versión adecuada.
        """
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

                # Evento raro de fallo durante aceleración (detalle encapsulado)
                if self._check_explosion(self.EXPLODE_PROB_ACCEL):
                    self._status = "exploded"
                    self.speed = 0
                    print(f"[{self.name}] 💥 ¡Falla catastrófica en vuelo!")
                    break

                # Dinámica simple: aumenta velocidad, consume combustible y sube temperatura
                self.speed += 500
                self._burn_fuel(self.FUEL_BURN_RATE)
                self._temperature += 1.5

                print(f"[{self.name}] status: {self._status} | speed: {self.speed} km/h | "
                      f"fuel: {self.fuel:.1f} | temp: {self._temperature:.1f} °C")
                time.sleep(1)

            # Cuando termina la aceleración sin explotar/agotarse el combustible
            if self._status not in ("exploded", "fuel depleted"):
                self._status = "coasting"
                print(f"[{self.name}] Vuelo en inercia. Velocidad: {self.speed} km/h")

        except KeyboardInterrupt:
            # Permite romper el bucle manualmente (simulación)
            self._status = "manual hold"
            print(f"[{self.name}] Aceleración interrumpida manualmente.")

    def decelerate(self) -> None:
        """
        POLIMORFISMO: implementación concreta de decelerate() para Spacecraft.
        Igual interfaz que en la clase base, pero con lógica específica
        (retropropulsión/freno atmosférico simulado).
        """
        if self._status == "exploded":
            print(f"[{self.name}] No puede frenar; estado: {self._status}")
            return

        self._status = "decelerating"
        while self.speed > 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            # Freno "fuerte" por tick; también quema algo de combustible
            self.speed = max(0, self.speed - 800)
            self._burn_fuel(self.FUEL_BURN_RATE * 0.5)
            print(f"[{self.name}] status: {self._status} | speed: {self.speed} km/h | fuel: {self.fuel:.1f}")
            time.sleep(1)

        # Reutiliza stop() heredado -> HERENCIA
        self.stop()
        print(f"[{self.name}] Detenida.")
