import requests, datetime, json
import re, flask
from threading import Thread

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const


za = flask.Flask(__name__)

#https://en.wikipedia.org/wiki/Zodiac
zodiacs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']

def insert_newlines(string, every=47):
    lines = []
    for i in range(0, len(string), every):
        lines.append(string[i:i+every])
    return '\n'.join(lines)



countries = [
{'timezones': ['Europe/Andorra'], 'code': 'AD', 'continent': 'Europe', 'name': 'Andorra', 'capital': 'Andorra la Vella'},
{'timezones': ['Asia/Kabul'], 'code': 'AF', 'continent': 'Asia', 'name': 'Afghanistan', 'capital': 'Kabul'},
{'timezones': ['America/Antigua'], 'code': 'AG', 'continent': 'North America', 'name': 'Antigua and Barbuda', 'capital': "St. John's"},
{'timezones': ['Europe/Tirane'], 'code': 'AL', 'continent': 'Europe', 'name': 'Albania', 'capital': 'Tirana'},
{'timezones': ['Asia/Yerevan'], 'code': 'AM', 'continent': 'Asia', 'name': 'Armenia', 'capital': 'Yerevan'},
{'timezones': ['Africa/Luanda'], 'code': 'AO', 'continent': 'Africa', 'name': 'Angola', 'capital': 'Luanda'},
{'timezones': ['America/Argentina/Buenos_Aires', 'America/Argentina/Cordoba', 'America/Argentina/Jujuy', 'America/Argentina/Tucuman', 'America/Argentina/Catamarca', 'America/Argentina/La_Rioja', 'America/Argentina/San_Juan', 'America/Argentina/Mendoza', 'America/Argentina/Rio_Gallegos', 'America/Argentina/Ushuaia'], 'code': 'AR', 'continent': 'South America', 'name': 'Argentina', 'capital': 'Buenos Aires'},
{'timezones': ['Europe/Vienna'], 'code': 'AT', 'continent': 'Europe', 'name': 'Austria', 'capital': 'Vienna'},
{'timezones': ['Australia/Lord_Howe', 'Australia/Hobart', 'Australia/Currie', 'Australia/Melbourne', 'Australia/Sydney', 'Australia/Broken_Hill', 'Australia/Brisbane', 'Australia/Lindeman', 'Australia/Adelaide', 'Australia/Darwin', 'Australia/Perth'], 'code': 'AU', 'continent': 'Oceania', 'name': 'Australia', 'capital': 'Canberra'},
{'timezones': ['Asia/Baku'], 'code': 'AZ', 'continent': 'Asia', 'name': 'Azerbaijan', 'capital': 'Baku'},
{'timezones': ['America/Barbados'], 'code': 'BB', 'continent': 'North America', 'name': 'Barbados', 'capital': 'Bridgetown'},
{'timezones': ['Asia/Dhaka'], 'code': 'BD', 'continent': 'Asia', 'name': 'Bangladesh', 'capital': 'Dhaka'},
{'timezones': ['Europe/Brussels'], 'code': 'BE', 'continent': 'Europe', 'name': 'Belgium', 'capital': 'Brussels'},
{'timezones': ['Africa/Ouagadougou'], 'code': 'BF', 'continent': 'Africa', 'name': 'Burkina Faso', 'capital': 'Ouagadougou'},
{'timezones': ['Europe/Sofia'], 'code': 'BG', 'continent': 'Europe', 'name': 'Bulgaria', 'capital': 'Sofia'},
{'timezones': ['Asia/Bahrain'], 'code': 'BH', 'continent': 'Asia', 'name': 'Bahrain', 'capital': 'Manama'},
{'timezones': ['Africa/Bujumbura'], 'code': 'BI', 'continent': 'Africa', 'name': 'Burundi', 'capital': 'Bujumbura'},
{'timezones': ['Africa/Porto-Novo'], 'code': 'BJ', 'continent': 'Africa', 'name': 'Benin', 'capital': 'Porto-Novo'},
{'timezones': ['Asia/Brunei'], 'code': 'BN', 'continent': 'Asia', 'name': 'Brunei Darussalam', 'capital': 'Bandar Seri Begawan'},
{'timezones': ['America/La_Paz'], 'code': 'BO', 'continent': 'South America', 'name': 'Bolivia', 'capital': 'Sucre'},
{'timezones': ['America/Noronha', 'America/Belem', 'America/Fortaleza', 'America/Recife', 'America/Araguaina', 'America/Maceio', 'America/Bahia', 'America/Sao_Paulo', 'America/Campo_Grande', 'America/Cuiaba', 'America/Porto_Velho', 'America/Boa_Vista', 'America/Manaus', 'America/Eirunepe', 'America/Rio_Branco'], 'code': 'BR', 'continent': 'South America', 'name': 'Brazil', 'capital': 'Bras\xc3\xadlia'},
{'timezones': ['America/Nassau'], 'code': 'BS', 'continent': 'North America', 'name': 'Bahamas', 'capital': 'Nassau'},
{'timezones': ['Asia/Thimphu'], 'code': 'BT', 'continent': 'Asia', 'name': 'Bhutan', 'capital': 'Thimphu'},
{'timezones': ['Africa/Gaborone'], 'code': 'BW', 'continent': 'Africa', 'name': 'Botswana', 'capital': 'Gaborone'},
{'timezones': ['Europe/Minsk'], 'code': 'BY', 'continent': 'Europe', 'name': 'Belarus', 'capital': 'Minsk'},
{'timezones': ['America/Belize'], 'code': 'BZ', 'continent': 'North America', 'name': 'Belize', 'capital': 'Belmopan'},
{'timezones': ['America/St_Johns', 'America/Halifax', 'America/Glace_Bay', 'America/Moncton', 'America/Goose_Bay', 'America/Blanc-Sablon', 'America/Montreal', 'America/Toronto', 'America/Nipigon', 'America/Thunder_Bay', 'America/Pangnirtung', 'America/Iqaluit', 'America/Atikokan', 'America/Rankin_Inlet', 'America/Winnipeg', 'America/Rainy_River', 'America/Cambridge_Bay', 'America/Regina', 'America/Swift_Current', 'America/Edmonton', 'America/Yellowknife', 'America/Inuvik', 'America/Dawson_Creek', 'America/Vancouver', 'America/Whitehorse', 'America/Dawson'], 'code': 'CA', 'continent': 'North America', 'name': 'Canada', 'capital': 'Ottawa'},
{'timezones': ['Africa/Kinshasa', 'Africa/Lubumbashi'], 'code': 'CD', 'continent': 'Africa', 'name': 'Democratic Republic of the Congo', 'capital': 'Kinshasa'},
{'timezones': ['Africa/Brazzaville'], 'code': 'CG', 'continent': 'Africa', 'name': 'Republic of the Congo', 'capital': 'Brazzaville'},
{'timezones': ['Africa/Abidjan'], 'code': 'CI', 'continent': 'Africa', 'name': "C\xc3\xb4te d'Ivoire", 'capital': 'Yamoussoukro'},
{'timezones': ['America/Santiago', 'Pacific/Easter'], 'code': 'CL', 'continent': 'South America', 'name': 'Chile', 'capital': 'Santiago'},
{'timezones': ['Africa/Douala'], 'code': 'CM', 'continent': 'Africa', 'name': 'Cameroon', 'capital': 'Yaound\xc3\xa9'},
{'timezones': ['Asia/Shanghai', 'Asia/Harbin', 'Asia/Chongqing', 'Asia/Urumqi', 'Asia/Kashgar'], 'code': 'CN', 'continent': 'Asia', 'name': "People's Republic of China", 'capital': 'Beijing'},
{'timezones': ['America/Bogota'], 'code': 'CO', 'continent': 'South America', 'name': 'Colombia', 'capital': 'Bogot\xc3\xa1'},
{'timezones': ['America/Costa_Rica'], 'code': 'CR', 'continent': 'North America', 'name': 'Costa Rica', 'capital': 'San Jos\xc3\xa9'},
{'timezones': ['America/Havana'], 'code': 'CU', 'continent': 'North America', 'name': 'Cuba', 'capital': 'Havana'},
{'timezones': ['Atlantic/Cape_Verde'], 'code': 'CV', 'continent': 'Africa', 'name': 'Cape Verde', 'capital': 'Praia'},
{'timezones': ['Asia/Nicosia'], 'code': 'CY', 'continent': 'Asia', 'name': 'Cyprus', 'capital': 'Nicosia'},
{'timezones': ['Europe/Prague'], 'code': 'CZ', 'continent': 'Europe', 'name': 'Czech Republic', 'capital': 'Prague'},
{'timezones': ['Europe/Berlin'], 'code': 'DE', 'continent': 'Europe', 'name': 'Germany', 'capital': 'Berlin'},
{'timezones': ['Africa/Djibouti'], 'code': 'DJ', 'continent': 'Africa', 'name': 'Djibouti', 'capital': 'Djibouti City'},
{'timezones': ['Europe/Copenhagen'], 'code': 'DK', 'continent': 'Europe', 'name': 'Denmark', 'capital': 'Copenhagen'},
{'timezones': ['America/Dominica'], 'code': 'DM', 'continent': 'North America', 'name': 'Dominica', 'capital': 'Roseau'},
{'timezones': ['America/Santo_Domingo'], 'code': 'DO', 'continent': 'North America', 'name': 'Dominican Republic', 'capital': 'Santo Domingo'},
{'timezones': ['America/Guayaquil', 'Pacific/Galapagos'], 'code': 'EC', 'continent': 'South America', 'name': 'Ecuador', 'capital': 'Quito'},
{'timezones': ['Europe/Tallinn'], 'code': 'EE', 'continent': 'Europe', 'name': 'Estonia', 'capital': 'Tallinn'},
{'timezones': ['Africa/Cairo'], 'code': 'EG', 'continent': 'Africa', 'name': 'Egypt', 'capital': 'Cairo'},
{'timezones': ['Africa/Asmera'], 'code': 'ER', 'continent': 'Africa', 'name': 'Eritrea', 'capital': 'Asmara'},
{'timezones': ['Africa/Addis_Ababa'], 'code': 'ET', 'continent': 'Africa', 'name': 'Ethiopia', 'capital': 'Addis Ababa'},
{'timezones': ['Europe/Helsinki'], 'code': 'FI', 'continent': 'Europe', 'name': 'Finland', 'capital': 'Helsinki'},
{'timezones': ['Pacific/Fiji'], 'code': 'FJ', 'continent': 'Oceania', 'name': 'Fiji', 'capital': 'Suva'},
{'timezones': ['Europe/Paris'], 'code': 'FR', 'continent': 'Europe', 'name': 'France', 'capital': 'Paris'},
{'timezones': ['Africa/Libreville'], 'code': 'GA', 'continent': 'Africa', 'name': 'Gabon', 'capital': 'Libreville'},
{'timezones': ['Asia/Tbilisi'], 'code': 'GE', 'continent': 'Asia', 'name': 'Georgia', 'capital': 'Tbilisi'},
{'timezones': ['Africa/Accra'], 'code': 'GH', 'continent': 'Africa', 'name': 'Ghana', 'capital': 'Accra'},
{'timezones': ['Africa/Banjul'], 'code': 'GM', 'continent': 'Africa', 'name': 'The Gambia', 'capital': 'Banjul'},
{'timezones': ['Africa/Conakry'], 'code': 'GN', 'continent': 'Africa', 'name': 'Guinea', 'capital': 'Conakry'},
{'timezones': ['Europe/Athens'], 'code': 'GR', 'continent': 'Europe', 'name': 'Greece', 'capital': 'Athens'},
{'timezones': ['America/Guatemala'], 'code': 'GT', 'continent': 'North America', 'name': 'Guatemala', 'capital': 'Guatemala City'},
{'timezones': ['America/Guatemala'], 'code': 'GT', 'continent': 'North America', 'name': 'Haiti', 'capital': 'Port-au-Prince'},
{'timezones': ['Africa/Bissau'], 'code': 'GW', 'continent': 'Africa', 'name': 'Guinea-Bissau', 'capital': 'Bissau'},
{'timezones': ['America/Guyana'], 'code': 'GY', 'continent': 'South America', 'name': 'Guyana', 'capital': 'Georgetown'},
{'timezones': ['America/Tegucigalpa'], 'code': 'HN', 'continent': 'North America', 'name': 'Honduras', 'capital': 'Tegucigalpa'},
{'timezones': ['Europe/Budapest'], 'code': 'HU', 'continent': 'Europe', 'name': 'Hungary', 'capital': 'Budapest'},
{'timezones': ['Asia/Jakarta', 'Asia/Pontianak', 'Asia/Makassar', 'Asia/Jayapura'], 'code': 'ID', 'continent': 'Asia', 'name': 'Indonesia', 'capital': 'Jakarta'},
{'timezones': ['Europe/Dublin'], 'code': 'IE', 'continent': 'Europe', 'name': 'Republic of Ireland', 'capital': 'Dublin'},
{'timezones': ['Asia/Jerusalem'], 'code': 'IL', 'continent': 'Asia', 'name': 'Israel', 'capital': 'Jerusalem'},
{'timezones': ['Asia/Calcutta'], 'code': 'IN', 'continent': 'Asia', 'name': 'India', 'capital': 'New Delhi'},
{'timezones': ['Asia/Baghdad'], 'code': 'IQ', 'continent': 'Asia', 'name': 'Iraq', 'capital': 'Baghdad'},
{'timezones': ['Asia/Tehran'], 'code': 'IR', 'continent': 'Asia', 'name': 'Iran', 'capital': 'Tehran'},
{'timezones': ['Atlantic/Reykjavik'], 'code': 'IS', 'continent': 'Europe', 'name': 'Iceland', 'capital': 'Reykjav\xc3\xadk'},
{'timezones': ['Europe/Rome'], 'code': 'IT', 'continent': 'Europe', 'name': 'Italy', 'capital': 'Rome'},
{'timezones': ['America/Jamaica'], 'code': 'JM', 'continent': 'North America', 'name': 'Jamaica', 'capital': 'Kingston'},
{'timezones': ['Asia/Amman'], 'code': 'JO', 'continent': 'Asia', 'name': 'Jordan', 'capital': 'Amman'},
{'timezones': ['Asia/Tokyo'], 'code': 'JP', 'continent': 'Asia', 'name': 'Japan', 'capital': 'Tokyo'},
{'timezones': ['Africa/Nairobi'], 'code': 'KE', 'continent': 'Africa', 'name': 'Kenya', 'capital': 'Nairobi'},
{'timezones': ['Asia/Bishkek'], 'code': 'KG', 'continent': 'Asia', 'name': 'Kyrgyzstan', 'capital': 'Bishkek'},
{'timezones': ['Pacific/Tarawa', 'Pacific/Enderbury', 'Pacific/Kiritimati'], 'code': 'KI', 'continent': 'Oceania', 'name': 'Kiribati', 'capital': 'Tarawa'},
{'timezones': ['Asia/Pyongyang'], 'code': 'KP', 'continent': 'Asia', 'name': 'North Korea', 'capital': 'Pyongyang'},
{'timezones': ['Asia/Seoul'], 'code': 'KR', 'continent': 'Asia', 'name': 'South Korea', 'capital': 'Seoul'},
{'timezones': ['Asia/Kuwait'], 'code': 'KW', 'continent': 'Asia', 'name': 'Kuwait', 'capital': 'Kuwait City'},
{'timezones': ['Asia/Beirut'], 'code': 'LB', 'continent': 'Asia', 'name': 'Lebanon', 'capital': 'Beirut'},
{'timezones': ['Europe/Vaduz'], 'code': 'LI', 'continent': 'Europe', 'name': 'Liechtenstein', 'capital': 'Vaduz'},
{'timezones': ['Africa/Monrovia'], 'code': 'LR', 'continent': 'Africa', 'name': 'Liberia', 'capital': 'Monrovia'},
{'timezones': ['Africa/Maseru'], 'code': 'LS', 'continent': 'Africa', 'name': 'Lesotho', 'capital': 'Maseru'},
{'timezones': ['Europe/Vilnius'], 'code': 'LT', 'continent': 'Europe', 'name': 'Lithuania', 'capital': 'Vilnius'},
{'timezones': ['Europe/Luxembourg'], 'code': 'LU', 'continent': 'Europe', 'name': 'Luxembourg', 'capital': 'Luxembourg City'},
{'timezones': ['Europe/Riga'], 'code': 'LV', 'continent': 'Europe', 'name': 'Latvia', 'capital': 'Riga'},
{'timezones': ['Africa/Tripoli'], 'code': 'LY', 'continent': 'Africa', 'name': 'Libya', 'capital': 'Tripoli'},
{'timezones': ['Indian/Antananarivo'], 'code': 'MG', 'continent': 'Africa', 'name': 'Madagascar', 'capital': 'Antananarivo'},
{'timezones': ['Pacific/Majuro', 'Pacific/Kwajalein'], 'code': 'MH', 'continent': 'Oceania', 'name': 'Marshall Islands', 'capital': 'Majuro'},
{'timezones': ['Europe/Skopje'], 'code': 'MK', 'continent': 'Europe', 'name': 'Macedonia', 'capital': 'Skopje'},
{'timezones': ['Africa/Bamako'], 'code': 'ML', 'continent': 'Africa', 'name': 'Mali', 'capital': 'Bamako'},
{'timezones': ['Asia/Rangoon'], 'code': 'MM', 'continent': 'Asia', 'name': 'Myanmar', 'capital': 'Naypyidaw'},
{'timezones': ['Asia/Ulaanbaatar', 'Asia/Hovd', 'Asia/Choibalsan'], 'code': 'MN', 'continent': 'Asia', 'name': 'Mongolia', 'capital': 'Ulaanbaatar'},
{'timezones': ['Africa/Nouakchott'], 'code': 'MR', 'continent': 'Africa', 'name': 'Mauritania', 'capital': 'Nouakchott'},
{'timezones': ['Europe/Malta'], 'code': 'MT', 'continent': 'Europe', 'name': 'Malta', 'capital': 'Valletta'},
{'timezones': ['Indian/Mauritius'], 'code': 'MU', 'continent': 'Africa', 'name': 'Mauritius', 'capital': 'Port Louis'},
{'timezones': ['Indian/Maldives'], 'code': 'MV', 'continent': 'Asia', 'name': 'Maldives', 'capital': 'Mal\xc3\xa9'},
{'timezones': ['Africa/Blantyre'], 'code': 'MW', 'continent': 'Africa', 'name': 'Malawi', 'capital': 'Lilongwe'},
{'timezones': ['America/Mexico_City', 'America/Cancun', 'America/Merida', 'America/Monterrey', 'America/Mazatlan', 'America/Chihuahua', 'America/Hermosillo', 'America/Tijuana'], 'code': 'MX', 'continent': 'North America', 'name': 'Mexico', 'capital': 'Mexico City'},
{'timezones': ['Asia/Kuala_Lumpur', 'Asia/Kuching'], 'code': 'MY', 'continent': 'Asia', 'name': 'Malaysia', 'capital': 'Kuala Lumpur'},
{'timezones': ['Africa/Maputo'], 'code': 'MZ', 'continent': 'Africa', 'name': 'Mozambique', 'capital': 'Maputo'},
{'timezones': ['Africa/Windhoek'], 'code': 'NA', 'continent': 'Africa', 'name': 'Namibia', 'capital': 'Windhoek'},
{'timezones': ['Africa/Niamey'], 'code': 'NE', 'continent': 'Africa', 'name': 'Niger', 'capital': 'Niamey'},
{'timezones': ['Africa/Lagos'], 'code': 'NG', 'continent': 'Africa', 'name': 'Nigeria', 'capital': 'Abuja'},
{'timezones': ['America/Managua'], 'code': 'NI', 'continent': 'North America', 'name': 'Nicaragua', 'capital': 'Managua'},
{'timezones': ['Europe/Amsterdam'], 'code': 'NL', 'continent': 'Europe', 'name': 'Kingdom of the Netherlands', 'capital': 'Amsterdam'},
{'timezones': ['Europe/Oslo'], 'code': 'NO', 'continent': 'Europe', 'name': 'Norway', 'capital': 'Oslo'},
{'timezones': ['Asia/Katmandu'], 'code': 'NP', 'continent': 'Asia', 'name': 'Nepal', 'capital': 'Kathmandu'},
{'timezones': ['Pacific/Nauru'], 'code': 'NR', 'continent': 'Oceania', 'name': 'Nauru', 'capital': 'Yaren'},
{'timezones': ['Pacific/Auckland', 'Pacific/Chatham'], 'code': 'NZ', 'continent': 'Oceania', 'name': 'New Zealand', 'capital': 'Wellington'},
{'timezones': ['Asia/Muscat'], 'code': 'OM', 'continent': 'Asia', 'name': 'Oman', 'capital': 'Muscat'},
{'timezones': ['America/Panama'], 'code': 'PA', 'continent': 'North America', 'name': 'Panama', 'capital': 'Panama City'},
{'timezones': ['America/Lima'], 'code': 'PE', 'continent': 'South America', 'name': 'Peru', 'capital': 'Lima'},
{'timezones': ['Pacific/Port_Moresby'], 'code': 'PG', 'continent': 'Oceania', 'name': 'Papua New Guinea', 'capital': 'Port Moresby'},
{'timezones': ['Asia/Manila'], 'code': 'PH', 'continent': 'Asia', 'name': 'Philippines', 'capital': 'Manila'},
{'timezones': ['Asia/Karachi'], 'code': 'PK', 'continent': 'Asia', 'name': 'Pakistan', 'capital': 'Islamabad'},
{'timezones': ['Europe/Warsaw'], 'code': 'PL', 'continent': 'Europe', 'name': 'Poland', 'capital': 'Warsaw'},
{'timezones': ['Europe/Lisbon', 'Atlantic/Madeira', 'Atlantic/Azores'], 'code': 'PT', 'continent': 'Europe', 'name': 'Portugal', 'capital': 'Lisbon'},
{'timezones': ['Pacific/Palau'], 'code': 'PW', 'continent': 'Oceania', 'name': 'Palau', 'capital': 'Ngerulmud'},
{'timezones': ['America/Asuncion'], 'code': 'PY', 'continent': 'South America', 'name': 'Paraguay', 'capital': 'Asunci\xc3\xb3n'},
{'timezones': ['Asia/Qatar'], 'code': 'QA', 'continent': 'Asia', 'name': 'Qatar', 'capital': 'Doha'},
{'timezones': ['Europe/Bucharest'], 'code': 'RO', 'continent': 'Europe', 'name': 'Romania', 'capital': 'Bucharest'},
{'timezones': ['Europe/Kaliningrad', 'Europe/Moscow', 'Europe/Volgograd', 'Europe/Samara', 'Asia/Yekaterinburg', 'Asia/Omsk', 'Asia/Novosibirsk', 'Asia/Krasnoyarsk', 'Asia/Irkutsk', 'Asia/Yakutsk', 'Asia/Vladivostok', 'Asia/Sakhalin', 'Asia/Magadan', 'Asia/Kamchatka', 'Asia/Anadyr'], 'code': 'RU', 'continent': 'Europe', 'name': 'Russia', 'capital': 'Moscow'},
{'timezones': ['Africa/Kigali'], 'code': 'RW', 'continent': 'Africa', 'name': 'Rwanda', 'capital': 'Kigali'},
{'timezones': ['Asia/Riyadh'], 'code': 'SA', 'continent': 'Asia', 'name': 'Saudi Arabia', 'capital': 'Riyadh'},
{'timezones': ['Pacific/Guadalcanal'], 'code': 'SB', 'continent': 'Oceania', 'name': 'Solomon Islands', 'capital': 'Honiara'},
{'timezones': ['Indian/Mahe'], 'code': 'SC', 'continent': 'Africa', 'name': 'Seychelles', 'capital': 'Victoria'},
{'timezones': ['Africa/Khartoum'], 'code': 'SD', 'continent': 'Africa', 'name': 'Sudan', 'capital': 'Khartoum'},
{'timezones': ['Europe/Stockholm'], 'code': 'SE', 'continent': 'Europe', 'name': 'Sweden', 'capital': 'Stockholm'},
{'timezones': ['Asia/Singapore'], 'code': 'SG', 'continent': 'Asia', 'name': 'Singapore', 'capital': 'Singapore'},
{'timezones': ['Europe/Ljubljana'], 'code': 'SI', 'continent': 'Europe', 'name': 'Slovenia', 'capital': 'Ljubljana'},
{'timezones': ['Europe/Bratislava'], 'code': 'SK', 'continent': 'Europe', 'name': 'Slovakia', 'capital': 'Bratislava'},
{'timezones': ['Africa/Freetown'], 'code': 'SL', 'continent': 'Africa', 'name': 'Sierra Leone', 'capital': 'Freetown'},
{'timezones': ['Europe/San_Marino'], 'code': 'SM', 'continent': 'Europe', 'name': 'San Marino', 'capital': 'San Marino'},
{'timezones': ['Africa/Dakar'], 'code': 'SN', 'continent': 'Africa', 'name': 'Senegal', 'capital': 'Dakar'},
{'timezones': ['Africa/Mogadishu'], 'code': 'SO', 'continent': 'Africa', 'name': 'Somalia', 'capital': 'Mogadishu'},
{'timezones': ['America/Paramaribo'], 'code': 'SR', 'continent': 'South America', 'name': 'Suriname', 'capital': 'Paramaribo'},
{'timezones': ['Africa/Sao_Tome'], 'code': 'ST', 'continent': 'Africa', 'name': 'S\xc3\xa3o Tom\xc3\xa9 and Pr\xc3\xadncipe', 'capital': 'S\xc3\xa3o Tom\xc3\xa9'},
{'timezones': ['Asia/Damascus'], 'code': 'SY', 'continent': 'Asia', 'name': 'Syria', 'capital': 'Damascus'},
{'timezones': ['Africa/Lome'], 'code': 'TG', 'continent': 'Africa', 'name': 'Togo', 'capital': 'Lom\xc3\xa9'},
{'timezones': ['Asia/Bangkok'], 'code': 'TH', 'continent': 'Asia', 'name': 'Thailand', 'capital': 'Bangkok'},
{'timezones': ['Asia/Dushanbe'], 'code': 'TJ', 'continent': 'Asia', 'name': 'Tajikistan', 'capital': 'Dushanbe'},
{'timezones': ['Asia/Ashgabat'], 'code': 'TM', 'continent': 'Asia', 'name': 'Turkmenistan', 'capital': 'Ashgabat'},
{'timezones': ['Africa/Tunis'], 'code': 'TN', 'continent': 'Africa', 'name': 'Tunisia', 'capital': 'Tunis'},
{'timezones': ['Pacific/Tongatapu'], 'code': 'TO', 'continent': 'Oceania', 'name': 'Tonga', 'capital': 'Nuku\xca\xbbalofa'},
{'timezones': ['Europe/Istanbul'], 'code': 'TR', 'continent': 'Asia', 'name': 'Turkey', 'capital': 'Ankara'},
{'timezones': ['America/Port_of_Spain'], 'code': 'TT', 'continent': 'North America', 'name': 'Trinidad and Tobago', 'capital': 'Port of Spain'},
{'timezones': ['Pacific/Funafuti'], 'code': 'TV', 'continent': 'Oceania', 'name': 'Tuvalu', 'capital': 'Funafuti'},
{'timezones': ['Africa/Dar_es_Salaam'], 'code': 'TZ', 'continent': 'Africa', 'name': 'Tanzania', 'capital': 'Dodoma'},
{'timezones': ['Europe/Kiev', 'Europe/Uzhgorod', 'Europe/Zaporozhye', 'Europe/Simferopol'], 'code': 'UA', 'continent': 'Europe', 'name': 'Ukraine', 'capital': 'Kiev'},
{'timezones': ['Africa/Kampala'], 'code': 'UG', 'continent': 'Africa', 'name': 'Uganda', 'capital': 'Kampala'},
{'timezones': ['America/New_York', 'America/Detroit', 'America/Kentucky/Louisville', 'America/Kentucky/Monticello', 'America/Indiana/Indianapolis', 'America/Indiana/Marengo', 'America/Indiana/Knox', 'America/Indiana/Vevay', 'America/Chicago', 'America/Indiana/Vincennes', 'America/Indiana/Petersburg', 'America/Menominee', 'America/North_Dakota/Center', 'America/North_Dakota/New_Salem', 'America/Denver', 'America/Boise', 'America/Shiprock', 'America/Phoenix', 'America/Los_Angeles', 'America/Anchorage', 'America/Juneau', 'America/Yakutat', 'America/Nome', 'America/Adak', 'Pacific/Honolulu'], 'code': 'US', 'continent': 'North America', 'name': 'United States', 'capital': 'Washington, D.C.'},
{'timezones': ['America/Montevideo'], 'code': 'UY', 'continent': 'South America', 'name': 'Uruguay', 'capital': 'Montevideo'},
{'timezones': ['Asia/Samarkand', 'Asia/Tashkent'], 'code': 'UZ', 'continent': 'Asia', 'name': 'Uzbekistan', 'capital': 'Tashkent'},
{'timezones': ['Europe/Vatican'], 'code': 'VA', 'continent': 'Europe', 'name': 'Vatican City', 'capital': 'Vatican City'},
{'timezones': ['America/Caracas'], 'code': 'VE', 'continent': 'South America', 'name': 'Venezuela', 'capital': 'Caracas'},
{'timezones': ['Asia/Saigon'], 'code': 'VN', 'continent': 'Asia', 'name': 'Vietnam', 'capital': 'Hanoi'},
{'timezones': ['Pacific/Efate'], 'code': 'VU', 'continent': 'Oceania', 'name': 'Vanuatu', 'capital': 'Port Vila'},
{'timezones': ['Asia/Aden'], 'code': 'YE', 'continent': 'Asia', 'name': 'Yemen', 'capital': "Sana'a"},
{'timezones': ['Africa/Lusaka'], 'code': 'ZM', 'continent': 'Africa', 'name': 'Zambia', 'capital': 'Lusaka'},
{'timezones': ['Africa/Harare'], 'code': 'ZW', 'continent': 'Africa', 'name': 'Zimbabwe', 'capital': 'Harare'},
{'timezones': ['Africa/Algiers'], 'code': 'DZ', 'continent': 'Africa', 'name': 'Algeria', 'capital': 'Algiers'},
{'timezones': ['Europe/Sarajevo'], 'code': 'BA', 'continent': 'Europe', 'name': 'Bosnia and Herzegovina', 'capital': 'Sarajevo'},
{'timezones': ['Asia/Phnom_Penh'], 'code': 'KH', 'continent': 'Asia', 'name': 'Cambodia', 'capital': 'Phnom Penh'},
{'timezones': ['Africa/Bangui'], 'code': 'CF', 'continent': 'Africa', 'name': 'Central African Republic', 'capital': 'Bangui'},
{'timezones': ['Africa/Ndjamena'], 'code': 'TD', 'continent': 'Africa', 'name': 'Chad', 'capital': "N'Djamena"},
{'timezones': ['Indian/Comoro'], 'code': 'KM', 'continent': 'Africa', 'name': 'Comoros', 'capital': 'Moroni'},
{'timezones': ['Europe/Zagreb'], 'code': 'HR', 'continent': 'Europe', 'name': 'Croatia', 'capital': 'Zagreb'},
{'timezones': ['Asia/Dili'], 'code': 'TL', 'continent': 'Asia', 'name': 'East Timor', 'capital': 'Dili'},
{'timezones': ['America/El_Salvador'], 'code': 'SV', 'continent': 'North America', 'name': 'El Salvador', 'capital': 'San Salvador'},
{'timezones': ['Africa/Malabo'], 'code': 'GQ', 'continent': 'Africa', 'name': 'Equatorial Guinea', 'capital': 'Malabo'},
{'timezones': ['America/Grenada'], 'code': 'GD', 'continent': 'North America', 'name': 'Grenada', 'capital': "St. George's"},
{'timezones': ['Asia/Almaty', 'Asia/Qyzylorda', 'Asia/Aqtobe', 'Asia/Aqtau', 'Asia/Oral'], 'code': 'KZ', 'continent': 'Asia', 'name': 'Kazakhstan', 'capital': 'Astana'},
{'timezones': ['Asia/Vientiane'], 'code': 'LA', 'continent': 'Asia', 'name': 'Laos', 'capital': 'Vientiane'},
{'timezones': ['Pacific/Truk', 'Pacific/Ponape', 'Pacific/Kosrae'], 'code': 'FM', 'continent': 'Oceania', 'name': 'Federated States of Micronesia', 'capital': 'Palikir'},
{'timezones': ['Europe/Chisinau'], 'code': 'MD', 'continent': 'Europe', 'name': 'Moldova', 'capital': 'Chi\xc5\x9fin\xc4\x83u'},
{'timezones': ['Europe/Monaco'], 'code': 'MC', 'continent': 'Europe', 'name': 'Monaco', 'capital': 'Monaco'},
{'timezones': ['Europe/Podgorica'], 'code': 'ME', 'continent': 'Europe', 'name': 'Montenegro', 'capital': 'Podgorica'},
{'timezones': ['Africa/Casablanca'], 'code': 'MA', 'continent': 'Africa', 'name': 'Morocco', 'capital': 'Rabat'},
{'timezones': ['America/St_Kitts'], 'code': 'KN', 'continent': 'North America', 'name': 'Saint Kitts and Nevis', 'capital': 'Basseterre'},
{'timezones': ['America/St_Lucia'], 'code': 'LC', 'continent': 'North America', 'name': 'Saint Lucia', 'capital': 'Castries'},
{'timezones': ['America/St_Vincent'], 'code': 'VC', 'continent': 'North America', 'name': 'Saint Vincent and the Grenadines', 'capital': 'Kingstown'},
{'timezones': ['Pacific/Apia'], 'code': 'WS', 'continent': 'Oceania', 'name': 'Samoa', 'capital': 'Apia'},
{'timezones': ['Europe/Belgrade'], 'code': 'RS', 'continent': 'Europe', 'name': 'Serbia', 'capital': 'Belgrade'},
{'timezones': ['Africa/Johannesburg'], 'code': 'ZA', 'continent': 'Africa', 'name': 'South Africa', 'capital': 'Pretoria'},
{'timezones': ['Europe/Madrid', 'Africa/Ceuta', 'Atlantic/Canary'], 'code': 'ES', 'continent': 'Europe', 'name': 'Spain', 'capital': 'Madrid'},
{'timezones': ['Asia/Colombo'], 'code': 'LK', 'continent': 'Asia', 'name': 'Sri Lanka', 'capital': 'Sri Jayewardenepura Kotte'},
{'timezones': ['Africa/Mbabane'], 'code': 'SZ', 'continent': 'Africa', 'name': 'Swaziland', 'capital': 'Mbabane'},
{'timezones': ['Europe/Zurich'], 'code': 'CH', 'continent': 'Europe', 'name': 'Switzerland', 'capital': 'Bern'},
{'timezones': ['Asia/Dubai'], 'code': 'AE', 'continent': 'Asia', 'name': 'United Arab Emirates', 'capital': 'Abu Dhabi'},
{'timezones': ['Europe/London'], 'code': 'GB', 'continent': 'Europe', 'name': 'United Kingdom', 'capital': 'London'}
]

