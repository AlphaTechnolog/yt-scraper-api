from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.channels.service import YoutubeService

router = APIRouter()


@router.get("/channel-videos/{channel_id}")
def get_channel_videos(channel_id: str):
    service = YoutubeService()
    videos = service.get_channel_videos(channel_id)
    return JSONResponse(content={'videos': videos}, status_code=200)


@router.get('/channel-videos/hashes/{channel_id}')
def get_channel_videos_hashes(channel_id: str):
    service = YoutubeService()
    videos = service.get_channel_videos(channel_id)
    hashes = [service.get_video_hash(video) for video in videos]
    return JSONResponse(content={'hashes': hashes}, status_code=200)


@router.get('/search/{query}')
def search(query: str, skip_shorts: bool = False):
    service = YoutubeService()
    videos = service.search(query, skip_shorts)
    return JSONResponse(content={'videos': videos}, status_code=200)


@router.get('/video-details/{video_hash}')
def get_video_details(video_hash: str):
    service = YoutubeService()
    details = service.get_video_details(video_hash=video_hash)
    return JSONResponse(content={'details': details}, status_code=200)
