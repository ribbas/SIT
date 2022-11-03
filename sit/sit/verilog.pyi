from typing import Literal

from .sit import SIT

class Verilog(SIT):
    def __init__(
        self,
        ipc: Literal["sock", "zmq"],
        module: str,
        lib: str,
        module_dir: str = ...,
        lib_dir: str = ...,
        desc: str = ...,
        driver_template_path: str = ...,
        component_template_path: str = ...,
    ) -> None: ...
    def _parse_signal_type(self, signal: str) -> int: ...
    def _get_driver_outputs(self) -> str: ...
    def _get_driver_inputs(self) -> str: ...
    def _get_driver_defs(self) -> dict[str, str]: ...
    def _generate_extra_files(self) -> None: ...