
sudo ./set_pci_10G.sh

python program_roach_raw_v4.py 163.10.43.167 192.168.5.10

python read_spectra_gbe.py

#./valon-minicom.sh # change frequencies
#sudo tcpdump -i ens4 -vvv  udp # to see UDP packets
#sudo iftop -i ens4 # to see data-flow

#ipython2 # for roach-fpga  
