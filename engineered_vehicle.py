# engineered_vehicle.py
class EngineeredVehicle:
    """Interfaz base para demostrar polimorfismo."""
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

    # Métodos que las subclases deben implementar (polimorfismo)
    def accelerate(self) -> None:
        raise NotImplementedError

    def decelerate(self) -> None:
        raise NotImplementedError
