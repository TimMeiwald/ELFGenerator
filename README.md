# ELFGenerator
Generates an ELF file binary using Python. WIP but can be used to directly create binaries that can run on System V OS's and x86-64 architechtures.
Most of the stuff is there to create it for other architechtures and systems. Currently only creates segments.

Currently it only writes segments so there is no debugger information and can only be used for executables not shared relocatable files. 
Currently you also need to manually provide memory alignment and positioning information to the segments since it's not a completed project yet and WIP.

TODO: Add sections.   
TODO: Add automatic memory alignment and positioning etc.    
TODO: Add and test most significant byte order.      
  
