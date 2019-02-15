from data.model import configuration
from presentation import split_questions
from presentation.export import format_save

print("Started")
config = configuration.Environment()

questions, has_error = split_questions.start(config)

print("Saving questions as PDF")
format_save(config)







