class UserIP:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.got_root = False

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.ip_address})"
