#!/usr/bin/env python3
"""
Coupled oscillator dynamics for TTST
Mathematical framework for rhythm coupling and synchronization

Author: Tomoyuki Kano
License: MIT
"""

import numpy as np
from scipy.integrate import odeint
from scipy.signal import hilbert
from typing import Tuple, List, Optional, Callable
import matplotlib.pyplot as plt


class CoupledOscillator:
    """Base class for coupled oscillator systems"""

    def __init__(self, frequencies: List[float],
                 amplitudes: List[float],
                 coupling_matrix: Optional[np.ndarray] = None):
        """
        Initialize coupled oscillator system

        Args:
            frequencies: Natural frequencies of oscillators (rad/s)
            amplitudes: Amplitude of each oscillator
            coupling_matrix: Coupling strength between oscillators
        """
        self.n_oscillators = len(frequencies)
        self.frequencies = np.array(frequencies)
        self.amplitudes = np.array(amplitudes)

        if coupling_matrix is None:
            # Default: weak uniform coupling
            self.coupling = 0.1 * (np.ones((self.n_oscillators, self.n_oscillators))
                                  - np.eye(self.n_oscillators))
        else:
            self.coupling = np.array(coupling_matrix)

    def kuramoto_model(self, phases: np.ndarray, t: float) -> np.ndarray:
        """
        Kuramoto model for phase coupling

        Args:
            phases: Current phases of oscillators
            t: Current time

        Returns:
            Phase derivatives
        """
        dphases = self.frequencies.copy()

        for i in range(self.n_oscillators):
            coupling_term = 0
            for j in range(self.n_oscillators):
                if i != j:
                    coupling_term += self.coupling[i, j] * np.sin(phases[j] - phases[i])
            dphases[i] += coupling_term

        return dphases

    def van_der_pol_coupled(self, state: np.ndarray, t: float,
                           mu: float = 1.0) -> np.ndarray:
        """
        Coupled Van der Pol oscillators

        Args:
            state: Current state [x1, v1, x2, v2, ...]
            t: Current time
            mu: Nonlinearity parameter

        Returns:
            State derivatives
        """
        n = self.n_oscillators
        x = state[::2]  # Positions
        v = state[1::2]  # Velocities

        dx = v.copy()
        dv = np.zeros(n)

        for i in range(n):
            # Van der Pol dynamics
            dv[i] = mu * (1 - x[i]**2) * v[i] - self.frequencies[i]**2 * x[i]

            # Coupling terms
            for j in range(n):
                if i != j:
                    dv[i] += self.coupling[i, j] * (x[j] - x[i])

        # Interleave derivatives
        dstate = np.zeros(2*n)
        dstate[::2] = dx
        dstate[1::2] = dv

        return dstate

    def simulate_kuramoto(self, t_span: Tuple[float, float],
                         dt: float = 0.01,
                         initial_phases: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Simulate Kuramoto model

        Args:
            t_span: Time span (start, end)
            dt: Time step
            initial_phases: Initial phases (random if None)

        Returns:
            Time array and phase trajectories
        """
        t = np.arange(t_span[0], t_span[1], dt)

        if initial_phases is None:
            initial_phases = 2 * np.pi * np.random.random(self.n_oscillators)

        phases = odeint(self.kuramoto_model, initial_phases, t)

        return t, phases

    def calculate_order_parameter(self, phases: np.ndarray) -> np.ndarray:
        """
        Calculate Kuramoto order parameter (synchronization measure)

        Args:
            phases: Phase trajectories

        Returns:
            Order parameter over time
        """
        complex_phases = np.exp(1j * phases)
        r = np.abs(np.mean(complex_phases, axis=1))
        return r


class TTSTCoupledSystem(CoupledOscillator):
    """TTST-specific coupled oscillator system"""

    def __init__(self):
        """Initialize TTST oscillator system"""
        # Convert periods (hours) to frequencies (rad/hour)
        thermal_freq = 2 * np.pi / 0.5    # 30 min period
        tidal_freq = 2 * np.pi / 12.4     # 12.4 hour period
        solar_freq = 2 * np.pi / 24.0     # 24 hour period

        frequencies = [thermal_freq, tidal_freq, solar_freq]
        amplitudes = [1.0, 1.0, 1.0]

        # TTST coupling matrix (asymmetric)
        # Thermal -> Tidal: weak
        # Tidal -> Solar: moderate
        # Solar -> Thermal: weak feedback
        coupling = np.array([
            [0.0, 0.3, 0.2],   # Thermal couples to others
            [0.3, 0.0, 0.5],   # Tidal couples to others
            [0.2, 0.5, 0.0]    # Solar couples to others
        ])

        super().__init__(frequencies, amplitudes, coupling)

    def biological_feedback(self, state: np.ndarray, t: float,
                           feedback_strength: float = 0.1) -> np.ndarray:
        """
        Add biological feedback to the coupled system

        Args:
            state: Current state
            t: Current time
            feedback_strength: Strength of biological feedback

        Returns:
            Modified state derivatives
        """
        base_dynamics = self.van_der_pol_coupled(state, t)

        # Add feedback based on combined rhythm
        n = self.n_oscillators
        x = state[::2]
        combined = np.sum(self.amplitudes * x)

        # Feedback affects velocities
        feedback = np.zeros_like(base_dynamics)
        feedback[1::2] = feedback_strength * combined * x

        return base_dynamics + feedback

    def arnold_tongue_analysis(self, freq_ratios: List[Tuple[int, int]],
                              coupling_range: Tuple[float, float] = (0, 1),
                              n_points: int = 50) -> dict:
        """
        Analyze Arnold tongues for given frequency ratios

        Args:
            freq_ratios: List of (p, q) frequency ratios to test
            coupling_range: Range of coupling strengths
            n_points: Number of points to test

        Returns:
            Dictionary with synchronization data
        """
        coupling_strengths = np.linspace(coupling_range[0], coupling_range[1], n_points)
        results = {}

        for p, q in freq_ratios:
            sync_values = []

            for coupling_strength in coupling_strengths:
                # Modify coupling matrix
                self.coupling *= coupling_strength / np.max(self.coupling)

                # Run simulation
                t, phases = self.simulate_kuramoto((0, 100), dt=0.1)

                # Check if p:q synchronization occurs
                phase_diff = p * phases[:, 0] - q * phases[:, 1]
                phase_diff_wrapped = np.mod(phase_diff, 2*np.pi)

                # Measure synchronization (variance of phase difference)
                sync_measure = 1 / (1 + np.var(phase_diff_wrapped[-1000:]))
                sync_values.append(sync_measure)

            results[f"{p}:{q}"] = {
                'coupling_strengths': coupling_strengths,
                'synchronization': np.array(sync_values)
            }

        return results


class StochasticResonance:
    """Stochastic resonance in the TTST framework"""

    def __init__(self, signal_freq: float, noise_level: float):
        """
        Initialize stochastic resonance system

        Args:
            signal_freq: Frequency of weak periodic signal
            noise_level: Noise intensity
        """
        self.signal_freq = signal_freq
        self.noise_level = noise_level

    def bistable_potential(self, x: float, a: float = 1.0, b: float = 1.0) -> float:
        """
        Double-well potential

        V(x) = -a*x^2/2 + b*x^4/4
        """
        return -a * x**2 / 2 + b * x**4 / 4

    def potential_derivative(self, x: float, a: float = 1.0, b: float = 1.0) -> float:
        """Derivative of the potential"""
        return -a * x + b * x**3

    def simulate(self, duration: float, dt: float = 0.01,
                signal_amplitude: float = 0.1) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Simulate stochastic resonance

        Args:
            duration: Simulation duration
            dt: Time step
            signal_amplitude: Amplitude of weak periodic signal

        Returns:
            Time, trajectory, and signal
        """
        n_steps = int(duration / dt)
        t = np.linspace(0, duration, n_steps)

        # Weak periodic signal
        signal = signal_amplitude * np.sin(2 * np.pi * self.signal_freq * t)

        # Initialize trajectory
        x = np.zeros(n_steps)
        x[0] = np.random.randn()

        # Euler-Maruyama integration
        noise = np.sqrt(2 * self.noise_level * dt) * np.random.randn(n_steps)

        for i in range(1, n_steps):
            drift = -self.potential_derivative(x[i-1]) + signal[i]
            x[i] = x[i-1] + drift * dt + noise[i]

        return t, x, signal

    def calculate_snr(self, x: np.ndarray, signal_freq: float) -> float:
        """
        Calculate signal-to-noise ratio at signal frequency

        Args:
            x: Time series
            signal_freq: Signal frequency

        Returns:
            SNR in dB
        """
        # Compute power spectrum
        fft = np.fft.fft(x)
        power = np.abs(fft)**2
        freqs = np.fft.fftfreq(len(x))

        # Find signal peak
        signal_idx = np.argmin(np.abs(freqs - signal_freq))
        signal_power = power[signal_idx]

        # Estimate noise power (excluding signal peak)
        noise_mask = np.abs(freqs - signal_freq) > 0.01
        noise_power = np.mean(power[noise_mask])

        snr = 10 * np.log10(signal_power / noise_power)
        return snr


def demonstrate_coupling():
    """Demonstrate coupled oscillator dynamics"""
    print("Demonstrating TTST Coupled Oscillators")
    print("=" * 50)

    # Create TTST system
    system = TTSTCoupledSystem()

    # Simulate Kuramoto dynamics
    print("Simulating phase coupling...")
    t, phases = system.simulate_kuramoto((0, 100), dt=0.01)

    # Calculate order parameter
    r = system.calculate_order_parameter(phases)

    # Plot results
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))

    # Phase trajectories
    axes[0].plot(t, np.mod(phases, 2*np.pi))
    axes[0].set_xlabel('Time (hours)')
    axes[0].set_ylabel('Phase (rad)')
    axes[0].set_title('Phase Evolution of Coupled Oscillators')
    axes[0].legend(['Thermal', 'Tidal', 'Solar'])
    axes[0].grid(True, alpha=0.3)

    # Order parameter
    axes[1].plot(t, r, 'k-', linewidth=2)
    axes[1].set_xlabel('Time (hours)')
    axes[1].set_ylabel('Order Parameter')
    axes[1].set_title('Synchronization Level')
    axes[1].set_ylim([0, 1])
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()

    print(f"Final synchronization level: {r[-1]:.3f}")

    return fig


if __name__ == "__main__":
    fig = demonstrate_coupling()
    plt.show()
