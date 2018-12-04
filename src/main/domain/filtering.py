from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer

def pdf_questions(questions, pdf_input_path, path):
    filtered = []
    excluded = []
    for question in questions:
        if _contain_image(question, pdf_input_path, path):
            excluded.append(question)
        else:
            filtered.append(question)
    return filtered, excluded

def _contain_image(question, input_path, question_path):
    for part in question.parts:
        part.save_as_pdf(input_path, question_path)
        with open(question_path) as pdf_file:
            # Create a PDF document object that stores the document structure.
            document = PDFDocument(PDFParser(pdf_file))

            # Create a PDF resource manager object that stores shared resources.
            resource_manager = PDFResourceManager()

            # Create a PDF page aggregator object.
            device = PDFPageAggregator(resource_manager,
                                       laparams=LAParams())

            # Create a PDF interpreter object.
            interpreter = PDFPageInterpreter(resource_manager,
                                             device)

            # loop over all pages in the document
            for page in PDFPage.create_pages(document):
                # read the page into a layout object
                interpreter.process_page(page)
                layout = device.get_result()
                # check for invalid objects
                if _parse_obj(layout._objs, part.lower, part.upper):
                    return True
    return False

def _parse_obj(lt_objects, lower, upper):
    for obj in lt_objects:
        if _contains(obj.bbox, lower, upper):
            if isinstance(obj, pdfminer.layout.LTImage):
                return True
            if isinstance(obj, pdfminer.layout.LTCurve):
                if obj.width > 50 and 50 < obj.height < 300:
                    return True
            if isinstance(obj, pdfminer.layout.LTContainer) and \
                    not isinstance(obj, pdfminer.layout.LTTextBox):
                if _parse_obj(obj._objs, lower, upper):
                    return True
    return False

def _contains(bbox, lower, upper):
    return \
        lower[0] <= bbox[0] + lower[0] <= upper[0] and \
        lower[0] <= bbox[2] + lower[0] <= upper[0] and \
        lower[1] <= bbox[1] + lower[1] <= upper[1] and \
        lower[1] <= bbox[3] + lower[1] <= upper[1]