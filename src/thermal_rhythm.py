#!/usr/bin/env python3
"""
Thermal rhythm module for TTST
Models hydrothermal vent pulsations and thermal oscillations

Author: Tomoyuki Kano
License: MIT
"""

import numpy as np
from typing import Tuple, Optional, Dict
from scipy import signal
import matplotlib.pyplot as plt


class ThermalRhythm:
    """Model thermal oscillations from hydrothermal vents"""

    def __init__(self,
                 base_period: float = 0.5,
                 amplitude: float = 1.0,
                 temperature_range: Tuple[float, float] = (2, 400)):
        """
        Initialize thermal rhythm model

        Args:
            base_period: Base oscillation period in hours
            amplitude: Oscillation amplitude
            temperature_range: Temperature range (min, max) in Celsius
        """
        self.base_period = base_period
        self.amplitude = amplitude
        self.temp_min, self.temp_max = temperature_range
        self.temp_mean = (self.temp_min + self.temp_max) / 2
        self.temp_amplitude = (self.temp_max - self.temp_min) / 2

    def convective_oscillation(self, t: np.ndarray,
                              rayleigh_number: float = 1e6) -> np.ndarray:
        """
        Model convective oscillations based on Rayleigh-Bénard convection

        Args:
            t: Time array in hours
            rayleigh_number: Rayleigh number for convection

        Returns:
            Convective oscillation signal
        """
        # Critical Rayleigh number for onset of convection
        Ra_critical = 1708

        if rayleigh_number < Ra_critical:
            # No convection - steady state
            return np.zeros_like(t)

        # Frequency scales with sqrt(Ra - Ra_c)
        freq_factor = np.sqrt((rayleigh_number - Ra_critical) / Ra_critical)

        # Primary convective mode
        omega1 = 2 * np.pi / (self.base_period / freq_factor)
        oscillation = self.amplitude * np.sin(omega1 * t)

        # Add higher harmonics for turbulent convection
        if rayleigh_number > 1e5:
            oscillation += 0.3 * self.amplitude * np.sin(2 * omega1 * t + np.pi/4)
            oscillation += 0.1 * self.amplitude * np.sin(3 * omega1 * t + np.pi/2)

        return oscillation

    def pressure_fluctuations(self, t: np.ndarray,
                            depth: float = 3000) -> np.ndarray:
        """
        Model pressure-driven fluctuations at hydrothermal vents

        Args:
            t: Time array in hours
            depth: Ocean depth in meters

        Returns:
            Pressure fluctuation signal
        """
        # Pressure increases with depth
        pressure_factor = depth / 1000  # Normalize by 1 km

        # Multiple frequency components from different sources
        f1 = 1 / (self.base_period * 0.7)  # Fast component
        f2 = 1 / (self.base_period * 1.5)  # Slow component
        f3 = 1 / (self.base_period * 3.0)  # Very slow component

        signal_components = (
            0.5 * np.sin(2 * np.pi * f1 * t) +
            0.3 * np.sin(2 * np.pi * f2 * t + np.pi/3) +
            0.2 * np.sin(2 * np.pi * f3 * t + 2*np.pi/3)
        )

        return pressure_factor * self.amplitude * signal_components

    def chemical_oscillations(self, t: np.ndarray,
                            pH_variation: float = 2.0) -> np.ndarray:
        """
        Model chemical oscillations (e.g., pH, redox potential)

        Args:
            t: Time array in hours
            pH_variation: Range of pH variation

        Returns:
            Chemical oscillation signal
        """
        # Belousov-Zhabotinsky-like oscillations
        omega = 2 * np.pi / self.base_period

        # Relaxation oscillations with sharp transitions
        base_signal = np.sin(omega * t)
        relaxation = np.tanh(5 * base_signal)

        # Add chemical reaction noise
        reaction_noise = 0.1 * np.random.randn(len(t))

        return pH_variation * (relaxation + reaction_noise)

    def stochastic_pulsations(self, t: np.ndarray,
                            correlation_time: float = 0.1,
                            noise_level: float = 0.2) -> np.ndarray:
        """
        Generate stochastic pulsations with temporal correlation

        Args:
            t: Time array in hours
            correlation_time: Correlation time for noise
            noise_level: Noise intensity

        Returns:
            Correlated noise signal
        """
        dt = t[1] - t[0] if len(t) > 1 else 0.01
        n_points = len(t)

        # Generate white noise
        white_noise = np.random.randn(n_points)

        # Apply exponential filter for correlation
        alpha = dt / (correlation_time + dt)
        filtered_noise = np.zeros(n_points)
        filtered_noise[0] = white_noise[0]

        for i in range(1, n_points):
            filtered_noise[i] = (1 - alpha) * filtered_noise[i-1] + alpha * white_noise[i]

        return noise_level * self.amplitude * filtered_noise

    def composite_thermal_signal(self, t: np.ndarray,
                               rayleigh: float = 1e6,
                               depth: float = 3000,
                               include_stochastic: bool = True) -> Dict[str, np.ndarray]:
        """
        Generate composite thermal signal with all components

        Args:
            t: Time array in hours
            rayleigh: Rayleigh number
            depth: Ocean depth in meters
            include_stochastic: Whether to include stochastic component

        Returns:
            Dictionary with signal components and total
        """
        components = {
            'convection': self.convective_oscillation(t, rayleigh),
            'pressure': self.pressure_fluctuations(t, depth),
            'chemical': self.chemical_oscillations(t)
        }

        if include_stochastic:
            components['stochastic'] = self.stochastic_pulsations(t)
        else:
            components['stochastic'] = np.zeros_like(t)

        # Combine all components
        components['total'] = sum(components.values())

        # Convert to temperature
        components['temperature'] = (
            self.temp_mean +
            self.temp_amplitude * components['total'] / np.max(np.abs(components['total']))
        )

        return components

    def early_earth_conditions(self, t: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Simulate thermal rhythms under early Earth conditions (4 Ga)

        Args:
            t: Time array in hours

        Returns:
            Dictionary with early Earth thermal signals
        """
        # Early Earth had higher heat flow and more active volcanism
        early_rayleigh = 1e7  # Higher Rayleigh number
        early_depth = 3000     # Similar ocean depth

        # Generate signals with early Earth parameters
        signals = self.composite_thermal_signal(
            t,
            rayleigh=early_rayleigh,
            depth=early_depth,
            include_stochastic=True
        )

        # Add additional high-frequency components from more active volcanism
        volcanic_pulses = 0.5 * self.amplitude * np.sin(
            2 * np.pi * t / (self.base_period / 3) +
            np.random.random() * 2 * np.pi
        )

        signals['volcanic'] = volcanic_pulses
        signals['total'] += volcanic_pulses

        return signals

    def power_spectrum(self, signal: np.ndarray,
                      sampling_rate: float = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate power spectrum of thermal signal

        Args:
            signal: Input signal
            sampling_rate: Sampling rate in samples per hour

        Returns:
            Frequencies and power spectrum
        """
        freqs, psd = signal.welch(signal, fs=sampling_rate, nperseg=min(256, len(signal)))
        return freqs, psd

    def visualize(self, duration: float = 24.0, dt: float = 0.01):
        """
        Visualize thermal rhythm components

        Args:
            duration: Duration in hours
            dt: Time step in hours
        """
        t = np.arange(0, duration, dt)
        signals = self.composite_thermal_signal(t)

        fig, axes = plt.subplots(3, 1, figsize=(12, 10))

        # Component signals
        ax = axes[0]
        ax.plot(t, signals['convection'], label='Convection', alpha=0.7)
        ax.plot(t, signals['pressure'], label='Pressure', alpha=0.7)
        ax.plot(t, signals['chemical'], label='Chemical', alpha=0.7)
        ax.set_ylabel('Amplitude')
        ax.set_title('Thermal Rhythm Components')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)

        # Total signal
        ax = axes[1]
        ax.plot(t, signals['total'], 'r-', linewidth=1.5)
        ax.fill_between(t, signals['total'], alpha=0.3, color='red')
        ax.set_ylabel('Total Signal')
        ax.set_title('Composite Thermal Rhythm')
        ax.grid(True, alpha=0.3)

        # Temperature
        ax = axes[2]
        ax.plot(t, signals['temperature'], 'k-', linewidth=1.5)
        ax.axhline(y=self.temp_mean, color='gray', linestyle='--', alpha=0.5)
        ax.set_ylabel('Temperature (°C)')
        ax.set_xlabel('Time (hours)')
        ax.set_title('Hydrothermal Vent Temperature')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig


def main():
    """Demonstrate thermal rhythm module"""
    print("TTST Thermal Rhythm Module")
    print("=" * 50)

    # Create thermal rhythm model
    thermal = ThermalRhythm(base_period=0.5, amplitude=1.0)

    # Generate signals
    t = np.arange(0, 24, 0.01)
    signals = thermal.composite_thermal_signal(t)

    print(f"Temperature range: {thermal.temp_min}°C - {thermal.temp_max}°C")
    print(f"Base period: {thermal.base_period} hours")
    print(f"Signal components: {list(signals.keys())}")

    # Visualize
    fig = thermal.visualize()
    plt.show()


if __name__ == "__main__":
    main()
