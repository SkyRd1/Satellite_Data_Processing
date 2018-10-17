#Author: Sepehr Roudini.
#University of Iowa.
#Department of Chemical Engineering.
#Date: 01/08/2018.
#Purpose: Reading VIIRS hdf5 file and printing out useful
#information.


#--------------------------------------------------------------------------------------------#
#Defining function and import necessary libraries
#--------------------------------------------------------------------------------------------#

##############################################################################################
#Libraries used in this function are: h5py.
##############################################################################################
#Path_To_File: full path to file with
#file name in it.
##############################################################################################
#Attributes: either 'True or 'False, if 'True'
#File_Attributes will be printed out, default is
#'True'.
##############################################################################################
#This function prints out the groups and datasets
#in the hdf5 file and also returns "File" which
#has the hdf5 file information in it.
##############################################################################################
def Read_HDF5(Path_To_File, Attributes='True'):
#This library is for reading hdf5 files
    import h5py
    import sys
#--------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------------------#
#Reading the data and printing them out
#--------------------------------------------------------------------------------------------#
#Reading the hdf5 file
    File_Name =Path_To_File
    File = h5py.File(File_Name, mode='r')
    if Attributes=='True':
        try:
            print('\x1b[6;30;42m' + 'File attributes are:' + '\x1b[0m' + '\n')
            Count = 1
            for i in File.attrs:
                print(str(Count) + ')' + i + ':', File.attrs[i])
                Count += 1
            print ('\n{:=<150}'.format(''))
            print ('{:=<150}'.format(''))
        except:
            pass
    try:
        print('\x1b[6;30;42m' + 'Groups/Datasets included in the file are as follow:'+ '\x1b[0m' + '\n')
        Count = 1
        for i in File:
            print(str(Count) + ')' + i)
            Count += 1
        print('\n{:=<150}'.format(''))
        print('{:=<150}'.format(''))
    except:
        pass
    try:
        for i in File:
            group1 = File[str(i)]
            print('\x1b[6;30;42m' + 'Groups/Datasets included in ' + str(i) + ':'+ '\x1b[0m' + '\n')
            Count = 1
            for i in group1:
               print(str(Count) + ')' + i)
               Count += 1
        print('\n{:=<150}'.format(''))
        print('{:=<150}'.format(''))
    except:
        pass
    try:
        for i in File:
            group1 = File[str(i)]
            for i in group1:
               subgroup1 = group1[str(i)]
               print('\x1b[6;30;42m' + 'Groups/Datasets included in ' + str(i) + ':' + '\x1b[0m' + '\n')
               count = 1
               for i in subgroup1:
                   print(str(Count) + ')' + i)
                   Count += 1
            print('\n{:=<150}'.format(''))
            print('{:=<150}'.format(''))
    except:
        pass
    return File