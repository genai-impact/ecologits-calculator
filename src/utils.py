from dataclasses import dataclass
from enum import Enum

from ecologits.model_repository import models
from ecologits.impacts.modeling import Impacts, Energy, GWP, ADPe, PE, Water
#from ecologits.tracers.utils import llm_impacts
from pint import UnitRegistry, Quantity

#####################################################################################
### UNITS DEFINITION
#####################################################################################

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
u.define('L = liter')
u.define('mL = milliliter')
#u.define('bottled waters = bottled waters')
q = u.Quantity

@dataclass
class QImpacts:
    energy: Quantity
    gwp: Quantity
    adpe: Quantity
    pe: Quantity
    water: Quantity


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

#####################################################################################
### EQUIVALENT RAW DATA
#####################################################################################

# From https://www.runningtools.com/energyusage.htm
RUNNING_ENERGY_EQ = q("294 kJ / km")     # running 1 km at 10 km/h with a weight of 70 kg
WALKING_ENERGY_EQ = q("196 kJ / km")     # walking 1 km at 3 km/h with a weight of 70 kg

# From https://selectra.info/energie/actualites/insolite/consommation-vehicules-electriques-france-2040
# and https://www.tesla.com/fr_fr/support/power-consumption
EV_ENERGY_EQ = q("0.17 kWh / km")

# From https://impactco2.fr/outils/comparateur?value=1&comparisons=streamingvideo
STREAMING_GWP_EQ = q("15.6 h / kgCO2eq")

BOTTLED_WATERS_EQ = q("0.75 L")

# From https://ourworldindata.org/population-growth
ONE_PERCENT_WORLD_POPULATION = 80_000_000

DAYS_IN_YEAR = 365.15

WORKDAYS_IN_YEAR_FRANCE = 251

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
AIRPLANE_PARIS_NYC_GWP_EQ = q("177000 kgCO2eq")

# From https://www.patagoniaalliance.org/wp-content/uploads/2014/08/How-much-water-does-an-Olympic-sized-swimming-pool-hold.pdf
OLYMPIC_SWIMMING_POOL = q("2500000 L") #2.5 million 

# From https://docs.google.com/spreadsheets/d/1uj8yA601uBtJ7GSf7k96Lv1NoQBfsCnVmTCII2HgZvo/edit?gid=0#gid=0
# Google : https://www.gstatic.com/gumdrop/sustainability/google-2025-environmental-report.pdf
# Meta: https://sustainability.atmeta.com/wp-content/uploads/2024/08/Meta-2024-Sustainability-Report.pdf
# Microsoft: https://azure.microsoft.com/en-us/blog/how-microsoft-measures-datacenter-water-and-energy-use-to-improve-azure-cloud-sustainability/
# OVHCloud: https://corporate.ovhcloud.com/en/sustainability/environment/
# Scaleway: https://www-uploads.scaleway.com/Impact_Report2024_A4_EN_e63efcae20.pdf
# AWS: https://sustainability.aboutamazon.com/2023-report
# Equinix: https://www.equinix.com/resources/infopapers/2023-corporate-sustainability-report
PROVIDER_WUE_ONSITE = { #Water use efficiency on-site, as opposed to off-site generated energy 
    "Google" : 0.916,
    "Meta": 0.18,    # L/kWh, 2023
    "Microsoft": 0.49, #2022
    "OVHCloud": 0.37, #2024
    "Scaleway": 0.216, #2023
    "AWS" : 0.18, #2023
    "Equinix" : 1.07 #2023
}


