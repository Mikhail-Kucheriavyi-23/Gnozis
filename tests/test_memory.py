from core.memory import KernelMemory, Workspace, MemoryView

def test_workspace_mutation_does_not_change_kernel():
    kernel = KernelMemory((("rule", "k0"),))
    memory = MemoryView(kernel, Workspace())
    updated = memory.mutate_workspace("x", 1)
    assert updated.kernel == kernel
    assert updated.workspace.values == (("x", 1),)

def test_kernel_has_no_workspace_setter():
    kernel = KernelMemory()
    assert not hasattr(kernel, "set")