def get_geo_cords(place, countrycode):
	#https://www.geonames.org/search.html?q=Stockholm&country=SE
	life = requests.get("https://www.geonames.org/search.html?q={}&country={}".format(place.title(),countrycode.upper())).text
	if 'We have found no places with the name' in life:
		return False
	asd = re.findall(r'<span class=\"latitude\">(.*)<\/span><span\sclass\=\"longitude\">(.*)</span>', life)
#	print(life, asd)
	stuff = asd[0]
	return stuff 

def explain_element(element):
    #print('i got input', element)
    blob = {"Fire":"""Like fire itself, fire signs tend to be passionate, dynamic, and temperamental. Fire can keep you warm, or it can do great destruction. While fire burns out quickly without fuel to keep it going, it can also regenerate its power from the ashes. A single spark can set off a forest fire. As a result, fire signs need to be nurtured and managed carefully.""","Air":"""Air signs are all about action, ideas, and motion—they are the “winds of change.” When a strong gust hits you, you can’t help but move. While some within their ranks may be true-life “airheads,” others are as powerful as a gravity-defying G-force. Air signs bring everyone a breath of fresh air when things start to get stale. Like the breeze, you can’t quite catch them, and you never know where they’ll drop you once they sweep you up. It will almost always been an adventure, though.""","Earth":"""Earth signs keep it real. They are the “grounded” people on the planet, the ones who bring us down to earth and remind us to start with a solid foundation. Slow and steady, these “builders” are loyal and stable, and stick by their people through hard times. On good days, they’re practical; at worst, they can be materialistic or too focused on the surface of things to dig into the depths.""","Water":"""Intuitive, emotional and ultra-sensitive, water signs can be as mysterious as the ocean itself. Like water, they can be refreshing, or they can drown you in their depths. These signs often have intense dreams and borderline-psychic intuition. Security is important to them—after all, water needs a container, or it dries up and disappears."""}
    return blob.get(element.lower().title())

