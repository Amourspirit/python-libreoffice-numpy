<p align="center">
<img src="https://github.com/Amourspirit/python-libreoffice-numpy/assets/4193389/1619cf7e-3400-4833-836d-b97fdf27da1d" alt="OooDev Logo" width="174" height="174">
</p>

# Python Numpy Extension for LibreOffice

[Numpy](https://numpy.org/) is The fundamental package for scientific computing with Python.

This is a LibreOffice extension that allows you to use Numpy in LibreOffice python macros and scripts.

## Example

```python
from lo_pip_numpy.dialog.message_dialog import MessageDialog
import numpy as np


def _show_msg(msg: str, title: str = "Message") -> None:
    doc = XSCRIPTCONTEXT.getDocument()
    top_win = doc.CurrentController.Frame.ContainerWindow

    msg_box = MessageDialog(ctx=XSCRIPTCONTEXT.getComponentContext(), parent=top_win, message=msg, title=title)
    _ = msg_box.execute()


def np_ex01(*args):
    # Create a 2-D array, set every second element in
    # some rows and find max per row:
    x = np.arange(15, dtype=np.int64).reshape(3, 5)
    x[1:, ::2] = -99
    _show_msg(str(x), "Numpy 01")
    # array([[  0,   1,   2,   3,   4],
    #        [-99,   6, -99,   8, -99],
    #        [-99,  11, -99,  13, -99]])

    _show_msg(str(x.max(axis=1)), "x.max(axis=1)")
    # array([ 4,  8, 13])


def np_ex02(*args):
    # Generate normally distributed random numbers:
    rng = np.random.default_rng()
    samples = rng.normal(size=2500)
    _show_msg(str(samples), "Numpy 02")


g_exportedScripts = (np_ex01, np_ex02)
```
