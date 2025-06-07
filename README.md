# bilibili-mcp
[NOTE]: Currently in development!!!

## Description

A mcp agent which allows LLMs to interact with the Bilibili video website.

## Features


## Installation

### Prerequisites
Make sure ``uv`` is installed correctly.

### Installation
```bash
git clone https://github.com/KitsuneX07/bilibili-mcp.git
cd bilibili-mcp
uv sync
```

## Usage
First, edit the .env file correctly.
```bash
cd /path/to/your/bilibili-mcp
cp .env.example .env
vi .env
# edit the .env file correctly, instructions can be found at https://nemo2011.github.io/bilibili-api/#/get-credential
```


To run the mcp:
```bash
uv run --directory /path/to/your/bilibili-mcp /path/to/your/bilibili-mcp/server.py
```

## Technologies Used
## MCP Tools

This project exposes several functionalities as MCP tools, allowing external systems to interact with Bilibili video features.

### Video Management

*   **`like_video(bvid: Optional[str] = None, aid: Optional[int] = None, like: bool = True)`**: Manages liking or unliking a Bilibili video.
*   **`get_video_info(bvid: Optional[str] = None, aid: Optional[int] = None)`**: Retrieves detailed and basic information for a specified Bilibili video.
*   **`add_to_toview(bvid: Optional[str] = None, aid: Optional[int] = None)`**: Adds a Bilibili video to the user's "Watch Later" list.
*   **`delete_from_toview(bvid: Optional[str] = None, aid: Optional[int] = None)`**: Removes a Bilibili video from the user's "Watch Later" list.
*   **`get_video_download_url(bvid: Optional[str] = None, aid: Optional[int] = None, cid: Optional[int] = None, page_index: Optional[int] = None)`**: Retrieves the download URL for a Bilibili video.


## Contribution Guidelines

Guidelines for how others can contribute to your project.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/YourFeature`).
6.  Open a Pull Request.

## Licensing Information

Information about the license under which your project is distributed.

This project is licensed under the [LICENSE NAME] - see the [LICENSE](LICENSE) file for details.
