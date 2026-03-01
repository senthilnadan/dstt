import library
from dstt_library import named_dstt

class PythonTool:
    def __init__(self, func):
        self.func = func

    def execute(self, *inputs):
        return self.func(*inputs)

class DsttTool:
    def __init__(self, dstt_structure):
        self.dstt_structure = dstt_structure

    def _extract_dstt_signature(self) -> list:
        produced = set()
        signature = []
        segments = self.dstt_structure.get("segments", [])
        for segment in segments:
            for transition in segment.get("transitions", []):
                for inp in transition.get("inputs", []):
                    if inp not in produced and inp not in signature:
                        signature.append(inp)
                for out in transition.get("outputs", []):
                    produced.add(out)
        return signature

    def execute(self, *inputs):
        # Local import to prevent circular dependency
        from dsttkernal import DsttKernal
        kernal = DsttKernal()
        
        sig = self._extract_dstt_signature()
        initial_state = dict(zip(sig, inputs))
        dstt_result_dict = kernal.execute(self.dstt_structure, ToolProvider, initial_state=initial_state)
        
        if len(dstt_result_dict) == 1:
            return list(dstt_result_dict.values())[0]
        else:
            return tuple(dstt_result_dict.values())

class ToolProvider:
    @staticmethod
    def get(name):
        if hasattr(library, name):
            return PythonTool(getattr(library, name))
        elif name in named_dstt:
            return DsttTool(named_dstt[name])
        else:
            raise ValueError(f"Tool not found: {name}")