def explain_house(mitthus):
	num = {}
	num["House1"] = {}
	num["House1"] =  {"Housenumber": 1, 	"sign": "Aries", "Latin motto":"Vita", "translate":"Life", "translated":"House of Self", "explain":"Physical appearance, traits and characteristics. Resourcefulness. Outlook and impressions. Ego. Beginnings and initiatives."}
	num["House2"] = {}
	num["House2"] = {"Housenumber": 2, 	"sign": "Taurus", "Latin motto":"Lucrum", "translate":"Gain", "translated":"House of Value", "explain":"Material and immaterial things of certain value. Money. Possessions and acquisitions. Cultivation. Substance. Self-worth."}
	num["House3"] = {}
	num["House3"] = {"Housenumber": 3, 	"sign": "Gemini", "Latin motto":"Fratres", "translate":"Order", "translated":"House of Communications", "explain":"Communication. Happiness. Intelligence/development. Achievements. Siblings. Neighborhood matters. Locomotion and transportation. Ephemera."}
	num["House4"] = {}
	num["House4"] = {"Housenumber": 4, 	"sign": "Cancer", "Latin motto":"Genitor", "translate":"Parent", "translated":"House of Home and Family", "explain":"Ancestry, heritage, roots. Early foundation and environment. Mother or caretaker. Housing and the household. Comfort. Pets."}
	num["House5"] = {}
	num["House5"] = {"Housenumber": 5, 	"sign": "Leo", "Latin motto":"Nati", "translate":"Children", "translated":"House of Pleasure", "explain":"Recreational and leisure activities. Things which makes for enjoyment and entertainment. Games/gambling/risk. Romance and limerence. Children/conception. Creative self-expression."}
	num["House6"] = {}
	num["House6"] = {"Housenumber": 6, 	"sign": "Virgo", "Latin motto":"Valetudo", "translate":"Health", "translated":"House of Health", "explain":"Routine tasks and duties. Skills or training acquired. Employment (job). Service performed for others. Health and overall well-being."}
	num["House7"] = {}
	num["House7"] = {"Housenumber": 7, 	"sign": "Libra", "Latin motto":"Uxor", "translate":"Spouse", "translated":"House of Partnerships", "explain":"Partnerships. Marriage and business matters. Diplomacy. Agreements, contracts and all things official."}
	num["House8"] = {}
	num["House8"] = {"Housenumber": 8, 	"sign": "Scorpio", "Latin motto":"Mors", "translate":"Death", "translated":"House of Transformation", "explain":"Cycles of deaths and rebirth. Sexual relationships and commitments of all kinds. Joint funds, finances. Other person's resource. Karma and spirituality. Regeneration. Self-transformation."}
	num["House9"] = {}
	num["House9"] = {"Housenumber": 9, 	"sign": "Sagittarius", "Latin motto":"Iter", "translate":"Journeys", "translated":"House of Philosophy", "explain":"Travel and foreigners. Culture. Journeys. Religion. Law and ethics. Education/learning/knowledge. Experience through expansion. Things long-term. Hope."}
	num["House10"] = {}
	num["House10"] = {"Housenumber": 10, 	"sign": "Capricorn", "Latin motto":"Regnum", "translate":"Kingdom", "translated":"House of Enterprise", "explain":"Ambitions. Motivations. Career. Status in society. Government. Father or authority. Notoriety."}
	num["House11"] = {}
	num["House11"] = {"Housenumber": 11, 	"sign": "Aquarius", "Latin motto":"Benefacta", "translate":"Friendship", "translated":"House of Blessings", "explain":"Friends and acquaintances of like-minded attitudes. Belonging. Fulfillment. Groups and communities. Volunteering. Higher associations. Connectedness. Love. Benefits from effort. Desires and wishes. Wealth."}
	num["House12"] = {}
	num["House12"] = {"Housenumber": 12, 	"sign": "Pisces", "Latin motto":"Carcer", "translate":"Rehabilitation", "translated":"House of Undoing", "explain":"Seclusion and retreating. Clandestiny/secrets/mystery. Privacy and sacrifice. Unconscious/subconscious, dreams. Releasing/relinquishing, healing, and peacefulness. Finality/completion."}
	return num.get(mitthus)


