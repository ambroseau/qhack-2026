"""Personal Best (Bronze): clean up PennyLane's default unitary decomposition.

Decompose qp.QubitUnitary into the cost-model gate set, then slide RZ gates
through CNOT controls and merge neighbouring rotations.
`TARGET_GATE_SET` comes from the QHack challenge template.
"""
import pennylane as qp
import pennylane.numpy as np


def submission_circ(u_mat):
    n=int(round(np.log2(len(u_mat))))
    def func():
        qp.QubitUnitary(u_mat, wires=range(n))
    tape = qp.tape.make_qscript(func)()
    tapes,_ = qp.decompose(tape,gate_set=TARGET_GATE_SET)
    tape=tapes[0]
    tapes,_=qp.transforms.commute_controlled(tape, direction="right")
    tape=tapes[0]
    tapes,_=qp.transforms.merge_rotations(tape)
    tape=tapes[0]
    for op in tape.operations:
        qp.apply(op)
