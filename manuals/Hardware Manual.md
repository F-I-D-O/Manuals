# Diagnostic
This chapter is about diagnosing the problem with the PC. Solutions to the problems described here are provided in the following chapters.


## PC is dead or shout down few seconds after start

 1. Unplug the power cables between the power supplz and the components and plug them again
 2. If the problem persists, check whether the source is not completely dead by connecting the green cable in the ATX 24 pin connector with anz of the black ones
 3. If the source works (power supply fan started), check the voltage on each PIN by the multimeter

## Corsair PIN Voltage![Corsair PIN Voltage](https://cdn.shopify.com/s/files/1/0015/3776/9518/files/PSU_Pinout_Voltage_-_Corsair_Type_4.png?v=1578641655)


## Hard drive diagnostics
When handling hard drive problems, we typically want to:

1. identify, whether the hard drive is faulty
1. if it is, try to backup the data
1. buy a new hard drive
1. clone the data from the old hard drive to the new one, or install a fresh copy of the OS, in case the old hard drive is not readable. 

This section is about step 1, i.e., identifying whether the hard drive is really faulty. Steps:

1. Restart the PC, if the problem persistss,
1. Move the hard drive to another slot, or connect it to another cable, in case of SATA drive.

If none of this helps, the hard drive is faulty. It is time to proceed further and try to backup the data.






# Backup a hard drive from a faulty drive
These steps assumes that the backup is run from linux, either from an installation, or from a live USB.

When backing the data from a faulty hard drive, we should first check, whether the drive is accessible at all:

1. run `lsblk` to list all the drives. If the drive is not listed, there is no hope
1. install `smartmontools` and run `smartctl -a <path-to-device>`. If this command fails with an error, there is no hope

If the `smartctl` command succeeds, it should show the SMART status of the drive, including statistics like bad sectors, worn out sectors, etc.

We can proceed with the backup now. First we should decide whether to clone the whole disk, or just backup files.


## Clone the disk
To clone the disk, we can use the [`ddrescue`](https://www.gnu.org/software/ddrescue/manual/ddrescue_manual.html) tool.





# Update GPU vBIOS
Steps:

1. search the manufacterer's web for the appropriate vBIOS `.rom` file. It needs to be a file specific for the specific model of the GPU, not just for a number or a series
2. create a bootable DOS USB. It can be easilly created by the [rufus](https://rufus.ie) tool, which can both download freeDOS and create a bootable USB from it.
3. Puth the rom file to the DOS USB, together with the dost version of the update tool (most likely nvflash for DOS, do not mistake it with the Windows version)
4. run the PC, boot DOS from USB
5. backup the old vBIOS
6. run the update tool using the `.rom` file

# Possible problems

## The USB is not detected in BIOS
This problem can have two very different causes:

- The USB is not bootable.
    - We could use a wrong procedure to create it, or
    - the USB image we try to use is not actually a bootable one, but requires some hardware support to be loaded (e.g., HP PC Hardware Diagnostics).
- The USB is faulty. We can try to use
    1. another USB port, or if still not detected
    1. another USB stick.





