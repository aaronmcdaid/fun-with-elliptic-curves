# Claude Code Session Notes

## Project Overview
This is an educational exploration of the **secp256k1** elliptic curve used in Bitcoin. The project was created collaboratively with Claude Code to understand elliptic curve cryptography from first principles.

## What We Built

### Core Implementation (`src/secp256k1.py`)
- Complete secp256k1 elliptic curve implementation with Bitcoin's exact parameters
- Point class with validation and arithmetic operations (`__add__`, point multiplication)
- Modular inverse calculation using extended Euclidean algorithm
- Visualization functions for both real curves and finite field discrete points
- Constants: P (prime field), N (curve order), G (generator point) - all matching Bitcoin

### Educational Analysis (`src/small_field_analysis.py`)
- Same curve equation (y² = x³ + 7) but over tiny field F₉₇ for visualization
- Point counting and Hasse's theorem verification
- Found 79 total points (78 finite + point at infinity)

### Testing & Quality
- Comprehensive test suite (15 tests) covering all edge cases
- Full type annotations and mypy compliance
- Ruff linting with proper code formatting
- All tests pass, no linting errors

## Key Mathematical Insights Discovered

1. **secp256k1 Parameters are Bitcoin's exact values**:
   - P = 2²⁵⁶ - 2³² - 977 (prime field)
   - N = curve order (~2²⁵⁶, also prime)
   - Both P and N are prime numbers

2. **Prime Order Curve Properties**:
   - N is prime, so every non-infinity point can generate the full curve
   - 2G, 3G, etc. are all equivalent generators (cofactor = 1)
   - Maximum cryptographic security with no weak subgroups

3. **Point Arithmetic Results**:
   - Computed G, 2G, 3G with full 256-bit coordinates
   - All points validated as being on the curve
   - Point at infinity (∞) acts as identity element: ∞ + ∞ = ∞

4. **Coordinate Properties**:
   - For most x-coordinates, there are exactly 2 valid y-coordinates (y and -y)
   - Some x have 0 solutions (not quadratic residues)
   - Rarely, exactly 1 solution (when y = 0)

## Development Commands

```bash
# Setup
poetry install

# Run demos
poetry run python src/secp256k1.py          # Point arithmetic + visualizations
poetry run python src/small_field_analysis.py  # F₉₇ analysis

# Testing & Quality
poetry run pytest tests/ -v                 # Run all tests
poetry run ruff check src/ tests/           # Linting
poetry run mypy src/ tests/                 # Type checking
```

## Session Context for Future Claude

**Educational Purpose**: Learning elliptic curve cryptography by implementing Bitcoin's actual curve from scratch. Focus was on mathematical understanding rather than production crypto code.

**Code Quality**: We fixed all linting issues, added proper type annotations, and maintained 100% test coverage throughout development.

**Mathematical Rigor**: Verified theoretical properties like Hasse bounds, primality of P and N, and proper elliptic curve group operations.

**Visualization Approach**: Dual approach - massive secp256k1 for real calculations, tiny F₉₇ for human comprehension of discrete structure.

## References
- [Andrea Corbellini's ECC series](https://andrea.corbellini.name/2015/05/17/elliptic-curve-cryptography-a-gentle-introduction/) (inspiration)
- [Cashu](https://cashu.space/) (mentioned as potential next project)

## Project Status
✅ Complete and fully functional  
✅ All tests passing  
✅ Code quality standards met  
✅ README.md documentation added  
🎯 Ready for educational use or as foundation for crypto projects

---

*This file created during collaborative session with Claude Code for future context preservation.*