import pytest
from dsttkernal import DsttKernal

def test_execute_multiple_segments():
    test_dstt_content = {
        "segments": [
            {
                "transitions": [
                    {
                        "id": "t1",
                        "tool": "get_user",
                        "inputs": [],
                        "outputs": ["user"]
                    }
                ],
                "milestone": ["user"]
            },
            {
                "transitions": [
                    {
                        "id": "t2",
                        "tool": "get_username",
                        "inputs": ["user"],
                        "outputs": ["username"]
                    }
                ],
                "milestone": ["username"]
            }
        ]
    }
    
    kernal = DsttKernal()
    
    # Execute the structure directly via a dictionary instead of a file
    result = kernal.execute(test_dstt_content)
    
    # We expect 'result' to return the state accumulated and compressed by the final segment's milestone
    assert result == {"username": "alice123"}



def test_execute_multiple_segments_miltiple_artifact():
    test_dstt_content = {
    "segments": [
        {
            "transitions": [
                {"id": "t1", "tool": "echo", "inputs": ["a"], "outputs": ["a"]},
                {"id": "t2", "tool": "echo", "inputs": ["b"], "outputs": ["b"]}
            ],
            "milestone": ["a", "b"]
        },
        {
            "transitions": [
                {"id": "t3", "tool": "combine", "inputs": ["a", "b"], "outputs": ["c"]}
            ],
            "milestone": ["c"]
        }
    ]
}
    kernal = DsttKernal()
    
    # Execute the structure directly via a dictionary instead of a file
    result = kernal.execute(test_dstt_content, initial_state={"a": "Hello", "b": "World"})
    
    # We expect 'result' to return the state accumulated and compressed by the final segment's milestone
    assert result == {"c": "HelloWorld"}



def test_execute_multiple_segments_miltiple_artifact():
    test_dstt_content = {
    "segments": [
        {
            "transitions": [
                {"id": "t1", "tool": "echo", "inputs": ["a"], "outputs": ["a"]},
                {"id": "t2", "tool": "echo", "inputs": ["b"], "outputs": ["b"]},
                {"id": "t2", "tool": "echo", "inputs": ["b"], "outputs": ["d"]}
            ],
            "milestone": ["a", "b"]
        },
        {
            "transitions": [
                {"id": "t3", "tool": "combine", "inputs": ["a", "b"], "outputs": ["c"]},
                {"id": "t3", "tool": "combine", "inputs": ["a", "d"], "outputs": ["c"]}
            ],
            "milestone": ["c"]
        }
    ]
}
    kernal = DsttKernal()
    
    with pytest.raises(ValueError) as exc_info:
        result = kernal.execute(test_dstt_content, initial_state={"a": "Hello", "b": "World"})
        
    assert str(exc_info.value) == "Missing Input: d"

    # Execute the structure directly via a dictionary instead of a file
    


def test_execute_multiple_segments_miltiple_overwrite():
    test_dstt_content = {
    "segments": [
        {
            "transitions": [
                {"id": "t1", "tool": "echo", "inputs": ["a"], "outputs": ["a"]},
                {"id": "t2", "tool": "echo", "inputs": ["b"], "outputs": ["b"]},
                {"id": "t3", "tool": "combine", "inputs": ["a", "b"], "outputs": ["c"]}
            ],
            "milestone": ["a", "b", "c"]
        },
        {
            "transitions": [
                {"id": "t3", "tool": "combine", "inputs": ["b", "a"], "outputs": ["c"]}
            ],
            "milestone": ["c"]
        }
    ]
}
    kernal = DsttKernal()
    
    # Execute the structure directly via a dictionary instead of a file
    result = kernal.execute(test_dstt_content, initial_state={"a": "Hello", "b": "World"})
    
    # We expect 'result' to return the state accumulated and compressed by the final segment's milestone
    assert result == {"c": "WorldHello"}


def test_execute_multiple_segments_identity():
    test_dstt_content = {
    "segments": [
        {
            "transitions": [
                {"id": "t1", "tool": "echo", "inputs": ["a"], "outputs": ["a"]},
                {"id": "t2", "tool": "echo", "inputs": ["b"], "outputs": ["b"]},
                {"id": "t3", "tool": "combine", "inputs": ["a", "b"], "outputs": ["c"]}
            ],
            "milestone": ["a", "b", "c"]
        },
        {
            "transitions": [                
            ],
            "milestone": ["c"]
        }
    ]
}
    kernal = DsttKernal()
    
    # Execute the structure directly via a dictionary instead of a file
    result = kernal.execute(test_dstt_content, initial_state={"a": "Hello", "b": "World"})
    
    # We expect 'result' to return the state accumulated and compressed by the final segment's milestone
    assert result == {"c": "HelloWorld"}