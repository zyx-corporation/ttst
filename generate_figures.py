#!/usr/bin/env python3

# from typing import Any, Tuple, List
from typing import Tuple, List
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
# from matplotlib.figure import Figure
# from matplotlib.axes import Axes
import warnings
warnings.filterwarnings("ignore")

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 300


print("Generating Figure 1: Conceptual overview...")
fig = plt.figure(figsize=(10, 8))  # type: ignore
ax = fig.add_subplot(111)  # type: ignore
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Title
ax.text(5, 9.5,  # type: ignore
        'Tidal-Thermal Synchronization Theory',
        fontsize=16, fontweight='bold', ha='center')

# Three circles
solar_circle = patches.Circle(
    (5, 5), 3.5, fill=False,
    edgecolor='orange', linewidth=3)
ax.add_patch(solar_circle)
ax.text(5, 8.8, 'Solar Rhythm (24h)', fontsize=11, ha='center',  # type: ignore
        color='orange')

tidal_circle = patches.Circle(
    (5, 5), 2.5, fill=False,
    edgecolor='blue', linewidth=3)
ax.add_patch(tidal_circle)
ax.text(x=7.2, y=6, s='Tidal Rhythm (12.4h)',  # type: ignore
        fontsize=11, ha='center',
        color='blue')

thermal_circle = patches.Circle(
    (5, 5), 1.5, fill=False,
    edgecolor='red', linewidth=3)
ax.add_patch(thermal_circle)
ax.text(5, 5, 'Thermal Rhythm',  # type: ignore
        fontsize=11, ha='center', color='red')

plt.tight_layout()
plt.savefig('figure1_conceptual.pdf',  # type: ignore
            dpi=300, bbox_inches='tight')
plt.close()


print("Generating Figure 2: Mathematical rhythms...")
fig, axes = plt.subplots(4, 1, figsize=(10, 10))  # type: ignore
t = np.linspace(0, 48, 4800)

# Thermal
thermal = 0.5 * np.sin(2 * np.pi * t / 0.5) + 0.05 * np.random.randn(len(t))
axes[0].plot(t, thermal, 'r-', alpha=0.7, linewidth=0.5)
axes[0].set_ylabel('Thermal')
axes[0].set_title('Environmental Rhythms', fontsize=14, fontweight='bold')

# Tidal
tidal = 1.0 * np.sin(2 * np.pi * t / 12.4)
axes[1].plot(t, tidal, 'b-', alpha=0.7)
axes[1].set_ylabel('Tidal')

# Solar
solar = 1.5 * (0.5 + 0.5 * np.tanh(5 * np.sin(2 * np.pi * t / 24)))
axes[2].plot(t, solar, color='orange', alpha=0.7)
axes[2].set_ylabel('Solar')

# Combined
combined = thermal + tidal + solar
axes[3].plot(t, combined, 'k-', linewidth=2)
axes[3].set_ylabel('Combined')
axes[3].set_xlabel('Time (hours)')

plt.tight_layout()
plt.savefig('figure2_rhythms.pdf', dpi=300,  # type: ignore
            bbox_inches='tight')
plt.close()


print("Generating Figure 3: Timeline...")
fig, ax = plt.subplots(figsize=(12, 6))    # type: ignore
events: List[Tuple[float, str, str]] = [
    (4.0, "Life Origin", 'red'),
    (2.0, "Eukaryotes", 'blue'),
    (0.75, "Snowball Earth", 'cyan'),
    (0.54, "Cambrian Explosion", 'orange'),
    (0, "Present", 'black')
]

ax.plot([0.0, 4.0], [0.0, 0.0], 'k-', linewidth=3)  # type: ignore
for time, label, color in events:
    ax.plot(time, 0, 'o', markersize=12, color=color)  # type: ignore
    ax.text(time, 0.3, label, ha='center', fontsize=9)  # type: ignore

ax.set_xlim(4.2, -0.2)
ax.set_ylim(-1, 1)
ax.set_xlabel('Billion Years Ago')  # type: ignore
ax.set_title('TTST Evolutionary Timeline')  # type: ignore
plt.tight_layout()
plt.savefig('figure3_timeline.pdf',   # type: ignore
            dpi=300, bbox_inches='tight')
plt.close()


print("Generating Figure 4: Arnold tongues...")
fig, ax = plt.subplots(figsize=(10, 8))  # type: ignore
x_vals = np.linspace(0.1, 2, 100)
y_vals = np.linspace(10, 15, 100)
X, Y = np.meshgrid(x_vals, y_vals)
Z = np.exp(-((Y/X - 24)**2)) + np.exp(-((Y/X - 12)**2)/2)
im = ax.contourf(X, Y, Z, levels=20, cmap='viridis')  # type: ignore
ax.set_xlabel('Thermal Period (hours)')  # type: ignore
ax.set_ylabel('Tidal Period (hours)')  # type: ignore
ax.set_title('Arnold Tongues: Synchronization Regions')  # type: ignore
plt.colorbar(im, ax=ax, label='Sync Strength')  # type: ignore
plt.tight_layout()
plt.savefig('figure4_arnold.pdf', dpi=300, bbox_inches='tight')  # type: ignore
plt.close()


print("Generating Figure 5: Snowball Earth...")
fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)  # type: ignore
periods = ['Before', 'During', 'After']
data = [[1.0, 1.0, 1.0], [1.0, 0.8, 0.0], [1.0, 0.9, 1.0]]

for i, (ax, period) in enumerate(zip(axes, periods)):
    ax.bar(['Thermal', 'Tidal', 'Solar'],
           data[i],
           color=['red', 'blue', 'orange'], alpha=0.7)  # type: ignore
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 1.2)
    ax.set_title(f'{period} Snowball Earth')

fig.suptitle('Rhythmic Disruption',  # type: ignore
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('figure5_snowball.pdf',   # type: ignore
            dpi=300, bbox_inches='tight')
plt.close()

print("All figures generated successfully!")
