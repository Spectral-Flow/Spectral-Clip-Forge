"""
Video Processing Tasks
The heart of the forge - where media is transformed into legendary artifacts
"""
from celery_worker import celery
from app import app, db
from models import Job
import ffmpeg
import os
import logging
from datetime import datetime
from utils.file_utils import ensure_directory

logger = logging.getLogger(__name__)

# Platform specifications for social media formats
PLATFORM_SPECS = {
    "tiktok": {
        "resolution": "720x1280",
        "aspect_ratio": "9:16",
        "video_codec": "libx264",
        "audio_codec": "aac",
        "video_bitrate": "2500k",
        "audio_bitrate": "128k",
        "fps": 30,
        "format": "mp4",
    },
    "shorts": {
        "resolution": "1080x1920",
        "aspect_ratio": "9:16",
        "video_codec": "libx264",
        "audio_codec": "aac",
        "video_bitrate": "3500k",
        "audio_bitrate": "192k",
        "fps": 30,
        "format": "mp4",
    },
    "reels": {
        "resolution": "1080x1920",
        "aspect_ratio": "9:16",
        "video_codec": "libx264",
        "audio_codec": "aac",
        "video_bitrate": "3500k",
        "audio_bitrate": "192k",
        "fps": 30,
        "format": "mp4",
    },
    "square": {
        "resolution": "1080x1080",
        "aspect_ratio": "1:1",
        "video_codec": "libx264",
        "audio_codec": "aac",
        "video_bitrate": "3000k",
        "audio_bitrate": "192k",
        "fps": 30,
        "format": "mp4",
    },
}


@celery.task(bind=True)
def process_video(self, job_id, input_path):
    """
    Process video/audio file and generate clips for multiple platforms

    Args:
        job_id: Unique job identifier
        input_path: Path to input media file
    """
    logger.info(f"Starting processing for job {job_id}")

    # Get job from database
    with app.app_context():
        job = Job.query.get(job_id)

        if not job:
            logger.error(f"Job {job_id} not found")
            return

        try:
            # Update job status
            job.status = "processing"
            job.started_at = datetime.utcnow()
            db.session.commit()

            # Create output directory
            output_dir = os.path.join(app.config["OUTPUT_FOLDER"], job_id)
            ensure_directory(output_dir)

            # Get job configuration
            target_formats = job.get_target_formats()
            options = job.get_options()

            output_files = []

            # Check if input is video or audio
            probe = ffmpeg.probe(input_path)
            has_video = any(stream["codec_type"] == "video" for stream in probe["streams"])

            # Process for each target format
            for platform in target_formats:
                if platform not in PLATFORM_SPECS:
                    logger.warning(f"Unknown platform: {platform}")
                    continue

                spec = PLATFORM_SPECS[platform]
                output_filename = f"{job.filename.rsplit('.', 1)[0]}_{platform}.{spec['format']}"
                output_path = os.path.join(output_dir, output_filename)

                try:
                    if has_video:
                        # Process video
                        success = process_video_clip(input_path, output_path, spec, options)
                    else:
                        # Process audio - create visualizer video
                        success = process_audio_to_video(input_path, output_path, spec, options)

                    if success:
                        output_files.append(output_filename)
                        logger.info(f"Generated {platform} clip: {output_filename}")

                except Exception as e:
                    logger.error(f"Error processing {platform} clip: {str(e)}", exc_info=True)
                    continue

            # Update job with results
            if output_files:
                job.status = "completed"
                job.set_output_files(output_files)
                job.completed_at = datetime.utcnow()
                job.processing_time = (job.completed_at - job.started_at).total_seconds()
                logger.info(f"Job {job_id} completed successfully")
            else:
                job.status = "failed"
                job.error_message = "No output files generated"
                logger.error(f"Job {job_id} failed: no output files")

            db.session.commit()

        except Exception as e:
            logger.error(f"Job {job_id} failed: {str(e)}", exc_info=True)
            job.status = "failed"
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()
            db.session.commit()


