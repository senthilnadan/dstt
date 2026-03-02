

class PythonTool:
    def __init__(self, func):
        self.func = func

    def execute(self, *inputs):
        return self.func(*inputs)

class DsttTool:
    def __init__(self, dstt_structure, tool_provider):
        self.dstt_structure = dstt_structure
        self.tool_provider = tool_provider

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
        dstt_result_dict = kernal.execute(self.dstt_structure, self.tool_provider, initial_state=initial_state)
        
        if len(dstt_result_dict) == 1:
            return list(dstt_result_dict.values())[0]
        else:
            return tuple(dstt_result_dict.values())

class ToolProvider:
    def __init__(self, python_lib: dict, dstt_lib: dict):
        self.python_lib = python_lib
        self.dstt_lib = dstt_lib

    def get(self, name):
        if name in self.python_lib:
            return PythonTool(self.python_lib[name])
        elif name in self.dstt_lib:
            return DsttTool(self.dstt_lib[name], self)
        else:
            raise ValueError(f"Tool not found: {name}")
