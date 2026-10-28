import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

# Exact SI physical constants (2019 redefinition)
EPSILON_0 = 8.8541878128e-12      # Vacuum permittivity [F/m]
MU_0 = 1.25663706212e-6           # Vacuum permeability [N/A^2]
C_EXACT = 299792458.0             # Exact speed of light in vacuum [m/s]

@dataclass(frozen=True)
class MaxwellEquation:
    name: str
    differential_form: str
    integral_form: str
    physical_meaning: str
    discovery_context: str

MAXWELL_EQUATIONS: List[MaxwellEquation] = [
    MaxwellEquation(
        name="Gauss's Law for Electricity",
        differential_form=r"\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}",
        integral_form=r"\oint_{\partial V} \mathbf{E} \cdot d\mathbf{A} = \frac{Q_{\text{encl}}}{\varepsilon_0}",
        physical_meaning="Electric charges act as sources or sinks of electric field flux.",
        discovery_context="Formulated by Carl Friedrich Gauss (1835); describes Coulomb electrostatic forces.",
    ),
    MaxwellEquation(
        name="Gauss's Law for Magnetism",
        differential_form=r"\nabla \cdot \mathbf{B} = 0",
        integral_form=r"\oint_{\partial V} \mathbf{B} \cdot d\mathbf{A} = 0",
        physical_meaning="Magnetic field lines are continuous closed loops; magnetic monopoles do not exist.",
        discovery_context="Absence of magnetic charges implies magnetic flux through any closed Gaussian surface vanishes identically.",
    ),
    MaxwellEquation(
        name="Maxwell-Faraday Law of Induction",
        differential_form=r"\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}",
        integral_form=r"\oint_{\partial \Sigma} \mathbf{E} \cdot d\mathbf{l} = -\frac{d}{dt}\iint_{\Sigma} \mathbf{B} \cdot d\mathbf{A}",
        physical_meaning="A time-varying magnetic field generates a spatially circulating electric field.",
        discovery_context="Discovered experimentally by Michael Faraday (1831); foundational principle of electromagnetic induction and dynamos.",
    ),
    MaxwellEquation(
        name="Ampère-Maxwell Law (with Displacement Current)",
        differential_form=r"\nabla \times \mathbf{B} = \mu_0 \mathbf{J} + \mu_0 \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}",
        integral_form=r"\oint_{\partial \Sigma} \mathbf{B} \cdot d\mathbf{l} = \mu_0 I_{\text{encl}} + \mu_0 \varepsilon_0 \frac{d}{dt}\iint_{\Sigma} \mathbf{E} \cdot d\mathbf{A}",
        physical_meaning="Electric currents and time-varying electric fields generate circulating magnetic fields.",
        discovery_context="Maxwell's revolutionary addition (1861): the displacement current term ensures continuity of electric charge and enables electromagnetic wave propagation.",
    ),
]

class ElectrodynamicsEngine:
    """Analytical and numerical engine for Maxwell's electrodynamics and EM waves."""

    @staticmethod
    def calculate_wave_speed(eps0: float = EPSILON_0, mu0: float = MU_0) -> float:
        """Calculates electromagnetic wave propagation velocity: c = 1 / sqrt(mu_0 * eps_0)."""
        if eps0 <= 0 or mu0 <= 0:
            raise ValueError("Permittivity and permeability must be strictly positive.")
        return 1.0 / math.sqrt(eps0 * mu0)

    @staticmethod
    def poynting_vector_magnitude(e_amplitude: float, eps0: float = EPSILON_0, mu0: float = MU_0) -> float:
        """
        Calculates time-averaged Poynting vector flux magnitude <S> = 1/2 * eps_0 * c * E_0^2.
        Units: W/m^2 (Watts per square meter).
        """
        c = ElectrodynamicsEngine.calculate_wave_speed(eps0, mu0)
        return 0.5 * eps0 * c * (e_amplitude ** 2)

    @staticmethod
    def sample_plane_wave(
        wavelength: float = 1.0,
        e0: float = 1.0,
        num_points: int = 40,
        t: float = 0.0,
    ) -> List[Tuple[float, float, float, float]]:
        """
        Samples a transverse harmonic EM plane wave traveling in the +z direction.
        Returns tuples of (z, E_x, B_y, S_z).
        """
        c = C_EXACT
        k = 2.0 * math.pi / wavelength
        omega = c * k
        b0 = e0 / c

        samples: List[Tuple[float, float, float, float]] = []
        dz = wavelength / num_points
        for i in range(num_points + 1):
            z = i * dz
            phase = k * z - omega * t
            ex = e0 * math.cos(phase)
            by = b0 * math.cos(phase)
            sz = (ex * by) / MU_0
            samples.append((z, ex, by, sz))

        return samples
