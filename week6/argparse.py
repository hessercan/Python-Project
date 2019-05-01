import argparse

def main():
  parser = argparse.ArgumentParser(description='This is a test program')
  parser.add_argument(dest='input', help='specify an input file')
  parser.add_argument('--output', '-o', dest='output', help='specify an output file', default='out.txt')
  parser.add_argument('--verbose', '-v', dest='verbose', help='If specified, print extra information', action='store_true')

  args = parser.parse_args()

  print("Input File:  %s" % args.input)
  print("Output File:  %s" % args.output)
  print("Verbose:  %s" % args.verbose)

main()
quit()
