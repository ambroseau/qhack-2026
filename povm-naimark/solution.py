"""Implementing POVMs: a generalised measurement via one auxiliary qubit.

Wire 0 is the auxiliary qubit, wire 1 the system. The top-left 2x2 block K of
the unitary is chosen so that p00 = alpha |<1|psi>|^2 and p01 = beta |<-|psi>|^2;
the rest of the unitary is filled in with the Halmos unitary dilation
U = [[K, -sqrt(I - K K^dag)], [sqrt(I - K^dag K), K^dag]].
"""
import pennylane as qp
import pennylane.numpy as np


def implement_POVM(alpha,beta):
    A = np.array([[0,np.sqrt(alpha)],[np.sqrt(beta/2),-np.sqrt(beta/2)]])
    B = -qp.math.sqrt_matrix(np.eye(2)-A@A.conj().T)
    C =qp.math.sqrt_matrix(np.eye(2)-A.conj().T@A)
    D = A.conj().T
    E = np.block([[A,B],[C,D]])
    qp.QubitUnitary(E, wires=[0, 1])
