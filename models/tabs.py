from datetime import datetime
from short_url import UrlEncoder
from web import db

su = UrlEncoder(alphabet='DEQhd2uFteibPwq0SWBInTpA_jcZL5GKz3YCR14Ulk87Jors9v'
                'NHgfaOmMXy6Vx-', block_size=16)


class GuitarTab(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    sha256 = db.Column(db.Text, unique=True)
    ext = db.Column(db.Text)
    band = db.Column(db.Text)
    album = db.Column(db.Text)
    song = db.Column(db.Text)
    track = db.Column(db.Integer)
    views = db.Column(db.Integer, default=0)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, sha256, ext, band, album, song, track):

        self.sha256 = sha256
        self.ext = ext
        self.band = band
        self.album = album
        self.song = song
        self.track = track

    def __repr__(self):

        return f'<GuitarTab: {self.song}>'

    def getname(self):

        return f'{su.enbase(self.id, 1)}{self.ext}'
