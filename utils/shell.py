from subprocess import Popen
import os.path
import re


# Execute ocropy to the desired pdf
# filePath : full path to the target pdf to be converted to textString
# Returns the name of the file containing the textString if it is ready or None if is being processed
def call_main(filePath):
    tokens = re.match(r'((?P<filePath>([^\.])+)/)*(?P<fileName>[^\.\s/]+)\.pdf', filePath)
    file_name = tokens.group('fileName')
    path = tokens.group('filePath')

    if path is None:
        exists = os.path.isfile(file_name) 
        path = " "
    else:
        exists = os.path.isfile(path+"/"+file_name+".html") 

    # We are not going to recalculate file
    if exists:
        return path+"/"+file_name+".html"
    
    Process=Popen('utils/run_ocropy.sh \"%s\" \"%s\"' % (str(file_name),str(path),), shell=True)

    return None