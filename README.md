# PINN Lookback Options Pricing

Physics-Informed Neural Networks (PINNs) for pricing European and American lookback options with free boundary conditions. This project implements PDE-constrained deep learning to solve Black-Scholes equations for path-dependent derivatives, replacing traditional numerical methods (finite difference, Monte Carlo) with neural network approximations that encode financial PDE structure directly into the loss function.

**Author**: Changyeol Oh  
**Independent Project**

---

## Table of Contents

- [Project Overview](#project-overview)
- [Background](#background)
- [Notebook Progression](#notebook-progression)
- [Project Structure](#project-structure)
- [Pipeline](#pipeline)
- [Methodology](#methodology)
- [Results](#results)
- [Colab Compatibility](#colab-compatibility)
- [How to Run](#how-to-run)
- [Future Work](#future-work)
- [References](#references)

---

## Project Overview

Lookback options are path-dependent financial derivatives whose payoff depends on the minimum or maximum price of the underlying asset over the option's life. Pricing these options requires solving PDEs with path-dependent boundary conditions — a computationally expensive task for traditional methods.

This project applies PINNs to solve the Black-Scholes PDE for four lookback option types (Fixed Call, Fixed Put, Floating Call, Floating Put) under both European and American exercise styles. For American options, a Free Boundary PINN architecture jointly learns the option price surface and the early exercise boundary.

---

## Background

### Lookback Option Types

| Type | Payoff |
|---|---|
| Fixed Call | max(max(S_T) - K, 0) |
| Fixed Put | max(K - min(S_T), 0) |
| Floating Call | max(S_T - min(S_t), 0) |
| Floating Put | max(max(S_t) - S_T, 0) |

### Black-Scholes PDE

The PINN enforces the Black-Scholes PDE as an unsupervised loss:

```
∂u/∂t + (σ²/2)·S²·(∂²u/∂S²) + r·S·(∂u/∂S) - r·u = 0
```

For American options, the free boundary condition adds a complementarity constraint that determines the optimal early exercise boundary.

---

## Notebook Progression

Development followed an iterative process across three notebooks:

| Order | Notebook | Role | Status |
|---|---|---|---|
| 1 | `free_boundary_pinn.ipynb` | Prototype — FreeBoundary_PINN class development, first Lookback 4-type PINN | Completed |
| 2 | `american_lb_lookback.ipynb` | Experimental — eta=M/S coordinate transform to extend Free Boundary to Lookback options | Convergence failed (nan); Lookback 4-type completed separately |
| 3 | `american_lookback_final.ipynb` | Final — Optimized hyperparameters, stable Free Boundary convergence (Best step 782), Lookback 4-type at 10⁻⁸ | **Final results** |

Discarded files: `Americal_LB_final.ipynb` (identical copy of `american_lookback_final.ipynb`, filename typo).

---

## Project Structure

```
pinn-lookback-options/
│
├── notebooks/
│   ├── European_LB_final.ipynb            # European lookback: MC simulation + PINN 4 types
│   ├── american_lookback_final.ipynb       # American lookback: Free Boundary PINN + 4 types (FINAL)
│   ├── free_boundary_pinn.ipynb            # Prototype: Free Boundary PINN development
│   ├── american_lb_lookback.ipynb          # Experimental: eta=M/S coordinate transform attempt
│   ├── Exotic_European_examples.ipynb      # Additional European exotic option examples
│   └── Stefan_1D_Freeboundary_Tensorflow2.ipynb  # Stefan problem reference
│
├── scripts/
│   ├── European_lb.py                      # European lookback modularized script
│   ├── American_lb.py                      # American lookback modularized script
│   └── LB_integrate_2.py                   # Integral pricing formula implementation
│
├── figures/                                # Generated plots and visualizations
│
├── data/
│   └── lookback_options_analysis.csv       # Greeks analysis (100 rows, Delta/Gamma/Theta)
│
├── docs/
│   └── Lookback_Options_Changyeol_Oh.pdf   # Project report
│
└── README.md
```

---

## Pipeline

```
                    Lookback Options with PINNs
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
      European Options                American Options
              │                               │
              ▼                               ▼
   Black-Scholes PDE              Black-Scholes PDE
   (analytical solution           + Free Boundary Condition
    available for validation)     (early exercise boundary)
              │                               │
              ▼                               ▼
   Monte Carlo Simulation         FreeBoundary_PINN Class
   (baseline comparison)          (dual-network architecture)
              │                        │            │
              ▼                        ▼            ▼
   PINN Training                  mdl network   fb network
   (4 option types)               (option price) (exercise boundary)
              │                        │            │
              ▼                        └─────┬──────┘
   MC vs PINN Comparison                    ▼
                                  Alternating Training
                                  (steps_fb_per_pde = 20)
                                         │
                              ┌──────────┴──────────┐
                              ▼                     ▼
                     Free Boundary Plot    Lookback 4-Type PINN
                     (Early Exercise       (Fixed/Floating ×
                      Boundary Curve)       Call/Put)
```

---

## Methodology

### Loss Function Components

The PINN total loss consists of multiple components that enforce PDE physics and boundary conditions:

**Unsupervised Loss (PDE Residual)**: Enforces the Black-Scholes equation at collocation points sampled via Sobol quasi-random sequences across the (S, t) domain.

**Initial Condition Loss**: Matches the known option payoff at maturity t = T.

**Dirichlet Boundary Loss**: Enforces option price values at domain boundaries (e.g., deep in-the-money or out-of-the-money).

**Neumann Boundary Loss**: Enforces gradient conditions (smooth pasting) at the free boundary.

**Free Boundary Losses** (American only): Three additional loss terms (initial, Dirichlet, Neumann) enforce that the free boundary network learns the correct early exercise boundary.

### FreeBoundary_PINN Architecture

The American option solver uses a dual-network architecture:

| Network | Input | Hidden Layers | Output | Role |
|---|---|---|---|---|
| mdl (main) | (S, t) | 8 × 15 neurons, tanh | 1 (option price) | Solves the PDE |
| fb (free boundary) | t | 3 × 150 neurons, tanh | 1 (boundary S*) | Learns exercise boundary |

Training alternates between the two networks, with 20 free boundary steps per PDE step, using RMSprop optimizer with exponential learning rate decay (initial lr=1e-3, decay every 300 steps, rate=0.9).

### Lookback 4-Type PINN

For each of the four lookback option types, an independent 3-layer network (50 neurons each, tanh activation) is trained with input (S, M, t) where M tracks the path-dependent min/max of S via GBM path simulation. Training cells are split per option type with explicit memory cleanup (`gc.collect()`) between runs to prevent OOM on A100 (83.5 GB System RAM).

### Parameters

| Parameter | Value |
|---|---|
| Risk-free rate (r) | 0.01 |
| Volatility (σ) | 0.05 |
| Strike price (K) | 10.0 |
| Maturity (T) | 3.0 years |
| Collocation points (N_f) | 9,000 |
| Sampling method | Sobol sequence |

---

## Results

### American Put — Free Boundary PINN

Training converged at Best step 782 (1,000 epochs) with the following loss components:

| Component | Final Loss |
|---|---|
| Unsupervised (PDE) | 4.40 × 10⁻⁶ |
| Initial | 2.35 × 10⁻⁴ |
| Dirichlet | 1.06 × 10⁻⁵ |
| Free Boundary | 9.60 × 10⁻⁴ |
| **Total** | **3.22 × 10⁻⁴** |

The early exercise boundary shows the expected behavior for an American put: starting near S* ≈ 0.57 at t = 0, increasing to S* ≈ 1.13 around t = 2, then gradually decreasing toward maturity.

<p align="center">
  <img src="figures/free_boundary_american_put.png" width="700">
</p>

### Lookback 4-Type PINN — Final Loss (10,000 epochs)

| Option Type | Final Loss |
|---|---|
| Fixed Call | 4.26 × 10⁻⁸ |
| Fixed Put | 1.65 × 10⁻⁸ |
| Floating Call | 3.07 × 10⁻⁸ |
| Floating Put | 2.16 × 10⁻⁸ |

All four cases converged to 10⁻⁸ order, demonstrating that the PINN framework successfully learns lookback option prices across all payoff structures.

### Training Environment Comparison

| Environment | FreeBoundary_PINN (1,000 epochs) | Lookback 4-Type (10,000 epochs each) |
|---|---|---|
| A100 GPU (Google Colab) | ~2.5 min | ~15 min per case |
| Apple M2 CPU (local) | ~8–9 hours | Not feasible |

---

## Colab Compatibility

The original notebooks were developed on Python 3.8 + TensorFlow 2.x (Keras 2). Running on Google Colab (Python 3.12 + TensorFlow 2.16+ / Keras 3) requires the following modifications:

| Issue | Symptom | Fix |
|---|---|---|
| Keras 3 default | `ValueError: Cannot convert '2' to a shape` | Install `tf_keras`, set `TF_USE_LEGACY_KERAS=1` before importing TF |
| Sobol package | `ModuleNotFoundError: No module named 'sobol'` | `pip install SobolSequence` (provides `import sobol`) |
| pyDOE numpy conflict | numpy version incompatibility | `pip install pyDOE2 "numpy<2.2"` |
| Optimizer mismatch | `KeyError: optimizer cannot recognize variable` | Use `tf.keras.optimizers.legacy.Adam/RMSprop` |
| GradientTape alias | `NameError: name 'G_Tape' is not defined` | Replace `G_Tape` with `tf.GradientTape` or keep import line |
| OOM on long training | System RAM exceeded (83.5 GB) | Split training into separate cells per option type with `gc.collect()` |

### Colab Setup

> **⚠️ IMPORTANT**: pip install and environment variable setup must be done in **separate steps** with a **runtime restart** between them.

**Step 1** — Run this cell, then **Restart runtime** (Runtime > Restart session):
```python
!pip install tf_keras "numpy<2.2" pyDOE2 SobolSequence
```

**Step 2** — After restart, run this cell **FIRST** before any other imports:
```python
import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"
```

---

## How to Run

### Google Colab (Recommended)

1. Upload notebook to Google Colab
2. Select A100 GPU runtime (Runtime > Change runtime type)
3. Follow the Colab Setup steps above (install → restart → env variable)
4. Run cells sequentially

### Local Environment

```bash
# Requires Python 3.8+, TensorFlow 2.x
pip install tensorflow numpy scipy matplotlib tqdm pyDOE SobolSequence

# Run notebooks
jupyter notebook notebooks/american_lookback_final.ipynb
```

---

## Future Work

**Free Boundary extension to Lookback options**: The current implementation successfully learns the early exercise boundary for standard American puts and separately learns lookback option prices. Combining both — learning the early exercise boundary for American lookback options — was attempted via eta=M/S coordinate transformation (`american_lb_lookback.ipynb`) but failed to converge (Unsupervised loss remained nan). Alternative approaches such as penalty methods or variational inequality formulations may be needed to solve this problem.

**Quanto Lookback Options**: Extending the PINN framework to Quanto lookback options involving coupled stochastic processes (asset price + currency exchange rate dynamics).

**DeepONet integration**: Applying Deep Operator Networks to learn mappings between entire function spaces for more efficient path-dependent option pricing.

---

## References

1. Goldman, M. B., Sosin, H. B., & Gatto, M. A. (1979). Path dependent options: "Buy at the low, sell at the high." *Journal of Finance*, 34(5), 1111-1127.
2. Conze, A., & Viswanathan, R. (1991). Path dependent options: The case of lookback options. *Journal of Finance*, 46(5), 1893-1907.
3. Raissi, M., Perdikaris, P., & Karniadakis, G. E. (2019). Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations. *Journal of Computational Physics*, 378, 686-707.
