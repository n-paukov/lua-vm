class OPCodeValidationError(RuntimeError):
    pass


class VirtualMachineRuntimeError(RuntimeError):
    pass


class VirtualMachineInvalidInstructionError(VirtualMachineRuntimeError):
    pass