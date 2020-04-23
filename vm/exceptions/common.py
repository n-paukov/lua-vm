class OPCodeValidationError(RuntimeError):
    pass


class VirtualMachineRuntimeError(RuntimeError):
    pass


class VirtualMachineInvalidInstructionError(VirtualMachineRuntimeError):
    pass


class VirtualMachineInvalidOperationError(VirtualMachineRuntimeError):
    pass


class VirtualMachineScopeOrderError(VirtualMachineRuntimeError):
    pass
