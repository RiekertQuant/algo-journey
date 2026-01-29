import sys
import platform
import matplotlib
import pandas
import pytest
import yfinance
import backtesting
import numpy

print("Sys Version: ", sys.version)
print("Python Version: ", platform.python_version)
for name, module in sorted(sys.modules.items()):
    if hasattr(module, '__version__'):
        print(f"{name}: {module.__version__}")