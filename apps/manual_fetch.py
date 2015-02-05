import sys

import GP.driver.access as access
import GP.driver.gpinfo
import GP.driver.timeutil as timeutil

import config as lconfig
            
def main(argv):
    """  Main
    """
    if len(argv) < 2:
        print "Fetch GP's daily data.  "
        print "Input: %s [gp index file 1] [gp index file 2] ..." % (argv[0])
        sys.exit(2)

    indexfilelist = []
    for argc in xrange(1, len(argv)):
        indexfile = argv[argc]
        indexfilelist.append(indexfile)
    print "Importing index files: ", indexfilelist

    # Get file prefix
    timezone = timeutil.getTimeZone(lconfig.TimeZone)
    today, timenow = timeutil.getNow(timezone)

    prefix = "%s_%02d-%02d" % (today, timenow.hour, timenow.minute)

    # Fetch data
    for indexfile in indexfilelist:
        # construct the instances to 
        myaccess = access.SinaAccess(indexfile)

        # # parse to get data
        indexes = myaccess.getGIndexes()
        print "%s has %d GPs" % (indexfile.split('.')[0], len(indexes))

        # fetch 
        gpdict = myaccess.fetchAllDataRT()

        # output
        myaccess.writeToFile(gpdict, indexfile, prefix)

    # ENDFOR


if __name__ == "__main__":
    main(sys.argv)

