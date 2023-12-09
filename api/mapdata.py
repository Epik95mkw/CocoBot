import sys

import requests
from attr import dataclass

from components.config import Mode
from utils.dotdict import DotDict
import utils.time as time

URL = 'https://splatoon3.ink/data/schedules.json'
MAX_ANNOUNCE_TIME = 600


def get():
    """ Get JSON from splatoon3.ink API """
    res = requests.get(URL)
    if not res.ok:
        print(f'Failed to fetch splatoon3.ink data (response code {res.status_code}: {res.reason})')
        return False
    return DotDict(res.json()).data


@dataclass
class AnnounceInfo:
    message: str
    role_key: str = ''


@dataclass
class PagerInfo:
    pages: list[dict]
    announcement: AnnounceInfo = None


def can_announce(ts: int) -> bool:
    return 0 < time.now() - ts < MAX_ANNOUNCE_TIME


def updated_footer() -> dict:
    """ Return embed footer with current time """
    return {'text': f'Last updated {time.now_str()}'}


def error_page() -> dict:
    """ Return error page with given title """
    return {
        'title': 'Error',
        'fields': [{'value': '\n*Unrecognized data*\n'}],
        'footer': updated_footer()
    }


def empty_embed(title) -> PagerInfo:
    """ Return empty embed with given title """
    return PagerInfo([{
        'title': title,
        'fields': [{
            'name': '',
            'value': '\n*No Data*\n'
        }],
        'footer': updated_footer()
    }])


def get_main_maps(data: DotDict) -> PagerInfo:
    """ Returns main 4v4 map data as a list of dicts formatted as Discord embeds. """
    if not data.regularSchedules.nodes:
        return empty_embed('Map Schedule')
    pages = []
    announcement = None

    for i, node in enumerate(data.regularSchedules.nodes):
        try:
            start = time.convert_dt(node.startTime)
            end = time.convert_dt(node.endTime)
            if end < time.now():
                continue
            suffix = '(Current)' if i == 0 else '(Next)' if i == 1 else ''

            festmaps = data.festSchedules.nodes[i].festMatchSettings

            if festmaps is not None:
                if can_announce(time.convert_dt(data.currentFest.startTime)):
                    announcement = AnnounceInfo(
                        f'Splatfest has started! {data.currentFest.title}'
                    )
                elif can_announce(time.convert_dt(data.currentFest.midtermTime)):
                    announcement = AnnounceInfo(
                        f'Splatfest halftime! '
                        f'Tricolor battles are now available to play on '
                        f'{data.currentFest.tricolorStage.name}'
                    )

                pages.append({
                    'title': f'Splatfest Schedule {suffix}\n'
                             f'<t:{start}:D> <t:{start}:t> - <t:{end}:t>',
                    'fields': [
                        {
                            'name': f'Turf War (Pro)',
                            'value': '\n'.join([f'> {stage.name}' for stage in festmaps[0].vsStages]),
                            'inline': False
                        },
                        {
                            'name': f'Turf War (Regular)',
                            'value': '\n'.join([f'> {stage.name}' for stage in festmaps[1].vsStages]),
                            'inline': False
                        },
                    ] + ([
                        {
                            'name': f'Tricolor Turf War',
                            'value': f'> {data.currentFest.tricolorStage.name}',
                            'inline': False
                        },
                    ] if data.currentFest.state == 'SECOND_HALF' else []),
                    'footer': updated_footer(),
                    'color': 0x16A80C
                })

            else:
                turf = data.regularSchedules.nodes[i].regularMatchSetting
                rseries = data.bankaraSchedules.nodes[i].bankaraMatchSettings[0]
                ropen = data.bankaraSchedules.nodes[i].bankaraMatchSettings[1]
                xrank = data.xSchedules.nodes[i].xMatchSetting

                pages.append({
                    'title': f'Map Schedule {suffix}\n'
                             f'<t:{start}:D> <t:{start}:t> - <t:{end}:t>',
                    'fields': [
                        {
                            'name': f'Turf War',
                            'value': '\n'.join([f'> {stage.name}' for stage in turf.vsStages]),
                            'inline': False
                        },
                        {
                            'name': f'Anarchy Series:  {rseries.vsRule.name}',
                            'value': '\n'.join([f'> {stage.name}' for stage in rseries.vsStages]),
                            'inline': True
                        },
                        {
                            'name': f'Anarchy Open:  {ropen.vsRule.name}',
                            'value': '\n'.join([f'> {stage.name}' for stage in ropen.vsStages]),
                            'inline': False
                        },
                        {
                            'name': f'X Battles:  {xrank.vsRule.name}',
                            'value': '\n'.join([f'> {stage.name}' for stage in xrank.vsStages]),
                            'inline': True
                        },
                    ],
                    'footer': updated_footer(),
                    'color': 0x16A80C
                })

        except Exception as e:
            pages.append(error_page())
            print(e, file=sys.stderr)

    return PagerInfo(pages, announcement)


