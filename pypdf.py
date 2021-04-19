from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from pathlib import Path
from sys import argv
from pdf2image import convert_from_path

## Instructions:
## python pdfHelper '<PATH1>,<PATH2>?' [m|r|d|s|sw] [pageNo|'<DESTINATION_PATH>'] [pageNo|degrees?] 
##
## Convert to Image 
## python pdfHelper '<PATH>' img '<DESTINATION_DIR>'
##
##
## Argument 1: PDF Document/s
## - If using multiple files separate them by comma
## - Multiple files only work if m is selected
##
## Argument 2: Command
## - m = Merge (position-based)
## - ma = Merge (append)
## - r = Rotate
## - d = Delete
## - s = split
## - sw = swap
##
## Argument 3: PageNo or Destination
## - PageNo
## - Required for R, D, S, SW
##
## - Destination 
## - Required for merges (m & ma)
##
## Argument 3: PageNo OR Degrees
## - PageNo
## - For sw, r & ma
##

### METHODS ###
def getReader(path):
    return PdfFileReader(path, strict=False)

def validPaths(paths):
    ## Check whether or not each value is a valid PDF 
    paths = paths.split(",")

    if (len(paths) < 2):
        raise Exception("Command requires at least two PDFs!")

    for path in paths:

        path = Path(path)

        # Check if its a file
        if not path.is_file():
            raise Exception(f"{path} is not a file!")

        # Check extension
        if not path.suffix[1:] == 'pdf':
            raise Exception(f"{path} is not a PDF file!")

    return True

def validPath(path):
    path = Path(path)

    # Check if its a file
    if not path.is_file():
        raise Exception(f"{path} is not a file!")

    # Check extension
    if not path.suffix[1:] == 'pdf':
        raise Exception(f"{path} is not a PDF file!")

    return True

def isDirectory(path):
    path = Path(path)

    if not path.exists():
        raise Exception(f"Destination {path} does not exist!")

    if not path.is_dir():
        raise Exception(f"Destination {path} is not a directory!")

    return True

def validAngle(angle):
    #Angle need to be divisible by 90
    return int(angle) % 90 == 0

def validDestination(destination):
    path = Path(destination)

    ##Destination may or may not exist
    if not path.is_file():
        #Likely doesnt exist, check suffix
        if not path.suffix[1:] == 'pdf':
            raise Exception("Destination is not a pdf!")

    ## If exists, check if pdf only
    else: 
        if not path.suffix[1:] == 'pdf':
            raise Exception("Destination is not a pdf!")

    return True

def generateNewName(path, newName):
    
    index = path.rindex('\\')

    ## Get all including last \
    basePath = path[:index + 1]

    return basePath + newName + ".pdf"


def hasValidArgs():

    if len(argv) < 2:
        print("Requires minimum of two arguments.")
        print(len(argv))
        exit(1)

    #Get command
    command = argv[1]

    if command == 'm':
        #Requires , separated path, a destination path and len of 5 (5 is page no)
        return len(argv) == 5 and validPaths(argv[2]) and validDestination(argv[3])

    elif command == 'ma':
        #Requires , separated path, a destination path and len of 4
        return len(argv) == 4 and validPaths(argv[2]) and validDestination(argv[3])

    elif command == 'r':
        #Requires non , separated path, len of 5 
        return len(argv) == 5 and validPath(argv[2]) and validAngle(argv[4])

    elif command == 'd' or command == 's':
        # Requires valid len 4, valid path, and page number (requires reader)
        return len(argv) == 4 and validPath(argv[2])

    elif command == 'sw':
        # Requries length of 5, non separated
        return len(argv) == 5 and validPath(argv[2])

    elif command == 'img':
        #needs to validate output destination ## TODO REQUIRES OUTPUT FIELD

        return len(argv) == 4 and validPath(argv[2]) and isDirectory(argv[3])

    else:
        print(f"Unknown command: {command}")
        return False

def pageExists(reader, pageNo):

    try:
        exists = reader.getPage(pageNo)

        return True

    except IndexError:
        print(f"Page {pageNo} does not exist!")
        return False

