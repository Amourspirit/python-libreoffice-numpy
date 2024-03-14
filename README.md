<p align="center">
<img src="https://github.com/Amourspirit/python-libreoffice-numpy/assets/4193389/1619cf7e-3400-4833-836d-b97fdf27da1d" alt="Numpy Extension Logo" width="174" height="174">
</p>

# Python Numpy Extension for LibreOffice

[Numpy](https://numpy.org/) is The fundamental package for scientific computing with Python.

This is a LibreOffice extension that allows you to use Numpy in LibreOffice python macros and scripts.

On LibreOffice Extensions the Numpy extension can be found [here](https://extensions.libreoffice.org/en/extensions/show/41995), locally the NumPy extension can is found in the [dist](./dist) folder.

## Example

The following is an example macro:

```python
# using OooDev to for easy access to LibreOffice
from __future__ import annotations
from ooodev.loader import Lo

try:
    import numpy as np  # type: ignore
except ImportError:
    raise ImportError("The Numpy Extension must be installed before running this macro!")


def np_ex01(*args):
    x = np.arange(15, dtype=np.int64).reshape(3, 5)
    x[1:, ::2] = -99
    _ = Lo.current_doc.msgbox(str(x), "Numpy 01")

    _ = Lo.current_doc.msgbox(str(x.max(axis=1)).center(50), "x.max(axis=1)")

def np_ex02(*args):
    # Generate normally distributed random numbers:
    rng = np.random.default_rng()
    samples = rng.normal(size=2500)
    _ = Lo.current_doc.msgbox(str(samples), "Numpy 02")

g_exportedScripts = (np_ex01, np_ex02)
```

## Dev Container

This project is generated from [Python LibreOffice Pip Extension Template](https://github.com/Amourspirit/python-libreoffice-pip) which in turn was generated from the [Live LibreOffice Python Template] This means this project can be run/developed in a Development container or Codespace with full access to LibreOffice.

### Accessing LibreOffice

The ports to access LibreOffice are `3030` for http and `3031` for https.

See also: [How do I access the LibreOffice in a GitHub Codespace?](https://github.com/Amourspirit/live-libreoffice-python/wiki/FAQ#how-do-i-access-the-libreoffice-in-a-github-codespace) on [Live LibreOffice Python Template].

## Running Macro

The example macro is already installed in LibreOffice when the container is started and be found in the [macro](./macro) folder.
However, the extension must be installed before running the example macro. From LibreOffice open the extension manager, `Tools -> Extension Manager ...` and add `numpy.oxt`

When prompted choose `Only for me`. Restart LibreOffice and numpy will install.

![Add Extension Dialog](https://github.com/Amourspirit/python-libreoffice-numpy-ext/assets/4193389/4e6e9046-b51b-4cd1-8961-c0f6724ffaad)


![For whom do you want to install the extension dialog box](https://github.com/Amourspirit/python-libreoffice-numpy-ext/assets/4193389/ee0369a2-f2f9-45d9-b093-66a138078f2a)

[Live LibreOffice Python Template]:https://github.com/Amourspirit/live-libreoffice-python