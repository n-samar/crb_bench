#!/usr/bin/python -u
# Return a pretty-printed short git version (like hg/svnversion)
from __future__ import print_function
import os
def cmd(c): return os.popen(c).read().rstrip()
#branch = cmd("git rev-parse --abbrev-ref HEAD")
revnum = cmd("git log | grep ^commit | wc -l")
rshort = cmd("git rev-parse --short HEAD")
dfstat = cmd("git diff HEAD --shortstat")
shstat = dfstat.replace(" files changed", "fc").replace(" file changed", "fc") \
               .replace(" insertions(+)", "+").replace(" insertion(+)", "+") \
               .replace(" deletions(-)", "-").replace(" deletion(-)", "-") \
               .replace(",", "")
diff = "clean" if len(dfstat) == 0 else shstat.lstrip()
print("{} : {} : {}".format(revnum, rshort, diff))
