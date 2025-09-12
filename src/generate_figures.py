#!/usr/bin/env python3
"""
Generate figures for TTST paper
Creates publication-quality figures demonstrating the theory

Author: Tomoyuki Kano
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import seaborn as sns
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from ttst_simulation import TTST, TTSTParameters
from coupled_oscillators import TTSTCoupledSystem, StochasticResonance
from thermal_rhythm import ThermalRhythm
from tidal_rhythm import TidalRhythm
from solar_rhythm import SolarRhythm

# Set style for publication
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10


def create_figure_dir():
    """Create figures directory if it doesn't exist"""
    fig_dir = Path(__file__).parent.parent / 'figures'
    fig_dir.mkdir(exist_ok=True)
    return fig_dir


def figure1_conceptual_overview():
    """Figure 1: Conceptual overview of TTST"""
    fig = plt.figure(figsize=(10, 10))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

    # Main conceptual diagram
    ax_main = fig.add_subplot(gs[0, :])

    # Create concentric circles for rhythms
    theta = np.linspace(0, 2*np.pi, 100)

    # Thermal (innermost)
    r_thermal = 1
    x_thermal = r_thermal * np.cos(theta)
    y_thermal = r_thermal * np.sin(theta)
    ax_main.fill(x_thermal, y_thermal, color='red', alpha=0.3, label='Thermal')
    ax_main.plot(x_thermal, y_thermal, 'r-', linewidth=2)

    # Tidal (middle)
    r_tidal = 2
    x_tidal = r_tidal * np.cos(theta)
    y_tidal = r_tidal * np.sin(theta)
    ax_main.fill(x_tidal, y_tidal, color='blue', alpha=0.2, label='Tidal')
    ax_main.plot(x_tidal, y_tidal, 'b-', linewidth=2)

    # Solar (outermost)
    r_solar = 3
    x_solar = r_solar * np.cos(theta)
    y_solar = r_solar * np.sin(theta)
    ax_main.fill(x_solar, y_solar, color='orange', alpha=0.1, label='Solar')
    ax_main.plot(x_solar, y_solar, 'orange', linewidth=2)

    # Add labels
    ax_main.text(0, 0, 'Earth\nCore', ha='center', va='center', fontsize=12, fontweight='bold')
    ax_main.text(0, -1.5, 'Thermal\n(minutes-hours)', ha='center', va='center', fontsize=10)
    ax_main.text(0, -2.5, 'Tidal\n(12.4 hours)', ha='center', va='center', fontsize=10)
    ax_main.text(0, -3.5, 'Solar\n(24 hours)', ha='center', va='center', fontsize=10)

    # Add arrows showing energy flow
    ax_main.annotate('', xy=(0.7, 0.7), xytext=(0, 0),
                    arrowprops=dict(arrowstyle='->', lw=2, color='red'))
    ax_main.annotate('', xy=(1.4, 1.4), xytext=(0.7, 0.7),
                    arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
    ax_main.annotate('', xy=(2.1, 2.1), xytext=(1.4, 1.4),
                    arrowprops=dict(arrowstyle='->', lw=2, color='orange'))

    ax_main.set_xlim([-4, 4])
    ax_main.set_ylim([-4, 4])
    ax_main.set_aspect('equal')
    ax_main.axis('off')
    ax_main.set_title('Tidal-Thermal Synchronization Theory\nHierarchical Environmental Rhythms',
                     fontsize=14, fontweight='bold')

    # Timeline
    ax_timeline = fig.add_subplot(gs[1, 0])
    times = [4.0, 2.5, 0.6, 0]
    labels = ['Life Origin\n(4 Ga)', 'Great Oxidation\n(2.5 Ga)',
              'Cambrian\n(0.6 Ga)', 'Present']
    colors = ['red', 'green', 'blue', 'black']

    ax_timeline.scatter(times, [1]*len(times), s=100, c=colors, zorder=3)
    ax_timeline.plot(times, [1]*len(times), 'k-', linewidth=1, zorder=1)

    for time, label, color in zip(times, labels, colors):
        ax_timeline.text(time, 1.1, label, ha='center', va='bottom', fontsize=9)

    ax_timeline.set_xlim([4.5, -0.5])
    ax_timeline.set_ylim([0.8, 1.3])
    ax_timeline.set_xlabel('Billion Years Ago')
    ax_timeline.set_title('Evolutionary Timeline')
    ax_timeline.set_yticks([])
    ax_timeline.grid(True, alpha=0.3, axis='x')

    # Biological systems
    ax_bio = fig.add_subplot(gs[1, 1])

    systems = ['Circulation', 'Neural\nOscillations', 'Circadian\nClocks']
    rhythms = ['Thermal', 'Tidal', 'Solar']
    connections = np.array([[1, 0.5, 0.2],
                           [0.3, 1, 0.3],
                           [0.2, 0.3, 1]])

    im = ax_bio.imshow(connections, cmap='RdYlBu_r', vmin=0, vmax=1)
    ax_bio.set_xticks(range(len(rhythms)))
    ax_bio.set_yticks(range(len(systems)))
    ax_bio.set_xticklabels(rhythms)
    ax_bio.set_yticklabels(systems)
    ax_bio.set_title('Rhythm-System Coupling')

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax_bio, fraction=0.046, pad=0.04)
    cbar.set_label('Coupling Strength')

    plt.suptitle('Figure 1: Conceptual Overview of TTST', fontsize=14, y=0.98)

    return fig


