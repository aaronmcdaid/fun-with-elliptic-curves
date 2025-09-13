import pytest

from src.secp256k1 import GX, GY, G, P, Point, mod_inverse, point_multiply


def test_generator_point_on_curve() -> None:
    """Test that the generator point is on the curve."""
    assert G.is_on_curve()
    assert G.x == GX
    assert G.y == GY


def test_point_at_infinity() -> None:
    """Test point at infinity behavior."""
    infinity = Point()
    assert infinity.is_infinity()
    assert infinity.is_on_curve()

    # Adding point at infinity should return the other point
    assert G + infinity == G
    assert infinity + G == G


def test_point_doubling() -> None:
    """Test point doubling (P + P)."""
    g2 = G + G
    assert g2.is_on_curve()
    assert g2 != G

    # Test with point multiplication
    g2_mult = point_multiply(2, G)
    assert g2 == g2_mult


def test_point_addition() -> None:
    """Test adding different points."""
    g2 = G + G
    g3 = g2 + G
    g3_mult = point_multiply(3, G)

    assert g3.is_on_curve()
    assert g3 == g3_mult


def test_point_inverse() -> None:
    """Test that P + (-P) = ∞."""
    # Create the inverse of G (same x, negative y)
    assert G.y is not None
    neg_g = Point(G.x, (-G.y) % P)

    assert neg_g.is_on_curve()
    result = G + neg_g
    assert result.is_infinity()


def test_point_multiplication() -> None:
    """Test scalar multiplication of points."""
    # Test with small scalars
    p1 = point_multiply(1, G)
    assert p1 == G

    p0 = point_multiply(0, G)
    assert p0.is_infinity()

    # Test that k*G is on the curve for various k
    for k in [2, 3, 5, 10, 100]:
        result = point_multiply(k, G)
        assert result.is_on_curve()


def test_modular_inverse() -> None:
    """Test modular inverse calculation."""
    # Test some known values
    assert mod_inverse(2, P) * 2 % P == 1
    assert mod_inverse(3, P) * 3 % P == 1
    assert mod_inverse(7, P) * 7 % P == 1


def test_point_equality() -> None:
    """Test point equality comparison."""
    # Use the generator point for valid point comparison
    p1 = Point(G.x, G.y)
    p2 = Point(G.x, G.y)

    # Use point at infinity for different point
    p3 = Point()

    assert p1 == p2
    assert p1 != p3


def test_associativity() -> None:
    """Test that point addition is associative: (P + Q) + R = P + (Q + R)."""
    p1 = point_multiply(2, G)
    p2 = point_multiply(3, G)
    p3 = point_multiply(5, G)

    left = (p1 + p2) + p3
    right = p1 + (p2 + p3)

    assert left == right


def test_commutativity() -> None:
    """Test that point addition is commutative: P + Q = Q + P."""
    p1 = point_multiply(2, G)
    p2 = point_multiply(3, G)

    assert p1 + p2 == p2 + p1


def test_invalid_point() -> None:
    """Test that invalid points raise ValueError."""
    with pytest.raises(ValueError):
        Point(1, 1)  # This point is not on secp256k1