#https://www.allure.com/story/gemini-zodiac-sign-personality-traits
def explain_zodiac(zodiac):
	stuff = {"Taurus":"Taurus is an earth sign represented by the bull. Like their celestial spirit animal, Taureans enjoy relaxing in serene, bucolic environments surrounded by soft sounds, soothing aromas, and succulent flavors.",
	"Gemini":"""Have you ever been so busy that you wished you could clone yourself just to get everything done? That’s the Gemini experience in a nutshell. Appropriately symbolized by the celestial twins, this air sign was interested in so many pursuits that it had to double itself.""",
	"Cancer":"""Cancer is a cardinal water sign. Represented by the crab, this crustacean seamlessly weaves between the sea and shore representing Cancer’s ability to exist in both emotional and material realms. Cancers are highly intuitive and their psychic abilities manifest in tangible spaces: For instance, Cancers can effortlessly pick up the energies in a room.""",
	"Leo":"""Roll out the red carpet because Leo has arrived. Leo is represented by the lion and these spirited fire signs are the kings and queens of the celestial jungle. They’re delighted to embrace their royal status: Vivacious, theatrical, and passionate, Leos love to bask in the spotlight and celebrate themselves.""",
	"Virgo":"""Virgo is an earth sign historically represented by the goddess of wheat and agriculture, an association that speaks to Virgo’s deep-rooted presence in the material world. Virgos are logical, practical, and systematic in their approach to life. This earth sign is a perfectionist at heart and isn’t afraid to improve skills through diligent and consistent practice.""", 
	"Libra":"""Libra is an air sign represented by the scales (interestingly, the only inanimate object of the zodiac), an association that reflects Libra's fixation on balance and harmony. Libra is obsessed with symmetry and strives to create equilibrium in all areas of life.""" ,
	"Scorpio":"""Scorpio is one of the most misunderstood signs of the zodiac. Because of its incredible passion and power, Scorpio is often mistaken for a fire sign. In fact, Scorpio is a water sign that derives its strength from the psychic, emotional realm.""",
	"Sagittarius":"""Represented by the archer, Sagittarians are always on a quest for knowledge. The last fire sign of the zodiac, Sagittarius launches its many pursuits like blazing arrows, chasing after geographical, intellectual, and spiritual adventures.""",
	"Capricorn":"""The last earth sign of the zodiac, Capricorn is represented by the sea goat, a mythological creature with the body of a goat and tail of a fish. Accordingly, Capricorns are skilled at navigating both the material and emotional realms.""",
	"Aquarius":"""Despite the “aqua” in its name, Aquarius is actually the last air sign of the zodiac. Aquarius is represented by the water bearer, the mystical healer who bestows water, or life, upon the land. Accordingly, Aquarius is the most humanitarian astrological sign.""",
	"Pisces":"Pisces, a water sign, is the last constellation of the zodiac. It's symbolized by two fish swimming in opposite directions, representing the constant division of Pisces's attention between fantasy and reality. As the final sign, Pisces has absorbed every lesson — the joys and the pain, the hopes and the fears — learned by all of the other signs."""}
	return stuff.get(zodiac.lower().title())






