import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

npoints = 100

gas = ct.Solution('gri30.xml')
gas.X = 'CH4:1'

# SV - with constant volume

phi = [0.5, 0.8, 1, 1.5]

temp05 = np.zeros(npoints)
temp08 = np.zeros(npoints)
temp1 = np.zeros(npoints)
temp15 = np.zeros(npoints)
temp2 = np.zeros(npoints)

press05 = np.zeros(npoints)
press08 = np.zeros(npoints)
press1 = np.zeros(npoints)
press15 = np.zeros(npoints)
press2 = np.zeros(npoints)

temp_SV = [temp05, temp08, temp1, temp15, temp2]
press_SV = [press05, press08, press1, press15, press2]

def T_PForDiffP(equlibrium, T0):
    P = np.linspace(0.1 * ct.one_atm, ct.one_atm * 6, npoints)



    for j in range(len(phi)):
        for i in range(npoints):
            gas.TP = T0, P[i]
            gas.set_equivalence_ratio(phi[j], 'CH4', 'O2:2.0, N2:7.52', basis='mole')
            gas.equilibrate(equlibrium)
            temp_SV[j][i] = gas.T
            press_SV[j][i] = gas.P

    fig, ax = plt.subplots()

    for j in range(len(phi)):
        plt.plot(P / 100000, temp_SV[j], label='$ \Phi$ = ' + str(phi[j]))

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    ax.set_xlabel('Initial pressure [bar]')
    ax.set_ylabel('Flame temperature [K]')
    ax.get_yaxis().get_major_formatter().set_useOffset(False)

    plt.savefig('temp_for_diff_press_for_' + equlibrium + '.png')

    fig, ax = plt.subplots()
    for j in range(len(phi)):
        plt.plot(P / 100000, press_SV[j]/100000, label='$ \Phi$ = ' + str(phi[j]))

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    ax.set_xlabel('Initial pressure [bar]')
    ax.set_ylabel('Flame pressure [bar]')
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    plt.savefig('press_for_diff_press_for_' + equlibrium + '.png')

    return plt


def T_PForDiffT(equlibrium, P0):
    T = np.linspace(400, 2000, npoints)


    for j in range(len(phi)):
        for i in range(npoints):
            gas.TP = T[i], P0
            gas.set_equivalence_ratio(phi[j], 'CH4', 'O2:2.0, N2:7.52', basis='mole')
            gas.equilibrate(equlibrium)
            temp_SV[j][i] = gas.T
            press_SV[j][i] = gas.P
    fig, ax = plt.subplots()

    for j in range(len(phi)):
        plt.plot(T, temp_SV[j], label='$ \Phi$ = ' + str(phi[j]))

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    ax.set_xlabel('Initial temperature [K]')
    ax.set_ylabel('Flame temperature [K]')
    ax.get_yaxis().get_major_formatter().set_useOffset(False)

    plt.savefig('temp_for_diff_init_temp_for_' + equlibrium + '.png')

    fig, ax = plt.subplots()
    for j in range(len(phi)):
        plt.plot(T, press_SV[j]/100000, label='$ \Phi$ = ' + str(phi[j]))

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    ax.set_xlabel('Initial temperature [K]')
    ax.set_ylabel('Flame pressure [bar]')
    ax.get_yaxis().get_major_formatter().set_useOffset(False)

    plt.savefig('press_for_diff_init_temp_for_' + equlibrium + '.png')
    return plt


def T_PForPhi(phi, equilibrium):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    temp = np.zeros((npoints, npoints))
    press = np.zeros((npoints,npoints))
    t = np.linspace(400, 2000, npoints)
    p = np.linspace(0.1 * ct.one_atm, ct.one_atm * 6, npoints)

    T, P = np.meshgrid(t, p)

    for i in range(npoints):
        for j in range(npoints):
            gas.TP = t[i], p[j]
            gas.set_equivalence_ratio(phi, 'CH4:1', 'O2:2.0, N2:7.52', basis='mole')
            gas.equilibrate(equilibrium)
            temp[j][i] = gas.T
            press[j][i] = gas.P

    surf = ax.plot_surface(P / 100000, T, temp, cmap=cm.Spectral_r,
                           linewidth=0, antialiased=False)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter('{x:.0f}')
    ax.set_ylabel('Initial temperature [K]')
    ax.set_xlabel("Initial pressure [bar]")

    fig.colorbar(surf, shrink=0.5, aspect=7)

    label = 'Flame temperature [K]'

    fig.suptitle(label + ' for $ \Phi$ = ' + str(phi))

    plt.savefig('3d_plot_for_phi_temperature=' + str(phi) + '_' + equilibrium + '.png')

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf = ax.plot_surface(P / 100000, T, press/100000, cmap=cm.Spectral_r,
                           linewidth=0, antialiased=False)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter('{x:.0f}')
    ax.set_ylabel('Initial temperature [K]')
    ax.set_xlabel("Initial pressure [bar]")

    fig.colorbar(surf, shrink=0.5, aspect=7)

    label = 'Flame pressure [bar]'

    fig.suptitle(label + ' for $ \Phi$ = ' + str(phi))

    plt.savefig('3d_plot_for_phi_pressure=' + str(phi) + '_' + equilibrium + '.png')

    return plt
