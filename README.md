# GhostBuild

----

GhostBuild is a (POC) collection of simple MSBuild launchers for various [GhostPack](https://github.com/GhostPack) projects (authored by [@harmj0y](https://twitter.com/harmj0y)).  Other .Net project launchers may be included later.

As with other GhostPack projects, GhostBuild is licensed under the BSD 3-Clause license.

## Instructions

*These launchers include compiled/compressed/encoded versions of GhostPack utilities.  However,  you should inspect and compile your own versions.*

1) Compile the target GhostPack project with the desired .NET Framework version.
2) Compress the .NET assembly with [Out-CompressedDll](https://github.com/PowerShellMafia/PowerSploit/blob/master/ScriptModification/Out-CompressedDll.ps1).
3) Update and customize the GhostBuild XML CSharp (C#) project file -
- Ensure the AssemblyFile represents the correct framework and path.
- Assign GhostPack .Net assembly arguments to the args variable if required.  This is a string array, so quote arguments and separate by commas (e.g. "arg1" , "arg2").
- Copy the compressed .Net assembly from the Out-CompressedDll operation and assign it to the compressedBin variable.
- Copy the byte length/size of the compressed .Net assembly from the Out-CompressedDll operation and assign it to the compressedBinSize variable.
4) Build and run with the proper version of MSBuild.exe.
- Example: C:\Windows\Microsoft.Net\Framework64\v4.0.30319\MSBuild.exe c:\path\to\project.xml
  
## Ethics

GhostBuild is designed to help security professionals perform ethical and legal security assessments and penetration tests. Do not use for nefarious purposes.

## Credits

- [@harmj0y](https://twitter.com/harmj0y) -  security researcher and primary author of GhostPack 
- [@mattifestation](https://twitter.com/mattifestation) - security researcher and author of the [Out-CompressedDll](https://github.com/PowerShellMafia/PowerSploit/blob/master/ScriptModification/Out-CompressedDll.ps1) utility
- [@subTee](https://twitter.com/subTee) - MSBuild (.Net) wizard and security researcher
- [@gentilkiwi](https://twitter.com/gentilkiwi) - [Mimikatz](https://github.com/gentilkiwi/mimikatz) author and security researcher
