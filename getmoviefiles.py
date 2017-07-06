import os
import sys

def main():
    link = 'https://s3-eu-west-1.amazonaws.com/dataanalysis53/DataAnalysisFiles.zip'
    dir = sys.argv[1]
    basename = "DataAnalysisFiles.zip"
    os.system('wget %s -O %s' % (link, os.path.join(dir, basename)))
    os.system("unzip -q -o %s -d %s" % (os.path.join(dir, basename), dir))

if __name__ == "__main__":
    main()