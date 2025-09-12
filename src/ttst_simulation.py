#!/usr/bin/env python3
"""
TTST - Tidal-Thermal Synchronization Theory
Main simulation module

Author: Tomoyuki Kano
License: MIT
"""

import numpy as np
import json
import pandas as pd
from typing import Tuple, Dict, Optional
from dataclasses import dataclass
import matplotlib.pyplot as plt
from scipy import signal
from pathlib import Path


@dataclass
class TTSTParameters:
    """Parameters for TTST simulation"""
    thermal_period: float = 0.5  # hours
    tidal_period: float = 12.4   # hours
    solar_period: float = 24.0    # hours
    thermal_amplitude: float = 1.0
    tidal_amplitude: float = 1.0
    solar_amplitude: float = 1.0
    coupling_strength: float = 0.3
    noise_level: float = 0.1


class TTST:
    """Main TTST simulation class"""

    def __init__(self, params: Optional[TTSTParameters] = None):
        """Initialize TTST simulation

        Args:
            params: Simulation parameters. If None, uses defaults.
        """
        self.params = params or TTSTParameters()
        self.load_data()
        self.time = None
        self.combined_rhythm = None
        self.thermal = None
        self.tidal = None
        self.solar = None

    def load_data(self):
        """Load configuration data from JSON and CSV files"""
        # Try to load from data directory
        data_dir = Path(__file__).parent.parent / 'data'

        if (data_dir / 'rhythm_frequencies.json').exists():
            with open(data_dir / 'rhythm_frequencies.json', 'r') as f:
                self.rhythm_config = json.load(f)
        else:
            # Use default configuration if file not found
            self.rhythm_config = self._get_default_config()

        if (data_dir / 'early_earth_params.csv').exists():
            self.earth_params = pd.read_csv(data_dir / 'early_earth_params.csv')
        else:
            self.earth_params = None

    def _get_default_config(self) -> Dict:
        """Get default configuration if files not found"""
        return {
            'coupling_parameters': {
                'thermal_tidal_coupling': 0.3,
                'tidal_solar_coupling': 0.5,
                'solar_thermal_coupling': 0.2,
                'biological_feedback_strength': 0.1
            }
        }

    def thermal_rhythm(self, t: np.ndarray) -> np.ndarray:
        """Calculate thermal rhythm signal

        Args:
            t: Time array in hours

        Returns:
            Thermal rhythm signal
        """
        # Primary oscillation
        primary = self.params.thermal_amplitude * np.sin(
            2 * np.pi * t / self.params.thermal_period
        )

        # Add harmonics
        second_harmonic = 0.3 * np.sin(
            4 * np.pi * t / self.params.thermal_period + np.pi/4
        )

        # Add stochastic component
        noise = self.params.noise_level * np.random.randn(len(t))

        return primary + second_harmonic + noise

    def tidal_rhythm(self, t: np.ndarray) -> np.ndarray:
        """Calculate tidal rhythm signal

        Args:
            t: Time array in hours

        Returns:
            Tidal rhythm signal
        """
        # Primary M2 tide
        M2 = self.params.tidal_amplitude * np.sin(
            2 * np.pi * t / self.params.tidal_period
        )

        # Nonlinear component (squared term)
        nonlinear = 0.2 * np.sin(
            2 * np.pi * t / self.params.tidal_period
        ) ** 2

        return M2 + nonlinear

    def solar_rhythm(self, t: np.ndarray) -> np.ndarray:
        """Calculate solar rhythm signal

        Args:
            t: Time array in hours

        Returns:
            Solar rhythm signal (sharp day-night transitions)
        """
        # Use tanh for sharp transitions
        sharpness = 10.0
        base_signal = np.sin(2 * np.pi * t / self.params.solar_period)

        return self.params.solar_amplitude * (
            0.5 + 0.5 * np.tanh(sharpness * base_signal)
        )

    def simulate(self, duration: float = 100.0, dt: float = 0.01) -> Tuple[np.ndarray, np.ndarray]:
        """Run TTST simulation

        Args:
            duration: Simulation duration in hours
            dt: Time step in hours

        Returns:
            Tuple of (time array, combined rhythm signal)
        """
        # Create time array
        self.time = np.arange(0, duration, dt)

        # Calculate individual rhythms
        self.thermal = self.thermal_rhythm(self.time)
        self.tidal = self.tidal_rhythm(self.time)
        self.solar = self.solar_rhythm(self.time)

        # Get coupling parameters
        coupling = self.rhythm_config.get('coupling_parameters', {})
        alpha = coupling.get('thermal_tidal_coupling', 0.3)
        beta = coupling.get('tidal_solar_coupling', 0.5)
        gamma = coupling.get('solar_thermal_coupling', 0.2)

        # Calculate coupled signal with nonlinear interactions
        self.combined_rhythm = (
            self.thermal +
            self.tidal +
            self.solar +
            alpha * self.thermal * self.tidal +
            beta * self.tidal * self.solar +
            gamma * self.solar * self.thermal
        )

        return self.time, self.combined_rhythm

    def calculate_synchronization(self) -> float:
        """Calculate synchronization index between rhythms

        Returns:
            Synchronization index (0-1)
        """
        if self.thermal is None or self.tidal is None:
            raise ValueError("Must run simulate() first")

        # Calculate phase synchronization using Hilbert transform
        thermal_phase = np.angle(signal.hilbert(self.thermal))
        tidal_phase = np.angle(signal.hilbert(self.tidal))

        # Phase difference
        phase_diff = thermal_phase - tidal_phase

        # Synchronization index (mean vector length)
        sync_index = np.abs(np.mean(np.exp(1j * phase_diff)))

        return sync_index

    def find_arnold_tongues(self,
                          thermal_range: Tuple[float, float] = (0.25, 2.0),
                          tidal_range: Tuple[float, float] = (10, 15),
                          resolution: int = 50) -> np.ndarray:
        """Find Arnold tongue synchronization regions

        Args:
            thermal_range: Range of thermal periods to test
            tidal_range: Range of tidal periods to test
            resolution: Grid resolution

        Returns:
            2D array of synchronization strengths
        """
        thermal_periods = np.linspace(thermal_range[0], thermal_range[1], resolution)
        tidal_periods = np.linspace(tidal_range[0], tidal_range[1], resolution)

        sync_map = np.zeros((resolution, resolution))

        for i, t_thermal in enumerate(thermal_periods):
            for j, t_tidal in enumerate(tidal_periods):
                # Create temporary parameters
                temp_params = TTSTParameters(
                    thermal_period=t_thermal,
                    tidal_period=t_tidal,
                    solar_period=self.params.solar_period
                )

                # Run short simulation
                temp_sim = TTST(temp_params)
                temp_sim.simulate(duration=50, dt=0.01)

                # Calculate synchronization
                sync_map[i, j] = temp_sim.calculate_synchronization()

        return sync_map

    def snowball_earth_modulation(self, t: np.ndarray) -> Dict[str, np.ndarray]:
        """Simulate rhythm disruption during Snowball Earth

        Args:
            t: Time array

        Returns:
            Dictionary with modulated rhythms
        """
        # Get Snowball Earth parameters
        snowball = self.rhythm_config.get('snowball_earth_modulation', {})

        # Normal rhythms
        thermal = self.thermal_rhythm(t)
        tidal = self.tidal_rhythm(t)
        solar = self.solar_rhythm(t)

        # Apply Snowball Earth modulation
        thermal_modulated = thermal * snowball.get('thermal_persistence', 1.0)
        tidal_modulated = tidal * snowball.get('tidal_persistence', 0.8)
        solar_modulated = solar * snowball.get('solar_reduction', 0.0)

        return {
            'thermal': thermal_modulated,
            'tidal': tidal_modulated,
            'solar': solar_modulated,
            'combined': thermal_modulated + tidal_modulated + solar_modulated
        }

    def plot_rhythms(self, duration: float = 48.0):
        """Plot the three rhythms and combined signal

        Args:
            duration: Duration to plot in hours
        """
        if self.time is None:
            self.simulate(duration=duration)

        fig, axes = plt.subplots(4, 1, figsize=(12, 10))

        # Thermal rhythm
        axes[0].plot(self.time, self.thermal, 'r-', linewidth=1)
        axes[0].set_ylabel('Thermal')
        axes[0].set_title('Environmental Rhythms')
        axes[0].grid(True, alpha=0.3)

        # Tidal rhythm
        axes[1].plot(self.time, self.tidal, 'b-', linewidth=1.5)
        axes[1].set_ylabel('Tidal')
        axes[1].grid(True, alpha=0.3)

        # Solar rhythm
        axes[2].plot(self.time, self.solar, 'orange', linewidth=2)
        axes[2].set_ylabel('Solar')
        axes[2].grid(True, alpha=0.3)

        # Add day/night shading
        for ax in axes[:3]:
            for i in range(int(duration / self.params.solar_period) + 1):
                start = i * self.params.solar_period
                ax.axvspan(start, start + self.params.solar_period/2,
                          alpha=0.1, color='yellow')
                ax.axvspan(start + self.params.solar_period/2,
                          start + self.params.solar_period,
                          alpha=0.1, color='blue')

        # Combined rhythm
        axes[3].plot(self.time, self.combined_rhythm, 'k-', linewidth=1.5)
        axes[3].set_ylabel('Combined')
        axes[3].set_xlabel('Time (hours)')
        axes[3].grid(True, alpha=0.3)

        plt.tight_layout()
        return fig


def main():
    """Main function for testing"""
    print("TTST - Tidal-Thermal Synchronization Theory")
    print("=" * 50)

    # Initialize simulation
    model = TTST()

    # Run simulation
    print("Running simulation...")
    time, combined = model.simulate(duration=100)

    # Calculate synchronization
    sync_index = model.calculate_synchronization()
    print(f"Synchronization Index: {sync_index:.3f}")

    # Plot results
    print("Generating plots...")
    fig = model.plot_rhythms()
    plt.show()

    print("\nSimulation complete!")


if __name__ == "__main__":
    main()