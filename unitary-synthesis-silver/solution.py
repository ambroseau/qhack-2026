"""Personal Best (Silver): exact unitary synthesis at the rotation lower bound.

Method based on Mottonen, Vartiainen, Bergholm & Salomaa,
"Quantum circuits for general multiqubit gates", PRL 93, 130502 (2004).

Uses `cs_decomposition` from the QHack challenge template (not included here).
"""
import pennylane as qp
import pennylane.numpy as np


def submission_circ(u_mat):
    n=int(round(np.log2(len(u_mat))))
    def zyz(u):
        phi=np.angle(np.linalg.det(u)) / 2
        v=u*np.exp(-1j*phi)
        a=v[0,0]
        b=v[1,0]
        beta=2*np.arctan2(abs(b),abs(a))
        s=-np.angle(a)    
        d=np.angle(b)
        alpha=s+d
        gamma=s-d
        return phi,alpha,beta,gamma 

    def collect(U,n):
        seq=[("blocks",[U],0)]
        for i in range(n-1):
            new=[]
            for j in seq:
                if j[0]=="cs":
                    new.append(j)
                else:
                    _, blocks, q = j
                    lefts=[]
                    rights=[]
                    angles=[]
                    for B in blocks:
                        l0, l1, th, r0, r1 = cs_decomposition(B)
                        lefts.append(l0)
                        lefts.append(l1)
                        rights.append(r0)
                        rights.append(r1)
                        angles.append(2*th)
                    new.append(("blocks", rights, q + 1))
                    new.append(("cs", q, np.concatenate(angles)))
                    new.append(("blocks", lefts, q + 1))
            seq=new
        return seq
            
    seq= collect(u_mat,n)

    phase = np.zeros(2**n)
    gate = []
   
    for i in range(len(seq)-1,-1,-2):
        matrices=seq[i][1]
        RY=[]
        RZ=[]   
        phase_leaf=np.zeros(2**n)
        for j in range(len(matrices)):
            leaf_matrix=np.diag([np.exp(1j*phase[2*j]), np.exp(1j*phase[2*j+1])]) @ matrices [j]
            phi,alpha,beta,gamma=zyz(leaf_matrix)
            RY.append(beta)
            RZ.append(alpha)
            phase_leaf[2*j]=phi-gamma/2
            phase_leaf[2*j+1]=phi+gamma/2
        gate.append(("z",RZ,list(range(n-1)),n-1))
        gate.append(("y",RY,list(range(n-1)),n-1))
        if i==0: 
            gate.append(("diag",phase_leaf))
            break
        else: #factor the phase
            _, qubit_no, angles =seq[i-1]
            basis_no=2**(n-1-qubit_no)
            wire=[]
            for w in range(n):
                if w!=qubit_no:
                    wire.append(w)
            twist_RZ =[]
            phase=np.zeros(2**n)
            for p in range(2**n):
                if p & basis_no:
                    continue
                else:
                    o = p+basis_no
                    twist_RZ.append(phase_leaf[o]-phase_leaf[p])
                    average=(phase_leaf[p]+phase_leaf[o])/2
                    phase[p]=average
                    phase[o]=average
            gate.append(("z",twist_RZ,wire,qubit_no)) 
            gate.append(("y",angles,wire,qubit_no)) 
    
    for i in range(len(gate)-1,0-1,-1):
        if gate[i][0]=="diag":
            qp.DiagonalQubitUnitary(np.exp(1j * gate[i][1]), wires=range(n))
        elif gate[i][0]=="z":
            qp.SelectPauliRot(np.array(gate[i][1]), control_wires=gate[i][2], target_wire=gate[i][3], rot_axis="Z")
        else: 
            qp.PauliZ(gate[i][3])
            qp.S(gate[i][3])
            qp.Hadamard(gate[i][3])
            qp.SelectPauliRot(np.array(gate[i][1]), control_wires=gate[i][2], target_wire=gate[i][3], rot_axis="Z")
            qp.Hadamard(gate[i][3])
            qp.S(gate[i][3])
