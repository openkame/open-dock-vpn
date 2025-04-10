from enum import Enum
from typing import Union

class ConfigPath:
    def __init__(self, enum_type, path: tuple[str, ...]):
        self.enum = enum_type  # GlobalConfig ou ClientConfig
        self.path = path

    def __iter__(self):
        return iter(self.path)

    def __repr__(self):
        return f"ConfigPath({self.enum}, {self.path})"

    def __eq__(self, other):
        return isinstance(other, ConfigPath) and self.enum == other.enum and self.path == other.path
    
def cfgp(enum_class: type):
    def wrapper(*parts: str) -> "ConfigPath":
        return ConfigPath(enum_class, parts)
    return wrapper


class GlobalConfig(Enum):
    GlobalPath = cfgp("GlobalConfig")
    
    LANGUAGE = GlobalPath("language")

    THEME_NAME = GlobalPath("theme", "name")
    THEME_MODE = GlobalPath("theme", "mode")

    PROFILES = GlobalPath("profiles")
    
    PROFILE = GlobalPath("profiles", "{profile_id}")
    PROFILE_ERROR = GlobalPath("profiles", "{profile_id}", "error")

    CLIENTS = GlobalPath("clients")

    CLIENT = GlobalPath("clients", "{client_id}")
    CLIENT_USER = GlobalPath("clients", "{client_id}", "user")
    CLIENT_VPN = GlobalPath("clients", "{client_id}", "vpn")
    CLIENT_DOMAIN = GlobalPath("clients", "{client_id}", "domain")
    CLIENT_FAVORITE = GlobalPath("clients", "{client_id}", "favorite")
    CLIENT_ERROR = GlobalPath("clients", "{client_id}", "error")

    def __call__(self, **kwargs) -> Union["GlobalConfig", ConfigPath]:
        if kwargs:
            return ConfigPath(type(self), tuple(part.format(**kwargs) for part in self.value))
        return self
    

class ClientConfig(Enum):
    ClientPath = cfgp("ClientConfig")
    PROFILE = ClientPath("profile")
    AUTOSTART = ClientPath("autostart")

    def __call__(self, **kwargs) -> Union["ClientConfig", ConfigPath]:
        if kwargs:
            return ConfigPath(type(self), tuple(part.format(**kwargs) for part in self.value))
        return self