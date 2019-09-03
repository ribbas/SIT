#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import {ipc}
import sys

sys.path.append("{module_dir}")
import {module}

# Connect the PyRTL simulation to SST through {ipc}
# _sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
{driver_bind}
_sock.connect(sys.argv[1])

_sock.{send}(str(os.getpid()).encode())

while True:
    signal = str(_sock.recv({sig_len}).decode("utf-8"))
    alive = int(signal[0])
    signal = signal[1:]
    if not alive:
        break
    {module}.sim.step({{
        {inputs}
    }})
    _outputs = {outputs}
    _sock.{send}(_outputs)