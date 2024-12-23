import socket
import socketserver

from udp_sockets import CollectServerHandler, CollectServer

import peewee

db = peewee.SqliteDatabase("track_data.db")

class TrackData(peewee.Model):
    track_id = peewee.IntegerField()
    x_pos = peewee.IntegerField()
    y_pos = peewee.IntegerField()
    z_pos = peewee.IntegerField()
    lap_progress = peewee.IntegerField()
    center_distance = peewee.IntegerField()
    side = peewee.IntegerField()

    class Meta:
        database = db
        indexes = (
            (('lap_progress', 'side', 'track_id'), True),
        )


if __name__ == '__main__':
    HOST, PORT = "localhost", 7650
    db.connect()
    db.create_tables([TrackData])
    with CollectServer((HOST, PORT), CollectServerHandler) as server:
        server.serve_forever()
    
