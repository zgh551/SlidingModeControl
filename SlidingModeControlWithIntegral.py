# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 20:20:31 2019

@author: zhuguohua
"""

import numpy as np
import control as ct
import matplotlib.pyplot as plt

c = 1.5
c_bar = 10.0

rho = 30.0

x1_ref = 0
x2_ref = 0
u_ref = 0

x1_0 = 1
x2_0 = -2
u_0  = 0


def f(x1,x2,t):
    return np.sin(2*t)
# System state: x1,x2,u
# System input: v
# System output: x1,x2,u
# System parameters: none
def mass_update(t, x, u, params):
    # Return the derivative of the state
    return np.array([
        x[1],                   # dx1 = x2
        x[2] + f(x[0],x[1],t),  # dx2 = u + f(x1,x2,t)
        u[0]                    # du  = v
    ])

def mass_output(t, x, u, params):
    return x # return x1, x2 , u (full state)

unit_mass = ct.NonlinearIOSystem(
    mass_update, mass_output, states=3, name='unit_mass',
    inputs=('v'),
    outputs=('x1', 'x2', 'u'))

###############################################################################
# Control 
###############################################################################
# s = u + (c + c_bar)x2 c*c_bar*x1 + f(x1,x2,t)
# System state: none
# System input: x1,x2,u
# System output: v
# System parameters: none
def control_output(t, x, u, params):
    s = u[2] + (c + c_bar)*u[1] + c*c_bar*u[0] + f(u[0],u[1],t)
    return np.array([c*c_bar*u[1] + (c + c_bar)*u[2] + rho*np.sign(s)])

# Define the controller as an input/output system
controller = ct.NonlinearIOSystem(
    None, control_output, name='controller',    # static system
    inputs=('x1', 'x2', 'u'),                   # system inputs
    outputs=('v')                               # system outputs
)

###############################################################################
# Target
###############################################################################
def target_output(t, x, u, params):
    x1_ref, x2_ref ,u_ref = u
    return np.array([x1_ref,x2_ref,u_ref])

# Define the trajectory generator as an input/output system
target = ct.NonlinearIOSystem(
    None, target_output, name='target',
    inputs=('x1_ref', 'x2_ref', 'u_ref'),
    outputs=('x1_r', 'x2_r', 'u_r'))

###############################################################################
# System Connect
###############################################################################
fastest = ct.InterconnectedSystem(
    # List of subsystems
    (target,controller, unit_mass), name='fastest',

    # Interconnections between  subsystems
    connections=(
        ('controller.x1','target.x1_r','-unit_mass.x1'),
        ('controller.x2','target.x2_r','-unit_mass.x2'),
        ('controller.u' ,'target.u_r' ,'-unit_mass.u'),
        ('unit_mass.v', 'controller.v')
    ),

    # System inputs
    inplist=['target.x1_ref', 'target.x2_ref', 'target.u_ref'],
    inputs=['x1_ref', 'x2_ref', 'u_ref'],

    #  System outputs
    outlist=['unit_mass.x1', 'unit_mass.x2', 'unit_mass.u','controller.v'],
    outputs=['x1', 'x2', 'u','v']
)

###############################################################################
# Input Output Response
###############################################################################
# time of response
T = np.linspace(0, 8, 1000)
# the response
tout, yout = ct.input_output_response(fastest, T, [x1_ref*np.ones(len(T)),x2_ref*np.ones(len(T)),u_ref*np.ones(len(T))],X0=[x1_0,x2_0,u_0])

s = []
for i in range(len(tout)):
    s.append(yout[2][i] + (c + c_bar)*yout[1][i] + c*c_bar*yout[0][i] + f(yout[0][i],yout[1][i],tout[i]))

#v = []
#for i in range(len(tout)):
#    v.append ( -c*c_bar*yout[1][i] - (c + c_bar)*yout[2][i] + rho*np.sign(s[i]) )


plt.figure()
plt.grid()
plt.title("Sliding Variable")
plt.xlabel("Time[s]")
plt.plot(tout,c*yout[0]+yout[1],label='sigma')
plt.plot(tout,s,label='s')
plt.legend()


plt.figure() 
plt.grid()
plt.title("Asymptotic convergence for f(x,v,t)=sin(2t)")
plt.xlabel("Time(s)")
plt.plot(tout,yout[0],label='distance(m)')
plt.plot(tout,yout[1],label='velocity(m/s)')
plt.legend()
plt.title('unit mass modle(with disturbance[sin(2t)])')

plt.figure()
plt.grid()
plt.title("Phase portrait")
plt.xlabel("x1")
plt.ylabel("x2")
plt.plot(yout[0],yout[1])

plt.figure()
plt.grid()
plt.title("Sliding mode control[v]")
plt.plot(tout,yout[3])
#plt.plot(tout,v)

plt.figure()
plt.grid()
plt.title("Sliding mode control[u]")
plt.xlabel("Time[s]")
plt.plot(tout,yout[2])

plt.show()