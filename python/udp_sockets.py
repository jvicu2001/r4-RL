import socket
import socketserver

from proto import track_pb2

# Track collection uses sockerserver
class CollectServer(socketserver.UDPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

class CollectServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        print(socket)

        track_point = track_pb2.TrackPoint()
        track_point.ParseFromString(data)

        print(track_point)

        track_point_db = TrackData(
            track_id=track_point.track_id, 
            x_pos=track_point.x_pos,
            y_pos=track_point.y_pos,
            z_pos=track_point.z_pos,
            lap_progress=track_point.lap_progress,
            center_distance=track_point.center_distance,
            side=track_point.side
            )
        print(f"Saved {track_point_db.save()} point.")

# Car data will be received with socket, not socketserver
# Couldn't figure out how to receive data with socketserver
# without blocking
