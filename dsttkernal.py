import library
from dstt_library import named_dstt
class DsttKernal:
    def execute(self, dstt_structure: dict, initial_state: dict = None) -> dict:
        state = initial_state.copy() if initial_state else {}
        
        segments = dstt_structure.get("segments", [])
        for segment in segments:
            for transition in segment.get("transitions", []):
                inputs = self._validate_inputs(transition, state)
                result = self._call_tool(transition, inputs)
                state.update(result)
                
            state = self._compress_to_milestone(state, segment.get("milestone", []))
            
        return state

    def _validate_inputs(self, transition: dict, state: dict) -> list:
        # Treat all inputs as variable names to look up in the state.
        raw_inputs = transition.get("inputs", [])
        resolved_inputs = []
        
        for input_val in raw_inputs:
            # We assume input_val is a string representing a variable name
            if input_val not in state:
                raise ValueError(f"Missing Input: {input_val}")
            resolved_inputs.append(state[input_val])
                
        return resolved_inputs

    def _map_outputs_to_result(self, outputs_keys, tool_result, result_dict):
        if len(outputs_keys) == 1:
            result_dict[outputs_keys[0]] = tool_result
        elif isinstance(tool_result, (list, tuple)) and len(outputs_keys) == len(tool_result):
            for key, value in zip(outputs_keys, tool_result):
                result_dict[key] = value

    def _execute_tool(self, tool_name, inputs, outputs_keys, result_dict):
        if hasattr(library, tool_name):
            tool_func = getattr(library, tool_name)
            tool_result = tool_func(*inputs)
            self._map_outputs_to_result(outputs_keys, tool_result, result_dict)
        else:
            if tool_name in named_dstt:
                tool_func = named_dstt[tool_name]
                kernal = DsttKernal()
                tool_result = kernal.execute(tool_func, inputs)
                self._map_outputs_to_result(outputs_keys, tool_result, result_dict)
            else:
                raise ValueError(f"Tool not found: {tool_name}")
        return tool_result

    def _call_tool(self, transition: dict, inputs: list) -> dict:
        tool_name = transition.get("tool")
        outputs_keys = transition.get("outputs", [])
        result_dict = {}
        
        value = self._execute_tool(tool_name, inputs, outputs_keys, result_dict)
                    
        return result_dict

    def _compress_to_milestone(self, state: dict, milestone: list) -> dict:
        # Retain only the keys present in the milestone list.
        return {key: state[key] for key in milestone if key in state}
