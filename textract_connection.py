import boto3
from collections import Counter
import logger_handler
from Instagram_handler import OCR_instagram
import re

class Textract_setup:

    def __init__(self):
        """
            initialize input path of csv file
        """
        self.textract_client = boto3.client('textract')
        self.local_img_path = "Data/test2.jpg"
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

    def social_media_handler(self, social_media_name, check_followers_list, extracted_text):
        """
           Social Media handler
           input : extracted_text, social_media_name & followers_list for checking
           Output : Followers present or not Present
        """

        try:
            switcher = {
                "instagram": ocr_insta_obj.instagram_handler(check_followers_list, extracted_text),
                #     "facebook": ,
                #     "twitter": ,
                #     "linkedin": ,
            }
            switcher.get(social_media_name, "Incorrect Input")

        except Exception as e:
            logger.exception("Something went Wrong {}".format(e))

if __name__ == "__main__":
    try:
        textract_obj = Textract_setup()
        logger = logger_handler.set_logger()
        ocr_insta_obj = OCR_instagram()
        extracted_lines = ""
        social_media_name = "instagram"
        check_followers_list = ['bridgelabz', 'codermacha', 'confident_coder']

        choice = int(input(" 1. local Input \n 2. S3 Bucket \n"))
        if choice == 1:
            bytes_img = textract_obj.locally_read_img_bytes()
            extracted_lines = textract_obj.extract_text(bytes_img)
        if choice == 2:
            extracted_lines = textract_obj.s3_read_img_extract_text()

        textract_obj.social_media_handler(social_media_name, check_followers_list, extracted_lines)

        logger.info('Extracted text got Successfully..!')

    except Exception as e:
        logger.exception("Something went Wrong in main controller {}".format(e))