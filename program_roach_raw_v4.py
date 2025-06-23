#!/usr/bin/env python

# tut5.py
# CASPER Tutorial 5: Heterogeneous Instrumentation
#   Config script.

import corr
import time
import numpy
import math
import struct
import sys

katcpPort = 7147
destPort = 10000
srcIP = 192*(2**24) + 168*(2**16) + 5*(2**8) + 20
srcPort = 10000
MACBase = 123456780000
gbe0 = 'gbe0'



if __name__ == '__main__':
    from optparse import OptionParser

    p = OptionParser()
    p.set_usage('tut5.py <ROACH_HOSTNAME_or_IP> <GPU server 10GbE IP>')
    p.set_description(__doc__)

    p.add_option('-b', '--bof', dest='boffile', type='str', default='',
        help='Specify the bof file to load')
    opts, args = p.parse_args(sys.argv[1:])

    if len(args)!=2:
        print 'Please specify a ROACH board and GPU server 10GbE IP. \nExiting.'
        exit()
    else:
        roach = args[0]
        destIP = args[1]
        tmp = destIP.split('.')
        destIP = int(tmp[0])*(2**24) + int(tmp[1])*(2**16) + int(tmp[2])*(2**8) + int(tmp[3])

    if opts.boffile != '':
        boffile = opts.boffile
    else:
        boffile = 'adc_hi_snapshot_gbe_4_2024_Nov_26_1043.bof' #'tut5.bof'


    print 'Connecting to server %s... ' %(roach),
    sys.stdout.flush()
    fpga = corr.katcp_wrapper.FpgaClient(roach, katcpPort)
    time.sleep(1)
    if fpga.is_connected():
        print 'DONE'
    else:
        print 'ERROR: Failed to connect to server %s!' %(roach)
        sys.exit(0);

    print 'Programming FPGA with %s...' %boffile,
    sys.stdout.flush()
    fpga.progdev(boffile)
    print 'DONE'

    time.sleep(5)

    fpga.listdev()
    gbe0_link = bool(fpga.read_int(gbe0))
    if not gbe0_link:
       print 'ERROR: There is no cable plugged into port0!'

    print 'Setting up packet generation...',
    sys.stdout.flush()
    fpga.write_int('dest_ip', destIP)
    fpga.write_int('dest_port', destPort)

    # send data at a rate
    #   = (pkt_sim_payload_len / pkt_sim_period) * 10GbE core clock rate
    fpga.write_int('pkt_sim_period', 2048)
    fpga.write_int('pkt_sim_payload_len', 1024)  # send 128 * 8 bytes of data
                                                # per packet
    print 'DONE'
    print 'Resetting cores and counters...',
    sys.stdout.flush()

    fpga.write_int('rst',1)
    time.sleep(1)
    fpga.write_int('rst',0)
    print 'DONE'

    print 'Enabling the packetizer...',
    sys.stdout.flush()
    fpga.write_int('pkt_sim_enable', 1)
    print 'DONE'


