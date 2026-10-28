import math
from dataclasses import dataclass
from typing import List, Tuple

# Physical constants
C_LIGHT = 299792458.0              # Speed of light [m/s]
M_ELECTRON = 9.1093837e-31         # Electron mass [kg]
E_REST_ELECTRON_EV = 510998.95     # Electron rest energy ~ 511 keV

# Complex 4x4 matrix implementation for Dirac spinor algebra
class Matrix4x4:
    def __init__(self, data: List[List[complex]]):
        if len(data) != 4 or any(len(row) != 4 for row in data):
            raise ValueError("Matrix must be 4x4.")
        self.data = data

    @staticmethod
    def zero() -> 'Matrix4x4':
        return Matrix4x4([[0.0j for _ in range(4)] for _ in range(4)])

    @staticmethod
    def identity() -> 'Matrix4x4':
        return Matrix4x4([[1.0 + 0.0j if i == j else 0.0j for j in range(4)] for i in range(4)])

    def __add__(self, other: 'Matrix4x4') -> 'Matrix4x4':
        return Matrix4x4([[self.data[i][j] + other.data[i][j] for j in range(4)] for i in range(4)])

    def __sub__(self, other: 'Matrix4x4') -> 'Matrix4x4':
        return Matrix4x4([[self.data[i][j] - other.data[i][j] for j in range(4)] for i in range(4)])

    def __mul__(self, other: 'Matrix4x4') -> 'Matrix4x4':
        res = [[0.0j for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for k in range(4):
                if self.data[i][k] != 0.0j:
                    for j in range(4):
                        res[i][j] += self.data[i][k] * other.data[k][j]
        return Matrix4x4(res)

    def scale(self, scalar: complex) -> 'Matrix4x4':
        return Matrix4x4([[self.data[i][j] * scalar for j in range(4)] for i in range(4)])

    def anticommutator(self, other: 'Matrix4x4') -> 'Matrix4x4':
        """Computes Clifford anticommutator {A, B} = AB + BA."""
        return (self * other) + (other * self)

    def trace(self) -> complex:
        return sum(self.data[i][i] for i in range(4))

    def is_close(self, other: 'Matrix4x4', tol: float = 1e-9) -> bool:
        for i in range(4):
            for j in range(4):
                diff = abs(self.data[i][j] - other.data[i][j])
                if diff > tol:
                    return False
        return True

def get_dirac_gamma_matrices() -> List[Matrix4x4]:
    """
    Constructs the 4x4 Dirac Gamma matrices in the standard Dirac-Pauli representation:
    gamma^0 = diag(1, 1, -1, -1)
    gamma^1 = [[0, sigma_x], [-sigma_x, 0]]
    gamma^2 = [[0, sigma_y], [-sigma_y, 0]]
    gamma^3 = [[0, sigma_z], [-sigma_z, 0]]
    """
    # gamma^0
    g0 = Matrix4x4([
        [1.0,  0.0,  0.0,  0.0],
        [0.0,  1.0,  0.0,  0.0],
        [0.0,  0.0, -1.0,  0.0],
        [0.0,  0.0,  0.0, -1.0],
    ])

    # gamma^1
    g1 = Matrix4x4([
        [0.0,  0.0,  0.0,  1.0],
        [0.0,  0.0,  1.0,  0.0],
        [0.0, -1.0,  0.0,  0.0],
        [-1.0, 0.0,  0.0,  0.0],
    ])

    # gamma^2 (contains imaginary unit i)
    g2 = Matrix4x4([
        [0.0,  0.0,  0.0, -1.0j],
        [0.0,  0.0,  1.0j, 0.0],
        [0.0,  1.0j, 0.0,  0.0],
        [-1.0j, 0.0, 0.0,  0.0],
    ])

    # gamma^3
    g3 = Matrix4x4([
        [0.0,  0.0,  1.0,  0.0],
        [0.0,  0.0,  0.0, -1.0],
        [-1.0, 0.0,  0.0,  0.0],
        [0.0,  1.0,  0.0,  0.0],
    ])

    return [g0, g1, g2, g3]

class RelativisticDiracEngine:
    """Computes relativistic dispersion, Clifford algebra invariants, and Dirac sea energies."""

    @staticmethod
    def verify_clifford_algebra() -> List[Tuple[int, int, bool]]:
        """
        Verifies the Clifford algebra anti-commutation relations:
        {gamma^mu, gamma^nu} = 2 * eta^(mu nu) * I_4
        where eta = diag(1, -1, -1, -1).
        """
        gammas = get_dirac_gamma_matrices()
        eta = [1.0, -1.0, -1.0, -1.0]
        results = []

        for mu in range(4):
            for nu in range(4):
                anticomm = gammas[mu].anticommutator(gammas[nu])
                expected_factor = 2.0 * (eta[mu] if mu == nu else 0.0)
                expected = Matrix4x4.identity().scale(expected_factor)
                matches = anticomm.is_close(expected)
                results.append((mu, nu, matches))

        return results

    @staticmethod
    def dispersion_energy(momentum_ev_c: float, mass_ev_c2: float = E_REST_ELECTRON_EV) -> Tuple[float, float]:
        """
        Computes positive and negative relativistic energy states:
        E = +/- sqrt((p*c)^2 + (m*c^2)^2).
        Returns (E_plus, E_minus) in eV.
        """
        energy_mag = math.sqrt(momentum_ev_c ** 2 + mass_ev_c2 ** 2)
        return (energy_mag, -energy_mag)
