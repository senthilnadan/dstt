import pytest
from dsttkernal import DsttKernal

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
    result = kernal.execute(square_dstt, initial_state={"x": 5})
    
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
    result = kernal.execute(fourthpower_dstt, initial_state={"x": 5})
    
    assert result == {"fourthpower": 625}