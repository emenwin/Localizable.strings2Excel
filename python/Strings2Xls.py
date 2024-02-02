# -*- coding:utf-8 -*-

from __future__ import print_function
import os
from optparse import OptionParser
from StringsFileUtil import StringsFileUtil
import pyexcelerate
import time

# Add command option


def addParser():
    parser = OptionParser()

    parser.add_option("-f", "--stringsDir",
                      help=".strings files directory.",
                      metavar="stringsDir")

    parser.add_option("-t", "--targetDir",
                      help="The directory where the excel(.xls) files will be saved.",
                      metavar="targetDir")

    parser.add_option("-e", "--excelStorageForm",
                      type="string",
                      default="multiple",
                      help="The excel(.xls) file storage forms including single(single file), multiple(multiple files), default is multiple.",
                      metavar="excelStorageForm")

    (options, _) = parser.parse_args()

    return options

#  convert .strings files to single xls file


def convertToSingleFile(stringsDir, targetDir):
    destDir = targetDir + "/strings-files-to-xls_" + \
        time.strftime("%Y%m%d_%H%M%S")
    if not os.path.exists(destDir):
        os.makedirs(destDir)

    # Create xls sheet
    for _, dirnames, _ in os.walk(stringsDir):
        lprojDirs = [di for di in dirnames if di.endswith(".lproj")]
        for dirname in lprojDirs:
            for _, _, filenames in os.walk(stringsDir+'/'+dirname):
                stringsFiles = [
                    fi for fi in filenames if fi.endswith(".strings")]
                for stringfile in stringsFiles:
                    fileName = stringfile.replace(".strings", "")
                    filePath = os.path.join(destDir  , fileName + ".xls")
                    if not os.path.exists(filePath):
                        workbook = pyexcelerate.Workbook()
                        ws = workbook.new_sheet(fileName)
                        index = 0
                        for dirname in dirnames:
                            if index == 0:
                                ws.set_cell_value(0, 1, 'keyName')
                            countryCode = dirname.replace(".lproj", "")
                            ws.set_cell_value(0, index+2, countryCode)

                            path = os.path.join(stringsDir, dirname + '/' + stringfile)
                            (keys, values) = StringsFileUtil.getKeysAndValues(
                                path)
                            for x in range(len(keys)):
                                key = keys[x]
                                value = values[x]
                                if (index == 0):
                                    ws.set_cell_value(x+1, 1, key)
                                    ws.set_cell_value(x+1, 2, value)
                                else:
                                    ws.set_cell_value(x+1, index + 2, value)
                            index += 1
                        workbook.save(filePath)
    print ("Convert %s successfully! you can see xls file in %s" % (
        stringsDir, destDir))


#  convert .strings files to multiple xls files


def convertToMultipleFiles(stringsDir, targetDir):
    destDir = targetDir + "/strings-files-to-xls_" + \
        time.strftime("%Y%m%d_%H%M%S")
    if not os.path.exists(destDir):
        os.makedirs(destDir)

    for _, dirnames, _ in os.walk(stringsDir):
        lprojDirs = [di for di in dirnames if di.endswith(".lproj")]
        for dirname in lprojDirs:
            workbook = pyexcelerate.Workbook()
            for _, _, filenames in os.walk(stringsDir+'/'+dirname):
                stringsFiles = [
                    fi for fi in filenames if fi.endswith(".strings")]
                for stringfile in stringsFiles:
                    ws = workbook.new_sheet(stringfile)

                    path = os.path.join(stringsDir, dirname+'/' + stringfile)
                    (keys, values) = StringsFileUtil.getKeysAndValues(
                        path)
                    for keyIndex in range(len(keys)):
                        key = keys[keyIndex]
                        value = values[keyIndex]
                        ws.set_cell_value(keyIndex, 1, key)
                        ws.set_cell_value(keyIndex, 2, value)

            filePath = os.path.join(destDir , dirname.replace(".lproj", "") + ".xls")
            workbook.save(filePath)

    print ("Convert %s successfully! you can see xls file in %s" % (
        stringsDir, destDir))

# Start convert .strings files to xls


def startConvert(options):
    stringsDir = options.stringsDir
    targetDir = options.targetDir

    print ("Start converting")

    if stringsDir is None:
        print (".strings files directory can not be empty! try -h for help.")
        return

    if targetDir is None:
        print ("Target file directory can not be empty! try -h for help.")
        return

    if options.excelStorageForm == "single":
        convertToSingleFile(stringsDir, targetDir)
    else:
        convertToMultipleFiles(stringsDir, targetDir)


def main():
    options = addParser()
    startConvert(options)


main()
