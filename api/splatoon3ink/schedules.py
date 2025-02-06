from typing import TypedDict, Literal, Optional

from . import _util


# General models used throughout the API

class ImageRef(TypedDict):
    url: str

class MapData(TypedDict):
    vsStageId: int
    name: str
    image: ImageRef
    id: str

class ModeData(TypedDict):
    name: str
    rule: str
    id: str

class NodeList[T](TypedDict):
    nodes: list[T]


# Models for normal rotation data

class MatchSetting(TypedDict):
    __isVsSetting: str
    __typename: str
    vsStages: list[MapData]
    vsRule: ModeData

class AnarchyMatchSetting(MatchSetting):
    bankaraMode: Literal['CHALLENGE', 'OPEN']

class MatchSettingPlaceholder(TypedDict):
    __typename: str


class MapRotation(TypedDict):
    startTime: str
    endTime: str
    festMatchSettings: Optional[MatchSettingPlaceholder]

class TurfRotation(MapRotation):
    regularMatchSetting: Optional[MatchSetting]

class AnarchyRotation(MapRotation):
    bankaraMatchSettings: Optional[list[AnarchyMatchSetting]]

class XRotation(MapRotation):
    xMatchSetting: Optional[MatchSetting]


# Models for challenge data

class ChallengeInfo(TypedDict):
    leagueMatchEventId: str
    name: str
    desc: str
    regulationUrl: None
    regulation: str
    id: str

class ChallengeMatchSetting(MatchSetting):
    leagueMatchEvent: ChallengeInfo

class TimePeriod(TypedDict):
    startTime: str
    endTime: str

class ChallengeEvent(TypedDict):
    leagueMatchSetting: ChallengeMatchSetting
    timePeriods: list[TimePeriod]


# Models for splatfest data

class SplatfestRotation(MapRotation):
    festMatchSettings: Optional[MatchSetting]

class SplatfestColor(TypedDict):
    a: float
    b: float
    g: float
    r: float

class SplatfestTeam(TypedDict):
    id: str
    color: SplatfestColor
    myVoteState: None

class TricolorMap(TypedDict):
    name: str
    image: ImageRef
    id: str

class SplatfestData(TypedDict):
    id: str
    title: str
    startTime: str
    endTime: str
    midtermTime: str
    state: Literal['SCHEDULED', 'FIRST_HALF', 'SECOND_HALF']  # TODO: This is a guess, need confirmation
    teams: list[SplatfestTeam]
    tricolorStage: TricolorMap  # TODO: This is probably different now


# Models for salmon run data

class SalmonRunMapData(TypedDict):
    name: str
    thumbnailImage: ImageRef
    image: ImageRef
    id: str

class WeaponData(TypedDict):
    __splatoon3ink_id: str
    name: str
    image: ImageRef

class KingSalmonidData(TypedDict):
    name: str
    id: str

class SalmonRunSetting(TypedDict):
    __typename: str
    boss: KingSalmonidData
    coopStage: SalmonRunMapData
    __isCoopSetting: str
    weapons: list[WeaponData]

class SalmonRunRotation(TypedDict):
    startTime: str
    endTime: str
    setting: SalmonRunSetting
    __splatoon3ink_king_salmonid_guess: str

class SalmonRunData(TypedDict):
    bannerImage: Optional[ImageRef]
    regularSchedules: NodeList[SalmonRunRotation]
    bigRunSchedules: NodeList[SalmonRunRotation]
    teamContestSchedules: NodeList[SalmonRunRotation]


# Other models that aren't really important

class CurrentPlayer(TypedDict):
    userIcon: ImageRef

class PlayerMapData(TypedDict):
    vsStageId: int
    originalImage: ImageRef
    name: str
    stats: None
    id: str


# Root model

class ScheduleData(TypedDict):
    regularSchedules: NodeList[TurfRotation]
    bankaraSchedules: NodeList[AnarchyRotation]
    xSchedules: NodeList[XRotation]
    eventSchedules: NodeList[ChallengeEvent]
    festSchedules: NodeList[SplatfestRotation]
    coopGroupingSchedule: SalmonRunData
    currentFest: Optional[SplatfestData]
    currentPlayer: CurrentPlayer
    vsStages: NodeList[PlayerMapData]


def get() -> Optional[ScheduleData]:
    return _util.fetch_api('/schedules.json')
