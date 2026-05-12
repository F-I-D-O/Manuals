[`Hierarchical Data Format (HDF)`](https://en.wikipedia.org/wiki/Hierarchical_Data_Format) is a binary data format designed to store large amounts of data. It is widely used and it has support for many programming languages. It is a self-contained format: all metadata needed to read the data is embedded in the file. 

# HDF in C++

# HDF in Python

# HDF in Java
In Java, there are many options to work with HDF files. We list some of them in the following table:

| Name | Type | Description | last update |
|------|------|-------------|-------------|
| [HDF5](https://portal.hdfgroup.org) | wrapper | The official wrapper for the HDF5 library. It is a jar file provided by the main installer of HDF5 library. (in the lib folder). The documentation for Java is missing. | 2023-10-27 | 
| [sis-jhdf5](https://unlimited.ethz.ch/display/JHDF) | wrapper | A wrapper for the HDF5 library developed at ETH Zurich. | 2022-07-28 |
| [netCDF-Java](https://github.com/unidata/netcdf-java) | library for multiple file formats | A library that provides an interface to read and write netCDF, HDF5, GRIB, BUFR, and other file formats. | daily, last release 2022-07-05 |
| [HDFQL](https://www.hdfql.com/) | query language access to HDF5 | A library that provides a SQL-like access to HDF5 files. It has wrappers for Java, Python, C#, Fortran, R. Also, it contains a command-line tool to query HDF5 files. | 2023-09-04 |
| [JHDF](https://github.com/jamesmudd/jhdf) | pure Java implementation | A pure Java implementation of the HDF5 file format. Currently, it only supports reading HDF5 files. Also, **the file size is limited to 32-bit integer size** (an array of about 4 billion members) | weekly, last release 2023-05-10 |
