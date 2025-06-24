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

Use in json format:
```json
"mcpServers": {
  "bilibili-mcp": {
    "command": "uv",
    "args": [
        "run",
        "--directory",
        "/path/to/your/bilibili-mcp",
        "/path/to/your/bilibili-mcp/server.py"
      ]
  }
}
```

## Technologies Used
## MCP Tools

This project exposes several functionalities as MCP tools, allowing external systems to interact with Bilibili video features.

### Video Management

*   **`get_video_comments(bvid: str, page_index: int = 1, time_order: bool = False)`**: Retrieves comments for a given Bilibili video.
*   **`send_comment(bvid: str, message: str)`**: Sends a comment to a specified Bilibili video.
*   **`download_video_best_quality(bvid: str, part_name: Optional[str] = None, out_dir: str = os.getenv("DOWNLOAD_DIR", "downloads"))`**: Downloads a Bilibili video in the best available quality.
*   **`get_hot_videos(num_videos: int = 10)`**: Retrieves a list of hot videos from Bilibili.
*   **`search_video(keyword: str, num_results: int = 10, descending: bool = True, order_type: search.OrderVideo = search.OrderVideo.TOTALRANK)`**: Searches for videos on Bilibili based on a keyword.
*   **`get_video_info(bvid: str)`**: Retrieves detailed information about a Bilibili video.
*   **`pay_video_coin(bvid: str, num: int = 1, like: bool = False)`**: Pays coins to a Bilibili video.
*   **`triple_video(bvid: str)`**: Performs a "triple" action (like, coin, favorite) on a Bilibili video.
*   **`add_video_to_toview(bvid: str)`**: Adds a Bilibili video to the "Watch Later" list.
*   **`delete_video_from_toview(bvid: str)`**: Deletes a Bilibili video from the "Watch Later" list.
*   **`like_video(bvid: str, like: bool = True)`**: Likes or unlikes a Bilibili video.

### Favorite List Management

*   **`create_video_favorite_list(title: str, introduction: str = "", private: bool = True)`**: Creates a new video favorite list.
*   **`delete_video_favorite_list(favorite_list_name: str)`**: Deletes a video favorite list by its name.
*   **`set_video_favorite(bvid: str, favorite_list_name: str)`**: Adds a video to a specified favorite list.
*   **`unset_video_favorite(bvid: str, favorite_list_name: str)`**: Removes a video from a specified favorite list.


## Contribution Guidelines

Guidelines for how others can contribute to this project.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/YourFeature`).
6.  Open a Pull Request.

## Licensing Information

Information about the license under which your project is distributed.

This project is licensed under the [LICENSE NAME] - see the [LICENSE](LICENSE) file for details.
