# abakit: Active Brain Atlas Toolkit

## Installation

- `git clone` this repo.
- `pip install -e .` in this directory to install in develop mode.

## Usage

```python
import abakit
```

## Development Workflow

The whole development workflow is automated by the following make commands. [Conda](https://docs.conda.io) (Miniconda is enough) is the only prerequisite for development. Other required tools could be installed in a local conda environment.

- Environment management:
    - `make init` to create the local conda environment.
    - `make up` to update the local conda environment.
    - `conda activate ./dev/env` to activate the local conda environment.
- Code development:
    - `make fmt` to format source code automatically and consistently.
    - `make lint` until all pass.
    - `make test` until all pass.
- Documatation editing:
    - `make doc` to build the doc.
    - `make doc-preview` to preview the doc.
- Misc:
    - `make clean` to remove intermediate files.
