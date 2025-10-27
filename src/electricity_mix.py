from __future__ import annotations


PATH = "src/data/electricity_mix.csv"
COUNTRY_CODES = [
    ("🌎 World", "WOR"),
    ("🇦🇺 Australia", "AUS"),
    ("🇦🇹 Austria", "AUT"),
    ("🇦🇷 Argentina", "ARG"),
    ("🇧🇪 Belgium", "BEL"),
    ("🇧🇬 Bulgaria", "BGR"),
    ("🇧🇷 Brazil", "BRA"),
    ("🇨🇦 Canada", "CAN"),
    ("🇨🇭 Switzerland", "CHE"),
    ("🇨🇱 Chile", "CHL"),
    ("🇨🇳 China", "CHN"),
    ("🇨🇾 Cyprus", "CYP"),
    ("🇨🇿 Czech Republic", "CZE"),
    ("🇩🇪 Germany", "DEU"),
    ("🇩🇰 Denmark", "DNK"),
    ("🇪🇸 Spain", "ESP"),
    ("🇪🇪 Estonia", "EST"),
    ("🇫🇮 Finland", "FIN"),
    ("🇫🇷 France", "FRA"),
    ("🇬🇧 United Kingdom", "GBR"),
    ("🇬🇷 Greece", "GRC"),
    ("🇭🇺 Hungary", "HUN"),
    ("🇮🇩 Indonesia", "IDN"),
    ("🇮🇳 India", "IND"),
    ("🇮🇪 Ireland", "IRL"),
    ("🇮🇸 Iceland", "ISL"),
    ("🇮🇹 Italy", "ITA"),
    ("🇯🇵 Japan", "JPN"),
    ("🇰🇷 South Korea", "KOR"),
    ("🇱🇹 Lithuania", "LTU"),
    ("🇱🇺 Luxembourg", "LUX"),
    ("🇱🇻 Latvia", "LVA"),
    ("🇲🇽 Mexico", "MEX"),
    ("🇲🇹 Malta", "MLT"),
    ("🇲🇾 Malaysia", "MYS"),
    ("🇳🇱 Netherlands", "NLD"),
    ("🇳🇴 Norway", "NOR"),
    ("🇳🇿 New Zealand", "NZL"),
    ("🇵🇱 Poland", "POL"),
    ("🇵🇹 Portugal", "PRT"),
    ("🇷🇴 Romania", "ROU"),
    ("🇷🇺 Russian Federation", "RUS"),
    ("🇸🇰 Slovak Republic", "SVK"),
    ("🇸🇮 Slovenia", "SVN"),
    ("🇸🇪 Sweden", "SWE"),
    ("🇺🇦 Ukraine", "UKR"),
    ("🇹🇭 Thailand", "THA"),
    ("🇹🇷 Turkey", "TUR"),
    ("🇹🇼 Taiwan", "TWN"),
    ("🇺🇸 United States", "USA")
]

CRITERIA = {
    "gwp": "GHG Emission (kg CO2 eq)",
    "adpe": "Abiotic Resources (kg Sb eq)",
    "pe": "Primary Energy (MJ)",
    "wue": "Water Usage Effectiveness (L/kWh)"
}


def format_country_name(code: str) -> str | None:
    for country_name, country_code in COUNTRY_CODES:
        if country_code == code:
            return country_name
    return None


def format_electricity_mix_criterion(criterion: str) -> str | None:
    return CRITERIA.get(criterion)
