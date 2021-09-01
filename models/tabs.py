from datetime import datetime
from short_url import UrlEncoder
from web import db

su = UrlEncoder(
    alphabet="DEQhd2uFteibPwq0SWBInTpA_jcZL5GKz3YCR14Ulk87Jors9v" "NHgfaOmMXy6Vx-",
    block_size=16,
)


class Tab(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    band = db.Column(db.Text)
    album = db.Column(db.Text)
    song = db.Column(db.Text)
    track = db.Column(db.Integer)
    views = db.Column(db.Integer, default=0)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    fileid = db.Column(db.Integer)

    def __init__(self, band, album, song, track):

        self.band = band
        self.album = album
        self.song = song
        self.track = track

    def __repr__(self):

        return f"<GuitarTab: {self.song}>"

    def getname(self):

        return f"{su.enbase(self.id, 1)}{self.ext}"


class TabFile(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    sha256 = db.Column(db.Text)
    ext = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    tabid = db.Column(db.Integer)
    comment = db.Column(db.Text)

    def __init__(self, sha256, ext, tabid, comment="initial version"):

        self.sha256 = sha256
        self.ext = ext
        self.tabid = tabid
        self.comment = comment

    def getname(self):

        return f"{su.enbase(self.id, 1)}{self.ext}"
