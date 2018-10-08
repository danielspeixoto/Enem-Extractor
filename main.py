import pdf
from split import split

pdf.crop("/home/daniel/Documents/enem/2017-1.pdf", "data/out.pdf", (311, 730), (59, 60), pages=[3])
print "ENEM borders cut out"

split("data/out.pdf", "data", "res/question_pattern.png")
