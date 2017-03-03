from subprocess import Popen
from pathlib import Path
import re


# Execute ocropy to the desired pdf
# filePath : full path to the folder containing the target pdf to be converted to textString
# fileName : name the target pdf to be converted to textString. Without the extension
# Returns the name of the file containing the textString if it is ready or None if is being processed
def call_main(filePath, fileName):

    if filePath is None:
        exists = Path(fileName+".html").is_file() 
        filePath = " "
    else:
        exists = Path(filePath+"/"+fileName+".html").is_file()

    # We are not going to recalculate file
    if exists:
        return filePath+"/"+fileName+".html"
    
    Process=Popen('utils/run_ocropy.sh \"%s\" \"%s\"' % (str(fileName),str(filePath),), shell=True)

    return None