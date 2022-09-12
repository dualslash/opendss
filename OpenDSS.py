from dss import DSS as dss_engine

import argparse
import pathlib
import click
import json
import sys
import os


parser = argparse.ArgumentParser(description='OpenDSS Python Interface')
parser.add_argument('input', help='input file path (.DSS)')
parser.add_argument('output', nargs='*', help='output file path, optional (.json)')
args = parser.parse_args()

inExt = ['.DSS']
outExt = ['.json']
inPath = None
outPath = None


# Process input path
inPath = args.input
if not os.path.exists(args.input):
    print("ERROR: no such file '{}'".format(args.input), file=sys.stderr)
    sys.exit()

inType = pathlib.Path(inPath).suffix
if inType not in inExt:
    print("ERROR: not a valid input file type '{}'".format(args.inType), file=sys.stdout)
    sys.exit()

# Process output path
if args.output:
    outPath = args.output[0]
    outType = pathlib.Path(outPath).suffix
    
    if outType not in outExt:
        print("ERROR: not a valid output file type '{}'".format(args.outType), file=sys.stdout)
        sys.exit()
    
    if os.path.exists(outPath):
        print("WARNING: file already exists '{}'".format(args.input), file=sys.stderr)
        if click.confirm('Overwrite existing file?', default=True):
            outPath = outPath
        else:
            outPath = None

# Run OpenDSS Simulation
dss_engine.Text.Command = f"compile '{inPath}'"
dss_engine.ActiveCircuit.Solution.Solve()

#dss.solution_solve()
outDict = {"busses":{},"lines":{}}

# Log results to terminal
print('Phase voltage magnitudes for each bus:')
for i in range(len(dss_engine.ActiveCircuit.AllBusVmag)):
    if outPath:
        outDict["busses"][dss_engine.ActiveCircuit.AllNodeNames[i]] = {"voltage":{"magnitude":round(dss_engine.ActiveCircuit.AllBusVmag[i],2)}}
    print('Bus', dss_engine.ActiveCircuit.AllNodeNames[i], round(dss_engine.ActiveCircuit.AllBusVmag[i],2), 'V')


print('Phase current magnitudes and angles for each line:')
for l in range(dss_engine.ActiveCircuit.Lines.Count):
    dss_engine.ActiveCircuit.SetActiveElement('Line.line{0}'.format(l + 1))
    
    for i in range(1,4):
        if outPath:
            outDict["lines"][str(l+1)+"."+str(i)] = {"current":{"magnitude":round(dss_engine.ActiveCircuit.ActiveCktElement.CurrentsMagAng[(i-1)*2],2),
                                                     "angle":round(dss_engine.ActiveCircuit.ActiveCktElement.CurrentsMagAng[(i-1)*2+1],2)}}
        print('Line {0}.{1}'.format(l+1,i), round(dss_engine.ActiveCircuit.ActiveCktElement.CurrentsMagAng[(i-1)*2],2), 'A /_',
              round(dss_engine.ActiveCircuit.ActiveCktElement.CurrentsMagAng[(i-1)*2+1],2))

# Write results to output file
if outPath:
    try:
        f = open(outPath, 'w')
    except OSError:
        print("Could not write-lock file:" + str(outPath))
        sys.exit()

    with f:
        buffer = json.dumps(outDict, indent=4)
        f.write(buffer)
        print("Output written to: " + str(outPath))
