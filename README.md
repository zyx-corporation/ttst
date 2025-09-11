# TTST - Tidal-Thermal Synchronization Theory

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo/10.5281/zenodo.17096536.svg)](https://doi.org/10.5281/zenodo.17096536)

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![CLA: Required](https://img.shields.io/badge/CLA-Required-brightgreen.svg)](./CONTRIBUTING.md)
[![Ethical Standard](https://img.shields.io/badge/Ethical%20Standard-In%20Place-lightgrey.svg)](./ETHICS.md)


## Environmental Rhythms as Drivers of Early Life Evolution

This repository contains the mathematical models, simulations, and analysis code for the **Tidal-Thermal Synchronization Theory (TTST)**, which proposes that life's fundamental organization emerged through the synchronization of environmental rhythms.

## 📄 Preprint

**Kano, T. (2025).** Tidal-Thermal Synchronization Theory: Environmental Rhythms as Drivers of Early Life Evolution.
[doi:10.5281/zenodo.17096536](https://zenodo.org/badge/DOI/10.5281/zenodo/10.5281/zenodo.17096536.svg)

## 🌟 Key Concepts

TTST proposes that early life evolved under three hierarchical environmental rhythms:

1. **🌡️ Thermal Rhythm** (minutes-hours): High-frequency pulsations from hydrothermal vents
2. **🌊 Tidal Rhythm** (12.4 hours): Periodic forces from the early Moon
3. **☀️ Solar Rhythm** (24 hours): Day-night cycle from Earth's rotation

The theory suggests these rhythms were internalized into biological systems, forming the basis for:
- Circulatory systems
- Neural oscillations
- Cellular timing mechanisms


## 📜 License

This project adopts a **dual license** model:

1.  **AGPLv3 (Community License)**: This license promotes open development by the community. If you use this software as a network service, you are required to publish any modified source code under the terms of the AGPL. See the [LICENSE](./LICENSE) file for details.

2.  **Commercial License**: For companies wishing to avoid the AGPL disclosure requirement and incorporate this technology into proprietary commercial products. For commercial license inquiries, please contact ZYX Corp. ([contact@zyxcorp.jp](mailto:contact@zyxcorp.jp)).


## ⚖️ Ethical Standard

We strongly hope that this technology will be used for peaceful and humanitarian purposes. All contributors and users are expected to respect our [**Ethical Standard (ETHICS.md)**](./ETHICS.md).


## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/zyx-corporation/ttst.git
cd ttst

# Install dependencies
pip install -r requirements.txt

# Run the main simulation
python src/ttst_simulation.py

# Generate figures
python src/generate_figures.py
```

## 📂 Repository Structure

```
ttst/
├── README.md                 # This file
├── LICENSE                   # MIT License
├── requirements.txt          # Python dependencies
├── data/                     # Data files
│   ├── early_earth_params.csv
│   └── rhythm_frequencies.json
├── src/                      # Source code
│   ├── ttst_simulation.py   # Main TTST simulation
│   ├── coupled_oscillators.py
│   ├── thermal_rhythm.py
│   ├── tidal_rhythm.py
│   ├── solar_rhythm.py
│   └── generate_figures.py
├── notebooks/                # Jupyter notebooks
│   ├── 01_basic_theory.ipynb
│   ├── 02_mathematical_models.ipynb
│   ├── 03_snowball_earth.ipynb
│   └── 04_92_structure.ipynb
├── figures/                  # Generated figures
│   ├── fig1_conceptual.pdf
│   ├── fig2_rhythms.pdf
│   └── fig3_evolution.pdf
├── docs/                     # Documentation
│   ├── theory_summary.md
│   ├── mathematical_details.md
│   └── future_predictions.md
└── tests/                    # Unit tests
    └── test_oscillators.py
```

## 💻 Core Simulations

### Basic TTST Model

```python
import numpy as np
from src.ttst_simulation import TTST

# Initialize the model
model = TTST(
    thermal_period=0.5,  # hours
    tidal_period=12.4,   # hours
    solar_period=24.0    # hours
)

# Run simulation
time, combined_rhythm = model.simulate(duration=100)  # 100 hours

# Analyze synchronization
sync_index = model.calculate_synchronization()
print(f"Synchronization Index: {sync_index:.3f}")
```

### 9+2 Structure Analysis (Coming Soon)

```python
from src.structure_evolution import CiliaryStructure

# Simulate evolution of ciliary structures
structures = CiliaryStructure.evolve_possibilities()
optimal = structures.find_optimal(constraints=['physical', 'environmental', 'biochemical'])
print(f"Optimal structure: {optimal}")  # Expected: 9+2
```

## 📊 Key Results

1. **Environmental rhythms create Arnold tongues** - regions of enhanced synchronization
2. **9+2 structure emerges as inevitable** - convergence of multiple constraints
3. **Snowball Earth events** - selective disruption drives evolution
4. **Modern implications** - circadian disruption as rhythm dissonance

## 🔬 Reproducibility

All figures and analyses in the paper can be reproduced using:

```bash
# Reproduce all paper figures
python reproduce_paper.py

# Run all tests
pytest tests/
```

## 📚 Related Publications

### Published

- Kano, T. (2025). Tidal-Thermal Synchronization Theory. *bioRxiv*.

### In Preparation

- Kano, T. (2025). The Emergent Inevitability of 9+2 Architecture. *(in preparation)*

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

**Tomoyuki Kano**

- Email: <tomyuk@zyxcorp.jp>
- GitHub: [tomyuk](https://github.com/tomyuk)
- Twitter: [@tomyuk](https://twitter.com/tomyuk)
- note: [tomyukz](https://note.com/tomyukz)

ORCID: [0009-0004-8213-4631](https://orcid.org/0009-0004-8213-4631)

## 🙏 Acknowledgments

- Inspired by 4 billion years of evolution
- Thanks to the rhythms of Earth, Moon, and Sun
- Special thanks to the open science community

## 📖 Citation

If you use this code or theory in your research, please cite:

```bibtex
@article{kano2025ttst,
  title={Tidal-Thermal Synchronization Theory: Environmental Rhythms as Drivers of Early Life Evolution},
  author={Kano, Tomoyuki},
  journal={bioRxiv},
  year={2025},
  doi={10.1101/2025.01.20.XXXXXX}
}
```

## 🌍 Media Coverage

- [Coming soon]

## 📈 Statistics

![GitHub stars](https://img.shields.io/github/stars/zyx-corporation/ttst?style=social)
![GitHub forks](https://img.shields.io/github/forks/zyx-corporation/ttst?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/zyx-corporation/ttst?style=social)

---

**"We are living repositories of cosmic time"** - TTST Theory
