# DSTT Kernel

Deterministic State Transition Tree (DSTT) Kernel

A minimal forward-only execution engine for structured task graphs.

---

## What It Is

DSTT Kernel executes a structured computation described as:

- Segments
- Transitions
- Milestones

It guarantees:

- Forward-only execution
- Immutable milestone boundaries
- No rollback within an execution instance
- Explicit state passing
- Deterministic transition evaluation (assuming deterministic tools)

DSTT Kernel does not perform planning, optimization, healing, or session management.

It only executes.

---

## Core Philosophy

1. Execution is forward-only.
2. A segment closes only when its milestone is satisfied.
3. Only milestone artifacts survive segment boundaries.
4. No mutation of prior segments is allowed.
5. If recovery is needed, spawn a new execution instance from a milestone.

No hidden state.  
No implicit memory.  
No rollback.

---

## DSTT Structure

A DSTT is a dictionary of the form:

```json
{
  "segments": [
    {
      "transitions": [
        {
          "id": "t1",
          "tool": "add",
          "inputs": ["a", "b"],
          "outputs": ["sum_ab"]
        }
      ],
      "milestone": ["sum_ab"]
    }
  ]
}
```

### Definitions

**Segment**  
A boundary of execution. Transitions inside a segment execute sequentially.

**Transition**  
A tool invocation.

**Milestone**  
The set of artifact names that must exist in state at segment completion.  
Only milestone artifacts are carried forward.

---

## Execution Model

```python
from dstt_kernel.kernel import DsttKernal

kernel = DsttKernal()

result = kernel.execute(
    dstt_structure,
    tool_provider,
    initial_state={"a": 2, "b": 3}
)
```

Execution:

- Starts from segment 0 unless otherwise specified.
- Runs transitions in order.
- Validates milestone at end of segment.
- Compresses state to milestone artifacts.
- Proceeds to next segment.
- Returns final milestone state.

---

## Tool Model

Tools are provided externally via a ToolProvider.

Each tool must implement:

```python
execute(*inputs) -> value or tuple
```

DSTT Kernel does not:

- Manage tool lifecycle
- Manage tool sessions
- Handle retries
- Perform validation of tool logic

ToolProvider is responsible for supplying tools.

---

## External Dependency Signature

DSTTTool may extract required external inputs by:

- Collecting transition inputs
- Subtracting internally produced artifacts

This defines the boundary contract of the DSTT.

The kernel itself does not depend on this helper.

---

## Resuming Execution

DSTT supports spawning a new execution instance from a prior milestone.

Rules:

- No segment may be reopened within the same execution instance.
- A new instance may start from any valid milestone state.
- History is append-only.
- Fork instead of rewind.

---

## What DSTT Kernel Does Not Do

- Planning
- Graph optimization
- Tool discovery
- Healing
- Session management
- REPL orchestration
- Version compatibility enforcement

These belong to the surrounding ecosystem.

---

## Invariants (Frozen Contract)

1. Forward-only execution per instance.
2. Milestone boundaries are immutable.
3. Only milestone state survives segment closure.
4. Kernel does not mutate past state.
5. Kernel does not maintain hidden memory.

These invariants define DSTT Kernel.

---

## Intended Audience

DSTT Kernel is designed for:

- Engineers who want deterministic execution semantics
- Systems requiring reproducibility
- Tool-based computational pipelines
- Structured agent orchestration layers

It is not a full agent framework.

It is a deterministic execution core.

---

## Versioning Philosophy

If invariants change:

- Release a new version.
- Do not mutate semantics of prior versions.

DSTT favors structural stability over feature growth.

---

## Minimal Example

```python
python_lib = {
    "add": lambda a, b: a + b,
    "multiply": lambda a, b: a * b
}

tool_provider = ToolProvider(python_lib, {})

dstt = {
    "segments": [
        {
            "transitions": [
                {"id": "t1", "tool": "add", "inputs": ["a", "b"], "outputs": ["sum"]}
            ],
            "milestone": ["sum"]
        },
        {
            "transitions": [
                {"id": "t2", "tool": "multiply", "inputs": ["sum", "c"], "outputs": ["result"]}
            ],
            "milestone": ["result"]
        }
    ]
}

kernel = DsttKernal()
result = kernel.execute(dstt, tool_provider, initial_state={"a": 2, "b": 3, "c": 4})

print(result)  # {"result": 20}
```

---

## Final Note

DSTT Kernel is intentionally small.

It is not meant to be extended internally.  
Ecosystem logic must wrap around it.

Keep the core minimal.  
Let complexity live outside.