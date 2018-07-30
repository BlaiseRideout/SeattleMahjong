#!/usr/bin/env python3

__doc__ = """Rotate the public directory to preserve past updates made with
hugo."""

import os, glob, sys, argparse

prefix = 'public'
def history_number(publicdir):
   return int(publicdir[len(prefix)+1:])

if __name__ == '__main__':      
   parser = argparse.ArgumentParser(
      description=__doc__,
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument(
      '-p', '--prefix', default=prefix,
      help='Name of public directory (prefix of historical directories)')
   parser.add_argument(
      '-m', '--max-history-number', type=int, default=20,
      help='Max number of historical directories to keep')
   parser.add_argument(
      '-v', '--verbose', action='count', default=0,
      help='Add verbose comments')
   args = parser.parse_args()

   prefix = args.prefix

   past_public_dirs = glob.glob('{}.[0-9]*'.format(prefix))

   past_public_dirs.sort(key=history_number)
   if not os.path.isdir(prefix):
      print('{} is not a directory.  Exiting.'.format(prefix))
      sys.exit(-1)

   for dir_index in range(min(args.max_history_number,
                              len(past_public_dirs) - 1),
                          -1, -1):
      pubdir = past_public_dirs[dir_index]
      hist_number = history_number(pubdir)
      next = '{}.{}'.format(prefix, hist_number + 1)
      if args.verbose > 0:
         print("mv {} {}".format(pubdir, next))
      os.replace(pubdir, next)
   next = '{}.0'.format(prefix)
   if args.verbose > 0:
      print("mv {} {}".format(prefix, next))
   os.replace(prefix, next)
