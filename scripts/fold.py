import sys

w = int(sys.argv[2])
out = open(sys.argv[3], "a")
line = sys.argv[1].rstrip()
start=0
# get the length of long line
line_length = len(line)
# loop through the long line using the desired line
# width
while line_length - start >= w:
        out.write(line[start:start+w]+"\n")
        start += w
# The rest of the line that does not completely
# use a line of length w
if len(line[start:]) > 0: 
 out.write(line[start:]+"\n")
