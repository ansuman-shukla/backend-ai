import logging
from youtube_transcript_api import YouTubeTranscriptApi
from services.video import get_video_id

logging.basicConfig(level=logging.DEBUG)


def extract_transcript_details(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try to get English transcript first
        try:
            transcript = transcript_list.find_transcript(['en'])
            transcript_text = " ".join([item["text"] for item in transcript.fetch()])
            return {"en": transcript_text.strip()}
        except:
            # If English is not available, get the first available transcript
            for transcript in transcript_list:
                try:
                    transcript_text = " ".join([item["text"] for item in transcript.fetch()])
                    return {transcript.language_code: transcript_text.strip()}
                except:
                    continue
            logging.debug("No transcript could be fetched for any language")
            raise Exception("No transcript could be fetched for any language")
    except Exception as e:
        logging.debug(f"Extract Transcript Details Function Error: {e}")
        return None 