from web import app
import json
import os


def default():

    return {
        "registration_enabled": True,
        "log_file": "logs.json",
    }


def check(obj):

    df = default()

    for key in df.keys():
        if key not in obj:
            obj[key] = df[key]

    return obj


def get():

    if not os.path.isfile(app.config["CONFIGURATION_FILE"]):
        return default()

    file_content = ""
    with open(app.config["CONFIGURATION_FILE"], "r") as f:
        file_content = f.read()

    try:
        jobject = json.loads(file_content)
        return check(jobject)
    except Exception as e:
        print(f"exception while getting config: {e}")

    return default()


def set(obj):

    jstring = json.dumps(obj)

    with open(app.config["CONFIGURATION_FILE"], "w") as f:
        f.write(jstring)