def get_sr_shifts(data: DotDict) -> PagerInfo:
    """ Returns salmon run shift data as a list of dicts formatted as Discord embeds. """
    allruns = \
        data.coopGroupingSchedule.regularSchedules.nodes + \
        data.coopGroupingSchedule.bigRunSchedules.nodes
    if not allruns:
        return empty_embed('Salmon Run Schedule')
    pages = []
    announcement = None

    allruns.sort(key=lambda x: time.convert_dt(x.startTime))

    for i, node in enumerate(allruns):
        try:
            start = time.convert_dt(node.startTime)
            end = time.convert_dt(node.endTime)
            if end < time.now():
                continue
            is_bigrun = node.setting.__typename == 'CoopBigRunSetting'

            suffix = '(Current)' if i == 0 else '(Next)' if i == 1 else ''
            title = 'BIG RUN' if is_bigrun else 'Salmon Run Schedule'

            msg = ''
            if is_bigrun:
                msg = f'A Big Run on {node.setting.coopStage.name} has begun!'
            elif all(w.name == 'Random' for w in node.setting.weapons):
                msg = f'A wildcard shift on {node.setting.coopStage.name} has started.'

            if msg and can_announce(start):
                announcement = AnnounceInfo(msg, role_key=Mode.SR)

            pages.append({
                'title': f'{title} {suffix}\n'
                         f'<t:{start}:f> - <t:{end}:f>',
                'fields': [
                    {
                        'name': 'Map',
                        'value': f'> {node.setting.coopStage.name}\n',
                        'inline': False
                    },
                    {
                        'name': 'Weapons',
                        'value': '\n'.join([f'> {w.name}' for w in node.setting.weapons]),
                        'inline': False
                    },
                ],
                'footer': updated_footer(),
                'color': 0xC54B22
            })

        except Exception as e:
            pages.append(error_page())
            print(e, file=sys.stderr)

    return PagerInfo(pages, announcement)


def get_challenges(data: DotDict) -> PagerInfo:
    """ Returns challenge data as a list of dicts formatted as Discord embeds. """
    if not data.eventSchedules.nodes:
        return empty_embed('Challenge Schedule')
    pages = []
    announcement = None

    for i, node in enumerate(data.eventSchedules.nodes):
        try:
            timeslots = []
            is_ongoing = False
            for t in node.timePeriods:
                start = time.convert_dt(t.startTime)
                end = time.convert_dt(t.endTime)
                if end < time.now():
                    continue
                is_ongoing = is_ongoing or start <= time.now()
                timeslots.append((start, end))

            setting = node.leagueMatchSetting
            suffix = '(Open Now!)' if is_ongoing else '(Upcoming)'

            if not setting.leagueMatchEvent.regulation:  # if event is unknown
                continue

            if is_ongoing and len(timeslots) == 3:  # only triggers for first timeslot
                announcement = AnnounceInfo(
                    f'The {setting.leagueMatchEvent.name} event is now open.',
                    role_key=Mode.MAIN
                )

            pages.append({
                'title': f'Challenge Schedule:  {setting.leagueMatchEvent.name} {suffix}\n',
                'fields': [
                    {
                        'name': 'Description:',
                        'value': setting.leagueMatchEvent.regulation.replace('<br />', '\n').replace('\n\n', '\n'),
                        'inline': False
                    },
                    {
                        'name': setting.vsRule.name,
                        'value': '\n'.join([f'> {stage.name}' for stage in setting.vsStages]),
                        'inline': False
                    },
                    {
                        'name': 'Timeslots:',
                        'value': '\n'.join([f'> <t:{t[0]}:D> <t:{t[0]}:t> - <t:{t[1]}:t>' for t in timeslots]),
                        'inline': False
                    },
                ],
                'footer': updated_footer(),
                'color': 0xD60E6E
            })

        except Exception as e:
            pages.append(error_page())
            print(e, file=sys.stderr)

    return PagerInfo(pages, announcement)


def get_eggstra_shifts(data: DotDict) -> PagerInfo:
    """ Returns eggstra work data as a list of dicts formatted as Discord embeds. """
    nodes = data.coopGroupingSchedule.teamContestSchedules.nodes
    if not nodes:
        return PagerInfo([])
    pages = []
    announcement = None

    for i, node in enumerate(nodes):
        try:
            start = time.convert_dt(node.startTime)
            end = time.convert_dt(node.endTime)
            suffix = '(Open Now!)' if start <= time.now() else '(Upcoming)'

            if can_announce(start):
                announcement = AnnounceInfo(
                    f'Eggstra Work on {node.setting.coopStage.name} has started.',
                    role_key=Mode.SR
                )

            pages.append({
                'title': f'Eggstra Work {suffix}\n'
                         f'<t:{start}:f> - <t:{end}:f>',
                'fields': [
                    {
                        'name': 'Map',
                        'value': f'> {node.setting.coopStage.name}\n',
                        'inline': False
                    },
                    {
                        'name': 'Weapons',
                        'value': '\n'.join([f'> {w.name}' for w in node.setting.weapons]),
                        'inline': False
                    },
                ],
                'footer': updated_footer(),
                'color': 0xD8C100
            })

        except Exception as e:
            pages.append(error_page())
            print(e, file=sys.stderr)

    return PagerInfo(pages, announcement)


def format_all(data: DotDict) -> dict[str:PagerInfo]:
    """ Returns a dict containing all embed data. """
    return {
        Mode.MAIN: get_main_maps(data),
        Mode.SR: get_sr_shifts(data),
        Mode.CHALLENGE: get_challenges(data),
        Mode.EGGSTRA: get_eggstra_shifts(data)
    }
