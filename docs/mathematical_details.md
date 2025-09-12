# Mathematical Details of TTST

## 1. Environmental Rhythm Formulations

### 1.1 Thermal Rhythm

The thermal rhythm from hydrothermal vents is modeled as a superposition of multiple frequency components with stochastic fluctuations:

```textß
S_thermal(t) = Σᵢ A_h,i(t) · sin(2πt/T_h,i + φᵢ) + ξ(t)
```

Where:

- `A_h,i(t)`: Time-dependent amplitude of i-th component
- `T_h,i`: Period of i-th thermal oscillation (0.1-2 hours)
- `φᵢ`: Phase offset
- `ξ(t)`: Gaussian white noise with correlation time τ_c ≈ 0.1 hours

#### Convective Oscillation Model

Based on Rayleigh-Bénard convection:

```text
∂T/∂t = κ∇²T + v·∇T + Q(x,t)
```

The oscillation frequency scales with the Rayleigh number:

```text
f_convection ∝ √((Ra - Ra_c)/Ra_c)
```

Where `Ra_c = 1708` is the critical Rayleigh number.

### 1.2 Tidal Rhythm

The tidal forcing includes both linear and nonlinear components:

```text
S_tidal(t) = A_t sin(2πt/T_t(t)) + ε sin²(2πt/T_t(t))
```

#### Lunar Recession Model

The lunar distance evolves as:

```text
d(t) = d_current - (d_current - d_early) · exp(-t/τ)
```

With:

- `d_current = 60.3` Earth radii
- `d_early = 10` Earth radii (4 Ga)
- `τ ≈ 2 × 10⁹` years

The tidal period scales with distance:

```text
T_tidal ∝ d^(3/2)  (Kepler's third law)
```

The tidal amplitude scales inversely:

```text
A_tidal ∝ d^(-3)
```

### 1.3 Solar Rhythm

The solar rhythm with sharp day-night transitions:

```text
S_solar(t) = A_s · [1/2 + 1/2 tanh(β sin(2πt/T_s))]
```

Where `β` controls transition sharpness (typically β = 10).

#### Day Length Evolution

Earth's rotation has slowed due to tidal friction:

```text
T_day(t) = T_current - (T_current - T_early) · exp(-t/τ_rot)
```

With:
- `T_current = 24` hours
- `T_early = 10` hours (4 Ga)
- `τ_rot ≈ 2.5 × 10⁹` years

## 2. Coupled Oscillator Dynamics

### 2.1 General Coupling Framework

The coupled system of environmental rhythms:

```text
dS_env/dt = f(S_solar, S_tidal, S_thermal) + Σⱼ αⱼ gⱼ(S_env)
```

Where:

- `f`: Nonlinear interaction function
- `gⱼ`: Biological feedback mechanisms
- `αⱼ`: Coupling strengths

### 2.2 Kuramoto Model

For phase coupling between N oscillators:

```text
dθᵢ/dt = ωᵢ + Σⱼ Kᵢⱼ sin(θⱼ - θᵢ)
```

Where:

- `θᵢ`: Phase of oscillator i
- `ωᵢ`: Natural frequency
- `Kᵢⱼ`: Coupling strength matrix

The order parameter (synchronization measure):

```text
r(t) = |1/N Σⱼ exp(iθⱼ)|
```

### 2.3 Van der Pol Coupled System

For amplitude dynamics:

```
ẍᵢ + ωᵢ²xᵢ - μᵢ(1 - xᵢ²)ẋᵢ = Σⱼ εᵢⱼ(xⱼ - xᵢ)
```

Where:
- `μᵢ`: Nonlinearity parameter
- `εᵢⱼ`: Coupling coefficients

## 3. Arnold Tongues and Synchronization

### 3.1 Resonance Conditions

Synchronization occurs when frequency ratios approach rational numbers:

```text
T_tidal/T_thermal = p/q
```

Where p, q are small integers.

The width of Arnold tongues:

```text
Δω ∝ K^(q/2)
```

Where K is the coupling strength.

### 3.2 Phase Locking

For 1:1 synchronization:

```text
|φ_bio - φ_env| < constant
```

For p:q synchronization:

```text
|p·φ_bio - q·φ_env| < constant
```

### 3.3 Lyapunov Stability

The stability of synchronized states:

```text
λ = lim(t→∞) 1/t ln|δx(t)/δx(0)|
```

Where λ < 0 indicates stable synchronization.

## 4. Stochastic Resonance

### 4.1 Bistable System

