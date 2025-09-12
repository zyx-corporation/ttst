#!/usr/bin/env python3
"""
Tidal rhythm module for TTST
Models lunar tidal forces and their evolution through Earth history

Author: Tomoyuki Kano
License: MIT
"""

import numpy as np
from typing import Tuple, Dict, Optional
import matplotlib.pyplot as plt
from scipy import interpolate


class TidalRhythm:
    """Model tidal rhythms from lunar and solar gravitational forces"""

    def __init__(self,
                 current_period: float = 12.42,
                 early_period: float = 10.5,
                 age_earth: float = 4.5e9):
        """
        Initialize tidal rhythm model

        Args:
            current_period: Current M2 tidal period in hours
            early_period: Early Earth tidal period in hours (4 Ga)
            age_earth: Age of Earth in years
        """
        self.current_period = current_period
        self.early_period = early_period
        self.age_earth = age_earth

        # Tidal constituents (simplified)
        self.constituents = {
            'M2': {'period': 12.42, 'amplitude': 1.0, 'phase': 0.0},      # Principal lunar
            'S2': {'period': 12.00, 'amplitude': 0.46, 'phase': 0.0},     # Principal solar
            'N2': {'period': 12.66, 'amplitude': 0.19, 'phase': np.pi/4}, # Lunar elliptic
            'K1': {'period': 23.93, 'amplitude': 0.58, 'phase': np.pi/3}, # Diurnal
            'O1': {'period': 25.82, 'amplitude': 0.41, 'phase': np.pi/6}, # Diurnal
            'P1': {'period': 24.07, 'amplitude': 0.19, 'phase': np.pi/2}  # Solar diurnal
        }

    def lunar_recession_model(self, time_ago: float) -> float:
        """
        Model lunar distance as function of time

        Args:
            time_ago: Time before present in years

        Returns:
            Lunar distance in Earth radii
        """
        # Current lunar distance: 60.3 Earth radii
        # Early lunar distance: ~10 Earth radii (4 Ga)

        # Simplified exponential model
        current_distance = 60.3
        early_distance = 10.0

        if time_ago <= 0:
            return current_distance

        # Exponential recession model
        tau = 2e9  # Time constant in years
        distance = current_distance - (current_distance - early_distance) * np.exp(-time_ago / tau)

        return distance

    def tidal_period_evolution(self, time_ago: float) -> float:
        """
        Calculate tidal period at given time in Earth's history

        Args:
            time_ago: Time before present in years

        Returns:
            Tidal period in hours
        """
        # Tidal period scales with lunar distance^1.5 (Kepler's third law)
        current_distance = self.lunar_recession_model(0)
        past_distance = self.lunar_recession_model(time_ago)

        period_ratio = (past_distance / current_distance) ** 1.5
        return self.current_period * period_ratio

    def tidal_amplitude_evolution(self, time_ago: float) -> float:
        """
        Calculate tidal amplitude at given time in Earth's history

        Args:
            time_ago: Time before present in years

        Returns:
            Relative tidal amplitude
        """
        # Tidal force scales with 1/distance^3
        current_distance = self.lunar_recession_model(0)
        past_distance = self.lunar_recession_model(time_ago)

        amplitude_ratio = (current_distance / past_distance) ** 3
        return amplitude_ratio

    def harmonic_tides(self, t: np.ndarray,
                      constituents: Optional[Dict] = None) -> np.ndarray:
        """
        Calculate tidal height using harmonic constituents

        Args:
            t: Time array in hours
            constituents: Tidal constituents to use (default: all)

        Returns:
            Tidal height
        """
        if constituents is None:
            constituents = self.constituents

        tide = np.zeros_like(t)

        for name, params in constituents.items():
            omega = 2 * np.pi / params['period']
            tide += params['amplitude'] * np.cos(omega * t + params['phase'])

        return tide

    def nonlinear_shallow_water(self, t: np.ndarray,
                              depth: float = 3000,
                              basin_length: float = 5000e3) -> np.ndarray:
        """
        Model nonlinear tidal effects in shallow water

        Args:
            t: Time array in hours
            depth: Water depth in meters
            basin_length: Basin length in meters

        Returns:
            Nonlinear tidal signal
        """
        # Shallow water wave speed
        g = 9.81  # m/s^2
        c = np.sqrt(g * depth)

        # Fundamental period depends on basin size
        T_fundamental = 2 * basin_length / c / 3600  # Convert to hours

        # Linear tide
        linear_tide = self.harmonic_tides(t)

        # Add nonlinear components (harmonics)
        omega = 2 * np.pi / self.current_period
        nonlinear = (
            0.2 * linear_tide**2 +                    # Quadratic nonlinearity
            0.1 * np.sin(2 * omega * t) +            # M4 tide (overtide)
            0.05 * np.sin(3 * omega * t)             # M6 tide
        )

        return linear_tide + nonlinear

    def earth_tide(self, t: np.ndarray,
                  latitude: float = 0.0,
                  longitude: float = 0.0) -> Dict[str, np.ndarray]:
        """
        Calculate Earth tide (solid Earth deformation)

        Args:
            t: Time array in hours
            latitude: Latitude in degrees
            longitude: Longitude in degrees

        Returns:
            Dictionary with radial and horizontal components
        """
        # Love numbers for Earth
        h2 = 0.609  # Radial displacement
        l2 = 0.085  # Horizontal displacement

        # Tidal potential (simplified)
        omega = 2 * np.pi / self.current_period
        potential = np.cos(omega * t) * np.cos(np.radians(latitude))

        # Earth tide components
        radial = h2 * potential * 0.5  # meters
        horizontal_ns = l2 * potential * np.sin(2 * np.radians(latitude)) * 0.25
        horizontal_ew = l2 * potential * np.cos(np.radians(latitude)) * 0.25

        return {
            'radial': radial,
            'horizontal_ns': horizontal_ns,
            'horizontal_ew': horizontal_ew,
            'total': np.sqrt(radial**2 + horizontal_ns**2 + horizontal_ew**2)
        }

    def tidal_pumping(self, t: np.ndarray,
                     porosity: float = 0.3,
                     permeability: float = 1e-12) -> np.ndarray:
        """
        Model tidal pumping in porous media (relevant for early life)

        Args:
            t: Time array in hours
            porosity: Rock porosity (0-1)
            permeability: Permeability in m^2

        Returns:
            Pore pressure variation
        """
        # Tidal loading efficiency
        efficiency = porosity / (1 + porosity)

        # Tidal signal
        tide = self.harmonic_tides(t)

        # Pressure diffusion (simplified)
        diffusivity = permeability / (porosity * 1e-4)  # Hydraulic diffusivity
        damping = np.exp(-np.sqrt(2 * np.pi / (self.current_period * 3600) / diffusivity))

        # Pore pressure response
        pore_pressure = efficiency * tide * damping

        return pore_pressure

    def early_earth_tides(self, t: np.ndarray,
                         time_ago: float = 4e9) -> Dict[str, np.ndarray]:
        """
        Simulate tidal rhythms under early Earth conditions

        Args:
            t: Time array in hours
            time_ago: Time before present in years

        Returns:
            Dictionary with early Earth tidal signals
        """
        # Get period and amplitude for early Earth
        period = self.tidal_period_evolution(time_ago)
        amplitude = self.tidal_amplitude_evolution(time_ago)

        # Modify constituents for early Earth
        early_constituents = {}
        for name, params in self.constituents.items():
            early_constituents[name] = {
                'period': params['period'] * period / self.current_period,
                'amplitude': params['amplitude'] * amplitude,
                'phase': params['phase']
            }

        # Calculate tides
        results = {
            'ocean_tide': self.harmonic_tides(t, early_constituents),
            'period_hours': period,
            'amplitude_factor': amplitude,
            'lunar_distance_earth_radii': self.lunar_recession_model(time_ago)
        }

        # Add nonlinear effects (stronger in early Earth due to closer Moon)
        omega = 2 * np.pi / period
        results['nonlinear'] = 0.3 * amplitude * results['ocean_tide']**2
        results['total'] = results['ocean_tide'] + results['nonlinear']

        return results

    def snowball_earth_tides(self, t: np.ndarray,
                            ice_thickness: float = 1000) -> Dict[str, np.ndarray]:
        """
        Model tides during Snowball Earth events

        Args:
            t: Time array in hours
            ice_thickness: Ice sheet thickness in meters

        Returns:
            Dictionary with sub-ice tidal signals
        """
        # Regular ocean tide
        ocean_tide = self.harmonic_tides(t)

        # Ice sheet dampens but doesn't eliminate tides
        # Flexural response of ice sheet
        ice_damping = np.exp(-ice_thickness / 500)  # Empirical damping

        # Sub-ice ocean still experiences tides
        sub_ice_tide = ocean_tide * (0.8 + 0.2 * ice_damping)

        # Ice sheet flexure
        flexural_wavelength = 50e3  # meters
        ice_flexure = 0.1 * ocean_tide * ice_damping

        return {
            'surface_expression': ice_flexure,
            'sub_ice_ocean': sub_ice_tide,
            'damping_factor': ice_damping,
            'preserved_amplitude': np.mean(np.abs(sub_ice_tide)) / np.mean(np.abs(ocean_tide))
        }

    def visualize(self, duration: float = 100.0):
        """
        Visualize tidal evolution through Earth history

        Args:
            duration: Duration to simulate in hours
        """
        t = np.linspace(0, duration, 1000)

        fig, axes = plt.subplots(3, 1, figsize=(12, 10))

        # Current tides
        ax = axes[0]
        current = self.harmonic_tides(t)
        ax.plot(t, current, 'b-', linewidth=1.5, label='Current Earth')
        ax.set_ylabel('Tidal Height')
        ax.set_title('Tidal Evolution Through Earth History')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Early Earth tides
        ax = axes[1]
        early = self.early_earth_tides(t, time_ago=4e9)
        ax.plot(t, early['total'], 'r-', linewidth=1.5, label=f"Early Earth (4 Ga)")
        ax.set_ylabel('Tidal Height')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.text(0.02, 0.95, f"Period: {early['period_hours']:.1f} h\n"
                           f"Amplitude: {early['amplitude_factor']:.1f}x current",
                transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        # Snowball Earth
        ax = axes[2]
        snowball = self.snowball_earth_tides(t)
        ax.plot(t, snowball['sub_ice_ocean'], 'c-', linewidth=1.5,
                label='Sub-ice Ocean')
        ax.plot(t, snowball['surface_expression'], 'gray', linewidth=1,
                label='Ice Surface', alpha=0.7)
        ax.set_ylabel('Tidal Height')
        ax.set_xlabel('Time (hours)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.text(0.02, 0.95, f"Preservation: {snowball['preserved_amplitude']:.1%}",
                transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

        plt.tight_layout()
        return fig


def main():
    """Demonstrate tidal rhythm module"""
    print("TTST Tidal Rhythm Module")
    print("=" * 50)

    # Create tidal model
    tidal = TidalRhythm()

    # Show evolution
    times_ago = [4e9, 2e9, 600e6, 0]  # Years ago

    for time_ago in times_ago:
        period = tidal.tidal_period_evolution(time_ago)
        amplitude = tidal.tidal_amplitude_evolution(time_ago)
        distance = tidal.lunar_recession_model(time_ago)

        print(f"\nTime: {time_ago/1e9:.1f} Ga")
        print(f"  Tidal period: {period:.1f} hours")
        print(f"  Relative amplitude: {amplitude:.1f}x current")
        print(f"  Lunar distance: {distance:.1f} Earth radii")

    # Visualize
    fig = tidal.visualize()
    plt.show()


if __name__ == "__main__":
    main()
# End of tidal_rhythm.py