# Google https://www.gstatic.com/gumdrop/sustainability/google-2025-environmental-report.pdf
# Meta https://sustainability.atmeta.com/data-centers/#:~:text=Meta's%20operational%20data%20centers%2C%20on,Effectiveness%20(WUE)%20of%200.20.
# Microsoft https://azure.microsoft.com/en-us/blog/how-microsoft-measures-datacenter-water-and-energy-use-to-improve-azure-cloud-sustainability/
# OVHCloud https://corporate.ovhcloud.com/en/sustainability/environment/
# Scaleway https://www-uploads.scaleway.com/Impact_Report2024_A4_EN_e63efcae20.pdf
# AWS https://sustainability.aboutamazon.com/products-services/aws-cloud
# Equinix https://www.equinix.com/content/dam/eqxcorp/en_us/documents/resources/infopapers/ip_2023_sustainability_en.pdf
PROVIDER_PUE = { #Power use efficiency 
    "Google" : 1.09,
    "Meta" : 1.09,	
    "Microsoft" : 1.18,	
    "OVHCloud" : 1.26,	
    "Scaleway" : 1.37,	
    "AWS" : 1.15,	
    "Equinix" : 1.42	
}

AI_COMPANY_TO_DATA_CENTER_PROVIDER = { #A list that draws the connection between AI companies and their data center providers 
    "anthropic"	: "Google",
    "mistralai"	: "OVHCloud",
    "cohere"	: "AWS", 
    "databricks" : "Microsoft", 
    "meta"	: "Meta",
    "google"	: "Google",
    "microsoft"	: "Microsoft", 
    "openai" : "Microsoft"
} 


#####################################################################################
### IMPACTS FORMATING
#####################################################################################

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

def format_water(water: Water) -> Quantity:
    val = q(water.value, water.unit)
    if val < q("1 L"):
        val = val.to("mL")
    return val

def range_percent_impact_one_sided(impacts: Impacts) -> float:
    impacts_energy_mean = (impacts.energy.value.max + impacts.energy.value.min)/2
    range_percent_energy_one_sided = (impacts.energy.value.max - impacts.energy.value.min) / (2* impacts_energy_mean) * 100
    impacts_gwp_mean = (impacts.gwp.value.max + impacts.gwp.value.min)/2
    range_percent_gwp_one_sided = (impacts.gwp.value.max - impacts.gwp.value.min) / (2* impacts_gwp_mean) * 100
    impacts_adpe_mean = (impacts.adpe.value.max + impacts.adpe.value.min)/2
    range_percent_adpe_one_sided = (impacts.adpe.value.max - impacts.adpe.value.min) / (2* impacts_adpe_mean) * 100
    impacts_pe_mean = (impacts.pe.value.max + impacts.pe.value.min)/2
    range_percent_pe_one_sided = (impacts.pe.value.max - impacts.pe.value.min) / (2* impacts_pe_mean) * 100
    impacts_water_mean = (impacts.water.value.max + impacts.water.value.min)/2
    range_percent_water_one_sided = (impacts.water.value.max - impacts.water.value.min) / (2* impacts_water_mean) * 100
        
    results = {
        "energy" : range_percent_energy_one_sided,
        "gwp": range_percent_gwp_one_sided,
        "adpe": range_percent_adpe_one_sided,
        "pe": range_percent_pe_one_sided,
        "water" : range_percent_water_one_sided
    }
    return results



def format_impacts(impacts: Impacts) -> QImpacts:

    try:
        impacts.energy.value = (impacts.energy.value.max + impacts.energy.value.min)/2
        impacts.gwp.value = (impacts.gwp.value.max + impacts.gwp.value.min)/2
        impacts.adpe.value = (impacts.adpe.value.max + impacts.adpe.value.min)/2
        impacts.pe.value = (impacts.pe.value.max + impacts.pe.value.min)/2
        impacts.water.value = (impacts.water.value.max + impacts.water.value.min)/2
        return QImpacts(
            energy=format_energy(impacts.energy),
            gwp=format_gwp(impacts.gwp),
            adpe=format_adpe(impacts.adpe),
            pe=format_pe(impacts.pe),
            water=format_water(impacts.water)
        ), impacts.usage, impacts.embodied
    except: #when no range
        return QImpacts(
            energy=format_energy(impacts.energy),
            gwp=format_gwp(impacts.gwp),
            adpe=format_adpe(impacts.adpe),
            pe=format_pe(impacts.pe),
            water=format_water(impacts.water)
        ), impacts.usage, impacts.embodied

