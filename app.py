import os
import logging
from db import db
from image import *
from openai import OpenAI
from emotion import emotion
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
LOGGER = logging.getLogger("")
dbconn = db()


def getCompletion(messages, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model, messages=messages, temperature=0.9
    )
    return response.choices[0].message.content


def readyGPT(emotion, diary):
    messages = [
        {
            "role": "system",
            "content": "너는 사람들의 감정을 듣고, 그 감정에 대한 분석과 해결책을 제공하는 챗봇이야. 모든 입출력은 한국어로 이루어져야 해. 입력은 현재의 감정과 일기가 주어질 거야.",
        },
        {"role": "user", "content": f"감정: {emotion} 일기: {diary}"},
    ]

    return getCompletion(messages)


@app.route("/api/emotion", methods=["POST"])
def getEmotion():
    data = request.get_json()
    face = base64ToImage(data["face"])
    emotionInfo = emotion.getPrediction(face)
    LOGGER.info(emotionInfo)

    return jsonify({"emotion": emotionInfo[0]["label"]})


@app.route("/api/get/diaries", methods=["POST"])
def getDiary():
    data = request.get_json()
    LOGGER.info(data)

    try:
        user = data["user"]
    except:
        return jsonify({"diaries": []})

    diaries = dbconn.getAll(user)

    return jsonify({"diaries": diaries})


@app.route("/api/save/diary", methods=["POST"])
def saveDiary():
    data = request.get_json()
    LOGGER.info(data)

    user = data.get("user", 0)
    date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    emotion = data["emotion"]
    diary = data["diary"]
    # solution = readyGPT(emotion, diary)
    solution = "솔루션!"

    id = dbconn.insert(user, date, emotion, diary, solution)

    return jsonify({"id": id, "solution": solution})


@app.route("/api/save/image", methods=["POST"])
def saveImage():
    data = request.get_json()
    LOGGER.info(data)

    id = data["id"]
    image = data["image"]

    dbconn.updateImage(id, image)

    return jsonify({"id": id})


if __name__ == "__main__":
    # print(readyGPT("난 오늘 앱잼이라는 해커톤에 참여했는데, 너무 힘들었지만, 최우수상이라는 큰 상을 타게 되어서 매우 기뻐."))
    app.run(host="0.0.0.0", port=3000)
