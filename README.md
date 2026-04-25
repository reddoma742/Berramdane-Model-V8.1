# Berramdane-Model-V8.1
# Berramdane Model V8.1 – A Mechanical Interpretation of Double‑Slit Interference, Observer Effect, and Tunneling

**Author:** Al Moalim Berramdane (workshop owner, mechanical manufacturing & IT technician)  
**License:** CC BY 4.0  
**GitHub:** (رابط المستودع الخاص بك)

## Overview

The Berramdane Model V8.1 offers a mechanical analogy for key quantum phenomena:

- The double‑slit interference (7‑peak pattern) is explained by **mechanical interlocking of helical cones** emanating from the two slits.
- The observer effect is simulated as **asymmetric damping** (a simplified approximation).
- The de Broglie relation `λ = h/(mv)` is **derived** from helix properties, not assumed.
- Tunneling is hybrid: `T = Gamow × drill`, with `drill = tanh(ω_spin/ω_Compton)`. For a 1.5 eV electron through a 3.1 eV barrier (0.5 nm SiO₂), the model predicts `T_model / T_QM ≈ 0.004` – a falsifiable deviation.

The code produces four plots:
1. 1D interference pattern (7 peaks, symmetric).
2. 2D real‑screen view (vertical fringes).
3. Tunneling probability vs wall density.
4. Exponential decay (Gamow factor, log scale).

## Requirements

- Python 3.8+
- `numpy`, `matplotlib`

Install: `pip install numpy matplotlib`

## Run

```bash
python berramdane_v8.1.py
