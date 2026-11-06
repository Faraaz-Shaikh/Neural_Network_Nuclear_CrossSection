This is a wrapper for Talys 2.2 to be run and compare data with exfor entries for (𝛾 , n) reactions

## Exfor data
Experimental data has been extracted from [exfortables_py](https://github.com/IAEA-NDS/exfortables_py) 

`exfortables_py` is an EXFORTABLES-inspired collection of observable-based
datasets derived from the
[EXFOR library](https://www-nds.iaea.org/exfor/). It turns the entry-oriented
content in [IAEA-NDS/exfor_json](https://github.com/IAEA-NDS/exfor_json) into
files organized by projectile, target nuclide, reaction, and observable.

The pointwise datasets provide analysis-ready `(x, dx, y, dy)` tables.
Observable summaries and resonance-parameter files use additional,
observable-specific columns. Every file retains EXFOR provenance in a
human-readable header.

Additional energies have been extracted from each isotope for Talys

To see more see exfortables/Readme.md

## TALYS Configuration & Directory Structure

* **Input Folder:** `talys/input/`
* **Output Folder:** `talys/output/`

The input and output files are specified here

```python
from pathlib import Path

class Talys():
    def __init__(self):
        # Define TALYS, exfortables paths and working directories
        # self.talys_dir = Path("/run/media/faraaz/Data_faru_lnx/software/talys_tars/talys/bin/talys")
        self.exfortables_dir = Path("/run/media/faraaz/Data_faru_lnx/software/exfortables_py")
        self.working_dir = Path("/run/media/faraaz/Data_faru_lnx/talys")
        # self.input_dir = Path("/run/media/faraaz/Data_faru_lnx/talys/input")
        # self.output_dir = Path("/run/media/faraaz/Data_faru_lnx/talys/output")
```

The directory structure is the same as in [exfortables_py](https://github.com/IAEA-NDS/exfortables_py).
The output files are stored as rpZZZAAA.totld1.csv

```text
talys/
├── input/
│   ├── Zr-90/
│   │   ├── energies
│   │   ├── Zr90ld1.inp
│   │   ├── Zr90ld2.inp
│   │   └── Zr90ld3.inp
│   ├── Zr-91/
│   └── Mo-100/
│
└── output/
    ├── Zr-90/
    │   ├── rp040089.totld1.csv
    │   ├── rp040089.totld2.csv
    │   └── rp040089.totld3.csv
    ├── Zr-91/
    └── Mo-100/
```
      
      
      
      



