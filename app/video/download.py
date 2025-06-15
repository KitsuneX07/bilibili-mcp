import asyncio
import os
import tempfile
import aiofiles
from loguru import logger
from pathlib import Path
from tqdm.asyncio import tqdm
from bilibili_api import video, HEADERS, get_client
from app import mcp
from app.utils.credential import CredentialManager
from app.video.video import get_cid_by_part_name


FFMPEG_PATH = os.getenv("FFMPEG_PATH", "ffmpeg")


async def _run_command(command: list[str], description: str):

    logger.info(f"Executing: {description} - {' '.join(command)}")
    process = await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        error_msg = f"Command failed: {description}\nSTDOUT:\n{stdout.decode(errors='ignore')}\nSTDERR:\n{stderr.decode(errors='ignore')}"
        logger.error(error_msg)
        raise RuntimeError(f"Command '{' '.join(command)}' failed with exit code {process.returncode}")
    else:
        logger.info(f"Command completed successfully: {description}")
        # logger.debug(f"STDOUT:\n{stdout.decode(errors='ignore')}")
    return stdout.decode(errors="ignore"), stderr.decode(errors="ignore")


async def _download_chunked(url: str, out_path: Path, intro: str):

    logger.info(f"Starting download: {intro} to {out_path}")
    try:
        dwn_id = await get_client().download_create(url, HEADERS)
        total_bytes = get_client().download_content_length(dwn_id)
        downloaded_bytes = 0

        # Use tqdm.asyncio for an asynchronous progress bar
        with tqdm(total=total_bytes, unit="B", unit_scale=True, desc=f"{intro} - {out_path.name}") as pbar:
            async with aiofiles.open(out_path, "wb") as file:
                while downloaded_bytes < total_bytes:
                    chunk = await get_client().download_chunk(dwn_id)
                    if not chunk:  # Break if no more chunks are received
                        break
                    await file.write(chunk)
                    downloaded_bytes += len(chunk)
                    pbar.update(len(chunk))
        logger.info(f"Download finished: {intro} to {out_path}") 
    except Exception as e:
        logger.error(f"Download failed for {intro}: {e}")
        raise

@mcp.tool()
async def download_video_best_quality(bvid: str, part_name: str = None, out_dir: str = os.getenv("DOWNLOAD_DIR")):
    """Downloads a Bilibili video in the best available quality.

    This function downloads a Bilibili video, or a specific part of a multi-part video,
    to the specified output directory. It automatically detects the best available
    streams (FLV or Dash/MP4) and uses FFmpeg to process and merge them into a
    single MP4 file. Temporary files are managed internally.

    Args:
        bvid (str): The Bilibili video ID (e.g., "BV1xx411c7mR").
        part_name (str, optional): The name of the specific video part to download.
            If None, the first part of the video is downloaded. Defaults to None.
        out_dir (str, optional): The directory where the downloaded video will be saved.
            If the directory does not exist, it will be created. Defaults to the value
            of the "DOWNLOAD_DIR" environment variable.

    Returns:
        Path or None: The pathlib.Path object pointing to the downloaded MP4 file
        if the download is successful, otherwise None.

    Raises:
        RuntimeError: If an external command (e.g., FFmpeg) fails during execution.
        FileNotFoundError: If FFmpeg is not found in the system's PATH or at the
            specified FFMPEG_PATH.
        Exception: For any other unexpected errors that occur during the download process.
    """
    
    output_directory = Path(out_dir)
    output_directory.mkdir(parents=True, exist_ok=True)

    try:
        v = video.Video(bvid=bvid, credential=CredentialManager.get_instance())
        target_cid = None

        if part_name:
            target_cid = await get_cid_by_part_name(bvid, part_name)
            if target_cid is None:
                logger.error(f"Part '{part_name}' not found in video '{bvid}'.")
                return None

        download_url_data = await v.get_download_url(0) if not part_name else await v.get_download_url(cid=target_cid)
        detecter = video.VideoDownloadURLDataDetecter(data=download_url_data)
        streams = detecter.detect_best_streams()
        if not streams:
            logger.error(f"No available streams detected for BVID: {bvid}, Part: {part_name}.")
            return None

        final_filename_base = f"{bvid}_{part_name}" if part_name else bvid
        final_output_path = output_directory / f"{final_filename_base}.mp4"

        with tempfile.TemporaryDirectory() as temp_dir_str:
            temp_dir = Path(temp_dir_str)
            logger.info(f"Temporary files will be stored in: {temp_dir}")
            if detecter.check_flv_mp4_stream():

                logger.info("Detected FLV stream.")
                flv_temp_file = temp_dir / f"{final_filename_base}_temp.flv"
                await _download_chunked(streams[0].url, flv_temp_file, "Downloading FLV Stream")

                ffmpeg_command = [
                    FFMPEG_PATH,
                    "-i", str(flv_temp_file),
                    "-c", "copy",
                    "-loglevel", "error",
                    str(final_output_path)
                ]
                await _run_command(ffmpeg_command, "Converting FLV to MP4")
            else:
                if len(streams) < 2:
                    logger.error(f"Detected MP4 stream but not enough video/audio streams found for BVID: {bvid}, Part: {part_name}.")
                    return None
                
                logger.info("Detected MP4 (Dash) stream.")
                video_temp_file = temp_dir / f"{final_filename_base}_video.m4s"
                audio_temp_file = temp_dir / f"{final_filename_base}_audio.m4s"

                await _download_chunked(streams[0].url, video_temp_file, "Downloading Video Stream")
                await _download_chunked(streams[1].url, audio_temp_file, "Downloading Audio Stream")
                

                ffmpeg_command = [
                    FFMPEG_PATH,
                    "-i", str(video_temp_file),
                    "-i", str(audio_temp_file),
                    "-c:v", "copy",
                    "-c:a", "copy",
                    "-loglevel", "error",
                    str(final_output_path)
                ]
                await _run_command(ffmpeg_command, "Merging Video and Audio Streams")
            logger.success(f"Video '{final_output_path.name}' downloaded successfully to '{final_output_path.parent}'.")
            return final_output_path

    except RuntimeError as e:
        logger.error(f"Command execution error during download for {bvid}: {e}")
    except FileNotFoundError:
        logger.error(f"FFmpeg not found. Please ensure '{FFMPEG_PATH}' is in your PATH or specify its full path.")
    except Exception as e:
        print(f"DEBUG: Type of e: {type(e)}, Value of e: '{e}'")
        logger.error(f"An unexpected error occurred during download for {bvid}: {e}", exc_info=True)

    return None

