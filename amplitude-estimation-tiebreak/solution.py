"""Break the Tie: resolve the a / 1-a ambiguity of amplitude estimation.

Circuit 1: qp.QuantumMonteCarlo gives a two-peak readout -> candidates a, 1-a.
Circuit 2: direct encoding (StatePrep + multi-controlled RY) gives a coarse a,
used only to pick the right candidate. Reports f_max * the estimated candidate.
`run_circuit` and `rotation_angle` come from the QHack challenge template.
"""
import pennylane as qp
import pennylane.numpy as np


def estimate_mean(probabilities, values, n):
    probabilities = np.array(probabilities, dtype=float)
    values = np.array(values, dtype=float)
    m = int(round(np.log2(len(probabilities))))

    # --- Step 1: rescale the quantity into [0, 1] ----------------------------
    f_max = max(values)
    f_tilde = values/max(values)
    # --- Step 2: run the amplitude estimation --------------------------------
    def circuit1():
        qp.QuantumMonteCarlo(probabilities,lambda i: f_tilde[i],range(m + 1),range(m+1,m+1+n))
        return qp.probs(wires=range(m + 1, m + 1 + n))
    # --- Step 3: turn the readout into the two candidates --------------------
    probs1=run_circuit(n+m+1,circuit1)
    k=np.argmax(probs1)
    theta=k/(2**n)
    a1=(1-np.cos(np.pi*theta))/2
    a2=1-a1
    # --- Step 4: build the tie-breaker circuit  --------------------------
    def circuit2():
        qp.StatePrep(np.sqrt(probabilities),wires=range(m))
        for i in range(2**m):
            control_values=[int(b) for b in format(i,f'0{m}b')]
            qp.ctrl(qp.RY(rotation_angle(f_tilde[i]),wires=m),control=range(m),control_values=control_values)
        return qp.probs(wires=m)
    probs2=run_circuit(m+1,circuit2)
    a=probs2[1]
    # --- Step 5: break the tie -----------------------------------------------
    a1_diff = abs(a1-a)
    a2_diff = abs(a2-a)
    if a1_diff<a2_diff:
        a_est=a1
    else:
        a_est=a2
    return float(a_est*f_max)
