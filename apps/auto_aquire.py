#!/usr/bin/python
################################################################################
#
# Alarm clock
#
################################################################################
import sys
import datetime
import time

import GP.driver.gpinfo as gio
import GP.driver.access as gpa
import GP.driver.Alarm

import config as lconfig

# import access
# import Alarm
# from access.fetch_daily import *




def doAlarm(indexfilelist, time1, timenow):
    """
    """
    diffhour = timenow.hour - time1.hour
    diffmin = timenow.minute - time1.minute
    diffsecond = diffhour * 60 + diffmin

    wbuf = "\tBeep.... for alarm @ %s.  Due by %d minutes \n" % (str(time1), diffsecond)
    
    today = datetime.date.today()
    prefix = str(today)+"_"+str(timenow.hour)+"_"+str(timenow.minute)
    print prefix

    # Fetch data
    for indexfile in indexfilelist:
        # parse to get data
        indexes = parseIndexFromFile(indexfile)
        print "%s has %d GPs" % (indexfile.split('.')[0], len(indexes))

        # fetch 
        gpdict = gpa.fetchGPsByIndexes(indexes)

        # output
        writeToFile(gpdict, indexfile, prefix)

    # ENDFOR

    return wbuf


def autoFetch(alarms, indexfiles, statusPassed, statusAlarmed, mytimezone):
    """ 
    """

    ticking = True
    while ticking is True:
        timenow = Alarm.getNow(mytimezone)
        info = ""
        for ia in xrange(len(alarms)):
            if statusPassed[ia] is True and statusAlarmed[ia] is False:
                info += doAlarm(indexfiles, alarms[ia], timenow)
                statusAlarmed[ia] = True
            elif statusPassed[ia] is False and alarms[ia] <= timenow:
                info += doAlarm(indexfiles, alarms[ia], timenow)
                statusPassed[ia] = True
                statusAlarmed[ia] = True
        # ENDFOR

        # Output
        if info != "":
            print "@ Time = %s\n%s" % (str(timenow), info)
        
        time.sleep(SLEEPTIME)
    # ENDWHILE

    return

def main(argv):
    """ Set up daily alarm
    """
    # Process inputs
    if len(argv) == 0:
        print "Something wrong!"
        exit(2)
    elif len(argv) == 1:
        print "Input: %s [Index File 1 (.txt)] [Index File 2] ... [HH:MM 1] [HH:MM 2] ... " % (argv[0])
        exit(2)

    alarms = []
    indexfiles = []
    for argc in xrange(1, len(argv)):
        arg = argv[argc]
        if arg.count(":") == 1:
            # alarm
            timestr = argv[argc]
            terms = timestr.split(":")
            hour = int(terms[0])
            minute = int(terms[1])
            alarm = datetime.time(hour, minute)
            alarms.append(alarm)
        elif arg.endswith(".txt"):
            indexfiles.append(arg)
        else:
            print "Argument %s is not supported. " % (arg)
    # ENDFOR
    
    if len(alarms) == 0 or len(indexfiles) == 0:
        print "There must be at least one alarm and one index file."
        exit(2)

    # Set up
    mytimezone = Alarm.getTimeZone(TIMEZONE)

    isANewDay = True 
    
    statusPassed = []
    statusAlarmed = []
    for ia in xrange(len(alarms)):
        statusPassed.append(None)
        statusAlarmed.append(False)

    # Set up init status of all alarms
    Alarm.checkInitialAlarmStatus(mytimezone, alarms, statusPassed)

    for i in xrange(len(alarms)):
        print "Alarm @ %s is due ??? %s" % (str(alarms[i]), statusPassed[i])


    # Run into alarm
    autoFetch(alarms, indexfiles, statusPassed, statusAlarmed, mytimezone)

    return


if __name__ == "__main__":
    main(sys.argv)