def split_impacts_u_e(impacts: Impacts) -> QImpacts:
    return impacts.usage, impacts.embodied

def average_range_impacts(x):
    
    if isinstance(x, float):
        return x 
    else:
        return (x.max + x.min)/2

def format_impacts_expert(impacts: Impacts, display_range: bool) -> QImpacts:
    
    if display_range:
        return QImpacts(
            energy=format_energy(impacts.energy),
            gwp=format_gwp(impacts.gwp),
            adpe=format_adpe(impacts.adpe),
            pe=format_pe(impacts.pe),
            water=format_water(impacts.water)
        ), impacts.usage, impacts.embodied
    
    else:
        energy = {"value":(impacts.energy.value.max + impacts.energy.value.min)/2, "unit":impacts.energy.unit}
        gwp = (impacts.gwp.value.max + impacts.gwp.value.min)/2
        adpe = (impacts.adpe.value.max + impacts.adpe.value.min)/2
        pe = (impacts.pe.value.max + impacts.pe.value.min)/2
        return QImpacts(
            energy=format_energy(energy),
            gwp=format_gwp(gwp),
            adpe=format_adpe(adpe),
            pe=format_pe(pe),
            water=format_water(impacts.water)
        ), impacts.usage, impacts.embodied
    


######################################################################3

#####################################################################################
### EQUIVALENT FORMATING
#####################################################################################

def format_energy_eq_physical_activity(energy: Quantity) -> tuple[PhysicalActivity, Quantity]:
    energy = energy.to("kJ")
    running_eq = energy / RUNNING_ENERGY_EQ
    if running_eq > q("1 km"):
        return PhysicalActivity.RUNNING, running_eq

    walking_eq = energy / WALKING_ENERGY_EQ
    if walking_eq < q("1 km"):
        walking_eq = walking_eq.to("meter")
    return PhysicalActivity.WALKING, walking_eq

def format_energy_eq_electric_vehicle(energy: Quantity) -> Quantity:
    energy = energy.to("kWh")
    ev_eq = energy / EV_ENERGY_EQ
    if ev_eq < q("1 km"):
        ev_eq = ev_eq.to("meter")
    return ev_eq

def format_gwp_eq_streaming(gwp: Quantity) -> Quantity:
    gwp = gwp.to("kgCO2eq")
    streaming_eq = gwp * STREAMING_GWP_EQ
    if streaming_eq < q("1 h"):
        streaming_eq = streaming_eq.to("min")
    if streaming_eq < q("1 min"):
        streaming_eq = streaming_eq.to("s")
    return streaming_eq

def format_water_eq_bottled_waters(water: Quantity) -> Quantity:
    water = water.to("L")
    bottled_water_eq = water / BOTTLED_WATERS_EQ
    return bottled_water_eq

def format_energy_eq_electricity_production(energy: Quantity) -> tuple[EnergyProduction, Quantity]:
    electricity_eq = energy * ONE_PERCENT_WORLD_POPULATION * DAYS_IN_YEAR
    electricity_eq = electricity_eq.to("TWh")
    if electricity_eq > YEARLY_NUCLEAR_ENERGY_EQ:
        return EnergyProduction.NUCLEAR, electricity_eq / YEARLY_NUCLEAR_ENERGY_EQ
    electricity_eq = electricity_eq.to("GWh")
    return EnergyProduction.WIND, electricity_eq / YEARLY_WIND_ENERGY_EQ


def format_energy_eq_electricity_consumption_ireland(energy: Quantity) -> Quantity:
    electricity_eq = energy * ONE_PERCENT_WORLD_POPULATION * DAYS_IN_YEAR
    electricity_eq = electricity_eq.to("TWh")
    return electricity_eq / YEARLY_IRELAND_ELECTRICITY_CONSUMPTION


