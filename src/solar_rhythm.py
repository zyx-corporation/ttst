#!/usr/bin/env python3
"""
Solar rhythm module for TTST
Models day-night cycles and their evolution through Earth history

Author: Tomoyuki Kano
License: MIT
"""

import numpy as np
from typing import Tuple, Dict, Optional
import matplotlib.pyplot as plt
from scipy import interpolate
from datetime import datetime, timedelta


class SolarRhythm:
    """Model solar rhythms and day-night cycles"""

    def __init__(self,
                 current_day_length: float = 24.0,
                 early_day_length: float = 10.0):
        """
        Initialize solar rhythm model

        Args:
            current_day_length: Current day length in hours
            early_day_length: Early Earth day length in hours (4 Ga)
        """
        self.current_day_length = current_day_length
        self.early_day_length = early_day_length

    def day_length_evolution(self, time_ago: float) -> float:
        """
        Calculate day length at given time in Earth's history

        Args:
            time_ago: Time before present in years

        Returns:
            Day length in hours
        """
        if time_ago <= 0:
            return self.current_day_length

        # Simplified model: exponential approach to current value
        # Based on tidal friction slowing Earth's rotation
        tau = 2.5e9  # Time constant in years

        day_length = self.current_day_length - (
            self.current_day_length - self.early_day_length
        ) * np.exp(-time_ago / tau)

        return day_length

    def solar_irradiance(self, t: np.ndarray,
                        latitude: float = 0.0,
                        day_length: float = 24.0,
                        solar_constant: float = 1361) -> np.ndarray:
        """
        Calculate solar irradiance at given latitude

        Args:
            t: Time array in hours
            latitude: Latitude in degrees
            day_length: Length of day in hours
            solar_constant: Solar constant in W/m^2

        Returns:
            Solar irradiance in W/m^2
        """
        omega = 2 * np.pi / day_length

        # Solar zenith angle (simplified, no seasons)
        lat_rad = np.radians(latitude)
        zenith = np.arccos(np.cos(lat_rad) * np.cos(omega * t))

        # Irradiance (Lambert's cosine law)
        irradiance = solar_constant * np.maximum(0, np.cos(zenith))

        # Add atmospheric attenuation
        atmosphere_transmission = 0.75
        irradiance *= atmosphere_transmission

        return irradiance

    def photoperiod(self, t: np.ndarray,
                   day_length: float = 24.0,
                   twilight_duration: float = 0.5) -> np.ndarray:
        """
        Generate photoperiod signal (light/dark cycle)

        Args:
            t: Time array in hours
            day_length: Length of day in hours
            twilight_duration: Duration of twilight in hours

        Returns:
            Light intensity (0-1)
        """
        omega = 2 * np.pi / day_length

        # Base sinusoidal signal
        base_signal = np.sin(omega * t)

        # Sharp transitions with twilight
        sharpness = 2 * np.pi / twilight_duration
        light_signal = 0.5 + 0.5 * np.tanh(sharpness * base_signal)

        return light_signal

    def circadian_forcing(self, t: np.ndarray,
                        day_length: float = 24.0,
                        light_sensitivity: float = 1.0) -> np.ndarray:
        """
        Calculate circadian forcing signal

        Args:
            t: Time array in hours
            day_length: Length of day in hours
            light_sensitivity: Sensitivity to light (0-1)

        Returns:
            Circadian forcing signal
        """
        # Light signal
        light = self.photoperiod(t, day_length)

        # Non-photic signals (temperature, feeding, etc.)
        omega = 2 * np.pi / day_length
        temperature = 0.3 * np.sin(omega * t - np.pi/4)  # Temperature lags light

        # Combined forcing
        forcing = light_sensitivity * light + (1 - light_sensitivity) * temperature

        return forcing

    def uv_radiation(self, t: np.ndarray,
                    day_length: float = 24.0,
                    ozone_factor: float = 1.0) -> np.ndarray:
        """
        Model UV radiation levels

        Args:
            t: Time array in hours
            day_length: Length of day in hours
            ozone_factor: Ozone layer effectiveness (0-1, 0=no ozone)

        Returns:
            UV radiation intensity
        """
        # Solar elevation affects UV more strongly than visible light
        omega = 2 * np.pi / day_length
        elevation = np.maximum(0, np.sin(omega * t))

        # UV intensity (stronger at noon)
        uv_base = elevation ** 1.5

        # Ozone absorption
        uv_surface = uv_base * (1 - 0.9 * ozone_factor)

        return uv_surface

    def early_earth_solar(self, t: np.ndarray,
                         time_ago: float = 4e9) -> Dict[str, np.ndarray]:
        """
        Simulate solar rhythms under early Earth conditions

        Args:
            t: Time array in hours
            time_ago: Time before present in years

        Returns:
            Dictionary with early Earth solar signals
        """
        # Early Earth parameters
        day_length = self.day_length_evolution(time_ago)

        # Faint young Sun (70% current luminosity at 4 Ga)
        solar_luminosity = 0.7 + 0.3 * (1 - time_ago / 4.5e9)
        solar_constant = 1361 * solar_luminosity

        # No ozone layer
        ozone_factor = 0.0 if time_ago > 2.4e9 else (2.4e9 - time_ago) / 2.4e9

        results = {
            'day_length_hours': day_length,
            'photoperiod': self.photoperiod(t, day_length),
            'irradiance': self.solar_irradiance(t, day_length=day_length,
                                              solar_constant=solar_constant),
            'uv_radiation': self.uv_radiation(t, day_length, ozone_factor),
            'circadian_forcing': self.circadian_forcing(t, day_length),
            'solar_luminosity_fraction': solar_luminosity
        }

        return results

    def snowball_earth_solar(self, t: np.ndarray,
                           albedo: float = 0.9) -> Dict[str, np.ndarray]:
        """
        Model solar rhythms during Snowball Earth

        Args:
            t: Time array in hours
            albedo: Surface albedo (0-1, ice ~0.9)

        Returns:
            Dictionary with Snowball Earth solar signals
        """
        # Normal photoperiod continues
        photoperiod = self.photoperiod(t)

        # Very high albedo reduces absorbed radiation
        irradiance = self.solar_irradiance(t)
        absorbed = irradiance * (1 - albedo)

        # No photosynthesis possible at surface
        photosynthetic_radiation = np.zeros_like(t)

        # Subsurface light (through ice)
        ice_transmission = 0.01  # ~1% light through thick ice
        subsurface_light = photoperiod * ice_transmission

        return {
            'surface_irradiance': irradiance,
            'absorbed_radiation': absorbed,
            'subsurface_light': subsurface_light,
            'photosynthetic_radiation': photosynthetic_radiation,
            'albedo': albedo
        }

    def seasonal_variation(self, t: np.ndarray,
                          latitude: float = 23.5,
                          axial_tilt: float = 23.5,
                          day_of_year_start: int = 0) -> np.ndarray:
        """
        Model seasonal variation in day length

        Args:
            t: Time array in hours
            latitude: Latitude in degrees
            axial_tilt: Earth's axial tilt in degrees
            day_of_year_start: Starting day of year

        Returns:
            Day length variation in hours
        """
        # Convert time to days
        days = t / 24.0 + day_of_year_start

        # Solar declination
        declination = axial_tilt * np.sin(2 * np.pi * days / 365.25)

        # Day length calculation
        lat_rad = np.radians(latitude)
        decl_rad = np.radians(declination)

        # Hour angle at sunrise/sunset
        cos_hour_angle = -np.tan(lat_rad) * np.tan(decl_rad)

        # Handle polar day/night
        cos_hour_angle = np.clip(cos_hour_angle, -1, 1)

        # Day length
        hour_angle = np.arccos(cos_hour_angle)
        day_length = 2 * hour_angle * 12 / np.pi

        return day_length

    def biological_response(self, t: np.ndarray,
                          organism_type: str = 'cyanobacteria') -> Dict[str, np.ndarray]:
        """
        Model biological response to solar rhythms

        Args:
            t: Time array in hours
            organism_type: Type of organism

        Returns:
            Dictionary with biological responses
        """
        light = self.photoperiod(t)

        responses = {}

        if organism_type == 'cyanobacteria':
            # Photosynthesis rate
            responses['photosynthesis'] = light * (1 - 0.2 * light**2)  # Photoinhibition

            # Nitrogen fixation (higher at night)
            responses['nitrogen_fixation'] = 1 - light

            # Cell division (peaks at dusk)
            omega = 2 * np.pi / 24
            responses['cell_division'] = np.exp(-((t % 24 - 18)**2) / 8)

        elif organism_type == 'early_eukaryote':
            # More complex responses
            responses['metabolism'] = 0.5 + 0.5 * light
            responses['dna_repair'] = 0.3 + 0.7 * (1 - light)  # Higher at night
            responses['mitosis'] = np.sin(2 * np.pi * t / 24 + np.pi)

        return responses

    def visualize(self, duration: float = 72.0):
        """
        Visualize solar rhythms

        Args:
            duration: Duration to simulate in hours
        """
        t = np.linspace(0, duration, 1000)

        fig, axes = plt.subplots(4, 1, figsize=(12, 12))

        # Current Earth
        ax = axes[0]
        current = self.photoperiod(t)
        ax.fill_between(t, 0, current, alpha=0.3, color='yellow', label='Day')
        ax.fill_between(t, 0, 1-current, alpha=0.3, color='blue', label='Night')
        ax.plot(t, current, 'k-', linewidth=1.5)
        ax.set_ylabel('Light Level')
        ax.set_title('Solar Rhythms: Current vs Early Earth')
        ax.set_ylim([0, 1])
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Early Earth
        ax = axes[1]
        early = self.early_earth_solar(t, time_ago=4e9)
        ax.plot(t, early['photoperiod'], 'r-', linewidth=1.5)
        ax.set_ylabel('Light Level')
        ax.set_ylim([0, 1])
        ax.grid(True, alpha=0.3)
        ax.text(0.02, 0.95, f"Day length: {early['day_length_hours']:.1f} h\n"
                           f"Solar: {early['solar_luminosity_fraction']:.0%} current",
                transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        # UV Radiation
        ax = axes[2]
        ax.plot(t, self.uv_radiation(t, ozone_factor=1.0),
                'g-', label='With ozone', linewidth=1.5)
        ax.plot(t, self.uv_radiation(t, ozone_factor=0.0),
                'r--', label='No ozone', linewidth=1.5)
        ax.set_ylabel('UV Intensity')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Biological response
        ax = axes[3]
        bio = self.biological_response(t, 'cyanobacteria')
        ax.plot(t, bio['photosynthesis'], label='Photosynthesis', linewidth=1.5)
        ax.plot(t, bio['nitrogen_fixation'], label='N2 fixation', linewidth=1.5)
        ax.plot(t, bio['cell_division'], label='Cell division', linewidth=1.5)
        ax.set_ylabel('Activity')
        ax.set_xlabel('Time (hours)')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig


def main():
    """Demonstrate solar rhythm module"""
    print("TTST Solar Rhythm Module")
    print("=" * 50)

    # Create solar model
    solar = SolarRhythm()

    # Show evolution
    times_ago = [4e9, 2.4e9, 600e6, 0]  # Years ago

    for time_ago in times_ago:
        day_length = solar.day_length_evolution(time_ago)
        print(f"\nTime: {time_ago/1e9:.1f} Ga")
        print(f"  Day length: {day_length:.1f} hours")
        print(f"  Rotation rate: {24/day_length:.2f}x current")

    # Visualize
    fig = solar.visualize()
    plt.show()


if __name__ == "__main__":
    main()
# End of solar_rhythm.py
