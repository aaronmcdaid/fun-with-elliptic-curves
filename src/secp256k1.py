"""secp256k1 elliptic curve implementation and visualization."""

import matplotlib

matplotlib.use("TkAgg")  # Use interactive Tkinter backend
from dataclasses import dataclass
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np

# secp256k1 parameters
# Prime field
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
A = 0  # Coefficient a in y² = x³ + ax + b
B = 7  # Coefficient b in y² = x³ + ax + b
# Order of the curve
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
# Generator point x
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
# Generator point y
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8


@dataclass
class Point:
    """Represents a point on the secp256k1 elliptic curve."""
    x: Optional[int] = None
    y: Optional[int] = None

    def __post_init__(self) -> None:
        """Validate point after dataclass initialization."""
        if not self.is_infinity() and not self.is_on_curve():
            raise ValueError(
                f"Point ({self.x}, {self.y}) is not on the secp256k1 curve"
            )

    def is_infinity(self) -> bool:
        """Check if this is the point at infinity (identity element)."""
        return self.x is None and self.y is None

    def is_on_curve(self) -> bool:
        """Check if the point is on the secp256k1 curve: y² = x³ + 7 (mod p)."""
        if self.is_infinity():
            return True

        assert self.x is not None and self.y is not None
        left = (self.y * self.y) % P
        right = (self.x * self.x * self.x + B) % P
        return left == right

    def __add__(self, other: "Point") -> "Point":
        """Add two points on the elliptic curve."""
        return point_add(self, other)

    def __repr__(self) -> str:
        """String representation of the point."""
        if self.is_infinity():
            return "Point(∞)"
        assert self.x is not None and self.y is not None
        return f"Point({hex(self.x)}, {hex(self.y)})"


def mod_inverse(a: int, m: int) -> int:
    """Calculate modular inverse using extended Euclidean algorithm."""
    if a < 0:
        a = (a % m + m) % m

    # Extended Euclidean Algorithm
    old_r, r = a, m
    old_s, s = 1, 0

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s

    return old_s % m


def point_add(p1: Point, p2: Point) -> Point:
    """Add two points on the secp256k1 elliptic curve."""
    # Handle point at infinity
    if p1.is_infinity():
        return Point(p2.x, p2.y)
    if p2.is_infinity():
        return Point(p1.x, p1.y)

    # Both points are finite, so coordinates are not None
    assert p1.x is not None and p1.y is not None
    assert p2.x is not None and p2.y is not None

    # Handle point doubling
    if p1.x == p2.x:
        if p1.y == p2.y:
            # Point doubling: P + P
            s = (3 * p1.x * p1.x * mod_inverse(2 * p1.y, P)) % P
        else:
            # P + (-P) = ∞
            return Point()  # Point at infinity
    else:
        # Different points: P + Q
        s = ((p2.y - p1.y) * mod_inverse(p2.x - p1.x, P)) % P

    # Calculate new point
    x3 = (s * s - p1.x - p2.x) % P
    y3 = (s * (p1.x - x3) - p1.y) % P

    return Point(x3, y3)


def point_multiply(k: int, point: Point) -> Point:
    """Multiply a point by a scalar using double-and-add method."""
    if k == 0:
        return Point()  # Point at infinity
    if k == 1:
        return Point(point.x, point.y)

    result = Point()  # Start with point at infinity
    addend = Point(point.x, point.y)

    while k:
        if k & 1:
            result = result + addend
        addend = addend + addend
        k >>= 1

    return result


def plot_curve_over_small_field(p: int = 97, a: int = 0, b: int = 7) -> None:
    """Plot the elliptic curve y² = x³ + ax + b over a small finite field."""
    points = []

    # Find all points on the curve
    for x in range(p):
        y_squared = (x * x * x + a * x + b) % p
        for y in range(p):
            if (y * y) % p == y_squared:
                points.append((x, y))

    if not points:
        print(f"No points found on the curve over F_{p}")
        return

    x_coords, y_coords = zip(*points)

    plt.figure(figsize=(10, 8))
    plt.scatter(x_coords, y_coords, alpha=0.7, s=50)
    plt.title(f"Elliptic Curve y² = x³ + {a}x + {b} over F_{p}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True, alpha=0.3)
    plt.xlim(-1, p)
    plt.ylim(-1, p)

    # Add annotations for a few points
    if len(points) >= 2:
        p1_coords = points[1]
        p2_coords = points[2] if len(points) > 2 else points[0]

        plt.annotate(
            f"P1({p1_coords[0]}, {p1_coords[1]})",
            xy=p1_coords,
            xytext=(5, 5),
            textcoords="offset points",
        )
        plt.annotate(
            f"P2({p2_coords[0]}, {p2_coords[1]})",
            xy=p2_coords,
            xytext=(5, 5),
            textcoords="offset points",
        )

    plt.tight_layout()
    plt.show()


def plot_real_curve() -> None:
    """Plot the secp256k1 curve over real numbers for visualization."""
    x = np.linspace(-3, 3, 1000)

    # Calculate y² = x³ + 7
    y_squared = x**3 + 7

    # Only plot where y² >= 0
    valid_indices = y_squared >= 0
    x_valid = x[valid_indices]
    y_squared_valid = y_squared[valid_indices]

    y_positive = np.sqrt(y_squared_valid)
    y_negative = -np.sqrt(y_squared_valid)

    plt.figure(figsize=(12, 8))
    plt.plot(x_valid, y_positive, "b-", label="y = √(x³ + 7)", linewidth=2)
    plt.plot(x_valid, y_negative, "b-", label="y = -√(x³ + 7)", linewidth=2)

    plt.title("secp256k1 Elliptic Curve: y² = x³ + 7 (over real numbers)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color="k", linewidth=0.5)
    plt.axvline(x=0, color="k", linewidth=0.5)
    plt.legend()
    plt.xlim(-3, 3)
    plt.ylim(-5, 5)

    plt.tight_layout()
    plt.show()


# Generator point
G = Point(GX, GY)


if __name__ == "__main__":
    print("secp256k1 Elliptic Curve Demo")
    print("=" * 30)

    print(f"Generator point G: {G}")
    print(f"Is G on curve? {G.is_on_curve()}")

    # Test point doubling
    G2 = G + G
    print(f"2G = {G2}")

    # Test point addition
    G3 = G2 + G
    print(f"3G = {G3}")

    # Plot the curve over real numbers
    print("\nPlotting secp256k1 over real numbers...")
    plot_real_curve()

    # Plot over a small finite field for discrete visualization
    print("Plotting curve over small finite field F_97...")
    plot_curve_over_small_field()
