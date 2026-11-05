# QHack 2026 – selected solutions

My solutions to selected challenges from **QHack 2026**, Xanadu's quantum coding competition (Oct 2026), written in Python with [PennyLane](https://pennylane.ai). I completed 22 of 23 challenges. This repo collects the ones most relevant to fault-tolerant quantum computing and quantum algorithms.

Each folder contains my solution code only. The challenge templates, graders and helper functions belong to Xanadu and are not included, so the files are not meant to run on their own.

## Highlights

| Challenge | Folder | Key idea | Result |
|---|---|---|---|
| Personal Best (Silver) | [`unitary-synthesis-silver`](unitary-synthesis-silver) | Exact n-qubit unitary synthesis under a fault-tolerant cost model (each rotation ≈ 44 T gates) | 4ⁿ − 1 rotations (the parameter-count lower bound): **21% cheaper** than the Quantum Shannon Decomposition at 5 qubits |
| Personal Best (Bronze) | [`unitary-synthesis-bronze`](unitary-synthesis-bronze) | Commute RZ gates through CNOT controls and merge rotations | 8.1% cheaper than the baseline at 5 qubits |
| The Salary Cap | [`qpe-resource-estimation`](qpe-resource-estimation) | Symbolic T-count estimation of quantum phase estimation | Largest QPE precision that fits a given T-gate time and runtime budget |
| Implementing POVMs | [`povm-naimark`](povm-naimark) | Naimark dilation: a generalised measurement using one auxiliary qubit | Exact POVM probabilities for any input state |
| Break the Tie | [`amplitude-estimation-tiebreak`](amplitude-estimation-tiebreak) | Amplitude estimation returns *a* and *1 − a*; a cheap direct circuit picks the right one | Matches the estimate to 1e-9 |
| A Basket of Options | [`basket-option-qmc`](basket-option-qmc) | Quantum Monte Carlo pricing of a two-asset correlated basket call | Option value within 1e-3 |
| Fermionic VQE | [`fermionic-vqe`](fermionic-vqe) | Fermionic Hamiltonian → Jordan–Wigner → VQE | Ground-state energy |

## Unitary synthesis (Silver) in more detail

**Goal:** implement a Haar-random 2–5 qubit unitary exactly (to 1e-8), where every RX/RY/RZ costs 44 (≈ the T-count of synthesising one arbitrary rotation) and Clifford gates are free.

**Why 4ⁿ − 1 is the floor:** an n-qubit unitary has 4ⁿ real parameters, one of which is a free global phase. Each rotation carries one angle, so an exact circuit needs at least 4ⁿ − 1 rotations: 1023 at 5 qubits, against 1296 for the baseline.

**Method** (Möttönen et al., 2004):
1. Recursively apply the cosine-sine decomposition, which turns U into a chain of single-qubit "leaf" gates on the last qubit alternating with multiplexed RY rotations.
2. Write each leaf as RZ · RY · (diagonal phase).
3. Walk the chain backwards. Split each leaf's diagonal at the RY before it: the part that depends on that RY's qubit becomes a multiplexed RZ, and the rest commutes through and is absorbed into the previous leaf at no cost.
4. Only the first leaf pays for its full diagonal.

Multiplexed rotations use `qp.SelectPauliRot` (2ᵏ rotations for k controls). Multiplexed RY uses an S† H basis change around the RZ version, since those gates are free.

## References

- M. Möttönen, J. J. Vartiainen, V. Bergholm, M. M. Salomaa, *Quantum circuits for general multiqubit gates*, PRL **93**, 130502 (2004)
- V. V. Shende, S. S. Bullock, I. L. Markov, *Synthesis of quantum-logic circuits*, IEEE TCAD **25**, 1000 (2006)
- QHack 2026 challenges © Xanadu
