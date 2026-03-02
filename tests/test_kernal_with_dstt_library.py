import library
from dstt_library import named_dstt
import inspect
import pytest
from dsttkernal import DsttKernal
from tool_provider import ToolProvider

def test_execute_singe_as_named_segment():
    square_dstt = {
        "segments": [
            {
                "transitions": [
                    {
                        "id": "t1",
                        "tool": "multiply",
                        "inputs": ["x", "x"],
                        "outputs": ["product"]
                    }
                ],
                "milestone": ["product"]
            }
        ]
    }
    
    kernal = DsttKernal()
    python_lib = {name: getattr(library, name) for name in dir(library) if inspect.isfunction(getattr(library, name))}
    tool_provider_instance = ToolProvider(python_lib, named_dstt)
    result = kernal.execute(square_dstt, tool_provider_instance, initial_state={"x": 5})
    
    assert result == {"product": 25}


def test_execute_multiple_segments_as_named_segment():
    fourthpower_dstt = {
        "segments": [
            {
                "transitions": [
                    {
                        "id": "t1",
                        "tool": "square_dstt",
                        "inputs": ["x"],
                        "outputs": ["product"]
                    },
                    {
                        "id": "t2",
                        "tool": "square_dstt",
                        "inputs": ["product" ],
                        "outputs": ["fourthpower"]
                    }
                ],
                "milestone": ["fourthpower"]
            }
        ]
    }
    
    kernal = DsttKernal()
    python_lib = {name: getattr(library, name) for name in dir(library) if inspect.isfunction(getattr(library, name))}
    tool_provider_instance = ToolProvider(python_lib, named_dstt)
    result = kernal.execute(fourthpower_dstt, tool_provider_instance, initial_state={"x": 5})
    
    assert result == {"fourthpower": 625}