from __future__ import annotations

try:
    from lo_pip_numpy.dialog.message_dialog import MessageDialog
except ImportError:
    raise ImportError("The Numpy Extension must be installed from the 'dist' directory before running this macro!")
import numpy as np


def _show_msg(msg: str, title: str = "Message") -> None:
    doc = XSCRIPTCONTEXT.getDocument()
    top_win = doc.CurrentController.Frame.ContainerWindow

    msg_box = MessageDialog(ctx=XSCRIPTCONTEXT.getComponentContext(), parent=top_win, message=msg, title=title)
    _ = msg_box.execute()


def msg(*args):
    _show_msg("Hello World!", "Greetings")


def np_ex01(*args):
    x = np.arange(15, dtype=np.int64).reshape(3, 5)
    x[1:, ::2] = -99
    _show_msg(str(x), "Numpy 01")

    _show_msg(str(x.max(axis=1)).center(50), "x.max(axis=1)")


def np_ex02(*args):
    # Generate normally distributed random numbers:
    rng = np.random.default_rng()
    samples = rng.normal(size=2500)
    _show_msg(str(samples), "Numpy 02")


g_exportedScripts = (msg, np_ex01, np_ex02)
