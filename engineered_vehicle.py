# engineered_vehicle.py
# Diego Lemus Sepulveda
# Nestor Eduardo Perez Avalos
class EngineeredVehicle:
    """
    Clase base (superclase) para demostrar HERENCIA y POLIMORFISMO.

    - Define la interfaz común (métodos accelerate() y decelerate()) que
      TODA subclase debe implementar. Esto habilita el POLIMORFISMO:
      distintos tipos de vehículos responderán a estos mismos métodos
      con comportamientos diferentes.

    - Nota sobre ENCAPSULAMIENTO en Python:
      Usamos el prefijo de un guion bajo (p. ej., _status, _temperature)
      para indicar que son miembros "protegidos" por convención. Python
      no impide su acceso, pero la convención comunica que no deberían
      tocarse desde fuera de la clase/subclase.
    """
    MAX_SPEED = 9999  # Constante genérica; las subclases pueden redefinir

    def __init__(self):
        # Atributos "protegidos" por convención (encapsulamiento suave)
        self.speed = 0
        self._status = "stopped"
        self._temperature = 20.0

    def get_status(self) -> str:
        """Devuelve un texto de estado; subclases pueden extenderlo/usar super()."""
        return self._status

    def stop(self) -> None:
        """Acción genérica de 'detener'; reutilizable por subclases (HERENCIA)."""
        self.speed = 0
        self._status = "stopped"

    # ===== Interfaz abstracta (POLIMORFISMO) =====
    # Las subclases DEBEN implementar estos métodos. Aquí se marca con
    # NotImplementedError para dejar claro que la implementación concreta
    # ocurre en las subclases (p. ej., Spacecraft).
    def accelerate(self) -> None:
        raise NotImplementedError

    def decelerate(self) -> None:
        raise NotImplementedError
