# Fun with Elliptic Curves

A Python exploration of the **secp256k1** elliptic curve used in Bitcoin's cryptographic system. Bitcoin uses elliptic curve digital signatures (ECDSA) to secure transactions - each Bitcoin address corresponds to a point on this mathematical curve.

## The Mathematics

Elliptic curves represent points in 2D space as pairs of integers `(x, y)` where both coordinates are in the range `[0, p-1]` (inclusive) for a large prime number `p`. However, not every possible coordinate pair is valid - only those points that satisfy the **curve equation** are "on the curve."

For secp256k1, the equation is:
```
y² = x³ + 7 (mod p)
```

Where `p` is a massive 256-bit prime number. This creates a finite field with specific mathematical properties that make it perfect for cryptography.

## What This Repository Contains

### Core Implementation (`src/secp256k1.py`)
- **Point arithmetic**: Add and multiply points using the elliptic curve group law
- **Real Bitcoin parameters**: Uses the exact same constants as Bitcoin's implementation
- **Visualization**: Plot the curve over real numbers and small finite fields
- **Generator point**: The specific point `G` that Bitcoin uses to generate all public keys

### Educational Analysis (`src/small_field_analysis.py`)
- **Scaled-down version**: Same curve shape (y² = x³ + 7) but over tiny field F₉₇
- **Point counting**: Finds all 79 points on the curve (78 finite + point at infinity)
- **Hasse's theorem**: Verifies the curve order falls within theoretical bounds
- **Visualization-friendly**: Small enough to see every individual point

### Key Concepts Demonstrated

**Finite Fields**: All arithmetic happens modulo a prime `p`, creating a discrete mathematical structure

**Point Addition**: Special rules for adding two points on the curve that maintain the group structure

**Generator Points**: A single point `G` that, when multiplied by different integers, generates all other points on the curve

**Cryptographic Security**: The difficulty of the "discrete logarithm problem" - given points `P` and `Q = kP`, finding `k` is computationally infeasible

## Bitcoin Connection

In Bitcoin:
- **Private keys** are random integers between 1 and the curve order (~2²⁵⁶)  
- **Public keys** are points calculated as `private_key × G` (scalar multiplication)
- **Addresses** are derived from public key coordinates
- **Signatures** prove knowledge of the private key without revealing it

The secp256k1 curve was chosen for its security properties and computational efficiency.

## Running the Code

### Setup
```bash
poetry install
```

### Run Demos
```bash
# See point arithmetic and curve visualizations
poetry run python src/secp256k1.py

# Analyze the curve over small finite field F₉₇  
poetry run python src/small_field_analysis.py
```

### Run Tests
```bash
poetry run pytest tests/ -v
```

### Code Quality
```bash
poetry run ruff check src/ tests/    # Linting
poetry run mypy src/ tests/          # Type checking
```

## Key Features

- ✅ **Cryptographically accurate**: Uses Bitcoin's exact secp256k1 parameters
- ✅ **Educational visualization**: Shows curve structure over small and large fields  
- ✅ **Complete implementation**: Point addition, scalar multiplication, validation
- ✅ **Well-tested**: Comprehensive test suite covering edge cases
- ✅ **Type-safe**: Full type annotations and mypy compliance

## Mathematical Properties Explored

- **Prime order curve**: Every non-infinity point generates the full group
- **Hasse bounds**: Curve order falls within `p + 1 ± 2√p`
- **Point compression**: Each x-coordinate typically has 2 valid y-coordinates
- **Identity element**: Point at infinity acts as the "zero" for addition

## Learning Resources

This implementation helps understand:
- How Bitcoin's cryptography actually works under the hood
- The mathematical beauty of elliptic curves
- Why certain parameters were chosen for security
- The relationship between abstract algebra and practical cryptography

Perfect for anyone curious about the mathematics powering Bitcoin and modern cryptography!