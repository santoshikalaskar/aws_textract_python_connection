import logger_handler
import re

class OCR_instagram:
    def __init__(self):
        """
            initialize loggers
        """
        self.logger = logger_handler.set_logger()

    def get_acc_holder_name_text(self, extracted_lines):
        """
            get Account holder name in text format
        """
        try:
            account_holder_name = extracted_lines.split("Followers")[0]
            regex = re.compile('\w+')
            result = regex.findall(account_holder_name)
            account_holder_name = max(result, key=len)
            return account_holder_name

        except Exception as e:
            self.logger.exception("Something went Wrong while getting Account Holder Name {}".format(e))

    def check_followers(self, followers_list, extracted_text):
        """
            Check list of followers present or not from result list
        """
        try:
            result_list = []
            extracted_text_lower = extracted_text.lower()
            followers_list = [x.lower() for x in followers_list]
            for check_list_item in followers_list:
                if check_list_item in extracted_text_lower:
                    result_list.append(True)
                else:
                    result_list.append(False)
            return result_list
        except Exception as e:
            self.logger.exception("Something went Wrong while Checking list of followers present or not from result list {}".format(e))

    def instagram_handler(self, check_followers_list, extracted_text):
        """
           Instagram OCR
           input : img_path, social_media_name & followers_list for checking
           Output : Followers present or not Present
        """
        try:
            acc_holder_name = self.get_acc_holder_name_text(extracted_text)
            print("Account Holder Name : ", acc_holder_name)

            result = self.check_followers(check_followers_list, extracted_text)
            if all(bool(x) == True for x in result):
                print("\n ******************\n All Followers Present \n ******************\n")
            else:
                print("\n ******************\n Followers not Present : ", result, "\n ******************\n")
        except Exception as e:
            self.logger.exception("Something went Wrong in instagram handler {}".format(e))