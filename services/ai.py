from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import os
import logging
from config import generation_config
from services.video import get_video_id
from services.transrcipt import extract_transcript_details

logging.basicConfig(level=logging.DEBUG)


api_key = os.getenv("GOOGLE_API_KEY")


genai.configure(api_key=api_key)

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

def process_request(youtube_video_url, history):
    video_id = get_video_id(youtube_video_url)
    if not video_id:
        return {"error": "Invalid YouTube URL"}
    transcript_dict = extract_transcript_details(video_id=video_id)

    language, transcript_text = next(iter(transcript_dict.items()))

    initial_prompt = f"""You are an expert BOOK INDEXER tasked with organizing the transcript of a YouTube video. The transcript is in {language} language. Your goal is to arrange the information in a structured, markdown-formatted outline. Follow these strict guidelines and KEEP your response in English:

                        # 1. Use proper markdown syntax for formatting.
                        # 2. Each TOPIC should be a level 2 heading (##) and in bold.
                        # 3. Each SUB-TOPIC should be a level 3 heading (###).
                        # 4. Each Description should be a Bullet points.
                        # 5. [Conclusion] should have all the TOPIC in Ordered List.
                        # 6. Use line breaks appropriately for clear separation of sections.
                        # 7. For one prompt choose one out of [summary_format, quiz_format].

                        summary_format:
                        Structure your response as follows:

                        ## **1. [Main Topic 1 ]**

                         ### 1.1 [Sub-Topic 1.1  :- Description] 

                         ### 1.2 [Sub-Topic 1.2  :- Description]

                         ## **2. [Main Topic 2 ]**

                        ### 2.1 [Sub-Topic 2.1  :- Description]

                        ### 2.2 [Sub-Topic 2.2  :- Description]

                        [Continue this pattern for all main topics and sub-topics covered in the video]
                        
                        # If explicitly requested multiple-choice quiz, follow these strict guidelines:
                        quiz_format:
                        # 1. Each [Question] should be in bold.
                        # 2. Each [Option] should be an Ordered List.
                        # 3. Use line breaks appropriately for clear separation of [Question] and [Option].

                    Transcript:
                    {transcript_text}
                    """


    chat_session = model.start_chat(
        history=history
    )

    response = chat_session.send_message(initial_prompt)
    history.append({"role": "user", "parts": [f"{initial_prompt}"]})
    history.append({"role": "assistant", "parts": [f"{response}"]})

    return response

