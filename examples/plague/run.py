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
    "SEED5": "84568",
    "SEED6": "99999",
    "SEED7": "58465"
})

# SystemC components
###############################################################################
# RNG components
rng_limit_comp = sst.Component(
    "Random Limit Component (SystemC)", "plague.rng")
rng_limit_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "rng.o"),
    "ipc_port": get_rand_tmp(),
})

rng_pop_inf_comp = sst.Component(
    "Infected Population RNG Component (SystemC)", "plague.rng")
rng_pop_inf_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "rng.o"),
    "ipc_port": get_rand_tmp(),
})

rng_mut_comp = sst.Component(
    "Mutation RNG Component (SystemC)", "plague.rng")
rng_mut_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "rng.o"),
    "ipc_port": get_rand_tmp(),
})

# Random Float components
randf_sev_comp = sst.Component(
    "Severity Component (SystemC)", "plague.randf")
randf_sev_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "randf.o"),
    "ipc_port": get_rand_tmp(),
})

randf_inf_comp = sst.Component(
    "Infectivity Component (SystemC)", "plague.randf")
randf_inf_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "randf.o"),
    "ipc_port": get_rand_tmp(),
})

randf_let_comp = sst.Component(
    "Lethality Component (SystemC)", "plague.randf")
randf_let_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "randf.o"),
    "ipc_port": get_rand_tmp(),
})

randf_br_comp = sst.Component(
    "Birth Rate Component (SystemC)", "plague.randf")
randf_br_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "randf.o"),
    "ipc_port": get_rand_tmp(),
})

randf_rsrch_comp = sst.Component(
    "Research Component (SystemC)", "plague.randf")
randf_rsrch_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "randf.o"),
    "ipc_port": get_rand_tmp(),
})

# Ceiling components
ceil_cure_thresh_comp = sst.Component(
    "Ceiling Component for Cure Threshold (SystemC)", "plague.sc_ceil")
ceil_cure_thresh_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "sc_ceil.o"),
    "ipc_port": get_rand_tmp(),
})

ceil_pop_inf_comp = sst.Component(
    "Ceiling Component for Infected Population (SystemC)", "plague.sc_ceil")
ceil_pop_inf_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "sc_ceil.o"),
    "ipc_port": get_rand_tmp(),
})

ceil_pop_dead_comp = sst.Component(
    "Ceiling Component for Dead Population (SystemC)", "plague.sc_ceil")
ceil_pop_dead_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "sc_ceil.o"),
    "ipc_port": get_rand_tmp(),
})

# Exponential components
exp_pop_inf_comp = sst.Component(
    "Exponential Infectivity Component (SystemC)", "plague.sc_exp")
exp_pop_inf_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "sc_exp.o"),
    "ipc_port": get_rand_tmp(),
})

# Minimum float components
minf_let_comp = sst.Component(
    "Minimum Float Lethality Component (SystemC)", "plague.minf")
minf_let_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "minf.o"),
    "ipc_port": get_rand_tmp(),
})

minf_inf_comp = sst.Component(
    "Minimum Float Infectivity Component (SystemC)", "plague.minf")
minf_inf_comp.addParams({
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
print(os.path.join(BASE_PATH, "../pyrtl/blackboxes/mutation_driver.py"))
mutation_comp = sst.Component(
    "Gene Mutation Component (PyRTL)", "plague.mutation")
mutation_comp.addParams({
    "clock": CLOCK,
    "proc": os.path.join(BASE_PATH, "../pyrtl/blackboxes/mutation_driver.py"),
    "ipc_port": get_rand_tmp(),
})


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
connect_comps(rng_limit_comp, plague_main, "rng", "rng_limit")
connect_comps(rng_pop_inf_comp, plague_main, "rng", "rng_pop_inf")
connect_comps(rng_mut_comp, plague_main, "rng", "rng_mut")

connect_comps(randf_sev_comp, plague_main, "randf", "randf_sev")
connect_comps(randf_inf_comp, plague_main, "randf", "randf_inf")
connect_comps(randf_let_comp, plague_main, "randf", "randf_let")
connect_comps(randf_br_comp, plague_main, "randf", "randf_br")
connect_comps(randf_rsrch_comp, plague_main, "randf", "randf_rsrch")

connect_comps(minf_let_comp, plague_main, "minf", "min_let")
connect_comps(minf_inf_comp, plague_main, "minf", "min_inf")

connect_comps(ceil_cure_thresh_comp, plague_main, "sc_ceil", "ceil_cure_thresh")
connect_comps(ceil_pop_inf_comp, plague_main, "sc_ceil", "ceil_pop_inf")
connect_comps(ceil_pop_dead_comp, plague_main, "sc_ceil", "ceil_pop_dead")

connect_comps(exp_pop_inf_comp, plague_main, "sc_exp", "exp_pop_inf")

connect_comps(ram_comp, plague_main, "ram", "ram")

connect_comps(mutation_comp, plague_main, "mutation", "mutation")

sst.setProgramOption("stopAtCycle", "50000s")
