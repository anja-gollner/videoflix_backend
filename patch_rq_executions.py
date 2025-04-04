# patch_rq_executions.py
import types
import sys
# Erstelle ein Dummy-Modul für rq.executions
dummy_module = types.ModuleType("rq.executions")


class DummyExecution:
    pass


dummy_module.Execution = DummyExecution
sys.modules["rq.executions"] = dummy_module
