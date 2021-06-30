#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    CTRL=net.addController(name='CTRL',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    S_LIB = net.addSwitch('S_LIB', cls=OVSKernelSwitch, dpid='00000002')
    S_DOM = net.addSwitch('S_DOM', cls=OVSKernelSwitch, dpid='00000003')
    S_LAB = net.addSwitch('S_LAB', cls=OVSKernelSwitch, dpid='00000001')

    info( '*** Add hosts\n')
    DEVELOP = net.addHost('DEVELOP', cls=Host, ip='10.0.10.2', defaultRoute=None)
    WORK_2 = net.addHost('WORK_2', cls=Host, ip='10.0.20.2', defaultRoute=None)
    WORK_1 = net.addHost('WORK_1', cls=Host, ip='10.0.20.1', defaultRoute=None)
    WORK_3 = net.addHost('WORK_3', cls=Host, ip='10.0.20.3', defaultRoute=None)
    STU_1 = net.addHost('STU_1', cls=Host, ip='10.0.30.1', defaultRoute=None)
    STU_3 = net.addHost('STU_3', cls=Host, ip='10.0.30.3', defaultRoute=None)
    TEST = net.addHost('TEST', cls=Host, ip='10.0.10.3', defaultRoute=None)
    RESEARCH = net.addHost('RESEARCH', cls=Host, ip='10.0.10.1', defaultRoute=None)
    STU_2 = net.addHost('STU_2', cls=Host, ip='10.0.30.2', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(S_LIB, WORK_1)
    net.addLink(S_LIB, WORK_2)
    net.addLink(S_LIB, WORK_3)
    net.addLink(S_DOM, STU_1)
    net.addLink(S_DOM, STU_2)
    net.addLink(S_DOM, STU_3)
    net.addLink(S_LIB, S_LAB)
    net.addLink(S_LIB, S_DOM)
    net.addLink(S_LAB, S_DOM)
    net.addLink(S_LAB, RESEARCH)
    net.addLink(S_LAB, DEVELOP)
    net.addLink(S_LAB, TEST)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('S_LIB').start([CTRL])
    net.get('S_DOM').start([CTRL])
    net.get('S_LAB').start([CTRL])

    info( '*** Post configure switches and hosts\n')
    S_LIB.cmd('ifconfig S_LIB 10.0.20.254')
    S_DOM.cmd('ifconfig S_DOM 10.0.30.254')
    S_LAB.cmd('ifconfig S_LAB 10.0.10.254')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

