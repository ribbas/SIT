#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import SystemRandom
from string import ascii_uppercase, digits
import os

import sst

BASE_PATH = os.getcwd()

CLOCK = "1Hz"

LINK_DELAY = "1ps"

def get_rand_tmp():
    return "/tmp/" + ''.join(
        SystemRandom().choice(ascii_uppercase + digits) for _ in range(8)
    )

# Main SST component
###############################################################################
plague_main = sst.Component(
    "Strain Statistics", "plague.plague")
plague_main.addParams({
    "CLOCK": CLOCK,
    "SEED0": "11725",
    "SEED1": "55465",
    "SEED2": "84568",
    "SEED3": "99999",
    "SEED4": "58465",
    "SEED5": "55465",
    "SEED6": "84568",
    "SEED7": "99999",
    "SEED8": "58465"
})

# SystemC components
###############################################################################
# RNG components
limit_comp = sst.Component(
    "Limit Component (SystemC)", "plague.rng")
limit_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "rng.o"),
    "ipc_port": get_rand_tmp(),
})

pborn_today_comp = sst.Component(
    "Population Born Today Component (SystemC)", "plague.rng")
pborn_today_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "rng.o"),
    "ipc_port": get_rand_tmp(),
})

pinf_today_comp = sst.Component(
    "Population Infected Today Component (SystemC)", "plague.rng")
pinf_today_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "rng.o"),
    "ipc_port": get_rand_tmp(),
})

# Random Float components
severity_comp = sst.Component(
    "Severity Component (SystemC)", "plague.randf")
severity_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "randf.o"),
    "ipc_port": get_rand_tmp(),
})

infectivity_comp = sst.Component(
    "Infectivity Component (SystemC)", "plague.randf")
infectivity_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "randf.o"),
    "ipc_port": get_rand_tmp(),
})

lethality_comp = sst.Component(
    "Lethality Component (SystemC)", "plague.randf")
lethality_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "randf.o"),
    "ipc_port": get_rand_tmp(),
})

birth_rate_comp = sst.Component(
    "Birth Rate Component (SystemC)", "plague.randf")
birth_rate_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "randf.o"),
    "ipc_port": get_rand_tmp(),
})

# Ceiling components
pthresh_sc_ceil_comp = sst.Component(
    "Ceiling Component (SystemC)", "plague.sc_ceil")
pthresh_sc_ceil_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "sc_ceil.o"),
    "ipc_port": get_rand_tmp(),
})

# Minimum float components
minf_lethality_comp = sst.Component(
    "Minimum Float Lethality Component (SystemC)", "plague.minf")
minf_lethality_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "minf.o"),
    "ipc_port": get_rand_tmp(),
})

minf_infectivity_comp = sst.Component(
    "Minimum Float Infectivity Component (SystemC)", "plague.minf")
minf_infectivity_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "minf.o"),
    "ipc_port": get_rand_tmp(),
})

# Chisel components
###############################################################################
ram_comp = sst.Component(
    "Memory Component (Chisel)", "plague.ram")
ram_comp.addParams({
    "clock": CLOCK,
    "proc": "test:runMain ram.ramMain",
    "ipc_port": get_rand_tmp(),
})

# PyRTL
###############################################################################
# pyrtl_main = sst.Component(
#     "Traffic Light (PyRTL)", "plague.traffic_light_pyrtl")
# pyrtl_main.addParams({
#     "CLOCK": CLOCK,
# })
# pyrtl_comp = sst.Component(
#     "PyRTL Component", "plague.pyrtl_fsm")
# pyrtl_comp.addParams({
#     "clock": CLOCK,
#     "proc": os.path.join(BASE_PATH, "../pyrtl/blackboxes/pyrtl_fsm_driver.py"),
#     "ipc_port": get_rand_tmp(),
# })

def connect_comps(comp, main_comp, comp_name, main_comp_name):
    sst.Link(main_comp_name + "_din").connect(
        (comp, comp_name + "_din", LINK_DELAY),
        (main_comp, main_comp_name + "_din", LINK_DELAY)
    )
    sst.Link(main_comp_name + "_dout").connect(
        (comp, comp_name + "_dout", LINK_DELAY),
        (main_comp, main_comp_name + "_dout", LINK_DELAY)
    )

# connect the subcomponents
connect_comps(limit_comp, plague_main, "rng", "limit")
connect_comps(pborn_today_comp, plague_main, "rng", "pborn_today")
connect_comps(pinf_today_comp, plague_main, "rng", "pinf_today")

connect_comps(severity_comp, plague_main, "randf", "severity")
connect_comps(infectivity_comp, plague_main, "randf", "infectivity")
connect_comps(lethality_comp, plague_main, "randf", "lethality")
connect_comps(birth_rate_comp, plague_main, "randf", "birth_rate")

connect_comps(minf_lethality_comp, plague_main, "minf", "minf_lethality")
connect_comps(minf_infectivity_comp, plague_main, "minf", "minf_infectivity")

connect_comps(pthresh_sc_ceil_comp, plague_main, "sc_ceil", "pthresh_sc_ceil")

connect_comps(ram_comp, plague_main, "ram", "ram")

sst.setProgramOption("stopAtCycle", "20s")