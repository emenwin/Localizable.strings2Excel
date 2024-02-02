# -*- coding:utf-8 -*-

from __future__ import print_function
import os
from optparse import OptionParser
from XmlFileUtil import XmlFileUtil
import pyexcelerate
from Log import Log
import time


def addParser():
    parser = OptionParser()

    parser.add_option("-f", "--fileDir",
                      help="strings.xml files directory.",
                      metavar="fileDir")

    parser.add_option("-t", "--targetDir",
                      help="The directory where the xls files will be saved.",
                      metavar="targetDir")

    parser.add_option("-e", "--excelStorageForm",
                      type="string",
                      default="multiple",
                      help="The excel(.xls) file storage forms including single(single file), multiple(multiple files), default is multiple.",
                      metavar="excelStorageForm")

    (options, args) = parser.parse_args()
    Log.info("options: %s, args: %s" % (options, args))

    return options


def convertToMultipleFiles(fileDir, targetDir):
    destDir = genDestDir(targetDir)

    for _, dirnames, _ in os.walk(fileDir):
        valuesDirs = [di for di in dirnames if di.startswith("values")]
        for dirname in valuesDirs:
            workbook = pyexcelerate.Workbook()
            for _, _, filenames in os.walk(fileDir+'/'+dirname):
                xmlFiles = [fi for fi in filenames if fi.endswith(".xml")]
                for xmlfile in xmlFiles:
                    ws = workbook.new_sheet(xmlfile)
                    path = os.path.join(fileDir, dirname+'/' + xmlfile)
                    (keys, values) = XmlFileUtil.getKeysAndValues(path)
                    for keyIndex in range(len(keys)):
                        key = keys[keyIndex]
                        value = values[keyIndex]
                        ws.set_cell_value(keyIndex, 1, key)
                        ws.set_cell_value(keyIndex, 2, value)
            filePath = os.path.join(destDir ,  getCountryCode(dirname) + ".xls")
            workbook.save(filePath)
    print ("Convert %s successfully! you can see xls file in %s" % (
        fileDir, destDir))


def convertToSingleFile(fileDir, targetDir):
    destDir = genDestDir(targetDir)

    for _, dirnames, _ in os.walk(fileDir):
        valuesDirs = [di for di in dirnames if di.startswith("values")]
        for dirname in valuesDirs:
            for _, _, filenames in os.walk(fileDir+'/'+dirname):
                xmlFiles = [fi for fi in filenames if fi.endswith(".xml")]
                for xmlfile in xmlFiles:
                    fileName = xmlfile.replace(".xml", "")
                    filePath = os.path.join(destDir , fileName + ".xls")
                    if not os.path.exists(filePath):
                        workbook = pyexcelerate.Workbook()
                        ws = workbook.new_sheet(fileName)
                        index = 0
                        for dirname in dirnames:
                            if index == 0:
                                ws.set_cell_value(0, 1, 'keyName')
                            countryCode = getCountryCode(dirname)
                            ws.set_cell_value(0, index+2, countryCode)

                            path = os.path.join(fileDir, dirname+'/' + xmlfile)
                            (keys, values) = XmlFileUtil.getKeysAndValues(path)
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
        fileDir, destDir))


def genDestDir(targetDir):
    destDir = targetDir + "/xml-files-to-xls_" + \
        time.strftime("%Y%m%d_%H%M%S")
    if not os.path.exists(destDir):
        os.makedirs(destDir)
    return destDir


def getCountryCode(dirname):
    code = 'en'
    dirSplit = dirname.split('values-')
    if len(dirSplit) > 1:
        code = dirSplit[1]
    return code


def startConvert(options):
    fileDir = options.fileDir
    targetDir = options.targetDir

    print ("Start converting")

    if fileDir is None:
        print ("strings.xml files directory can not be empty! try -h for help.")
        return

    if targetDir is None:
        print ("Target file path can not be empty! try -h for help.")
        return

    if options.excelStorageForm == "single":
        convertToSingleFile(fileDir, targetDir)
    else:
        convertToMultipleFiles(fileDir, targetDir)


def main():
    options = addParser()
    startConvert(options)


main()
