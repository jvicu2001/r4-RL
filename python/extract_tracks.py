##
#   Thanks to Whitehole (https://github.com/whiteh0le)
#   for the tracks' collision data offsets and
#   structs.
##

import struct
from track_helper import Track

offsets = {
    'Helter Skelter': 0x0F9AA8,
    'Out of Blue': 0x21E758,
    'Edge of the Earth': 0x337164,
    'Brightest Nite': 0x44EE64,
    'Wonderhill': 0x5715EC,
    'Heaven and Hell': 0x688AC0,
    'Phantomile': 0x74F7AC,
    'Shooting Hoops': 0x8091C4
}

track_ids = {
    'Helter Skelter': 0,
    'Out of Blue': 3,
    'Edge of the Earth': 2,
    'Brightest Nite': 5,
    'Wonderhill': 1,
    'Heaven and Hell': 6,
    'Phantomile': 4,
    'Shooting Hoops': 7
}


waypoint_struct = "<xxxxxxxxiihhxxxxhhhxxxxxxxxxxxxxxhhxxxxxxxxxxxx"
waypoint_size = struct.calcsize(waypoint_struct)

def get_tracks() -> list[Track] | FileNotFoundError:
    tracks = []
    try:
        r4_bin = open("../extracted/R4.BIN", 'rb')
        for track in offsets:
            # Jump to track offset
            r4_bin.seek(offsets[track])

            # Get how many waypoints this track has
            waypoint_count = struct.unpack("i", r4_bin.read(4))[0]

            # Create track instance and iterate through all waypoints
            track_checkpoints = Track(track, track_ids[track])
            for i in range(waypoint_count):
                waypoint_data = struct.unpack(waypoint_struct, r4_bin.read(waypoint_size))
                # print(waypoint_data)
                track_checkpoints.add_waypoint(*waypoint_data)
            tracks.append(track_checkpoints)

        r4_bin.close()

        return tracks
    except FileNotFoundError:
        print("File R4.BIN not found in the /extracted folder.\nExtract the file within PCSX-Redux.")
        return FileNotFoundError

    except Exception as err:
        print(err)
        return err


    # for x in tracks:
    #     print(f"{x}\nFirst waypoint: {x.waypoints[0]}")