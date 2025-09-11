# TTST - 潮汐・熱同期理論

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![CLA: Required](https://img.shields.io/badge/CLA-Required-brightgreen.svg)](./CONTRIBUTING.md)
[![Ethical Standard](https://img.shields.io/badge/Ethical%20Standard-In%20Place-lightgrey.svg)](./ETHICS.md)

## 環境リズムによる初期生命進化の駆動

このリポジトリは、**潮汐・熱同期理論（TTST）**のための数理モデル、シミュレーション、解析コードを含みます。TTSTは、生命の基本的な組織が環境リズムの同期化によって生まれたと提案します。

## 📄 プレプリント

**加納智之 (2025).** 潮汐・熱同期理論: 環境リズムによる初期生命進化の駆動. *bioRxiv*. [doi:10.1101/2025.01.20.XXXXXX](https://www.biorxiv.org/content/10.1101/2025.01.20.XXXXXX)

## 🌟 キーコンセプト

TTSTは、初期生命が3階層の環境リズムの下で進化したと提案します：

1. **🌡️ 熱リズム**（分〜時間）：熱水噴出孔による高頻度パルス
2. **🌊 潮汐リズム**（12.4時間）：初期の月による周期的な力
3. **☀️ 太陽リズム**（24時間）：地球の自転による昼夜サイクル

これらのリズムが生物システムに内在化され、以下の基盤となったと考えられます：
- 循環系
- 神経振動
- 細胞タイミング機構

## 📜 ライセンス

本プロジェクトは**デュアルライセンス**モデルを採用しています。

1. **AGPLv3（コミュニティライセンス）**：オープンな開発を促進するライセンス。ネットワークサービスとして利用する場合、AGPLの条項に基づき、改変したソースコードの公開義務があります。詳細は[LICENSE](./LICENSE)参照。
2. **商用ライセンス**：AGPLの公開義務を避け、クローズドな商用製品に組み込みたい企業向け。商用ライセンスはZYX Corp.（[contact@zyxcorp.jp](mailto:contact@zyxcorp.jp)）までお問い合わせください。

## ⚖️ 倫理規定

本技術が平和的・人道的目的で利用されることを強く望みます。すべてのコントリビューター・ユーザーは[**倫理規範 (ETHICS.md)**](./ETHICS.md)を尊重してください。

## 🚀 クイックスタート

```bash
# リポジトリをクローン
 git clone https://github.com/zyx-corporation/ttst.git
 cd ttst

# 依存関係をインストール
 pip install -r requirements.txt

# メインシミュレーションを実行
 python src/ttst_simulation.py

# 図を生成
 python src/generate_figures.py
```

## 📂 リポジトリ構成

```
ttst/
├── README.md                 # 本ファイル
├── LICENSE                   # MITライセンス
├── requirements.txt          # Python依存関係
├── data/                     # データファイル
│   ├── early_earth_params.csv
│   └── rhythm_frequencies.json
├── src/                      # ソースコード
│   ├── ttst_simulation.py   # メインTTSTシミュレーション
│   ├── coupled_oscillators.py
│   ├── thermal_rhythm.py
│   ├── tidal_rhythm.py
│   ├── solar_rhythm.py
│   └── generate_figures.py
├── notebooks/                # Jupyterノートブック
│   ├── 01_basic_theory.ipynb
│   ├── 02_mathematical_models.ipynb
│   ├── 03_snowball_earth.ipynb
│   └── 04_92_structure.ipynb
├── figures/                  # 生成図
│   ├── fig1_conceptual.pdf
│   ├── fig2_rhythms.pdf
│   └── fig3_evolution.pdf
├── docs/                     # ドキュメント
│   ├── theory_summary.md
│   ├── mathematical_details.md
│   └── future_predictions.md
└── tests/                    # ユニットテスト
    └── test_oscillators.py
```

## 💻 コアシミュレーション

### 基本TTSTモデル

```python
import numpy as np
from src.ttst_simulation import TTST

# モデル初期化
model = TTST(
    thermal_period=0.5,  # 時間
    tidal_period=12.4,   # 時間
    solar_period=24.0    # 時間
)

# シミュレーション実行
time, combined_rhythm = model.simulate(duration=100)  # 100時間

# 同期解析
sync_index = model.calculate_synchronization()
print(f"Synchronization Index: {sync_index:.3f}")
```

### 9+2構造解析（近日公開）

```python
from src.structure_evolution import CiliaryStructure

# 繊毛構造の進化をシミュレート
structures = CiliaryStructure.evolve_possibilities()
optimal = structures.find_optimal(constraints=['physical', 'environmental', 'biochemical'])
print(f"Optimal structure: {optimal}")  # 期待値: 9+2
```

## 📊 主な結果

1. 環境リズムがArnold tongue（同期強化領域）を形成
2. 9+2構造が必然的に出現
3. スノーボールアース事象による選択的進化
4. 現代的意義：概日リズム障害はリズム不協和

## 🔬 再現性

論文中の全図・解析は以下で再現可能です：

```bash
# 論文図をすべて再現
python reproduce_paper.py

# テスト実行
pytest tests/
```

## 📚 関連文献

### 公開済み
- 加納智之 (2025). 潮汐・熱同期理論. *bioRxiv*.

### 準備中
- 加納智之 (2025). 9+2構造の必然性.（準備中）
- 加納智之 (2025). パルス医学：TTSTの治療応用.（準備中）

## 🤝 コントリビューション

貢献歓迎！ガイドラインは[CONTRIBUTING.md](CONTRIBUTING.md)参照。

### 貢献方法
1. リポジトリをフォーク
2. フィーチャーブランチ作成（`git checkout -b feature/AmazingFeature`）
3. 変更をコミット（`git commit -m 'Add AmazingFeature'`）
4. ブランチをプッシュ（`git push origin feature/AmazingFeature`）
5. プルリクエスト作成

## 📧 連絡先

**加納智之**
Email: tomyuk@zyxcorp.jp
ORCID: [0009-0004-8213-4631](https://orcid.org/0009-0004-8213-4631)

## 📄 ライセンス

本プロジェクトはMITライセンスです。詳細は[LICENSE](LICENSE)参照。

## 🙏 謝辞

- 40億年の進化にインスパイア
- 地球・月・太陽のリズムに感謝
- オープンサイエンスコミュニティに特別な感謝

## 📖 引用

本コード・理論を研究で利用する場合は以下を引用してください：

```bibtex
@article{kano2025ttst,
  title={潮汐・熱同期理論: 環境リズムによる初期生命進化の駆動},
  author={加納智之},
  journal={bioRxiv},
  year={2025},
  doi={10.1101/2025.01.20.XXXXXX}
}
```

## 🌍 メディア掲載

- 近日公開

## 📈 統計

![GitHub stars](https://img.shields.io/github/stars/zyx-corporation/ttst?style=social)
![GitHub forks](https://img.shields.io/github/forks/zyx-corporation/ttst?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/zyx-corporation/ttst?style=social)

---

**「私たちは宇宙時間の生きたリポジトリである」** - TTST理論
