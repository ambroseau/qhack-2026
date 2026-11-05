"""A Basket of Options: price a two-asset basket call with quantum Monte Carlo.

(z1, z2) discretised on an 8x8 grid over [-3, 3]; probabilities from the
bivariate normal density with correlation rho; payoff max(B_T - K, 0)
normalised by its maximum and passed to qp.QuantumMonteCarlo.
"""
import pennylane as qp
import pennylane.numpy as np

M = 64
S10 = 100.0
S20 = 100.0
sigma1 = 0.20
sigma2 = 0.30
r = 0.05

points = np.linspace(-3, 3, 8)
lists=[]
for z1 in points:
    for z2 in points:
        lists.append((z1,z2))

def payoff(i,w,T,K):
        z1,z2=lists[i]
        S1=S10*np.exp((r-sigma1**2/2)*T+sigma1*np.sqrt(T)*z1)
        S2=S20*np.exp((r-sigma2**2/2)*T+sigma2*np.sqrt(T)*z2)
        B_T=w*S1+(1-w)*S2
        return max(B_T-K,0)

def nor_payoff(i,w,T,K):
    payoff_list = []
    for j in range(M):
        payoff_list.append(payoff(j,w,T,K))
    g_max=max(payoff_list)
    return np.array(payoff_list)[i]/g_max

def prob(z1,z2,rho):
    return 1/(2*np.pi*np.sqrt(1-rho**2))*np.exp(-(z1**2-2*rho*z1*z2+z2**2)/(2*(1-rho**2)))

def prob_1(rho):
    probabilities=[]
    for z1 in points:
        for z2 in points:
            probabilities.append(prob(z1,z2,rho))
    return np.array(probabilities)/np.sum(np.array(probabilities))

n = 10
N = 2 ** n
m = int(np.log2(M))
target_wires = range(m + 1)
estimation_wires = range(m + 1, n + m + 1)

dev = qp.device("default.qubit", wires=(n + m + 1))

@qp.qnode(dev)
def quantum_montecarlo(rho, w, T, K):
    prob=prob_1(rho)

    def f(i):
        return nor_payoff(i, w, T, K)
    qp.QuantumMonteCarlo(prob,f,target_wires,estimation_wires)

    return qp.probs(estimation_wires)
