from __future__ import annotations

try:
    import numpy as np  # type: ignore
except ImportError:
    raise ImportError("The Numpy Extension must be installed from the 'dist' directory before running this macro!")

from ooodev.loader import Lo


def msg(*args):
    _ = Lo.current_doc.msgbox("Hello World!", "Greetings")


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


g_exportedScripts = (msg, np_ex01, np_ex02)
