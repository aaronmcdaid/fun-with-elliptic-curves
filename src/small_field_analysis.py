"""Analyze the elliptic curve y² = x³ + 7 over small finite field F₉₇."""

from typing import List, Tuple


def count_curve_points(
    p: int = 97, a: int = 0, b: int = 7
) -> Tuple[List[Tuple[int, int]], int]:
    """Count and return all points on the curve y² = x³ + ax + b over F_p."""
    points = []

    # Find all points on the curve
    for x in range(p):
        y_squared = (x * x * x + a * x + b) % p
        for y in range(p):
            if (y * y) % p == y_squared:
                points.append((x, y))

    # Add point at infinity (represented as None, None)
    total_points = len(points) + 1

    return points, total_points


if __name__ == "__main__":
    points, total = count_curve_points()

    print("Curve: y² = x³ + 7 over F₉₇")
    print("Field order (p): 97")
    print(f"Curve order (total points): {total}")
    print(f"Finite points: {len(points)}")
    print("Point at infinity: 1")
    print()

    # Show first few points
    print("First 10 points:")
    for i, point in enumerate(points[:10]):
        print(f"  P{i+1}: ({point[0]}, {point[1]})")

    print(f"  ... and {len(points) - 10} more points")
    print("  P∞: (∞)")

    # Verify Hasse's bound
    import math

    hasse_lower = 97 + 1 - 2 * math.sqrt(97)
    hasse_upper = 97 + 1 + 2 * math.sqrt(97)

    print("\nHasse's theorem bounds:")
    print(f"  {hasse_lower:.1f} ≤ curve order ≤ {hasse_upper:.1f}")
    print(f"  Actual curve order: {total}")
    print(f"  ✓ Within Hasse bounds: {hasse_lower <= total <= hasse_upper}")
