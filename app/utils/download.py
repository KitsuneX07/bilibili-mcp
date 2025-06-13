import httpx
import json
import os
from typing import List, Dict, Optional, Union
from loguru import logger

RPC_URL = f"http://localhost:{os.getenv('RPC_PORT', '6800')}/jsonrpc"
SECRET_TOKEN = os.getenv("RPC_SECRET_TOKEN")


async def add_aria2_uri(
	uri: str,
	*,
	dir: Optional[str] = None,
	out: Optional[str] = None,
	referer: Optional[str] = "https://bilibili.com",
	user_agent: Optional[str] = "Mozilla/5.0",
	custom_headers: Optional[Union[List[str], Dict[str, str]]] = None,
	**kwargs,
):
	"""
	Adds a URI to Aria2 for download.

	This function constructs an Aria2 RPC request to add a new download task
	with various optional parameters such as download directory, output filename,
	and custom headers.

	Args:
	    uri (str): The URI of the file to download.
	    dir (Optional[str]): The directory where the file should be saved.
	    out (Optional[str]): The output filename.
	    referer (Optional[str]): The Referer header for the download request.
	    user_agent (Optional[str]): The User-Agent header for the download request.
	    custom_headers (Optional[Union[List[str], Dict[str, str]]]):
	        Additional custom headers. Can be a list of "Key: Value" strings
	        or a dictionary of key-value pairs.
	    **kwargs: Arbitrary keyword arguments that will be passed as Aria2 options.
	              Keys will be converted from snake_case to kebab-case.

	Returns:
	    Optional[str]: The GID (Global ID) of the added download task if successful,
	                   otherwise None.
	"""
	aria2_options: Dict[str, str] = {}

	if dir:
		aria2_options["dir"] = dir
	if out:
		aria2_options["out"] = out

	headers_list: List[str] = []
	# Add Referer header if provided
	if referer:
		headers_list.append(f"Referer: {referer}")
	# Add User-Agent header if provided
	if user_agent:
		headers_list.append(f"User-Agent: {user_agent}")

	# Process custom headers
	if custom_headers:
		if isinstance(custom_headers, list):
			# If custom_headers is a list, extend the headers_list directly
			headers_list.extend(custom_headers)
		elif isinstance(custom_headers, dict):
			# If custom_headers is a dictionary, format and add each key-value pair
			for key, value in custom_headers.items():
				headers_list.append(f"{key}: {value}")
		else:
			logger.warning("Warning: custom_headers should be a list of strings or a dictionary. Ignoring.")

	# Add compiled headers to Aria2 options if any headers are present
	if headers_list:
		aria2_options["header"] = headers_list

	# Process additional keyword arguments as Aria2 options
	for key, value in kwargs.items():
		# Convert snake_case keys to kebab-case for Aria2
		aria2_key = key.replace("_", "-")
		aria2_options[aria2_key] = str(value)

	params = []
	if SECRET_TOKEN:
		params.append(f"token:{SECRET_TOKEN}")

	params.append([uri])

	if aria2_options:
		params.append(aria2_options)

	payload = {
		"jsonrpc": "2.0",  # JSON-RPC protocol version
		"method": "aria2.addUri",  # Aria2 RPC method to call
		"id": "add_uri_async_task",  # Unique ID for the request
		"params": params,  # Parameters for the method call
	}

	logger.info(f"Sending payload (async): {json.dumps(payload, indent=2)}")

	try:
		async with httpx.AsyncClient() as client:
			response = await client.post(RPC_URL, json=payload)
			response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

			result = response.json()
			logger.info(f"Aria2 RPC Response (async): {json.dumps(result, indent=2)}")

			if "result" in result:
				logger.info(f"Task successfully added. GID: {result['result']}")
				return result["result"]
			elif "error" in result:
				logger.error(f"Error adding task: {result['error']['message']} (Code: {result['error']['code']})")
				return None
	except httpx.HTTPStatusError as e:
		# Handle HTTP status errors (e.g., 404, 500)
		logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
		return None
	except httpx.RequestError as e:
		# Handle request errors (e.g., network issues)
		logger.error(f"An error occurred while requesting: {e}")
		return None
	except Exception as e:
		# Handle any other unexpected errors
		logger.error(f"An unexpected error occurred: {e}")
		return None