def process_video_clip(input_path, output_path, spec, options):
    """
    Process a video clip with specified specs

    Args:
        input_path: Input video path
        output_path: Output video path
        spec: Platform specifications
        options: Processing options (watermark, effects, etc.)

    Returns:
        bool: Success status
    """
    try:
        # Get input video info
        probe = ffmpeg.probe(input_path)
        video_stream = next(
            (stream for stream in probe["streams"] if stream["codec_type"] == "video"), None
        )

        if not video_stream:
            return False

        # Build FFmpeg filter chain
        filters = []

        # Scale and crop to target aspect ratio
        width, height = map(int, spec["resolution"].split("x"))
        filters.append(f"scale={width}:{height}:force_original_aspect_ratio=increase")
        filters.append(f"crop={width}:{height}")

        # Add Spectral Flow watermark if enabled
        if options.get("watermark", True):
            watermark_path = os.getenv("WATERMARK_PATH", "static/images/spectral_watermark.png")
            if os.path.exists(watermark_path):
                opacity = float(os.getenv("WATERMARK_OPACITY", "0.7"))
                # Position watermark in bottom-right corner
                filters.append(f"[0:v]overlay=W-w-10:H-h-10:format=auto,format=yuv420p[v]")

        # Apply effects if requested
        if options.get("effects") == "spectral":
            # Add purple/neon color grading
            filters.append("curves=r='0/0 0.5/0.58 1/1':g='0/0 0.5/0.48 1/1':b='0/0.1 0.5/0.7 1/1'")
        elif options.get("effects") == "tribal":
            # Add high contrast, vibrant colors
            filters.append("eq=contrast=1.2:saturation=1.3")

        # Build FFmpeg command
        stream = ffmpeg.input(input_path)

        if filters:
            filter_str = ",".join(filters)
            stream = ffmpeg.filter(stream, "filter_complex", filter_str)

        stream = ffmpeg.output(
            stream,
            output_path,
            vcodec=spec["video_codec"],
            acodec=spec["audio_codec"],
            video_bitrate=spec["video_bitrate"],
            audio_bitrate=spec["audio_bitrate"],
            r=spec["fps"],
            format=spec["format"],
            **{"preset": "medium", "crf": "23"},
        )

        ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)

        return True

    except Exception as e:
        logger.error(f"Video processing error: {str(e)}", exc_info=True)
        return False


def process_audio_to_video(input_path, output_path, spec, options):
    """
    Convert audio to video with visualizer

    Args:
        input_path: Input audio path
        output_path: Output video path
        spec: Platform specifications
        options: Processing options

    Returns:
        bool: Success status
    """
    try:
        width, height = map(int, spec["resolution"].split("x"))

        # Create visualizer using showwaves or showcqt
        if options.get("caption_style") == "neon":
            # Neon waveform
            visualizer = f"showwaves=s={width}x{height}:mode=cline:rate={spec['fps']}:colors=0x9D4EDD|0x7B2CBF"
        else:
            # Spectral analyzer
            visualizer = f"showcqt=s={width}x{height}:fps={spec['fps']}:sono_h=0:bar_h={height}"

        # Build command
        stream = ffmpeg.input(input_path)
        stream = ffmpeg.filter(stream, "filter_complex", visualizer)

        # Add watermark if enabled
        if options.get("watermark", True):
            watermark_path = os.getenv("WATERMARK_PATH", "static/images/spectral_watermark.png")
            if os.path.exists(watermark_path):
                # Overlay watermark
                pass  # Would need more complex filter chain

        stream = ffmpeg.output(
            stream,
            output_path,
            vcodec=spec["video_codec"],
            acodec=spec["audio_codec"],
            video_bitrate=spec["video_bitrate"],
            audio_bitrate=spec["audio_bitrate"],
            r=spec["fps"],
            format=spec["format"],
            **{"preset": "medium"},
        )

        ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)

        return True

    except Exception as e:
        logger.error(f"Audio visualization error: {str(e)}", exc_info=True)
        return False