## dayly
"""
{
  "date": "2020-02-08",
  "horoscope": "Warmth abounds under the current cosmic energy. If you have a hard time getting into the fun, romantic swing of things, it won't be for lack of passion. In fact, the problem might be a little too much passion! You're all fired up about something. The more worked up you feel, the more careful you'll have to be in how you express yourself. Try to temper your aggressive, possessive urges.",
  "meta": {
    "intensity": "84%",
    "keywords": "possibilities, narrow",
    "mood": "understandable"
  },
  "sunsign": "Scorpio"
}
"""
def asktheastrologer(zodiacsign):
	if not zodiacs.__contains__(zodiacsign):
		return False
	blob = json.loads(requests.get("http://theastrologer-api.herokuapp.com/api/horoscope/{}/today".format(zodiacsign)).text).get('horoscope')#.get('horoscope')
	return insert_newlines(blob)#.replace('','')


def askhoroscopesandastrology(zodiac):
	if not zodiacs.__contains__(zodiac):
		return False
	zodiac = zodiac.lower()
	blob = json.loads(requests.get("https://www.horoscopes-and-astrology.com/json").text)
	return insert_newlines(blob.get('dailyhoroscope').get(zodiac.title()).replace('<a href="https://horoscopes-and-astrology.com/{}?language=en" alt="{}" target="_blank"> <i>Read more...</i></a>'.format(zodiac.title(),zodiac.title()), ''))


