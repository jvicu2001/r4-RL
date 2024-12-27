from enum import Enum

class TrackLenght(Enum):
    HELTER      = 170330
    WONDER      = 217817
    EDGE        = 184848
    OUT         = 182049
    PHANTOMILE  = 98395
    BRIGHTEST   = 189523
    HEAVEN      = 209919
    SHOOTING    = 129750

def get_track_name(track_id: int) -> str:
    match track_id:
        case 0:
            return "Helter Skelter"
        case 1:
            return "Wonderhill"
        case 2:
            return "Edge of the earth"
        case 3:
            return "Out of blue"
        case 4:
            return "Phantomile"
        case 5:
            return "Brightest nite"
        case 6:
            return "Heaven and hell"
        case 7:
            return "Shooting Hoops"
        case 8:
            return "Helter Skelter (Reverse)"
        case 9:
            return "Wonderhill (Reverse)"
        case 10:
            return "Edge of the earth (Reverse)"
        case 11:
            return "Out of blue (Reverse)"
        case 12:
            return "Phantomile (Reverse)"
        case 13:
            return "Brightest nite (Reverse)"
        case 14:
            return "Heaven and hell (Reverse)"
        case 15:
            return "Shooting Hoops (Reverse)"

def get_track_lenght(track_id: int) -> int:
    match track_id:
        case 0:
            return TrackLenght.HELTER.value
        case 1:
            return TrackLenght.WONDER.value
        case 2:
            return TrackLenght.EDGE.value
        case 3:
            return TrackLenght.OUT.value
        case 4:
            return TrackLenght.PHANTOMILE.value
        case 5:
            return TrackLenght.BRIGHTEST.value
        case 6:
            return TrackLenght.HEAVEN.value
        case 7:
            return TrackLenght.SHOOTING.value
        case 8:
            return TrackLenght.HELTER.value
        case 9:
            return TrackLenght.WONDER.value
        case 10:
            return TrackLenght.EDGE.value
        case 11:
            return TrackLenght.OUT.value
        case 12:
            return TrackLenght.PHANTOMILE.value
        case 13:
            return TrackLenght.BRIGHTEST.value
        case 14:
            return TrackLenght.HEAVEN.value
        case 15:
            return TrackLenght.SHOOTING.value
            