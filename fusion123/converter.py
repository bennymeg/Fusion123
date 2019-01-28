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


def _extract3d(zipFileDir, destDirectory, outputFileName):
    ''' a wrapper function for the recursive file extraction function '''

    with zipfile.ZipFile(zipFileDir) as zipFile:
        _extract3dRecursively(zipFile.namelist(), zipFile, destDirectory, outputFileName)


def _extract3dRecursively(fileList, baseZipFile, destDirectory, outputFileName, numOfFileExtracted=0):
    ''' extracts all the illustations and models from the 123dx file recursively '''

    imageExtList = ['.jpg', '.png']
    fusionExtList = ['.smt', '.smb', '.sat', '.igs', '.dxf', '.stp', '.stl']

    for member in fileList:
        if os.path.isdir(member):
            # traverse zip
            _extract3dRecursively(os.listdir(member), baseZipFile, destDirectory, outputFileName)
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


def _execute(srcDirectory, destDirectory, filename):
    ''' converts the file into fusion 360 file (this file might be usable in other CAD software as well) '''

    outputFileName = os.path.splitext(os.path.basename(filename))[0]
    newFileName = outputFileName + '.zip'
    oldFilePath = os.path.join(srcDirectory, filename)
    newFilePath = os.path.join(srcDirectory, newFileName)

    # covert to zip
    os.rename(oldFilePath, newFilePath)

    # extract files
    print('Extracting %s' % oldFilePath)
    _extract3d(newFilePath, destDirectory, outputFileName)

    # covert back to 123dx
    os.rename(newFilePath, oldFilePath)

    # delete zip
    # os.remove(newFilePath)


def convert(filepath=None):
    args = sys.argv
    usage = 'USAGE: %s [123D FILE PATH OR DIRECTORY]' % args[0]
    directory = os.path.dirname(os.path.realpath(__file__))
    succeeded = False

    # define working directory and file path
    if filepath:
        directory = os.path.dirname(filepath)
    elif len(args) == 2:
        directory = os.path.dirname(args[1])
        filepath = args[1]
    else:
        print(usage)
        print('Using current directory..')

    extractDirectory = os.path.join(directory, '3DFiles')

    # ensure all the variables defined correctly
    if os.path.isdir(directory) or (filepath and filepath.endswith(".123dx")):
        # create output dir if needed
        if not os.path.exists(extractDirectory):
            os.makedirs(extractDirectory)
    else:
        print(usage)
        # exit(-1)        # incase we are running as a script, exit it
        return False

    # start the convertion process
    if filepath and filepath.endswith(".123dx"):
        # single file
        if os.path.exists(filepath):
            _execute(directory, extractDirectory, filepath)
            succeeded = True
        else:
            print('Failed, %s does not exist' % filepath)
    elif os.path.isdir(directory):
        # directory
        for filename in os.listdir(directory):
            if filename.endswith(".123dx"):
                _execute(directory, extractDirectory, filename)
                succeeded = True

        if not succeeded:
            print('Failed, could not found *.123dx file in %s' % directory)

    if succeeded:
        print('Succeeded, you can find you model files inside the 3DFiles folder')

    return succeeded
    

if __name__ == '__main__':
    convert()
