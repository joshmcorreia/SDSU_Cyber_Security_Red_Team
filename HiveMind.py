from SQLiteDatabase import SQLiteDatabase
from TargetMachine import TargetMachine
import os
import yaml
from BetterLogger import logger


class SQLiteDatabaseAlreadyExistsException(Exception):
    pass


class HiveMind:
    """
    HiveMind keeps track of all target machines and allows you to mass-control machines
    """

    def __init__(self) -> None:
        self.parsed_config = self.read_config_file()
        self.target_machines: dict[str, TargetMachine] = {}
        self.sqlite_filename: str = self.parsed_config["sqlite_filename"]
        self.initialize_sqlite_database()

    def read_config_file(self):
        config_file_location = "config.yaml"
        logger.debug(f"Reading config file `{config_file_location}`...")
        with open(config_file_location, "r") as file_in:
            parsed_config = yaml.safe_load(file_in)
        logger.debug(f"Successfully read config file `{config_file_location}`.")
        return parsed_config

    def initialize_sqlite_database(self):
        """
        Initializes the local SQLite database used to store IPs and other info
        """
        logger.info(f"Initializing the SQLite database `{self.sqlite_filename}`...")

        if os.path.exists(self.sqlite_filename):
            logger.info(f"The SQLite database `{self.sqlite_filename}` already exists.")
            return

        with SQLiteDatabase(database_file_name=self.sqlite_filename) as database:
            create_IP_table_statement = "CREATE TABLE IP(address TEXT PRIMARY KEY, name TEXT);"
            database.cursor.execute(create_IP_table_statement)
            database.connection.commit()
        logger.info(f"Successfully initialized the SQLite database `{self.sqlite_filename}`.")

    def get_ips_from_database(self):
        with SQLiteDatabase(database_file_name=self.sqlite_filename) as database:
            select_statement = "SELECT address FROM IP"
            sql_arguments = ()
            database.cursor.execute(select_statement, sql_arguments)
            result = database.cursor.fetchall()
            result = [x[0] for x in result]
            return result

    def add_ip_to_database(self, address: str, name: str) -> int:
        with SQLiteDatabase(database_file_name=self.sqlite_filename) as database:
            insert_statement = "INSERT OR IGNORE INTO IP(address, name) VALUES (?, ?)"
            sql_arguments = (
                address,
                name,
            )  # a tuple is expected so we need the trailing comma
            database.cursor.execute(insert_statement, sql_arguments)
            database.connection.commit()
            return database.cursor.lastrowid

    def add_ips_from_roster_to_database(self):
        with open("roster.txt", "r") as file_in:
            for line in file_in:
                line = line.strip()
                if line == "":
                    continue
                ip = line.split(",")[0]
                name = line.split(",")[1]
                self.add_ip_to_database(address=ip, name=name)

    def convert_database_ips_to_target_machines(self):
        ips_from_database = self.get_ips_from_database()
        credentials = self.parsed_config["credentials"]
        self.target_machines = {}  # reset the target machines because we're going to recreate it based on the database ips
        for ip in ips_from_database:
            new_user = TargetMachine(
                ip_address=ip,
                credentials=credentials,
                parsed_config=self.parsed_config,
            )
            self.target_machines[ip] = new_user

    def ping_all_target_machines(self):
        logger.info("Pinging all target machines...")
        for ip, machine in self.target_machines.items():
            try:
                machine.ping()
            except Exception:
                continue
        logger.info("Finished pinging all target machines.")

    def test_all_machines_for_vulnerabilities(self):
        for ip, machine in self.target_machines.items():
            try:
                logger.info(f"===== CHECKING {ip} FOR VULNERABILITIES =====")

                if not machine.ping():  # in the real world you wouldn't be able to rule out that a machine is offline based on a ping, but for the purposes of this lab it is highly unlikely that a student disabled ICMP so we can skip those target machines
                    continue

                machine.test_all_vulnerabilities()
            except Exception:
                continue

    def run_hellevator_on_all_target_machines(self):
        logger.info("***** RUNNING HELLEVATOR ON ALL TARGET MACHINES *****")
        for ip, machine in self.target_machines.items():
            try:
                logger.info(f"===== RUNNING HELLEVATOR ON {ip} =====")

                if not machine.ping():  # in the real world you wouldn't be able to rule out that a machine is offline based on a ping, but for the purposes of this lab it is highly unlikely that a student disabled ICMP so we can skip those target machines
                    continue

                machine.run_hellevator()
            except Exception:
                continue

    def check_for_hellevator_on_all_target_machines(self):
        for ip, machine in self.target_machines.items():
            try:
                logger.info(f"===== CHECKING IF HELLEVATOR RAN ON {ip} =====")

                if not machine.ping():  # in the real world you wouldn't be able to rule out that a machine is offline based on a ping, but for the purposes of this lab it is highly unlikely that a student disabled ICMP so we can skip those target machines
                    continue

                machine.check_for_hellevator()
            except Exception:
                continue

    def install_salt_minion_on_all_target_machines(self):
        for ip, machine in self.target_machines.items():
            try:
                logger.info(f"===== INSTALLING SALT MINION ON {ip} =====")

                if not machine.ping():  # in the real world you wouldn't be able to rule out that a machine is offline based on a ping, but for the purposes of this lab it is highly unlikely that a student disabled ICMP so we can skip those target machines
                    continue

                machine.install_salt_minion()
            except Exception:
                continue
