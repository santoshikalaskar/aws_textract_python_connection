import boto3
from collections import Counter
import logger_handler

class Textract_setup:

    def __init__(self):
        """
            initialize input path of csv file
        """
        self.textract_client = boto3.client('textract')
        self.local_img_path = "Data/test.jpg"
        self.s3_bucket_path = "imgtextracttestingbucket"
        self.s3_bucket_img_path = "test.jpg"

    def locally_read_img_bytes(self):
        "Use img stored in local path"
        with open(self.local_img_path, 'rb') as raw_image:
            img_temp = raw_image.read()
            bytes_img = bytearray(img_temp)
            return bytes_img

    def s3_read_img_extract_text(self):
        """ Use Image stored in s3 bucket """
        extracted_lines = ""
        response = self.textract_client.detect_document_text(Document={
            'S3Object' : {
                "Bucket" : self.s3_bucket_path,
                "Name" : self.s3_bucket_img_path
            }
        })

        blocks = response["Blocks"]
        all_lines = [line for line in blocks if line["BlockType"] == "LINE"]
        for line in all_lines:
            extracted_lines = extracted_lines + line["Text"] + "\n"
        return extracted_lines

    def extract_text(self, bytes_img):
        extracted_lines = ""
        response = self.textract_client.detect_document_text(Document={'Bytes': bytes_img})
        blocks = response["Blocks"]
        all_lines = [line for line in blocks if line["BlockType"] == "LINE"]
        for line in all_lines:
            extracted_lines = extracted_lines + line["Text"]+ "\n"
        return extracted_lines

if __name__ == "__main__":
    try:
        textract_obj = Textract_setup()
        logger = logger_handler.set_logger()
        extracted_lines = ""
        choice = int(input(" 1. local Input \n 2. S3 Bucket \n"))
        if choice == 1:
            bytes_img = textract_obj.locally_read_img_bytes()
            extracted_lines = textract_obj.extract_text(bytes_img)
        if choice == 2:
            extracted_lines = textract_obj.s3_read_img_extract_text()
        print(extracted_lines,"------------------")
        logger.info('Extracted text got Successfully..!')

    except Exception as e:
        logger.exception("Something went Wrong in main controller {}".format(e))