import os
from bilibili_api import Credential

class CredentialManager:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """get_instance returns a singleton instance of Credential."""
        if cls._instance is None:
            cls._instance = Credential(
                sessdata=os.getenv("SESSDATA"),
                bili_jct=os.getenv("BILI_JCT"),
                buvid3=os.getenv("BUVID3"),
                dedeuserid=os.getenv("DEDEUSERID"),
                ac_time_value=os.getenv("AC_TIME_VALUE"),
            )
        return cls._instance
