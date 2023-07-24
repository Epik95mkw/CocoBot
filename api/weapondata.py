import random

data = [
    {'main': '.52 Gal', 'id': '50', 'sub': 'Splash Wall', 'special': 'Killer Wail 5.1', 'special_points': '190p',
     'class': 'Shooter'},
    {'main': '.96 Gal', 'id': '80', 'sub': 'Sprinkler', 'special': 'Ink Vac', 'special_points': '190p',
     'class': 'Shooter'},
    {'main': '.96 Gal Deco', 'id': '81', 'sub': 'Splash Wall', 'special': 'Kraken Royale', 'special_points': '210p',
     'class': 'Shooter'},
    {'main': 'Aerospray MG', 'id': '30', 'sub': 'Fizzy Bomb', 'special': 'Reefslider', 'special_points': '180p',
     'class': 'Shooter'},
    {'main': 'Aerospray RG', 'id': '31', 'sub': 'Sprinkler', 'special': 'Booyah Bomb', 'special_points': '200p',
     'class': 'Shooter'},
    {'main': 'Annaki Splattershot Nova', 'id': '101', 'sub': 'Ink Mine', 'special': 'Inkjet', 'special_points': '200p',
     'class': 'Shooter'},
    {'main': 'Ballpoint Splatling', 'id': '4030', 'sub': 'Fizzy Bomb', 'special': 'Inkjet', 'special_points': '200p',
     'class': 'Splatling'},
    {'main': 'Bamboozler 14 Mk I', 'id': '2050', 'sub': 'Autobomb', 'special': 'Killer Wail 5.1',
     'special_points': '200p', 'class': 'Charger'},
    {'main': 'Big Swig Roller', 'id': '1040', 'sub': 'Splash Wall', 'special': 'Ink Vac', 'special_points': '200p',
     'class': 'Roller'},
    {'main': 'Big Swig Roller Express', 'id': '1041', 'sub': 'Angle Shooter', 'special': 'Ink Storm',
     'special_points': '200p', 'class': 'Roller'},
    {'main': 'Blaster', 'id': '210', 'sub': 'Autobomb', 'special': 'Big Bubbler', 'special_points': '180p',
     'class': 'Blaster'},
    {'main': 'Bloblobber', 'id': '3030', 'sub': 'Sprinkler', 'special': 'Ink Storm', 'special_points': '190p',
     'class': 'Slosher'},
    {'main': 'Carbon Roller', 'id': '1000', 'sub': 'Autobomb', 'special': 'Zipcaster', 'special_points': '180p',
     'class': 'Roller'},
    {'main': 'Carbon Roller Deco', 'id': '1001', 'sub': 'Burst Bomb', 'special': 'Trizooka', 'special_points': '190p',
     'class': 'Roller'},
    {'main': 'Clash Blaster', 'id': '230', 'sub': 'Splat Bomb', 'special': 'Trizooka', 'special_points': '180p',
     'class': 'Blaster'},
    {'main': 'Clash Blaster Neo', 'id': '231', 'sub': 'Curling Bomb', 'special': 'Super Chump',
     'special_points': '180p', 'class': 'Blaster'},
    {'main': 'Classic Squiffer', 'id': '2000', 'sub': 'Point Sensor', 'special': 'Big Bubbler',
     'special_points': '190p', 'class': 'Charger'},
    {'main': 'Custom Dualie Squelchers', 'id': '5031', 'sub': 'Squid Beakon', 'special': 'Super Chump',
     'special_points': '200p', 'class': 'Dualie'},
    {'main': 'Custom Jet Squelcher', 'id': '91', 'sub': 'Toxic Mist', 'special': 'Ink Storm', 'special_points': '180p',
     'class': 'Shooter'},
    {'main': 'Custom Splattershot Jr.', 'id': '11', 'sub': 'Torpedo', 'special': 'Wave Breaker',
     'special_points': '190p', 'class': 'Shooter'},
    {'main': 'Dapple Dualies', 'id': '5000', 'sub': 'Squid Beakon', 'special': 'Tacticooler', 'special_points': '180p',
     'class': 'Dualie'},
    {'main': 'Dapple Dualies Nouveau', 'id': '5001', 'sub': 'Torpedo', 'special': 'Reefslider',
     'special_points': '190p', 'class': 'Dualie'},
    {'main': 'Dark Tetra Dualies', 'id': '5040', 'sub': 'Autobomb', 'special': 'Reefslider', 'special_points': '200p',
     'class': 'Dualie'},
    {'main': 'Dualie Squelchers', 'id': '5030', 'sub': 'Splat Bomb', 'special': 'Wave Breaker',
     'special_points': '200p', 'class': 'Dualie'},
    {'main': 'Dynamo Roller', 'id': '1020', 'sub': 'Sprinkler', 'special': 'Tacticooler', 'special_points': '190p',
     'class': 'Roller'},
    {'main': 'E-liter 4K', 'id': '2030', 'sub': 'Ink Mine', 'special': 'Wave Breaker', 'special_points': '210p',
     'class': 'Charger'},
    {'main': 'E-liter 4K Scope', 'id': '2040', 'sub': 'Ink Mine', 'special': 'Wave Breaker', 'special_points': '210p',
     'class': 'Charger'},
    {'main': 'Explosher', 'id': '3040', 'sub': 'Point Sensor', 'special': 'Ink Storm', 'special_points': '200p',
     'class': 'Slosher'},
    {'main': 'Flingza Roller', 'id': '1030', 'sub': 'Ink Mine', 'special': 'Tenta Missiles', 'special_points': '210p',
     'class': 'Roller'},
    {'main': 'Forge Splattershot Pro', 'id': '71', 'sub': 'Suction Bomb', 'special': 'Booyah Bomb',
     'special_points': '210p', 'class': 'Shooter'},
    {'main': 'Glooga Dualies', 'id': '5020', 'sub': 'Splash Wall', 'special': 'Booyah Bomb', 'special_points': '180p',
     'class': 'Dualie'},
    {'main': 'Goo Tuber', 'id': '2060', 'sub': 'Torpedo', 'special': 'Tenta Missiles', 'special_points': '200p',
     'class': 'Charger'},
    {'main': 'H-3 Nozzlenose', 'id': '310', 'sub': 'Point Sensor', 'special': 'Tacticooler', 'special_points': '190p',
     'class': 'Shooter'},
    {'main': 'H-3 Nozzlenose D', 'id': '311', 'sub': 'Splash Wall', 'special': 'Big Bubbler', 'special_points': '200p',
     'class': 'Shooter'},
    {'main': 'Heavy Splatling', 'id': '4010', 'sub': 'Sprinkler', 'special': 'Wave Breaker', 'special_points': '200p',
     'class': 'Splatling'},
    {'main': 'Heavy Splatling Deco', 'id': '4011', 'sub': 'Point Sensor', 'special': 'Kraken Royale',
     'special_points': '200p', 'class': 'Splatling'},
    {'main': 'Hero Shot Replica', 'id': '45', 'sub': 'Suction Bomb', 'special': 'Trizooka', 'special_points': '190p',
     'class': 'Shooter'},
    {'main': 'Hydra Splatling', 'id': '4020', 'sub': 'Autobomb', 'special': 'Booyah Bomb', 'special_points': '190p',
     'class': 'Splatling'},
    {'main': 'Inkbrush', 'id': '1100', 'sub': 'Splat Bomb', 'special': 'Killer Wail 5.1', 'special_points': '180p',
     'class': 'Brush'},
    {'main': 'Inkbrush Nouveau', 'id': '1101', 'sub': 'Ink Mine', 'special': 'Ultra Stamp', 'special_points': '180p',
     'class': 'Brush'},
    {'main': 'Jet Squelcher', 'id': '90', 'sub': 'Angle Shooter', 'special': 'Ink Vac', 'special_points': '190p',
     'class': 'Shooter'},
    {'main': 'Krak-On Splat Roller', 'id': '1011', 'sub': 'Squid Beakon', 'special': 'Kraken Royale',
     'special_points': '180p', 'class': 'Roller'},
    {'main': 'L-3 Nozzlenose', 'id': '300', 'sub': 'Curling Bomb', 'special': 'Crab Tank', 'special_points': '200p',
     'class': 'Shooter'},
    {'main': 'L-3 Nozzlenose D', 'id': '301', 'sub': 'Burst Bomb', 'special': 'Ultra Stamp', 'special_points': '200p',
     'class': 'Shooter'},
    {'main': 'Light Tetra Dualies', 'id': '5041', 'sub': 'Sprinkler', 'special': 'Zipcaster', 'special_points': '190p',
     'class': 'Dualie'},
    {'main': 'Luna Blaster', 'id': '200', 'sub': 'Splat Bomb', 'special': 'Zipcaster', 'special_points': '180p',
     'class': 'Blaster'},
    {'main': 'Luna Blaster Neo', 'id': '201', 'sub': 'Fizzy Bomb', 'special': 'Ultra Stamp', 'special_points': '180p',
     'class': 'Blaster'},
    {'main': 'Mini Splatling', 'id': '4000', 'sub': 'Burst Bomb', 'special': 'Ultra Stamp', 'special_points': '180p',
     'class': 'Splatling'},
    {'main': "N-ZAP '85", 'id': '60', 'sub': 'Suction Bomb', 'special': 'Tacticooler', 'special_points': '180p',
     'class': 'Shooter'},
    {'main': "N-ZAP '89", 'id': '61', 'sub': 'Autobomb', 'special': 'Super Chump', 'special_points': '180p',
     'class': 'Shooter'},
    {'main': 'Nautilus 47', 'id': '4040', 'sub': 'Point Sensor', 'special': 'Ink Storm', 'special_points': '190p',
     'class': 'Splatling'},
    {'main': 'Neo Splash-o-matic', 'id': '21', 'sub': 'Suction Bomb', 'special': 'Triple Inkstrike',
     'special_points': '210p', 'class': 'Shooter'},
    {'main': 'Neo Sploosh-o-matic', 'id': '1', 'sub': 'Squid Beakon', 'special': 'Killer Wail 5.1',
     'special_points': '180p', 'class': 'Shooter'},
    {'main': 'Octobrush', 'id': '1110', 'sub': 'Suction Bomb', 'special': 'Zipcaster', 'special_points': '200p',
     'class': 'Brush'},
    {'main': 'Painbrush', 'id': '1120', 'sub': 'Curling Bomb', 'special': 'Wave Breaker', 'special_points': '200p',
     'class': 'Brush'},
    {'main': 'Range Blaster', 'id': '220', 'sub': 'Suction Bomb', 'special': 'Wave Breaker', 'special_points': '200p',
     'class': 'Blaster'},
    {'main': 'Rapid Blaster', 'id': '240', 'sub': 'Ink Mine', 'special': 'Triple Inkstrike', 'special_points': '200p',
     'class': 'Blaster'},
    {'main': 'Rapid Blaster Deco', 'id': '241', 'sub': 'Torpedo', 'special': 'Inkjet', 'special_points': '210p',
     'class': 'Blaster'},
    {'main': 'Rapid Blaster Pro', 'id': '250', 'sub': 'Toxic Mist', 'special': 'Ink Vac', 'special_points': '180p',
     'class': 'Blaster'},
    {'main': 'Rapid Blaster Pro Deco', 'id': '251', 'sub': 'Angle Shooter', 'special': 'Killer Wail 5.1',
     'special_points': '180p', 'class': 'Blaster'},
    {'main': 'REEF-LUX 450', 'id': '7020', 'sub': 'Curling Bomb', 'special': 'Tenta Missiles', 'special_points': '210p',
     'class': 'Stringer'},
    {'main': "S-BLAST '92", 'id': '260', 'sub': 'Sprinkler', 'special': 'Reefslider', 'special_points': '180p',
     'class': 'Blaster'},
    {'main': 'Slosher', 'id': '3000', 'sub': 'Splat Bomb', 'special': 'Triple Inkstrike', 'special_points': '200p',
     'class': 'Slosher'},
    {'main': 'Slosher Deco', 'id': '3001', 'sub': 'Angle Shooter', 'special': 'Zipcaster', 'special_points': '180p',
     'class': 'Slosher'},
    {'main': 'Sloshing Machine', 'id': '3020', 'sub': 'Fizzy Bomb', 'special': 'Booyah Bomb', 'special_points': '220p',
     'class': 'Slosher'},
    {'main': 'Snipewriter 5H', 'id': '2070', 'sub': 'Sprinkler', 'special': 'Tacticooler', 'special_points': '200p',
     'class': 'Charger'},
    {'main': 'Splash-o-matic', 'id': '20', 'sub': 'Burst Bomb', 'special': 'Crab Tank', 'special_points': '200p',
     'class': 'Shooter'},
    {'main': 'Splat Brella', 'id': '6000', 'sub': 'Sprinkler', 'special': 'Triple Inkstrike', 'special_points': '200p',
     'class': 'Brella'},
    {'main': 'Splat Charger', 'id': '2010', 'sub': 'Splat Bomb', 'special': 'Ink Vac', 'special_points': '200p',
     'class': 'Charger'},
    {'main': 'Splat Dualies', 'id': '5010', 'sub': 'Suction Bomb', 'special': 'Crab Tank', 'special_points': '190p',
     'class': 'Dualie'},
    {'main': 'Splat Roller', 'id': '1010', 'sub': 'Curling Bomb', 'special': 'Big Bubbler', 'special_points': '180p',
     'class': 'Roller'},
    {'main': 'Splatana Stamper', 'id': '8000', 'sub': 'Burst Bomb', 'special': 'Zipcaster', 'special_points': '200p',
     'class': 'Splatana'},
    {'main': 'Splatana Wiper', 'id': '8010', 'sub': 'Torpedo', 'special': 'Ultra Stamp', 'special_points': '190p',
     'class': 'Splatana'},
    {'main': 'Splatana Wiper Deco', 'id': '8011', 'sub': 'Squid Beakon', 'special': 'Tenta Missiles',
     'special_points': '190p', 'class': 'Splatana'},
    {'main': 'Splatterscope', 'id': '2020', 'sub': 'Splat Bomb', 'special': 'Ink Vac', 'special_points': '200p',
     'class': 'Charger'},
    {'main': 'Splattershot', 'id': '40', 'sub': 'Suction Bomb', 'special': 'Trizooka', 'special_points': '190p',
     'class': 'Shooter'},
    {'main': 'Splattershot Jr.', 'id': '10', 'sub': 'Splat Bomb', 'special': 'Big Bubbler', 'special_points': '180p',
     'class': 'Shooter'},
    {'main': 'Splattershot Nova', 'id': '100', 'sub': 'Point Sensor', 'special': 'Killer Wail 5.1',
     'special_points': '190p', 'class': 'Shooter'},
    {'main': 'Splattershot Pro', 'id': '70', 'sub': 'Angle Shooter', 'special': 'Crab Tank', 'special_points': '180p',
     'class': 'Shooter'},
    {'main': 'Sploosh-o-matic', 'id': '0', 'sub': 'Curling Bomb', 'special': 'Ultra Stamp', 'special_points': '180p',
     'class': 'Shooter'},
    {'main': 'Squeezer', 'id': '400', 'sub': 'Splash Wall', 'special': 'Trizooka', 'special_points': '200p',
     'class': 'Shooter'},
    {'main': 'Tenta Brella', 'id': '6010', 'sub': 'Squid Beakon', 'special': 'Ink Vac', 'special_points': '190p',
     'class': 'Brella'},
    {'main': 'Tenta Sorella Brella', 'id': '6011', 'sub': 'Ink Mine', 'special': 'Trizooka', 'special_points': '200p',
     'class': 'Brella'},
    {'main': 'Tentatek Splattershot', 'id': '41', 'sub': 'Splat Bomb', 'special': 'Triple Inkstrike',
     'special_points': '190p', 'class': 'Shooter'},
    {'main': 'Tri-Slosher', 'id': '3010', 'sub': 'Toxic Mist', 'special': 'Inkjet', 'special_points': '180p',
     'class': 'Slosher'},
    {'main': 'Tri-Slosher Nouveau', 'id': '3011', 'sub': 'Fizzy Bomb', 'special': 'Tacticooler',
     'special_points': '180p', 'class': 'Slosher'},
    {'main': 'Tri-Stringer', 'id': '7010', 'sub': 'Toxic Mist', 'special': 'Killer Wail 5.1', 'special_points': '180p',
     'class': 'Stringer'},
    {'main': 'Undercover Brella', 'id': '6020', 'sub': 'Ink Mine', 'special': 'Reefslider', 'special_points': '180p',
     'class': 'Brella'},
    {'main': 'Z+F Splat Charger', 'id': '2011', 'sub': 'Splash Wall', 'special': 'Triple Inkstrike',
     'special_points': '210p', 'class': 'Charger'},
    {'main': 'Z+F Splatterscope', 'id': '2021', 'sub': 'Splash Wall', 'special': 'Triple Inkstrike',
     'special_points': '210p', 'class': 'Charger'},
    {'main': 'Zink Mini Splatling', 'id': '4001', 'sub': 'Toxic Mist', 'special': 'Big Bubbler',
     'special_points': '200p', 'class': 'Splatling'},
]


def get_random(args: tuple[str]):
    if not args:
        weapons = [w['main'] for w in data]
    else:
        filter_by = ' '.join(list(args)).lower()
        weapons = [w['main'] for w in data if filter_by in [v.lower() for v in w.values()]]
        if not weapons:
            return None

    return random.choice(weapons)
