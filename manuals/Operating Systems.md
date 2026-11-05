# Drive Management and File Systems
This section covers the management and initialization of disks, and also file systems and individual file handling. Note that the terminology in this area may be confusing. For reference of each term, consult the [File System Terminology](https://fido.ninja/terminology/other.html#file-system)

## Disk Initialization

Before using any [*disk*](https://fido.ninja/terminology/other.html#disk), we typically perform two steps:

1. *Partitioning* (optional): setting up the partition table and creating 1 or more partitions (or *slices*) of the disk
    - partitioning is optional, but e.g. Windows cannot work with internal disks that are not partitioned
1. *Formatting*, i.e., a file system is created on the partition


### Partitioning

- [Wikipedia](https://en.wikipedia.org/wiki/Disk_partitioning)
- [Arch Linux](https://wiki.archlinux.org/title/Partitioning)

Disk partitioning or disk slicing is dividing a disk into separate regions, called *partitions* or *slices*, each of which can be managed independently, i.e., having its own file system and mount point.

The data about the partitions is stored in a *partition table*, which is organized according to a specific *partitioning scheme*.

Common partitioning schemes include:

- [MBR (Master Boot Record)](https://en.wikipedia.org/wiki/Master_boot_record)
- [GPT (GUID Partition Table)](https://en.wikipedia.org/wiki/GUID_Partition_Table)

The partitioning is optional, but most of the storage devices are partitioned. The storage devices can be roughly divided into these categories (based on the partitioning requirements):

- **Internal disks (HDDs, SSDs)** usually require partitioning. This is a strong requirement for:
    - Operating system disks (bootable disks)
    - Any Windows disks
- **External disks, USB Flash Drives, SD Cards** typically come pre-partitioned with a single partition spanning the entire disk.
    - for SD cards, the single MBR partition is part of the standard
- **Old USB Flash Drives, Optical Discs, or Floppy Disks** does not require partitioning, it is assumed that the file system sits directly on the disk.


#### Master Boot Record (MBR)
[Wikipedia](https://en.wikipedia.org/wiki/Master_boot_record)

In MBR the disk can have up to 4 *primary partitions* and and *extended partitions*. 

The **primary partitions** are the partitions from which the operating system can boot. One of them is typically marked as the *active partition*, indicating that it contains the boot loader for the operating system.

The **extended partitions** are used to overcome the 4-partition limit of MBR. An extended partition can contain multiple *logical drives (volumes)*.

### Formatting

Formatting involves creating a file system. Typically, a partition is formatted, although it is also possible to format an entire disk without partitioning it first.