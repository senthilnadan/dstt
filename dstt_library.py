named_dstt =     {
    "square_dstt": {
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
    }, 
    "fourthpower_dstt": {
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
}

def get_named_dstt(name):
    return named_dstt.get(name)