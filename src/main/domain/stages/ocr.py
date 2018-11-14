# -*- coding: utf-8 -*-
import json
import re

from google.cloud import storage
from google.cloud import vision
from google.protobuf import json_format


def async_detect_document(gcs_source_uri, gcs_destination_uri):
    """OCR with PDF/TIFF as source files on GCS"""
    # Supported mime_types are: 'application/pdf' and 'image/tiff'
    mime_type = 'application/pdf'

    # How many pages should be grouped into each json output file.
    batch_size = 2

    client = vision.ImageAnnotatorClient()

    feature = vision.types.Feature(
        type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)

    gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
    input_config = vision.types.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.types.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.types.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size)

    async_request = vision.types.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)

    operation = client.async_batch_annotate_files(
        requests=[async_request])

    print('Waiting for the operation to finish.')
    operation.result(timeout=180)

def view(gcs_destination_uri):
    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.
    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name=bucket_name)

    # List objects with the given prefix.
    blob_list = list(bucket.list_blobs(prefix=prefix))
    print('Output files:')
    for blob in blob_list:
        print(blob.name)

    # Process the first output file from GCS.
    # Since we specified batch_size=2, the first response contains
    # the first two pages of the input file.
    output = blob_list[0]

    json_string = output.download_as_string()
    response = json_format.Parse(
        json_string, vision.types.AnnotateFileResponse())

    # The actual response for the first page of the input file.
    first_page_response = response.responses[0]
    annotation = first_page_response.full_text_annotation

    return annotation

def print_text(annotation):

    # Here we print the full text from the first page.
    # The response contains more information:
    # annotation/pages/blocks/paragraphs/words/symbols
    # including confidence scores and bounding boxes
    print(u'Full text:\n{}'.format(
        annotation.text))

def print_format(annotation):
    output = ""
    for page in annotation["pages"]:
        for block_index in range(len(page["blocks"])):
            block = page["blocks"][block_index]
            for paragraph in block["paragraphs"]:
                for word in paragraph["words"]:
                    ye = word["boundingBox"]["normalizedVertices"][1]["x"] > 0.042 and word["boundingBox"]["normalizedVertices"][1]["x"] < 0.047 and word["boundingBox"]["normalizedVertices"][0]["y"] > 0.7

                    for symbol in word["symbols"]:
                        output += symbol["text"]
                        if ye:
                            print(symbol["text"])
                        if "detectedBreak" in symbol["property"] :
                            if symbol["property"]["detectedBreak"]["type"] == "SPACE":
                                output += " "
                            else:
                                output += "\n"
                # output += "\n"
            output += "\n"
        # output += "\n"
    res = ""
    for i in range(len(output)):
        c = output[i]
        if c != "\n":
            res += c
        # print(i, end='')
        elif i + 1 < len(output) and re.match("[A-Z©]|\n", output[i+1]):
            res += "\n"
        else:
            res += " "


    options = ["A", "B", "C", "D", "E"]
    original = res
    start_list = [0]
    while True:
        for i in range(5):
            start = start_list[len(start_list) - 1]
            res = res[0:start] + re.sub("\n[" + options[i] + "©] ", "\n|*| ", res[start:], count=1)
            for i in range(start, len(res)):
                if res[i] == "|":
                    start_list.append(i + 4)
                    break
        aaa = res[start_list[len(start_list) - 1]:]
        if re.search("[A-Z©]", aaa):
            start_list = [start_list[1]]
            res = original
        else:
            break
    print(res)


dest = "gs://enempdf/parsed/"

# async_detect_document("gs://enempdf/1.pdf",
#                       "gs://enempdf/parsed/")

# json = view(dest)

with open('/home/daniel/Downloads/data.json') as j:
    print_format(json.load(j)["responses"][0]["fullTextAnnotation"])
