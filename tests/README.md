# Tests

## Executing a single test

Create a virtual environment

```
conda create -n test_env -python=3.7
conda activate test_env
```

Install the required dependencies

```
pip install -r requirements.txt
pip install pytest
pip install pytest-mock
```

Execute a single test

```
pytest tests/unit/package/module.py::test_function
```