# weeklong
def askastrologydotcom(zodiac):
	blob = requests.get("https://www.astrology.com/horoscope/weekly-overview/this-week/{}.html".format(zodiac)).text
	blab = re.findall(r'<span class=\"date\">(.*)\<\/p>', blob)[0]
#clean it 
	return insert_newlines(blab.replace('<br>', '').replace('</span>', ''))	
"""
zodiac = "gemini"#input("Whats you zodiac sign?: ")
if not zodiacs.__contains__(zodiac):
	print('invalid zodiac')
else:
	print("Getting daily horoscopes for", zodiac)
	yum = {}
	yum['theastrologer'] = {}
	yum['theastrologer']['horoscope'] = asktheastrologer(zodiac)#.get('horoscope')
	yum['theastrologer']['type'] = 'daily'
	yum['horoscopesandastrology'] = {}
	yum['horoscopesandastrology']['type'] = 'daily'
	yum['horoscopesandastrology']['horoscope'] = askhoroscopesandastrology(zodiac)
	yum['astrologydotcom'] = {}
	yum['astrologydotcom']['type'] = 'weekly'
	yum['astrologydotcom']['horoscope'] = askastrologydotcom(zodiac)
	for key in yum.keys():
		print("Getting: ", key)
		print(yum.get(key).get('horoscope'))
"""



