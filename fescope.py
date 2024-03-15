from scipy import integrate
from scipy import interpolate
import glob, os, sys, subprocess
import numpy as np
import time

def readit():
## Reads config file
    pass

def analyzeit(file_list):
## Analize waveform
    pass 

def takeit(N,run,folder_name,sources,trigger,screen_points,ni,nf,x):
    ## Takes data from the scope

    # Open scope
    tek = pyvisa.ResourceManager().open_resource('TCPIP::192.168.1.94::gpib0,1::INSTR')
    
    # Defining trigger settings
    tek.write('TRIG:A:EDG:SOUR {0}'.format(trigger[0]))
    tek.write('TRIG:A:MOD NORM')
    tek.write('ACQ:STOP SEQUENCE')
    
    # Setting up waveform information
    tek.write('DAT:ENC ASCII')
    tek.write('HORIZONTAL:RECORDLENGTH {0}'.format(screen_points)) 
    tek.write('DAT:STAR {0}'.format(ni))
    
    # Choose source
    tek.write('DAT:SOU {0}'.format(channel))
    
    # Acquire waveform
    pre_amble = tek.query('WFMPR?')
    
    # Save preamble
    file_pre = open(path_to_preamble,'w')
    file_pre.write(pre_amble)
    file_pre.close()

    # DAQ loop:
    i = 0
    while i < Nfiles:

        # Acquire a waveform
        y = []
        tek.write('ACQ:STATE ON')
        curve = tek.query('CURV?')
        y.append(np.fromstring(curve,dtype=int,sep=','))

        # Save waveform to file
        waveform_file = r".\{0}\waveforms\waveform-Run{1:02d}-{2:06d}.dat".format(folder_name,run,i)
        waveform = open(waveform_file,'w')
        for j in range(0, len(x)):
            waveform.write("{0:03d}, {1:d}\n".format(x[j], y[j]))
        waveform.close()   

        # Save sample
        if i < 1000:
            plot(folder_name, run, i, x, y)


def printProgress(message, i, N):
## Let user know what is going on
    # print("Analysis in progres ()\n")
    print("Status: {0}.".format(message),flush=True)

def main():
## Call all functions
    
    # Open config file
    fileconfig = open(sys.argv[1],"r")
    lines = fileconfig.readlines()
    fileconfig.close()

    # line[0]: run number
    split0 = lines[0].split(": ")
    run = int(split0[1].replace("\n",""))

    # line[1]: path to store data
    split1 = lines[1].split(": ")
    path_to_analize = split1[1].replace("\n","")
    
    # line[2]: path_to_preamble
    split2 = lines[2].split(": ")
    path_to_preamble = split2[1].replace("\n","")

    # line[3]: number of waveforms to acquire
    split3 = lines[3].split(": ")
    Nfiles = int(split3[1].replace("\n",""))

    # line[5]: source channel
    split5 = lines[5].split(": ")
    source = split5[1].replace("\n","")

    # line[6]: trigger channel
    split6 = lines[6].split(": ")
    trigger = split6[1].replace("\n","")

    # line[7]: screenpoints:
    split7 = lines[7].split(": ")
    screen_points = int(split7[1].replace("\n",""))

    # ni always 1
    ni = 1

    # nf always 500
    nf = screen_points

    #x 
    x = range(ni,nf+1)

    # Take data
    # takeit(Nfiles,run,folder_name,sources,trigger,screen_points,ni,nf,x)

    

## Run main fuction
if __name__ == "__main__":
    main()
