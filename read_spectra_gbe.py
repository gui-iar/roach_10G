import socket
import struct
import numpy as np
import matplotlib.pyplot as plt



def read_data_roach():
# Create UDP socket
    UDP_IP = "192.168.5.10"
    UDP_PORT = 10000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
# Initialize arrays for each channel
    pol_0 = []
    pol_1 = []
    fft_size = 65536
# Read 8192 words of 64 bits each
    WORDS_TO_READ = 8192
    SAMPLE_PER_PACKET = WORDS_TO_READ / 2
    data, addr = sock.recvfrom(WORDS_TO_READ)
    while len(pol_0) < fft_size:
        data, addr = sock.recvfrom(WORDS_TO_READ)
        if len(data)==WORDS_TO_READ:
            raw = np.array(struct.unpack('<8192b',data))
            for i in range(0,len(raw),8):
                pol_0.append(raw[i])
                pol_0.append(raw[i+1])
                pol_0.append(raw[i+2])
                pol_0.append(raw[i+3])
                pol_1.append(raw[i+4])
                pol_1.append(raw[i+5])
                pol_1.append(raw[i+6])
                pol_1.append(raw[i+7])
# Close the socket when done
    sock.close()
    return np.array(pol_0), np.array(pol_1)


pol_0 = []
pol_1 = []


pol_0, pol_1 = read_data_roach()
print ('read done')


freq_range_mhz = np.linspace(1600, 1200, (32768/2)-1)

plt.figure(0)
(S_0, f) = plt.psd(np.array(pol_0),32764)
(S_1, f) = plt.psd(np.array(pol_1),32764)

plt.figure(1)
plt.plot(freq_range_mhz,10*np.log10(S_0))
plt.plot(freq_range_mhz,10*np.log10(S_1))
plt.title('Total Power Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power')
plt.grid(True)

data_polarization1 = []
data_polarization1 = []
data_polarization1 = pol_0      
data_polarization2 = pol_1

data_polarization1 = data_polarization1.astype('float64')
data_polarization2 = data_polarization2.astype('float64')
window = np.hamming(len(pol_0))
data_polarization1 *= window
data_polarization2 *= window

spectrum_polarization1 = np.fft.fft(data_polarization1)
spectrum_polarization2 = np.fft.fft(data_polarization2)
frequency_axis = np.fft.fftfreq(len(pol_0))


total_power_spectrum = (np.abs(spectrum_polarization1) ** 2 + np.abs(spectrum_polarization2) ** 2)
# Plot the second half of the result (positive frequencies only)
plt.figure(2)
half_data_length = len(pol_0) // 2
freq_range_mhz = np.linspace(1200, 1600, 32768)
plt.plot(freq_range_mhz,10*np.log10(spectrum_polarization1[half_data_length:]))
plt.plot(freq_range_mhz,10*np.log10(spectrum_polarization2[half_data_length:]))
plt.title('Total Power Spectrum with Hamming Window (Positive Frequencies)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power')
plt.grid(True)


plt.figure(3)
plt.plot((pol_0))
plt.plot((pol_1))

plt.show()
