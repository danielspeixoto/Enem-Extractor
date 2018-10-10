import pdf
import question
from split import split

pdf.crop("/home/daniel/Documents/enem/2017-1.pdf", "data/out.pdf", pages=[17])
print "ENEM borders cut out"
#
split("data/out.pdf", "data", "res/question_pattern.png")
#
# question.answers("data", "res/alternative.png", [1])
