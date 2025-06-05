import os
from bilibili_api import Credential

class CredentialManager:
	_instance = None

	@classmethod
	def get_instance(cls):
		"""get_instance returns a singleton instance of Credential."""
		if cls._instance is None:
			sessdata = os.getenv("SESSDATA")
			bili_jct = os.getenv("BILI_JCT")
			buvid3 = os.getenv("BUVID3")
			dedeuserid = os.getenv("DEDEUSERID")
			ac_time_value = os.getenv("AC_TIME_VALUE")

			if all([sessdata, bili_jct, buvid3, dedeuserid, ac_time_value]):
				cls._instance = Credential(
					sessdata=sessdata, bili_jct=bili_jct, buvid3=buvid3, dedeuserid=dedeuserid, ac_time_value=ac_time_value
				)
			else:
				cls._instance = Credential()
		return cls._instance