### MAIN ###
if hasValidArgs():

    ## MERGE ##
    command = argv[1]

    if command == 'm':
        merger = PdfFileMerger(strict=False)

        paths = argv[2].split(',')

        ##Merge at position can only take two documents
        if len(paths) > 2:
            raise Exception("Merge at position. Can only take two documents.")
        
        destination = argv[3]

        pageNo = int(argv[4])

        if pageExists(getReader(paths[0]), pageNo):

            merger.append(paths[0])

            merger.merge(pageNo, paths[1])

            with open(destination, 'wb') as output:
                merger.write(output)

            print(f"{len(paths)} files merged to {destination}.")

    elif command == 'ma':
        merger = PdfFileMerger(strict=False)

        paths = argv[2].split(',')

        destination = argv[3]

        for path in paths:
             merger.append(path)

        with open(destination, 'wb') as output:
             merger.write(output)

        print(f"{len(paths)} files merged to {destination}.")

    ## ROTATE ##
    elif command == 'r':
        writer = PdfFileWriter()

        ## Check if page exists
        path = argv[2]

        reader = getReader(path)

        pageNo = int(argv[3])

        if pageExists(reader, pageNo):

            ## Convert secondary arg to int
            degrees = int(argv[4])

            for i in range(reader.numPages):

                page = reader.getPage(i)

                if i == pageNo:
                    page.rotateClockwise(degrees)
                
                writer.addPage(page)
            
            with open(path, 'wb') as output:
                writer.write(output)
                print(f"Page {pageNo} successfully rotated {degrees} degrees!")


    ## DELETE ##
    elif command == 'd':
        writer = PdfFileWriter()

        path = argv[2]

        reader = getReader(path)

        pageNo = int(argv[3])

        if pageExists(reader, pageNo):

            for i in range(reader.numPages):

                if i == pageNo:
                    continue

                page = reader.getPage(i)
                
                writer.addPage(page)
            
            with open(path, 'wb') as output:
                writer.write(output)
                print(f"Page {pageNo} successfully removed!")
    
    ## SPLIT ##
    elif command == 's':

        writer = PdfFileWriter()

        path = argv[2]

        reader = getReader(path)

        pageNo = int(argv[3])

        ##Check if page exists
        if pageExists(reader, pageNo):

            split1 = generateNewName(path, "Split 1")
            split2 = generateNewName(path, "Split 2")

            if pageNo == 0:
                pageNo = 1; #Split at 1 and zero are basically the same thing

            for i in range(pageNo):

                page = reader.getPage(i)
                
                writer.addPage(page)

            with open(split1, 'wb') as output:
                writer.write(output)

            # Write remainder pageNo ++
            altWriter = PdfFileWriter()

            for i in range(pageNo, reader.numPages):

                page = reader.getPage(i)
                
                altWriter.addPage(page)

            with open(split2, 'wb') as output:
                altWriter.write(output)

            print("Successfully split document into two!")


    ## SWAP ##
    elif command == 'sw':

        path = argv[2]

        pageNo = int(argv[3])

        altPageNo = int(argv[4])

        reader = getReader(path)

        writer = PdfFileWriter()

        ## If both pages exist
        if pageExists(reader, pageNo) and pageExists(reader, altPageNo):

            #Write its inverse
            for i in range(reader.numPages):

                page = None

                if i == pageNo:
                    page = reader.getPage(altPageNo)

                elif i == altPageNo:
                    page = reader.getPage(pageNo)

                else:
                    page = reader.getPage(i)

                writer.addPage(page)

            with open(path, 'wb') as output:
                writer.write(output)

            print(f"Successfully swapped pages {pageNo} and {altPageNo}.")

    ## PDF -> IMG ##
    elif command == 'img':
        pages = convert_from_path(argv[2], 500, poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
        
        destination = argv[3]

        for i, page in enumerate(pages):
            page.save(destination + "\\" + str(i+1) + ".jpg", 'JPEG')

        print(f"Successfully exported {len(pages)} images!")

else: 
    print("Failed to perform operation.")





