#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Implementation of the SystemC class

This class generates the boilerplate code required to build the black box
interface in SIT.
"""

import math

from .boilerplate import BoilerPlate


class SystemC(BoilerPlate):

    def __init__(self, ipc, module, lib, module_dir="", lib_dir="", desc="",
                 driver_template_path="", component_template_path=""):
        """Constructor for SystemC BoilerPlate.

        Parameters:
        -----------
        ipc : str (options: "sock", "zmq")
            method of IPC
        module : str
            SST element component and HDL module name
        lib : str
            SST element library name
        module_dir : str (default: "")
            directory of HDL module
        lib_dir : str (default: "")
            directory of SIT library
        desc : str (default: "")
            description of the SST model
        driver_template_path : str (default: "")
            path to the black box-driver boilerplate
        component_template_path : str (default: "")
            path to the black box-model boilerplate
        """
        super().__init__(
            ipc=ipc,
            module=module,
            lib=lib,
            module_dir=module_dir,
            lib_dir=lib_dir,
            desc=desc,
            driver_template_path=driver_template_path,
            component_template_path=component_template_path
        )

        if self.ipc == "sock":

            # driver attributes
            self.sig_type = "SocketSignal"

        elif self.ipc == "zmq":

            # driver attributes
            self.sig_type = "ZMQSignal"

        self.driver_path += "_driver.cpp"
        self.comp_path += "_comp.cpp"

    def __parse_signal_type(self, signal):
        """Parses the type and computes its size from the signal

        Parameters:
        -----------
        signal : str
            signal definition

        Returns:
        --------
        tuple2(str,int)
            C++ datatype and its size
        """
        # NoneTypes are explicitly assigned to SST component clock signals
        if not signal:
            return 0

        elif "sc" in signal:

            def __get_ints(sig):
                return int("".join(s for s in sig if s.isdigit())
                           if self._wdelim not in sig
                           else self._get_signal_width(sig))

            if "bv" in signal or "lv" in signal or "int" in signal:
                return math.floor(math.log2(__get_ints(signal)))

            if "bit" in signal or "logic" in signal:
                return __get_ints(signal)

        else:
            return 1

    def _get_driver_outputs(self):
        """Generates output bindings for both the components in the black box

        Returns:
        --------
        str
            snippet of code representing output bindings
        """
        return self._sig_fmt(
            "_data_out << {sig}",
            lambda x: {
                "sig": x[-1],
            },
            self.outputs,
            ";\n" + " " * 8
        )

    def _get_driver_inputs(self):

        return self._generate_driver_inputs(
            fmt="{sig} = std::stoi(_data_in.substr({sp}, {sl}));",
            start_pos=1,
            signal_type_parser=self.__parse_signal_type,
            clock_fmt="{sig} = std::stoi(_data_in.substr({sp})) % 2;",
        )

    def __get_driver_port_defs(self):
        """Generates port definitions for the black box-driver"""
        return "sc_signal" + ";\n    sc_signal".join(
            " ".join(i) for i in self.ports)

    def __get_driver_bindings(self):
        """Generates port bindings for the black box-driver

        Returns:
        --------
        str
            snippet of code representing port bindings
        """
        return self._sig_fmt(
            "DUT.{sig}({sig})",
            lambda x: {"sig": x[-1]}, self.ports
        )

    def _get_driver_defs(self):
        """Map definitions for the SystemC driver format string

        Returns:
        --------
        dict(str:str)
            format mapping of template SystemC driver string
        """
        return {
            "module_dir": self.module_dir,
            "lib_dir": self.lib_dir,
            "module": self.module,
            "port_defs": self.__get_driver_port_defs(),
            "bindings": self.__get_driver_bindings(),
            "sender": self.sender,
            "receiver": self.receiver,
            "buf_size": self.buf_size,
            "sig_type": self.sig_type,
        }
