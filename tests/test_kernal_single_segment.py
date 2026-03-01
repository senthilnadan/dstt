import json
import pytest
from dsttkernal import DsttKernal

def test_execute_singe_const():
    # Setup our test dstt file with the sample JSON provided
    test_dstt_content = {
        "segments": [
            {
                "transitions": [
                    {
                        "id": "t1",
                        "tool": "const",
                        "inputs": [],
                        "outputs": ["x"]
                    }
                ],
                "milestone": ["x"]
            }
        ]
    }
    
    # Initialize the kernal
    kernal = DsttKernal()
    
    # Execute the structure directly via a dictionary instead of a file
    result = kernal.execute(test_dstt_content)
    # For a 'const' tool with no inputs, let's assume it should output a specific value, e.g., True or a default value.
    # of execution returns the milestone 'x' mapping to some output.
    # Since we haven't defined the const tool's exact behavior yet, let's just assert that
    # the kernal returns a dictionary containing 'x' when tracking the milestone.
    
    # We expect 'result' to return the computed milestone value 'x'.
    # With the real const() tool from our library, this should be 1.
    assert result.get("x") == 1


def test_execute_singe_echo_tool():
    # Setup our test dstt file with the sample JSON provided
    test_dstt_content = {
        "segments": [
            {
                "transitions": [
                    {
                        "id": "t1",
                        "tool": "echo",
                        "inputs": ["msg"],
                        "outputs": ["x"]
                    }
                ],
                "milestone": ["x"]
            }
        ]
    }
    
    # Initialize the kernal
    kernal = DsttKernal()
    
    # Execute the structure directly via a dictionary instead of a file
    result = kernal.execute(test_dstt_content, initial_state={"msg": "Hello"})
    # For a 'const' tool with no inputs, let's assume it should output a specific value, e.g., True or a default value.
    # of execution returns the milestone 'x' mapping to some output.
    # Since we haven't defined the const tool's exact behavior yet, let's just assert that
    # the kernal returns a dictionary containing 'x' when tracking the milestone.
    
    # We expect 'result' to return the computed milestone value 'x'.
    # With the real const() tool from our library, this should be 1.
    assert result.get("x") == "Hello"



def test_execute_two_transitions():
    # Setup our test dstt file with the sample JSON provided
    test_dstt_content = {
            "segments": [
                {
                    "transitions": [
                        {
                            "id": "t1",
                            "tool": "echo",
                        "inputs": ["val1"],
                        "outputs": ["x"]
                        },
                        {
                        "id": "t2",
                        "tool": "echo",
                        "inputs": ["val2"],
                        "outputs": ["y"]
                        }
                    ],
        "milestone": ["y"]
        }
    ]
    }
    
    # Initialize the kernal
    kernal = DsttKernal()
    
    # Execute the structure directly via a dictionary instead of a file
    result = kernal.execute(test_dstt_content, initial_state={"val1": "Hello", "val2": "World"})
    # For a 'const' tool with no inputs, let's assume it should output a specific value, e.g., True or a default value.
    # of execution returns the milestone 'x' mapping to some output.
    # Since we haven't defined the const tool's exact behavior yet, let's just assert that
    # the kernal returns a dictionary containing 'x' when tracking the milestone.
    
    # We expect 'result' to return a dictionary containing only the milestone variables.
    assert result == {"y": "World"}


def test_execute_mutation_test():
    # Setup our test dstt file with the sample JSON provided
    test_dstt_content = {
            "segments": [
                {
                    "transitions": [
                        {
                            "id": "t1",
                            "tool": "echo",
                        "inputs": ["val1"],
                        "outputs": ["x"]
                        },
                        {
                        "id": "t2",
                        "tool": "echo",
                        "inputs": ["val2"],
                        "outputs": ["x"]
                        }
                    ],
        "milestone": ["x"]
        }
    ]
    }
    
    # Initialize the kernal
    kernal = DsttKernal()
    
    # Execute the structure directly via a dictionary instead of a file
    result = kernal.execute(test_dstt_content, initial_state={"val1": {"data": "Hello"}, "val2": "World"})

    assert result == {"x": "World"}

def test_execute_undefined_tool():
    test_dstt_content = {
        "segments": [
            {
                "transitions": [
                    {
                        "id": "t1",
                        "tool": "undefined_tool",
                        "inputs": [],
                        "outputs": ["x"]
                    }
                ],
                "milestone": ["x"]
            }
        ]
    }
    
    kernal = DsttKernal()
    
    # We expect this to raise a ValueError
    with pytest.raises(ValueError) as exc_info:
        kernal.execute(test_dstt_content)
        
    assert str(exc_info.value) == "Tool not found: undefined_tool"

def test_execute_initial_state():
    test_dstt_content = {
        "segments": [
            {
                "transitions": [
                    {
                        "id": "t1",
                        "tool": "echo",
                        "inputs": ["x"],
                        "outputs": ["y"]
                    }
                ],
                "milestone": ["y"]
            }
        ]
    }
    
    kernal = DsttKernal()
    
    # We pass an initial state containing 'x', and expect the tool to echo it into 'y'
    result = kernal.execute(test_dstt_content, initial_state={"x": 5})
    
    assert result == {"y": 5}

def test_execute_missing_variable_fails():
    test_dstt_content = {
        "segments": [
            {
                "transitions": [
                    {
                        "id": "t1",
                        "tool": "echo",
                        "inputs": ["missing_var"],  # This is missing from the state
                        "outputs": ["y"]
                    }
                ],
                "milestone": ["y"]
            }
        ]
    }
    
    kernal = DsttKernal()
    
    with pytest.raises(ValueError) as exc_info:
        kernal.execute(test_dstt_content)
        
    assert str(exc_info.value) == "Missing Input: missing_var"


def test_execute_output_canbe_a_dict_fails():
    test_dstt_content = {
        "segments": [
            {
                "transitions": [
                     {
                        "id": "t1",
                        "tool": "get_user_data",
                        "inputs": [],
                        "outputs": ["user"]
                    }
                ],
                "milestone": ["user"]
            }
        ]
    }
    
    kernal = DsttKernal()
    
    kernal.execute(test_dstt_content)
    assert result == {"user": {"name": "Alice", "age": 30}}

