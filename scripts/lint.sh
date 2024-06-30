set -euox pipefail


ruff check --config pyproject.toml --fix || true

python -m mypy --config-file pyproject.toml octoprobe || true

python -m pylint octoprobe || true
