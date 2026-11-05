"""Fermionic VQE: ground energy of H = sum_i c_i a_i a_i^dagger.

Build H from FermiWords, map to qubits with Jordan-Wigner (real coefficients),
prepare a trial state with one RY per mode qubit, minimise <H> by gradient descent.
"""
import pennylane as qp
import pennylane.numpy as np

w0=qp.FermiA(0)*qp.FermiC(0)
w1=qp.FermiA(1)*qp.FermiC(1)
w2=qp.FermiA(2)*qp.FermiC(2)


def build_hamiltonian(coeffs):
    H = coeffs[0]*w0+coeffs[1]*w1+coeffs[2]*w2
    H1=qp.jordan_wigner(H)
    number,ops=H1.terms()
    return qp.Hamiltonian(np.real(number),ops)


dev = qp.device("default.qubit", wires=6)

@qp.qnode(dev)
def vqe_circuit(params,coeffs):
    qp.RY(params[0],wires=0)
    qp.RY(params[1],wires=1)
    qp.RY(params[2],wires=2)
    H=build_hamiltonian(coeffs)
    return qp.expval(H)


def optimization(coeffs):
    def cost(params):
        return vqe_circuit(params,coeffs)
    params = np.array([np.pi/2,np.pi/2,np.pi/2],requires_grad=True)
    opt=qp.GradientDescentOptimizer(stepsize=0.01)
    for i in range(800):
        params = opt.step(cost,params)
    return vqe_circuit(params,coeffs)
