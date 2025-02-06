import sys
from datetime import datetime, timezone
from typing import TypedDict, NotRequired

from api import splatoon3ink
from api.splatoon3ink.schedules import TurfRotation, SalmonRunRotation, ChallengeEvent

# Discord Embed objects, as defined by Discord API (not comprehensive)
# https://discord.com/developers/docs/resources/message#embed-object-embed-structure

class EmbedField(TypedDict):
    name: str
    value: str
    inline: NotRequired[bool]

class EmbedFooter(TypedDict):
    text: str

class EmbedContent(TypedDict, total=False):
    title: str
    type: str
    description: str
    url: str
    timestamp: int
    color: int
    footer: EmbedFooter
    fields: list[EmbedField]

type PaginatorContent = list[EmbedContent]


# Utility functions for handling datetimes

def to_timestamp(dt: str) -> int:
    """ Convert API datetime format to unix timestamp """
    dt_utc = datetime.strptime(dt, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
    dt_local = dt_utc.astimezone(tz=None)  # Discord expects local time
    return int(dt_local.timestamp())

def now() -> int:
    """ Return current time as Unix timestamp """
    return int(datetime.now().timestamp())


# Utility functions for creating generic embed components

def updated_footer() -> EmbedFooter:
    """ Return embed footer with current time """
    return {'text': f'Last updated {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}'}

def error_page() -> EmbedContent:
    """ Return error page with given title """
    return {
        'title': 'Error',
        'fields': [{'name': '', 'value': '\n*Unrecognized data*\n'}],
        'footer': updated_footer()
    }

def empty_page(title: str) -> EmbedContent:
    """ Return empty embed with given title """
    return {
        'title': title,
        'fields': [{'name': '', 'value': '\n*No data available*\n'}],
        'footer': updated_footer()
    }


# The important functions

def create_maps_embed(data: splatoon3ink.ScheduleData) -> PaginatorContent:
    """ Takes splatoon API data and returns the main map rotations embed """
    if not data['regularSchedules']['nodes']:
        return [empty_page('Map Schedule')]
    pages = []

    for i, node in enumerate[TurfRotation](data['regularSchedules']['nodes']):
        try:
            start = to_timestamp(node['startTime'])
            end = to_timestamp(node['endTime'])
            if end < now():
                continue
            suffix = '(Current)' if i == 0 else '(Next)' if i == 1 else ''

            festmaps = data['festSchedules']['nodes'][i]['festMatchSettings']

            if festmaps is not None:
                pages.append({
                    'title': f'Splatfest Schedule {suffix}\n'
                             f'<t:{start}:D> <t:{start}:t> - <t:{end}:t>',
                    'fields': [
                        {
                            'name': f'Turf War (Pro)',
                            'value': '\n'.join([f'> {stage["name"]}' for stage in festmaps[0]['vsStages']]),
                            'inline': False
                        },
                        {
                            'name': f'Turf War (Regular)',
                            'value': '\n'.join([f'> {stage["name"]}' for stage in festmaps[1]['vsStages']]),
                            'inline': False
                        },
                    ] + ([
                        {
                            'name': f'Tricolor Turf War',
                            'value': f'> {data["currentFest"]["tricolorStage"]["name"]}',
                            'inline': False
                        },
                    ] if data['currentFest']['state'] == 'SECOND_HALF' else []),
                    'footer': updated_footer(),
                    'color': 0x16A80C
                })

            else:
                turf = data['regularSchedules']['nodes'][i]['regularMatchSetting']
                rseries = data['bankaraSchedules']['nodes'][i]['bankaraMatchSettings'][0]
                ropen = data['bankaraSchedules']['nodes'][i]['bankaraMatchSettings'][1]
                xrank = data['xSchedules']['nodes'][i]['xMatchSetting']

                pages.append({
                    'title': f'Map Schedule {suffix}\n'
                             f'<t:{start}:D> <t:{start}:t> - <t:{end}:t>',
                    'fields': [
                        {
                            'name': f'Turf War',
                            'value': '\n'.join([f'> {stage["name"]}' for stage in turf['vsStages']]),
                            'inline': False
                        },
                        {
                            'name': f'Anarchy Series:  {rseries["vsRule"]["name"]}',
                            'value': '\n'.join([f'> {stage["name"]}' for stage in rseries['vsStages']]),
                            'inline': True
                        },
                        {
                            'name': f'Anarchy Open:  {ropen["vsRule"]["name"]}',
                            'value': '\n'.join([f'> {stage["name"]}' for stage in ropen['vsStages']]),
                            'inline': False
                        },
                        {
                            'name': f'X Battles:  {xrank["vsRule"]["name"]}',
                            'value': '\n'.join([f'> {stage["name"]}' for stage in xrank['vsStages']]),
                            'inline': True
                        },
                    ],
                    'footer': updated_footer(),
                    'color': 0x16A80C
                })

        except Exception as e:
            pages.append(error_page())
            print(e, file=sys.stderr)

    if not pages:
        pages.append(empty_page('Map Schedule'))
    return pages


def create_sr_embed(data: splatoon3ink.ScheduleData) -> PaginatorContent:
    """ Takes splatoon API data and returns the salmon run rotations embed """
    allruns = \
        data['coopGroupingSchedule']['regularSchedules']['nodes'] + \
        data['coopGroupingSchedule']['bigRunSchedules']['nodes']
    if not allruns:
        return [empty_page('Salmon Run Schedule')]
    pages = []

    allruns.sort(key=lambda x: to_timestamp(x['startTime']))

    for i, node in enumerate[SalmonRunRotation](allruns):
        try:
            start = to_timestamp(node['startTime'])
            end = to_timestamp(node['endTime'])
            if end < now():
                continue
            is_bigrun = node['setting']['__typename'] == 'CoopBigRunSetting'

            suffix = '(Current)' if i == 0 else '(Next)' if i == 1 else ''
            title = 'BIG RUN' if is_bigrun else 'Salmon Run Schedule'

            pages.append({
                'title': f'{title} {suffix}\n'
                         f'<t:{start}:f> - <t:{end}:f>',
                'fields': [
                    {
                        'name': 'Map',
                        'value': f'> {node["setting"]["coopStage"]["name"]}\n',
                        'inline': False
                    },
                    {
                        'name': 'Weapons',
                        'value': '\n'.join([f'> {w["name"]}' for w in node['setting']['weapons']]),
                        'inline': False
                    },
                    {
                        'name': 'Boss',
                        'value': f'> {node["setting"]["boss"]["name"]}\n',
                        'inline': False
                    },
                ],
                'footer': updated_footer(),
                'color': 0xC54B22
            })

        except Exception as e:
            pages.append(error_page())
            print(e, file=sys.stderr)

    if not pages:
        pages.append(empty_page('Salmon Run Schedule'))
    return pages


def create_challenge_embed(data: splatoon3ink.ScheduleData) -> PaginatorContent:
    """ Takes splatoon API data and returns the challenge rotations embed """
    if not data['eventSchedules']['nodes']:
        return [empty_page('Challenge Schedule')]
    pages = []
    first_slot_start = None

    for i, node in enumerate[ChallengeEvent](data['eventSchedules']['nodes']):
        try:
            timeslots = []
            is_ongoing = False
            for t in node['timePeriods']:
                start = to_timestamp(t['startTime'])
                end = to_timestamp(t['endTime'])
                if first_slot_start is None:
                    first_slot_start = start
                if end < now():
                    continue
                is_ongoing = is_ongoing or start <= now()
                timeslots.append((start, end))

            setting = node['leagueMatchSetting']
            suffix = '(Open Now!)' if is_ongoing else '(Upcoming)'

            if not setting['leagueMatchEvent']['regulation']:  # if event is unknown
                continue

            pages.append({
                'title': f'Challenge Schedule:  {setting["leagueMatchEvent"]["name"]} {suffix}\n',
                'fields': [
                    {
                        'name': 'Description:',
                        'value': setting['leagueMatchEvent']['regulation']
                        .replace('<br />', '\n')
                        .replace('\n\n', '\n'),
                        'inline': False
                    },
                    {
                        'name': setting['vsRule']['name'],
                        'value': '\n'.join([f'> {stage["name"]}' for stage in setting['vsStages']]),
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

    if not pages:
        pages.append(empty_page('Challenge Schedule'))
    return pages


def create_eggstra_embed(data: splatoon3ink.ScheduleData) -> PaginatorContent | None:
    """ Takes splatoon API data and returns the eggstra work embed, or None if no eggstra work is scheduled """
    nodes = data['coopGroupingSchedule']['teamContestSchedules']['nodes']
    if not nodes:
        return None
    pages = []

    for i, node in enumerate(nodes):
        try:
            start = to_timestamp(node['startTime'])
            end = to_timestamp(node['endTime'])
            suffix = '(Open Now!)' if start <= now() else '(Upcoming)'

            pages.append({
                'title': f'Eggstra Work {suffix}\n'
                         f'<t:{start}:f> - <t:{end}:f>',
                'fields': [
                    {
                        'name': 'Map',
                        'value': f'> {node["setting"]["coopStage"]["name"]}\n',
                        'inline': False
                    },
                    {
                        'name': 'Weapons',
                        'value': '\n'.join([f'> {w["name"]}' for w in node['setting']['weapons']]),
                        'inline': False
                    },
                ],
                'footer': updated_footer(),
                'color': 0xD8C100
            })

        except Exception as e:
            pages.append(error_page())
            print(e, file=sys.stderr)

    return pages


def create_shop_embed(data: splatoon3ink.ShopData) -> EmbedContent:
    """ Return SplatNet gear data formatted as a Discord embed """
    fields = []
    try:
        all_gear = data['gesotown']['pickupBrand']['brandGears'] + data['gesotown']['limitedGears']
        for item in all_gear:
            end = to_timestamp(item['saleEndTime'])
            if end < now():
                continue
            fields.append({
                'name': item['gear']['name'],
                'value': f'Brand:  {item["gear"]["brand"]["name"]}\n'
                         f'Ability:  {item["gear"]["primaryGearPower"]["name"]}\n'
                         f'Sub Slots:  {len(item["gear"]["additionalGearPowers"])}\n'
                         f'Price:  {item["price"]}\n'
                         f'Sale ends <t:{end}:R>',
                'inline': True
            })
        return {
            'title': 'SplatNet Gear',
            'fields': fields or [{'name': '', 'value': '\n*No data available*\n'}],
            'footer': updated_footer(),
        }
    except Exception as e:
        print(e, file=sys.stderr)
        return error_page()
