import sys
import os
import shutil
import zipfile

'''
    Author:         Benny Megidish
    Description:    This program extracts all the drawing, image and 3D design files out of an 123dx file
                    Arguments naming conventions is used like in java (camelCase)
'''

numOfFileExtracted = 0


def extract3d(zipFileDir, destDirectory, outputFileName):
    with zipfile.ZipFile(zipFileDir) as zipFile:
        extract3dRecursively(zipFile.namelist(), zipFile, destDirectory, outputFileName)


def extract3dRecursively(fileList, baseZipFile, destDirectory, outputFileName, numOfFileExtracted=0):
    imageExtList = ['.jpg', '.png']
    fusionExtList = ['.smt', '.smb', '.sat', '.igs', '.dxf', '.stp', '.stl']

    for member in fileList:
        if os.path.isdir(member):
            # traverse zip
            extract3dRecursively(os.listdir(member), baseZipFile, destDirectory, outputFileName)
        else:
            fileExt = os.path.splitext(member)[1]
            fileName = os.path.splitext(os.path.basename(member))[0]

            # extract only drawing images and 3D files
            if fileExt in (fusionExtList + imageExtList):
                fullFileName = ''.join([outputFileName, "_", fileName, fileExt])

                # find unique file name
                while os.path.exists(os.path.join(destDirectory, fullFileName)):
                    fileName += "#"
                    fullFileName = ''.join([outputFileName, "_", fileName, fileExt])

                # copy file (taken from zipfile's extract)
                source = baseZipFile.open(member)
                target = open(os.path.join(destDirectory, fullFileName), "wb") # was file() / test for exceptions
                with source, target:
                    shutil.copyfileobj(source, target)
                    numOfFileExtracted += 1


def execute(srcDirectory, destDirectory, filename):
    outputFileName = os.path.splitext(os.path.basename(filename))[0]
    newFileName = outputFileName + '.zip'
    oldFilePath = os.path.join(srcDirectory, filename)
    newFilePath = os.path.join(srcDirectory, newFileName)

    # covert to zip
    os.rename(oldFilePath, newFilePath)

    # extract files
    print('Extracting %s' % oldFilePath)
    extract3d(newFilePath, destDirectory, outputFileName)

    # covert back to 123dx
    os.rename(newFilePath, oldFilePath)

    # delete zip
    # os.remove(newFilePath)


def main(filepath=None):
    args = sys.argv
    usage = 'USAGE: %s [123D FILE PATH OR DIRECTORY]' % args[0]
    directory = os.path.dirname(os.path.realpath(__file__))

    if len(args) == 2:
        directory = os.path.dirname(args[1])
    elif filepath:
        directory = os.path.dirname(filepath)
    else:
        print(usage)
        print('Using current directory..')

    extractDirectory = os.path.join(directory, '3DFiles')

    if os.path.isdir(directory) or args[1].endswith(".123dx"):
        # create output dir if needed
        if not os.path.exists(extractDirectory):
            os.makedirs(extractDirectory)
    else:
        print(usage)
        exit(-1)

    if args[1].endswith(".123dx"):
        if os.path.exists(args[1]):
            execute(directory, extractDirectory, args[1])
        else:
            print('%s does not exist' % args[1])
    elif os.path.isdir(directory):
        # rename files to zip
        for filename in os.listdir(directory):
            if filename.endswith(".123dx"):
                execute(directory, extractDirectory, filename)


if __name__ == '__main__':
    main()