The double-well potential:

```
V(x) = -ax²/2 + bx⁴/4
```

With dynamics:

```text
dx/dt = -dV/dx + A sin(ωt) + √(2D)η(t)
```

Where:

- `A`: Weak signal amplitude
- `D`: Noise intensity
- `η(t)`: White noise

### 4.2 Signal-to-Noise Ratio

The SNR at the signal frequency:

```text
SNR = 10 log₁₀(P_signal/P_noise)
```

Optimal noise level:

```text
D_opt ≈ ΔV/2
```

Where ΔV is the potential barrier height.

## 5. Snowball Earth Disruption

### 5.1 Rhythm Modulation

During Snowball Earth:

```text
S_thermal(t) → S_thermal(t)  (unchanged)
S_tidal(t) → 0.8 · S_tidal(t)  (damped)
S_solar(t) → 0  (eliminated for surface)
```

### 5.2 Sub-ice Preservation

Tidal amplitude under ice:

```text
A_sub-ice = A_ocean · exp(-h_ice/λ)
```

Where:

- `h_ice`: Ice thickness (~1000 m)
- `λ`: Damping length scale (~500 m)

## 6. Biological Response Functions

### 6.1 Circadian Entrainment

The circadian oscillator with forcing:

```text
dφ/dt = ω₀ + Z(φ) · F(t)
```

Where:

- `ω₀ = 2π/24`: Free-running frequency
- `Z(φ)`: Phase response curve
- `F(t)`: Environmental forcing

### 6.2 Metabolic Coupling

Temperature-compensated oscillations:

```text
ω(T) = ω₀ · Q₁₀^((T-T₀)/10)
```

With Q₁₀ ≈ 1 for circadian rhythms (temperature compensation).

### 6.3 Neural Oscillations

Hierarchical frequency organization:

```text
f_neural ∈ {δ(0.5-4 Hz), θ(4-8 Hz), α(8-13 Hz), β(13-30 Hz), γ(30-100 Hz)}
```

Mapping to environmental rhythms:

- γ, β → Thermal timescales
- α, θ → Tidal timescales
- δ → Solar timescales

## 7. Evolution Operators

### 7.1 Fitness Function

Rhythm-dependent fitness:

```text
W(sync) = W₀ · exp(β · r²)
```

Where r is the synchronization order parameter.

### 7.2 Selection Dynamics

Change in synchronization capability:

```text
ds/dt = s(1-s)[W(s) - W̄]
```

Where s is the proportion with synchronization trait.

## 8. Information-Theoretic Measures

### 8.1 Mutual Information

Between environmental and biological rhythms:

```text
I(E;B) = ΣΣ p(e,b) log[p(e,b)/(p(e)p(b))]
```

### 8.2 Transfer Entropy

Directional information flow:

```text
T_E→B = ΣΣΣ p(b_{t+1}, b_t, e_t) log[p(b_{t+1}|b_t, e_t)/p(b_{t+1}|b_t)]
```

## 9. Spectral Analysis

### 9.1 Power Spectral Density

For rhythm analysis:

```text
P(f) = |F{x(t)}|² = |∫x(t)e^(-2πift)dt|²
```

### 9.2 Wavelet Transform

For time-frequency analysis:

```text
W(a,b) = 1/√a ∫x(t)ψ*((t-b)/a)dt
```

Where ψ is the mother wavelet.

### 9.3 Cross-Spectral Coherence

Between two rhythms:

```text
C_xy(f) = |P_xy(f)|²/(P_xx(f)·P_yy(f))
```

## 10. Numerical Methods

### 10.1 Integration Schemes

For stiff oscillator equations:

- Runge-Kutta 4th order for smooth dynamics
- Euler-Maruyama for stochastic differential equations
- Implicit methods for stiff systems

### 10.2 Parameter Estimation

Maximum likelihood for rhythm parameters:

```text
L(θ|x) = Π p(xᵢ|θ)
```

### 10.3 Bifurcation Analysis

Detecting rhythm transitions:

- Floquet multipliers for periodic orbits
- Lyapunov exponents for chaos detection
- Continuation methods for parameter sweeps

## Conclusion

The mathematical framework of TTST combines:

- **Dynamical systems theory** for rhythm interactions
- **Synchronization theory** for coupling analysis
- **Stochastic processes** for noise effects
- **Information theory** for rhythm communication
- **Evolutionary dynamics** for selection pressures

This mathematical foundation enables quantitative predictions and experimental validation of the theory's core hypotheses.
