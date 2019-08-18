import pandas as pd
import yaml
import argparse
import glob
import subprocess
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import storage
from pydub import AudioSegment


with open("conf.yaml", "r") as f:
    CONF = yaml.safe_load(f)

parser = argparse.ArgumentParser(description=CONF["app-name"])
parser.add_argument("-e", "--env", required=True,
    help="define env: either prod or dev")
ARGS = parser.parse_args()

with open("conf.yaml", "r") as f:
    CONF = yaml.safe_load(f)


class RadioNLP(object):
    def __init__(self):
        self.args = ARGS
        self.env = ARGS.env
        self.service_account = CONF[ARGS.env]["service-account"]
        self.store_path = CONF[ARGS.env]["store-path"]

    def auth(self):
        if self.env == "dev":
            subprocess.run("set GOOGLE_APPLICATION_CREDENTIALS={service_account}" \
                .format(service_account=self.service_account), shell=True)

    def get_files_to_process(self, params={}):
        self.files_to_process = ["a", "b", "z"]
        client = storage.Client()
        print(client.__dict__)

    @staticmethod
    def partition_mp3_into_wav_slices(mp3_file):

        sound = AudioSegment.from_mp3(mp3_file)

        step = 20000
        stop = 120000
        slices = range(0,stop, step)
        slices = zip(slices, [s + step for s in slices])

        wav_list = []

        for s in slices:
            wav_file = mp3_file[:-4]+"{s0}_{s1}.wav"
            wav_file = wav_file.format(s0=s[0], s1=s[1])
            sound_slice = sound[s[0]:s[1]]
            sound_slice.export(wav_file, format="wav")
            wav_list.append(wav_file)

        return wav_list

rnlp = RadioNLP()
rnlp.auth()
print(rnlp.env)
print(rnlp.service_account)
print(rnlp.store_path)
rnlp.get_files_to_process()
print(rnlp.files_to_process)