def figure2_environmental_rhythms():
    """Figure 2: The three environmental rhythms"""
    # Create TTST simulation
    model = TTST()
    t, combined = model.simulate(duration=48, dt=0.01)

    fig, axes = plt.subplots(4, 1, figsize=(10, 10), sharex=True)

    # Thermal
    axes[0].plot(t, model.thermal, 'r-', linewidth=0.5, alpha=0.8)
    axes[0].fill_between(t, model.thermal, alpha=0.3, color='red')
    axes[0].set_ylabel('Thermal\nAmplitude')
    axes[0].set_title('Environmental Rhythms', fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim([-2, 2])

    # Tidal
    axes[1].plot(t, model.tidal, 'b-', linewidth=1.5)
    axes[1].fill_between(t, model.tidal, alpha=0.3, color='blue')
    axes[1].set_ylabel('Tidal\nAmplitude')
    axes[1].grid(True, alpha=0.3)
    axes[1].set_ylim([-1.5, 1.5])

    # Solar
    axes[2].plot(t, model.solar, 'orange', linewidth=2)
    axes[2].fill_between(t, model.solar, alpha=0.3, color='orange')
    axes[2].set_ylabel('Solar\nIntensity')
    axes[2].grid(True, alpha=0.3)
    axes[2].set_ylim([-0.2, 1.7])

    # Combined
    axes[3].plot(t, combined, 'k-', linewidth=1)
    axes[3].fill_between(t, combined, alpha=0.2, color='gray')
    axes[3].set_ylabel('Combined\nRhythm')
    axes[3].set_xlabel('Time (hours)')
    axes[3].grid(True, alpha=0.3)

    # Add day/night shading
    for ax in axes:
        for i in range(2):
            start = i * 24
            ax.axvspan(start + 6, start + 18, alpha=0.05, color='yellow')
            ax.axvspan(start + 18, start + 30, alpha=0.05, color='blue')

    plt.suptitle('Figure 2: Environmental Rhythms and Their Superposition',
                fontsize=14, y=0.995)
    plt.tight_layout()

    return fig


def figure3_arnold_tongues():
    """Figure 3: Arnold tongues showing synchronization regions"""
    model = TTST()

    print("Calculating Arnold tongues (this may take a minute)...")
    sync_map = model.find_arnold_tongues(
        thermal_range=(0.25, 2.0),
        tidal_range=(10, 15),
        resolution=50
    )

    fig, ax = plt.subplots(figsize=(10, 8))

    # Create contour plot
    thermal_periods = np.linspace(0.25, 2.0, 50)
    tidal_periods = np.linspace(10, 15, 50)

    im = ax.contourf(thermal_periods, tidal_periods, sync_map.T,
                     levels=20, cmap='viridis')

    # Add contour lines for major resonances
    contours = ax.contour(thermal_periods, tidal_periods, sync_map.T,
                          levels=[0.3, 0.5, 0.7, 0.9], colors='white',
                          linewidths=1, alpha=0.5)
    ax.clabel(contours, inline=True, fontsize=8)

    # Mark current and early Earth positions
    ax.plot(0.5, 12.4, 'r*', markersize=15, label='Current Earth')
    ax.plot(0.3, 10.5, 'b*', markersize=15, label='Early Earth (4 Ga)')

    ax.set_xlabel('Thermal Period (hours)')
    ax.set_ylabel('Tidal Period (hours)')
    ax.set_title('Figure 3: Arnold Tongues - Synchronization Regions',
                fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)

    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Synchronization Strength')

    return fig


def figure4_evolutionary_timeline():
    """Figure 4: Evolutionary timeline with rhythm persistence"""
    fig, axes = plt.subplots(2, 1, figsize=(12, 8),
                             gridspec_kw={'height_ratios': [1, 2]})

    # Timeline
    ax = axes[0]
    times = np.array([4.0, 3.5, 2.5, 2.0, 0.72, 0.635, 0.541, 0])
    events = ['Life Origin', 'LUCA', 'GOE', 'Eukaryotes',
              'Snowball Start', 'Snowball End', 'Cambrian', 'Present']

    ax.scatter(times, [1]*len(times), s=100, c=range(len(times)),
              cmap='coolwarm', zorder=3)
    ax.plot([4.0, 0], [1, 1], 'k-', linewidth=2, zorder=1)

    for time, event in zip(times, events):
        rotation = 45 if len(event) > 8 else 0
        ax.text(time, 1.05, event, ha='center', va='bottom',
               rotation=rotation, fontsize=9)

    ax.set_xlim([4.2, -0.2])
    ax.set_ylim([0.9, 1.2])
    ax.set_xlabel('Billion Years Ago')
    ax.set_title('Major Events in Earth History', fontweight='bold')
    ax.set_yticks([])
    ax.grid(True, alpha=0.3, axis='x')

    # Rhythm intensities
    ax = axes[1]

    time_array = np.linspace(4.0, 0, 100)

    # Model rhythm intensities through time
    thermal_intensity = 1.0 * np.exp(-time_array / 5)  # Decreasing
    tidal_intensity = 3.0 * np.exp(-time_array / 2)    # Decreasing faster
    solar_intensity = np.ones_like(time_array)         # Constant

    # Snowball Earth disruption
    snowball_mask = (time_array > 0.635) & (time_array < 0.72)
    solar_intensity[snowball_mask] *= 0.1

    ax.fill_between(time_array, 0, thermal_intensity,
                    color='red', alpha=0.3, label='Thermal')
    ax.fill_between(time_array, 0, tidal_intensity,
                    color='blue', alpha=0.3, label='Tidal')
    ax.fill_between(time_array, 0, solar_intensity,
                    color='orange', alpha=0.3, label='Solar')

    ax.plot(time_array, thermal_intensity, 'r-', linewidth=2)
    ax.plot(time_array, tidal_intensity, 'b-', linewidth=2)
    ax.plot(time_array, solar_intensity, 'orange', linewidth=2)

    # Mark Snowball Earth
    ax.axvspan(0.635, 0.72, alpha=0.2, color='cyan', label='Snowball Earth')

    ax.set_xlim([4.2, -0.2])
    ax.set_ylim([0, 3.5])
    ax.set_xlabel('Billion Years Ago')
    ax.set_ylabel('Relative Rhythm Intensity')
    ax.set_title('Rhythm Persistence Through Earth History', fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)

    plt.suptitle('Figure 4: TTST Evolutionary Timeline', fontsize=14, y=0.98)
    plt.tight_layout()

    return fig


def figure5_snowball_disruption():
    """Figure 5: Rhythm disruption during Snowball Earth"""
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    # Create models
    thermal = ThermalRhythm()
    tidal = TidalRhythm()
    solar = SolarRhythm()

    t = np.linspace(0, 48, 500)

    # Before Snowball
    ax = axes[0]
    ax.bar(['Thermal', 'Tidal', 'Solar'], [1.0, 1.0, 1.0],
          color=['red', 'blue', 'orange'], alpha=0.7)
    ax.set_ylim([0, 1.2])
    ax.set_ylabel('Rhythm Intensity')
    ax.set_title('Before Snowball Earth')
    ax.grid(True, alpha=0.3, axis='y')

    # During Snowball
    ax = axes[1]
    ax.bar(['Thermal', 'Tidal', 'Solar'], [1.0, 0.8, 0.0],
          color=['red', 'blue', 'orange'], alpha=0.7)
    ax.set_ylim([0, 1.2])
    ax.set_title('During Snowball Earth')
    ax.grid(True, alpha=0.3, axis='y')
    # Add ice overlay
    ax.axhspan(0, 1.2, alpha=0.2, color='cyan')
    ax.text(1, 0.6, 'Ice Coverage', ha='center', va='center',
           fontsize=12, fontweight='bold', color='darkblue')

    # After Snowball
    ax = axes[2]
    ax.bar(['Thermal', 'Tidal', 'Solar'], [1.0, 0.9, 1.0],
          color=['red', 'blue', 'orange'], alpha=0.7)
    ax.set_ylim([0, 1.2])
    ax.set_title('After Snowball Earth')
    ax.grid(True, alpha=0.3, axis='y')

    plt.suptitle('Figure 5: Rhythmic Disruption During Snowball Earth Events',
                fontsize=14, y=1.02)
    plt.tight_layout()

    return fig


def main():
    """Generate all figures"""
    print("TTST Figure Generation")
    print("=" * 50)

    fig_dir = create_figure_dir()

    # Generate figures
    figures = [
        ('fig1_conceptual.pdf', figure1_conceptual_overview),
        ('fig2_rhythms.pdf', figure2_environmental_rhythms),
        ('fig3_arnold_tongues.pdf', figure3_arnold_tongues),
        ('fig4_timeline.pdf', figure4_evolutionary_timeline),
        ('fig5_snowball.pdf', figure5_snowball_disruption)
    ]

    for filename, fig_func in figures:
        print(f"Generating {filename}...")
        fig = fig_func()

        # Save figure
        filepath = fig_dir / filename
        fig.savefig(filepath, bbox_inches='tight', dpi=300)
        print(f"  Saved to {filepath}")

        # Also save as PNG for viewing
        png_path = filepath.with_suffix('.png')
        fig.savefig(png_path, bbox_inches='tight', dpi=150)

        plt.close(fig)

    print("\nAll figures generated successfully!")
    print(f"Figures saved in: {fig_dir}")


if __name__ == "__main__":
    main()
