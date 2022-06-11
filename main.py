from functions import *

T0 = 400.0
P0 = 101325.0
Phi = [0.5, 0.8, 1, 1.5]


T_PForDiffP("SV", T0)
T_PForDiffT("SV", P0)
for phi in Phi: T_PForPhi(phi, "SV")
