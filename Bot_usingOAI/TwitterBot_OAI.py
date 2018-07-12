from lxml import etree
import yaml
import xmltodict
import requests
import random
import sys
from tweepy import OAuthHandler
from tweepy import API
from apscheduler.schedulers.blocking import BlockingScheduler

schedule = BlockingScheduler()

# Remove keys and secrets.
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)
print("Starting up the app!")
sys.stdout.flush()


class Settings:
    def __init__(self, yaml_file):
        self.provider = yaml_file['provider']
        self.collections = yaml_file['collections']

    def grab_random_collection(self):
        return random.choice(self.collections)


class Collection:
    def __init__(self, collection, provider, metadata_format="mods"):
        self.name = collection
        self.provider = provider
        self.metadata = metadata_format
        self.token = ""
        self.size = 0
        self.harvest_string = f"{self.provider}?verb=ListRecords&set={self.name}&metadataPrefix={self.metadata}"
        self.records = []

    def __repr__(self):
        return f"The {self.name} collection."

    def check_endpoint(self):
        r = requests.get(f"{self.provider}?verb=ListRecords&set={self.name}&metadataPrefix={self.metadata}")
        document = etree.fromstring(r.text.encode("utf-8"))
        error_code = document.findall('.//{http://www.openarchives.org/OAI/2.0/}error')
        if len(error_code) == 1:
            return True
        else:
            return False

    def populate(self):
        r = requests.get(f"{self.harvest_string}")
        document = etree.fromstring(r.text.encode("utf-8"))
        new_session_token = document.findall('.//{http://www.openarchives.org/OAI/2.0/}resumptionToken')
        if len(new_session_token) == 1:
            self.token = f'&resumptionToken={new_session_token[0].text}'
        else:
            self.token = None
        test = xmltodict.parse(r.text)
        for record in test['OAI-PMH']['ListRecords']['record']:
            self.size += 1
            new_record = Record(record)
            new_record.get_title()
            new_record.get_object_in_context()
            if new_record.title is not None and new_record.object_in_context is not None:
                self.records.append({"title": new_record.title, "url": new_record.object_in_context})
        if self.token is not None:
            self.harvest_string = f"{self.provider}?verb=ListRecords{self.token}"
            self.populate()

    def choose_random_record(self):
        return random.choice(self.records)


class Record:
    def __init__(self, contents):
        self.contents = contents
        self.title = None
        self.object_in_context = None

    def get_title(self):
        try:
            if type(self.contents["metadata"]["mods"]["titleInfo"]["title"]) is str:
                self.title = self.contents["metadata"]["mods"]["titleInfo"]["title"]
        except TypeError:
            print("Multiple Titles Detected")
            
    def get_object_in_context(self):
        if self.contents["metadata"]["mods"]["location"]['url']:
            for url in self.contents["metadata"]["mods"]["location"]['url']:
                if url["@access"] == "object in context":
                    self.object_in_context = url["#text"]


@schedule.scheduled_job('cron', day_of_week='mon-sun', hour=18, minute=38)
def scheduled_job():
    print("Firing scheduled job.")
    settings = yaml.load(open("settings.yml", "r"))
    my_settings = Settings(settings)
    new_collection = Collection(my_settings.grab_random_collection(), my_settings.provider)
    is_bad = new_collection.check_endpoint()
    if is_bad is False:
        new_collection.populate()
        x = new_collection.choose_random_record()
        tweet = (f"{x['title']} - Find it at: {x['url']}")
        print(tweet)
        api.update_status(tweet)
    sys.stdout.flush()


schedule.start()