updateday = ""#datetime.datetime.today()
zcache = {}
class zodiac_cache():
	def __init__(self):
		pass

	def getzodiac(self, zodiac):
		return zcache.get(zodiac)

	def getweekly():
		blab = {}
		for x in zcache.keys():
			if zcache.get(x).get('type') == 'weekly':
				blab[x] = {}
				blab[x]['horoscope'] = zcache.get(x).get('horoscope')
		return blab

	def getdaily():
		blab = {}
		for x in zcache.keys():
			if zcache.get(x).get('type') == 'daily':
				blab[x] = {}
				blab[x]['horoscope'] = zcache.get(x).get('horoscope')
		return blab

	def update(self):
		print('updating')
		global zcache
		for zz in zodiacs:
			zcache[zz] = {}
			zcache[zz]['theastrologer'] = {}
			zcache[zz]['theastrologer']['horoscope'] = asktheastrologer(zz)#.get('horoscope')
			zcache[zz]['theastrologer']['type'] = 'daily'
			zcache[zz]['horoscopesandastrology'] = {}
			zcache[zz]['horoscopesandastrology']['type'] = 'daily'
			zcache[zz]['horoscopesandastrology']['horoscope'] = askhoroscopesandastrology(zz)
			zcache[zz]['astrologydotcom'] = {}
			zcache[zz]['astrologydotcom']['type'] = 'weekly'
			zcache[zz]['astrologydotcom']['horoscope'] = askastrologydotcom(zz)
			print('added', zz)
		print('updated')
		return True

	def update_check(self):
		global updateday
		newupdateday = str(datetime.datetime.today())[:10]
		print(newupdateday,"|",updateday)
		if newupdateday == updateday:
