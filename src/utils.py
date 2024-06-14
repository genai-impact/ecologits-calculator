from dataclasses import dataclass
from enum import Enum

from ecologits.impacts.models import Impacts, Energy, GWP, ADPe, PE
from pint import UnitRegistry, Quantity


u = UnitRegistry()
u.define('Wh = watt_hour')
u.define('kWh = kilowatt_hour')
u.define('MWh = megawatt_hour')
u.define('GWh = gigawatt_hour')
u.define('TWh = terawatt_hour')
u.define('gCO2eq = gram')
u.define('kgCO2eq = kilogram')
u.define('tCO2eq = metricton')
u.define('kgSbeq = kilogram')
u.define('kJ = kilojoule')
u.define('MJ = megajoule')
u.define('m = meter')
u.define('km = kilometer')
u.define('s = second')
u.define('min = minute')
u.define('h = hour')
q = u.Quantity


@dataclass
class QImpacts:
    energy: Quantity
    gwp: Quantity
    adpe: Quantity
    pe: Quantity


class PhysicalActivity(str, Enum):
    RUNNING = "running"
    WALKING = "walking"


class EnergyProduction(str, Enum):
    NUCLEAR = "nuclear"
    WIND = "wind"


COUNTRIES = [
    ("cook_islands", 38.81, 9_556),
    ("tonga", 51.15, 104_490),
    ("comoros", 100, 821_632),
    ("samoa", 100, 821_632),
]


# From https://www.runningtools.com/energyusage.htm
RUNNING_ENERGY_EQ = q("294 kJ / km")     # running 1 km at 10 km/h with a weight of 70 kg
WALKING_ENERGY_EQ = q("196 kJ / km")     # walking 1 km at 3 km/h with a weight of 70 kg

# From https://selectra.info/energie/actualites/insolite/consommation-vehicules-electriques-france-2040
# and https://www.tesla.com/fr_fr/support/power-consumption
EV_ENERGY_EQ = q("0.17 kWh / km")

# From https://impactco2.fr/outils/comparateur?value=1&comparisons=streamingvideo
STREAMING_GWP_EQ = q("15.6 h / kgCO2eq")

# From https://ourworldindata.org/population-growth
ONE_PERCENT_WORLD_POPULATION = 80_000_000

DAYS_IN_YEAR = 365

# For a 900 MW nuclear plant -> 500 000 MWh / month
# From https://www.edf.fr/groupe-edf/espaces-dedies/jeunes-enseignants/pour-les-jeunes/lenergie-de-a-a-z/produire-de-lelectricite/le-nucleaire-en-chiffres
YEARLY_NUCLEAR_ENERGY_EQ = q("6 TWh")

# For a 2MW wind turbine
# https://www.ecologie.gouv.fr/eolien-terrestre
YEARLY_WIND_ENERGY_EQ = q("4.2 GWh")

# Ireland yearly electricity consumption
# From https://en.wikipedia.org/wiki/List_of_countries_by_electricity_consumption
YEARLY_IRELAND_ELECTRICITY_CONSUMPTION = q("33 TWh")
IRELAND_POPULATION_MILLION = 5

# From https://impactco2.fr/outils/comparateur?value=1&comparisons=&equivalent=avion-pny
AIRPLANE_PARIS_NYC_GWP_EQ = q("1770 kgCO2eq")


def format_energy(energy: Energy) -> Quantity:
    val = q(energy.value, energy.unit)
    if val < q("1 kWh"):
        val = val.to("Wh")
    return val


def format_gwp(gwp: GWP) -> Quantity:
    val = q(gwp.value, gwp.unit)
    if val < q("1 kgCO2eq"):
        val = val.to("gCO2eq")
    return val


def format_adpe(adpe: ADPe) -> Quantity:
    return q(adpe.value, adpe.unit)


def format_pe(pe: PE) -> Quantity:
    val = q(pe.value, pe.unit)
    if val < q("1 MJ"):
        val = val.to("kJ")
    return val


def format_impacts(impacts: Impacts) -> QImpacts:
    return QImpacts(
        energy=format_energy(impacts.energy),
        gwp=format_gwp(impacts.gwp),
        adpe=format_adpe(impacts.adpe),
        pe=format_pe(impacts.pe),
    )


def format_energy_eq_physical_activity(energy: Quantity) -> tuple[PhysicalActivity, Quantity]:
    energy = energy.to("kJ")
    running_eq = energy / RUNNING_ENERGY_EQ
    if running_eq > q("1 km"):
        return PhysicalActivity.RUNNING, running_eq

    walking_eq = energy / WALKING_ENERGY_EQ
    if walking_eq < q("1 km"):
        walking_eq = walking_eq.to("m")
    return PhysicalActivity.WALKING, walking_eq


def format_energy_eq_electric_vehicle(energy: Quantity) -> Quantity:
    energy = energy.to("kWh")
    ev_eq = energy / EV_ENERGY_EQ
    if ev_eq < q("1 km"):
        ev_eq = ev_eq.to("m")
    return ev_eq


def format_gwp_eq_streaming(gwp: Quantity) -> Quantity:
    gwp = gwp.to("kgCO2eq")
    streaming_eq = gwp * STREAMING_GWP_EQ
    if streaming_eq < q("1 h"):
        streaming_eq = streaming_eq.to("min")
    if streaming_eq < q("1 min"):
        streaming_eq = streaming_eq.to("s")
    return streaming_eq


def format_energy_eq_electricity_production(energy: Quantity) -> tuple[EnergyProduction, float]:
    electricity_eq = energy * ONE_PERCENT_WORLD_POPULATION * DAYS_IN_YEAR
    electricity_eq = electricity_eq.to("TWh")
    if electricity_eq > YEARLY_NUCLEAR_ENERGY_EQ:
        return EnergyProduction.NUCLEAR, electricity_eq / YEARLY_NUCLEAR_ENERGY_EQ
    electricity_eq = electricity_eq.to("GWh")
    return EnergyProduction.WIND, electricity_eq / YEARLY_WIND_ENERGY_EQ


def format_energy_eq_electricity_consumption_ireland(energy: Quantity) -> float:
    electricity_eq = energy * ONE_PERCENT_WORLD_POPULATION * DAYS_IN_YEAR
    electricity_eq = electricity_eq.to("TWh")
    return electricity_eq / YEARLY_IRELAND_ELECTRICITY_CONSUMPTION


def format_gwp_eq_airplane_paris_nyc(gwp: Quantity) -> float:
    gwp_eq = gwp * ONE_PERCENT_WORLD_POPULATION * DAYS_IN_YEAR
    gwp_eq = gwp_eq.to("kgCO2eq")
    return gwp_eq / AIRPLANE_PARIS_NYC_GWP_EQ


if __name__ == '__main__':
    # energy = 5590e-9    # GWh
    # energy = 3.58e-9    # GWh
    # val = q("5.59 kWh") # gpt4
    val = q("0.448 Wh")
    val = val.to("MWh")
    pop = 80_000_000
    days = 365

    tot = val * pop * days
    print(tot)
