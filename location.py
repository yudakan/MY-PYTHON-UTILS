# -*- coding: utf-8 -*-
import requests


COUNTRIES = {
    'af': 'afghanistan',
    'ax': 'åland islands',
    'al': 'albania',
    'dz': 'algeria',
    'as': 'american samoa',
    'ad': 'andorra',
    'ao': 'angola',
    'ai': 'anguilla',
    'aq': 'antarctica',
    'ag': 'antigua and barbuda',
    'ar': 'argentina',
    'am': 'armenia',
    'aw': 'aruba',
    'au': 'australia',
    'at': 'austria',
    'az': 'azerbaijan',
    'bs': 'bahamas',
    'bh': 'bahrain',
    'bd': 'bangladesh',
    'bb': 'barbados',
    'by': 'belarus',
    'be': 'belgium',
    'bz': 'belize',
    'bj': 'benin',
    'bm': 'bermuda',
    'bt': 'bhutan',
    'bo': 'bolivia, plurinational state of',
    'bq': 'bonaire, sint eustatius and saba',
    'ba': 'bosnia and herzegovina',
    'bw': 'botswana',
    'bv': 'bouvet island',
    'br': 'brazil',
    'io': 'british indian ocean territory',
    'bn': 'brunei darussalam',
    'bg': 'bulgaria',
    'bf': 'burkina faso',
    'bi': 'burundi',
    'kh': 'cambodia',
    'cm': 'cameroon',
    'ca': 'canada',
    'cv': 'cape verde',
    'ky': 'cayman islands',
    'cf': 'central african republic',
    'td': 'chad',
    'cl': 'chile',
    'cn': 'china',
    'cx': 'christmas island',
    'cc': 'cocos (keeling) islands',
    'co': 'colombia',
    'km': 'comoros',
    'cg': 'congo',
    'cd': 'congo, the democratic republic of the',
    'ck': 'cook islands',
    'cr': 'costa rica',
    'ci': 'côte d\'ivoire',
    'hr': 'croatia',
    'cu': 'cuba',
    'cw': 'curaçao',
    'cy': 'cyprus',
    'cz': 'czech republic',
    'dk': 'denmark',
    'dj': 'djibouti',
    'dm': 'dominica',
    'do': 'dominican republic',
    'ec': 'ecuador',
    'eg': 'egypt',
    'sv': 'el salvador',
    'gq': 'equatorial guinea',
    'er': 'eritrea',
    'ee': 'estonia',
    'et': 'ethiopia',
    'fk': 'falkland islands (malvinas)',
    'fo': 'faroe islands',
    'fj': 'fiji',
    'fi': 'finland',
    'fr': 'france',
    'gf': 'french guiana',
    'pf': 'french polynesia',
    'tf': 'french southern territories',
    'ga': 'gabon',
    'gm': 'gambia',
    'ge': 'georgia',
    'de': 'germany',
    'gh': 'ghana',
    'gi': 'gibraltar',
    'gr': 'greece',
    'gl': 'greenland',
    'gd': 'grenada',
    'gp': 'guadeloupe',
    'gu': 'guam',
    'gt': 'guatemala',
    'gg': 'guernsey',
    'gn': 'guinea',
    'gw': 'guinea-bissau',
    'gy': 'guyana',
    'ht': 'haiti',
    'hm': 'heard island and mcdonald islands',
    'va': 'holy see (vatican city state)',
    'hn': 'honduras',
    'hk': 'hong kong',
    'hu': 'hungary',
    'is': 'iceland',
    'in': 'india',
    'id': 'indonesia',
    'ir': 'iran, islamic republic of',
    'iq': 'iraq',
    'ie': 'ireland',
    'im': 'isle of man',
    'il': 'israel',
    'it': 'italy',
    'jm': 'jamaica',
    'jp': 'japan',
    'je': 'jersey',
    'jo': 'jordan',
    'kz': 'kazakhstan',
    'ke': 'kenya',
    'ki': 'kiribati',
    'kp': 'korea, democratic people\'s republic of',
    'kr': 'korea, republic of',
    'kw': 'kuwait',
    'kg': 'kyrgyzstan',
    'la': 'lao people\'s democratic republic',
    'lv': 'latvia',
    'lb': 'lebanon',
    'ls': 'lesotho',
    'lr': 'liberia',
    'ly': 'libya',
    'li': 'liechtenstein',
    'lt': 'lithuania',
    'lu': 'luxembourg',
    'mo': 'macao',
    'mk': 'macedonia, the former yugoslav republic of',
    'mg': 'madagascar',
    'mw': 'malawi',
    'my': 'malaysia',
    'mv': 'maldives',
    'ml': 'mali',
    'mt': 'malta',
    'mh': 'marshall islands',
    'mq': 'martinique',
    'mr': 'mauritania',
    'mu': 'mauritius',
    'yt': 'mayotte',
    'mx': 'mexico',
    'fm': 'micronesia, federated states of',
    'md': 'moldova, republic of',
    'mc': 'monaco',
    'mn': 'mongolia',
    'me': 'montenegro',
    'ms': 'montserrat',
    'ma': 'morocco',
    'mz': 'mozambique',
    'mm': 'myanmar',
    'na': 'namibia',
    'nr': 'nauru',
    'np': 'nepal',
    'nl': 'netherlands',
    'nc': 'new caledonia',
    'nz': 'new zealand',
    'ni': 'nicaragua',
    'ne': 'niger',
    'ng': 'nigeria',
    'nu': 'niue',
    'nf': 'norfolk island',
    'mp': 'northern mariana islands',
    'no': 'norway',
    'om': 'oman',
    'pk': 'pakistan',
    'pw': 'palau',
    'ps': 'palestine, state of',
    'pa': 'panama',
    'pg': 'papua new guinea',
    'py': 'paraguay',
    'pe': 'peru',
    'ph': 'philippines',
    'pn': 'pitcairn',
    'pl': 'poland',
    'pt': 'portugal',
    'pr': 'puerto rico',
    'qa': 'qatar',
    're': 'réunion',
    'ro': 'romania',
    'ru': 'russian federation',
    'rw': 'rwanda',
    'bl': 'saint barthélemy',
    'sh': 'saint helena, ascension and tristan da cunha',
    'kn': 'saint kitts and nevis',
    'lc': 'saint lucia',
    'mf': 'saint martin (french part)',
    'pm': 'saint pierre and miquelon',
    'vc': 'saint vincent and the grenadines',
    'ws': 'samoa',
    'sm': 'san marino',
    'st': 'sao tome and principe',
    'sa': 'saudi arabia',
    'sn': 'senegal',
    'rs': 'serbia',
    'sc': 'seychelles',
    'sl': 'sierra leone',
    'sg': 'singapore',
    'sx': 'sint maarten (dutch part)',
    'sk': 'slovakia',
    'si': 'slovenia',
    'sb': 'solomon islands',
    'so': 'somalia',
    'za': 'south africa',
    'gs': 'south georgia and the south sandwich islands',
    'ss': 'south sudan',
    'es': 'spain',
    'lk': 'sri lanka',
    'sd': 'sudan',
    'sr': 'suriname',
    'sj': 'svalbard and jan mayen',
    'sz': 'swaziland',
    'se': 'sweden',
    'ch': 'switzerland',
    'sy': 'syrian arab republic',
    'tw': 'taiwan, province of china',
    'tj': 'tajikistan',
    'tz': 'tanzania, united republic of',
    'th': 'thailand',
    'tl': 'timor-leste',
    'tg': 'togo',
    'tk': 'tokelau',
    'to': 'tonga',
    'tt': 'trinidad and tobago',
    'tn': 'tunisia',
    'tr': 'turkey',
    'tm': 'turkmenistan',
    'tc': 'turks and caicos islands',
    'tv': 'tuvalu',
    'ug': 'uganda',
    'ua': 'ukraine',
    'ae': 'united arab emirates',
    'gb': 'united kingdom',
    'us': 'united states',
    'um': 'united states minor outlying islands',
    'uy': 'uruguay',
    'uz': 'uzbekistan',
    'vu': 'vanuatu',
    've': 'venezuela, bolivarian republic of',
    'vn': 'viet nam',
    'vg': 'virgin islands, british',
    'vi': 'virgin islands, u.s.',
    'wf': 'wallis and futuna',
    'eh': 'western sahara',
    'ye': 'yemen',
    'zm': 'zambia',
    'zw': 'zimbabwe',
}


def get_boundingbox_country(country, output_as='boundingbox'):
    """
    get the bounding box of a country in EPSG4326 given a country name

    Parameters
    ----------
    country : str
        name of the country in english and lowercase
    output_as : 'str
        chose from 'boundingbox' or 'center'. 
         - 'boundingbox' for [latmin, latmax, lonmin, lonmax]
         - 'center' for [latcenter, loncenter]

    Returns
    -------
    output : list
        list with coordinates as str
    """
    # create url
    url = '{0}{1}{2}'.format('http://nominatim.openstreetmap.org/search?country=',
                             country,
                             '&format=json&polygon=0')
    response = requests.get(url).json()[0]

    # parse response to list
    if output_as == 'boundingbox':
        lst = response[output_as]
        output = [float(i) for i in lst]
    if output_as == 'center':
        lst = [response.get(key) for key in ['lat','lon']]
        output = [float(i) for i in lst]
    return output


def is_inside_bb(lat, lng, latmin, latmax, lonmin, lonmax):

    return latmin <= lat <= latmax and lonmin <= lng <= lonmax