#			print(newupdateday,updateday)
			return False
		updateday = newupdateday
		bird = Thread(target=self.update)
		bird.setDaemon(True)                                            
		bird.start()#bird flyes off                                     
		return True


@za.route('/', methods=['POST', 'GET'])
def indexsite():
	zodiac_cache().update_check()

	if flask.request.method == 'POST':
		yumm = flask.request.form.get('choiceit')
		print('yumm is:', yumm)
		if not yumm:
			pass
		else:
			if zodiacs.__contains__(yumm.lower()):
				return flask.redirect('/zodiac/{}'.format(yumm.lower()), code=302)
			else:
				print('no contain!')
	return flask.render_template("index.html")

@za.route('/zodiac/<zodiac>', methods=['GET'])
def indexzodiac(zodiac):
	zodiac = zodiac.lower()
	if not zodiacs.__contains__(zodiac):
		return flask.redirect('/', code=302)
	info = zodiac_cache().getzodiac(zodiac)
	if not info:
		return flask.redirect('/', code=302)
	return flask.render_template("viewzodiac.html", info=info, title=zodiac.lower().title(), today=str(updateday))

@za.route('/advanced', methods=["POST", "GET"])
def advancedview():

    if flask.request.method == "POST":
        num = flask.request.form.get('choiceit')
        town = flask.request.form.get('town')
        country  = flask.request.form.get('country')
#        print('num is:', num)
        if len(num) > 6:
            yy,mm,dd = num[:4], num[5:7], num[8:10] 
            tiden = yy+'/'+mm+'/'+dd
            date = Datetime(tiden, '17:00', '+00:00')
            geo_coordinates = get_geo_cords(town,country)
            if not geo_coordinates:
                return flask.render_template("advanced.html", countries=countries, error="Could not find the city")

            g0,g1 = float(geo_coordinates[0]), float(geo_coordinates[1].replace('</span>', ''))
            pos = GeoPos(g0, g1)
            chart = Chart(date, pos, IDs=const.LIST_OBJECTS)
            sun = chart.getObject(const.SUN)
#            print("Your sun sign is: ",sun.sign) #zodiac sign
#            print("Your zodiac is explained as: ", explain_zodiac(sun.sign))
#            print("Your sun movement is: ",sun.movement())
#            print("Your sun element is: ",sun.element())
#            print("Explained element:", explain_element(sun.element()))
#            print("Your sun faction is: ",sun.faction())
            #print(chart.__dict__)
            #house is different depending on chart
#            for merp in const.LIST_HOUSES:
#                    print(merp, 'sign is',chart.getHouse(merp).sign,'The condition is:',chart.getHouse(merp).condition())
#                    print("This is the",explain_house(merp).get("translated"), " the lating motto for it is '",explain_house(merp).get("Latin motto"),"' It's basicly means: ",explain_house(merp).get('explain'))
            ##print("Your sun element is: ",chart.getObject(const.SUN).figures())
            moon = chart.get(const.MOON)
 #           print("Your moon is in:", moon.sign)
 #           print("Your moon movement is: ",moon.movement())
 #           print("Your moon element is: ",moon.element())
#            print("Explained element:", explain_element(moon.element()))
#            print("Your moon faction is: ",moon.faction())
#            print("Your moon phase:", chart.getMoonPhase())
            return flask.render_template("advanced.html", moon=moon, sun=sun, const=const, explain_house=explain_house, chart=chart, explain_zodiac=explain_zodiac, explain_element=explain_element)


    return flask.render_template("advanced.html", countries=countries)







if __name__ == "__main__":
	za.run(host="0.0.0.0", debug=False, port=2510)
