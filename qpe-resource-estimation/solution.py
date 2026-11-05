"""The Salary Cap: largest QPE that fits a wall-clock budget.

Symbolic resource estimation with PennyLane's estimator: T-count of QPE on a
generic 2-qubit unitary, runtime = T-count x T-gate time.
"""
import pennylane as qp
import pennylane.numpy as np

qre = qp.estimator

GATE_SET = {"Hadamard", "S", "CNOT", "T"}
ROTATION_PRECISION = 1e-6


def affordable_precision(t_gate_seconds, budget_seconds, max_estimation_wires=40):
    best = None
    for m in range(1, max_estimation_wires + 1):
        qpe = qre.QPE(qre.QubitUnitary(num_wires=2),num_estimation_wires=m)
        config = qre.ResourceConfig()
        config.set_single_qubit_rot_precision(ROTATION_PRECISION)

        resources=qre.estimate(qpe,gate_set=GATE_SET,config=config)
        T_count=int(resources.gate_counts.get("T",0))

        runtime=T_count*t_gate_seconds
        if runtime > budget_seconds:
            break
        else:best=(m,2**(-m),T_count)

    return best