def format_gwp_eq_airplane_paris_nyc(gwp: Quantity) -> Quantity:
    gwp_eq = gwp * ONE_PERCENT_WORLD_POPULATION * DAYS_IN_YEAR
    gwp_eq = gwp_eq.to("kgCO2eq")
    return gwp_eq / AIRPLANE_PARIS_NYC_GWP_EQ

def format_water_eq_olympic_sized_swimming_pool(water: Quantity) -> Quantity:
    water_eq = water * ONE_PERCENT_WORLD_POPULATION * DAYS_IN_YEAR
    water_eq = water_eq.to("L")
    return water_eq / OLYMPIC_SWIMMING_POOL

########################################################################

def format_energy_eq_physical_activity_company(energy: Quantity, company_multiplier) -> tuple[PhysicalActivity, Quantity]:
    energy = energy.to("kJ")
    running_eq = energy / RUNNING_ENERGY_EQ * company_multiplier
    if running_eq > q("1 km"):
        return PhysicalActivity.RUNNING, running_eq

    walking_eq = energy / WALKING_ENERGY_EQ
    if walking_eq < q("1 km"):
        walking_eq = walking_eq.to("meter")
    return PhysicalActivity.WALKING, walking_eq

def format_energy_eq_electric_vehicle_company(energy: Quantity, company_multiplier) -> Quantity:
    energy = energy.to("kWh")
    ev_eq = energy / EV_ENERGY_EQ * company_multiplier
    if ev_eq < q("1 km"):
        ev_eq = ev_eq.to("meter")
    return ev_eq

def format_gwp_eq_streaming_company(gwp: Quantity, company_multiplier) -> Quantity:
    gwp = gwp.to("kgCO2eq")
    streaming_eq = gwp * STREAMING_GWP_EQ * company_multiplier
    if streaming_eq < q("1 h"):
        streaming_eq = streaming_eq.to("min")
    if streaming_eq < q("1 min"):
        streaming_eq = streaming_eq.to("s")
    return streaming_eq

def format_water_eq_bottled_waters_company(water: Quantity, company_multiplier) -> Quantity:
    water = water.to("L")
    bottled_water_eq = water / BOTTLED_WATERS_EQ * company_multiplier
    return bottled_water_eq

def format_energy_eq_electricity_production_company(energy: Quantity, company_multiplier) -> tuple[EnergyProduction, Quantity]:
    electricity_eq = energy * company_multiplier * WORKDAYS_IN_YEAR_FRANCE
    electricity_eq = electricity_eq.to("TWh")
    if electricity_eq > YEARLY_NUCLEAR_ENERGY_EQ:
        return EnergyProduction.NUCLEAR, electricity_eq / YEARLY_NUCLEAR_ENERGY_EQ
    electricity_eq = electricity_eq.to("GWh")
    return EnergyProduction.WIND, electricity_eq / YEARLY_WIND_ENERGY_EQ


def format_energy_eq_electricity_consumption_ireland_company(energy: Quantity, company_multiplier) -> Quantity:
    electricity_eq = energy * company_multiplier * WORKDAYS_IN_YEAR_FRANCE
    electricity_eq = electricity_eq.to("TWh")
    return electricity_eq / YEARLY_IRELAND_ELECTRICITY_CONSUMPTION


def format_gwp_eq_airplane_paris_nyc_company(gwp: Quantity, company_multiplier) -> Quantity:
    gwp_eq = gwp * company_multiplier * WORKDAYS_IN_YEAR_FRANCE
    gwp_eq = gwp_eq.to("kgCO2eq")
    return gwp_eq / AIRPLANE_PARIS_NYC_GWP_EQ

def format_water_eq_olympic_sized_swimming_pool_company(water: Quantity, company_multiplier) -> Quantity:
    water_eq = water * company_multiplier * WORKDAYS_IN_YEAR_FRANCE
    water_eq = water_eq.to("L")
    return water_eq / OLYMPIC_SWIMMING_POOL


####################################################################################### MODELS PARAMETER####################################################################################