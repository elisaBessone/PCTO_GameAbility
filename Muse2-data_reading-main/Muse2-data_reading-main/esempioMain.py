#-*- coding: utf-8 -*-

#esempio main

import argparse
import sys
#from cli import CLI
import import_ipynb
import matplotlib.pyplot as plt
import config

def main():

    parser = argparse.ArgumentParser(
        description='Python package for analysis in the Musedevices.',
        usage=''' __main__ <command> [<args>]
        14. Input
        15. Analyzabile folder
        16. folder input folder (with files inside)
        17. output folder
        18.
        19. Available commands:
        20. devices Analyzable devices
        21. -m --muse EEG data
        22. add channel to analyze
        23. TP9 AF7 AF8 TP10
        24. -p --ppg Include PPG data
        25. add channel to analyze
        26. PPG1 PPG2 PPG3
        27. -c --acc Include accelerometer data
        28. add channel to analyze
        29. X Y
        30.
        31. -g --gyro Include gyroscope data
        32. add channel to analyze
        33. Y Z
        43
        34.
        P.S.: if a channel isn't inserted, all will be analyzed
        ''')
    parser.add_argument('inputfoldername')
    parser.add_argument('outputfoldername')
    parser.add_argument('command', help='Command to run.')