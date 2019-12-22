# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 20:20:31 2019

@author: zhuguohua
"""

import numpy as np
import control as ct
import matplotlib.pyplot as plt

c = 1.5
rho = 2.0

xref = 0
vref = 0

# System state: x,v
# System input: ux,uv
# System output: x,v
# System parameters: none
def mass_update(t, x, u, params):
    # Return the derivative of the state
    return np.array([
        x[1],               # dx = v
        u[1] + np.sin(2*t)  # dv = u + d
    ])

def mass_output(t, x, u, params):
    return x # return x, v (full state)

unit_mass = ct.NonlinearIOSystem(
    mass_update, mass_output, states=2, name='unit_mass',
    inputs=('ux','uv'),
    outputs=('x', 'v'))

###############################################################################
# Control 
###############################################################################
# u = c*v + rho*sign(c*x + v)
def control_output(t, x, u, params):
    return  np.array([0,c*u[1] + rho*np.sign(c*u[0] + u[1])])

# Define the controller as an input/output system
controller = ct.NonlinearIOSystem(
    None, control_output, name='controller',        # static system
    inputs=('x', 'v'),    # system inputs
    outputs=('ux','uv')                            # system outputs
)

###############################################################################
# Target
###############################################################################
def target_output(t, x, u, params):
    xref, vref = u
    return np.array([xref,vref])

# Define the trajectory generator as an input/output system
target = ct.NonlinearIOSystem(
    None, target_output, name='target',
    inputs=('xref', 'vref'),
    outputs=('x', 'v'))

###############################################################################
# System Connect
###############################################################################
fastest = ct.InterconnectedSystem(
    # List of subsystems
    (target,controller, unit_mass), name='fastest',

    # Interconnections between  subsystems
    connections=(
        ('controller.x','target.x','-unit_mass.x'),
        ('controller.v','target.v','-unit_mass.v'),
        ('unit_mass.ux', 'controller.ux'),
        ('unit_mass.uv', 'controller.uv'),
    ),

    # System inputs
    inplist=['target.xref', 'target.vref'],
    inputs=['xref','vref'],

    #  System outputs
    outlist=['unit_mass.x', 'unit_mass.v'],
    outputs=['x', 'v']
)

###############################################################################
# Input Output Response
###############################################################################
# time of response
T = np.linspace(0, 8, 10000)
# the response
tout, yout = ct.input_output_response(fastest, T, [xref*np.ones(len(T)),vref*np.ones(len(T))],X0=[1,-2])

plt.close()
plt.figure()
plt.title("Sliding Variable")
plt.xlabel("Time[s]")
plt.plot(tout,c*yout[0]+yout[1])

plt.figure() 
plt.grid()
plt.title("Asymptotic convergence for f(x,v,t)=sin(2t)")
plt.xlabel("Time(s)")
plt.plot(tout,yout[0],label='distance(m)')
plt.plot(tout,yout[1],label='velocity(m/s)')
plt.legend()
plt.title('unit mass modle(without disturbance)')
plt.figure()
plt.title("Phase portrait")
plt.xlabel("x")
plt.ylabel("v")
plt.plot(yout[0],yout[1])

u = []
for i in range(len(tout)):
    u.append(c*yout[1][i] + rho*np.sign(c*yout[0][i] + yout[1][i]))
    
plt.figure()
plt.title("Sliding mode control")
plt.xlabel("Time[s]")
plt.plot(tout,u)
plt.show()