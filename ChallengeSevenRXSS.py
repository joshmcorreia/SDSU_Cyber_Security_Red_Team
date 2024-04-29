import requests
import BetterLogger
from BetterLogger import logger
from Exploit import Exploit, UnsupportedException


class ChallengeSevenRXSS(Exploit):
    def __init__(self, ip_address, parsed_config) -> None:
        super().__init__(ip_address=ip_address, parsed_config=parsed_config)

    def run_command(self, command):
        raise UnsupportedException("Running commands with ChallengeSevenRXSS is not supported.")

    def run_hellevator(self):
        raise UnsupportedException("Running Hellevator with ChallengeSevenRXSS is not supported.")

    def test_if_vulnerable(self):
        try:
            logger.info(f"{self.ip_address} - Testing if the target is vulnerable to ChallengeSevenRXSS...")
            quote = "<script>alert();</script>"
            server_response = requests.get(f"http://{self.ip_address}/xss/xss.php?quote={quote}", timeout=3)
            server_response_text = server_response.text
            # logger.debug(f"Response: {server_response_text}")
            if quote in server_response_text:
                logger.info(f"{BetterLogger.COLOR_GREEN}{self.ip_address} - The target is vulnerable to ChallengeSevenRXSS!{BetterLogger.COLOR_END}")
                return True
            else:
                # check that it stills works correctly
                quote = "Do or do not, there is no try"
                server_response = requests.get(f"http://{self.ip_address}/xss/xss.php?quote={quote}", timeout=3)
                server_response_text = server_response.text
                # logger.debug(f"Response: {server_response_text}")
                if quote not in server_response_text:
                    logger.info(
                        f"{BetterLogger.COLOR_PINK}{self.ip_address} - The student incorrectly patched ChallengeSevenRXSS so providing a quote no longer works correctly!{BetterLogger.COLOR_END}"
                    )
                    return None

                logger.info(f"{BetterLogger.COLOR_YELLOW}{self.ip_address} - The target is not vulnerable to ChallengeSevenRXSS.{BetterLogger.COLOR_END}")
                return False
        except requests.ConnectionError:
            logger.info(f"{BetterLogger.COLOR_PINK}{self.ip_address} - Unable to test ChallengeSevenRXSS because the student disabled the apache2 service!{BetterLogger.COLOR_END}")
            return None
        except Exception as err:
            logger.info(f"{BetterLogger.COLOR_RED}{self.ip_address} - Something went wrong while checking if ChallengeSevenRXSS is vulnerable.{BetterLogger.COLOR_END}")
            logger.exception(err)
            return False
