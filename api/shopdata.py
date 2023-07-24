import requests

from utils.dotdict import DotDict
import utils.time as time

URL = 'https://splatoon3.ink/data/gear.json'
MAX_ANNOUNCE_TIME = 600


def get():
    """ Get JSON from splatoon3.ink API """
    res = requests.get(URL)
    if not res.ok:
        print(f'Failed to fetch splatoon3.ink data (response code {res.status_code}: {res.reason})')
        return False
    return DotDict(res.json()).data


def updated_footer() -> dict:
    """ Return embed footer with current time """
    return {'text': f'Last updated {time.now_str()}'}


def error_page() -> dict:
    """ Return error page with given title """
    return {
        'title': '',
        'fields': [{'value': '\n*Error: Unrecognized data*\n'}],
        'footer': updated_footer()
    }


# def get_daily_gear(data: DotDict) -> dict:
#     """ Return SplatNet daily drop data formatted as a Discord embed """
#     try:
#         daily = data.gesotown.pickupBrand
#         fields = [{
#             'name': daily.brand.name,
#             'value': f'Favored ability:  {daily.brand.usualGearPower.name}\n'
#                      f'Sale ends in <t:{time.convert_dt(daily.saleEndTime)}:R>',
#             'inline': False
#         }]
#         for item in daily.brandGears:
#             fields.append({
#                 'name': item.gear.name,
#                 'value': f'> Ability:  {item.gear.primaryGearPower.name}\n'
#                          f'> Sub Slots:  {len(item.gear.additionalGearPowers)}\n'
#                          f'> Price:  {item.price}',
#                 'inline': True
#             })
#
#         return {
#             'title': 'Daily Drop',
#             'fields': fields,
#             'footer': updated_footer(),
#         }
#     except (TypeError, IndexError, KeyError) as e:
#         print(e)
#         return error_page()


def formatted(data: DotDict) -> dict:
    """ Return SplatNet gear data formatted as a Discord embed """
    fields = []
    try:
        all_gear = data.gesotown.pickupBrand.brandGears + data.gesotown.limitedGears
        for item in all_gear:
            fields.append({
                'name': item.gear.name,
                'value': f'Brand:  {item.gear.brand.name}\n'
                         f'Ability:  {item.gear.primaryGearPower.name}\n'
                         f'Sub Slots:  {len(item.gear.additionalGearPowers)}\n'
                         f'Price:  {item.price}\n'
                         f'Sale ends <t:{time.convert_dt(item.saleEndTime)}:R>',
                'inline': True
            })
        return {
            'title': 'SplatNet Gear',
            'fields': fields,
            'footer': updated_footer(),
        }
    except (TypeError, IndexError, KeyError) as e:
        print(e)
        return error_page()
