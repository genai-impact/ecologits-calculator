from dataclasses import dataclass
from enum import Enum
import math


from ecologits.impacts.modeling import Impacts, Energy, GWP, ADPe, PE, WCF

# from ecologits.tracers.utils import llm_impacts
from pint import UnitRegistry, Quantity
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

#####################################################################################
### UNITS DEFINITION
#####################################################################################

u = UnitRegistry()
u.define("Wh = watt_hour")
u.define("kWh = kilowatt_hour")
u.define("MWh = megawatt_hour")
u.define("GWh = gigawatt_hour")
u.define("TWh = terawatt_hour")
u.define("gCO2eq = gram")
u.define("kgCO2eq = kilogram")
u.define("tCO2eq = metricton")
u.define("kgSbeq = kilogram")
u.define("kJ = kilojoule")
u.define("MJ = megajoule")
u.define("m = meter")
u.define("km = kilometer")
u.define("s = second")
u.define("min = minute")
u.define("h = hour")
u.define('L = liter')
u.define('mL = milliliter')

q = u.Quantity


@dataclass
class QImpacts:
    energy: Quantity
    energy_min : Quantity
    energy_max : Quantity
    gwp: Quantity
    gwp_min : Quantity
    gwp_max : Quantity
    adpe: Quantity
    adpe_min : Quantity
    adpe_max : Quantity
    pe: Quantity
    pe_min : Quantity
    pe_max : Quantity
    wcf: Quantity
    wcf_min : Quantity
    wcf_max : Quantity



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
RUNNING_ENERGY_EQ = q("294 kJ / km")  # running 1 km at 10 km/h with a weight of 70 kg
WALKING_ENERGY_EQ = q("196 kJ / km")  # walking 1 km at 3 km/h with a weight of 70 kg

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
# 1.77t for one passenger (round-trip) x 100 passenger
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
    
    val_min = q(energy.value.min, energy.unit)
    val_max = q(energy.value.max, energy.unit)
    val_mean = (val_min + val_max)/2
    
    if val_max < q("1 kWh"):
        val_min = val_min.to("Wh")
        val_max = val_max.to("Wh")
        val_mean = val_mean.to("Wh")
    
    return val_mean, val_min, val_max
 

def format_gwp(gwp: GWP) -> Quantity:

    val_min = q(gwp.value.min, gwp.unit)
    val_max =q(gwp.value.max, gwp.unit)
    val_mean = (val_min + val_max)/2

    if val_max < q("1 kgCO2eq"):
        val_min = val_min.to("gCO2eq")
        val_max = val_max.to("gCO2eq")
        val_mean = val_mean.to("gCO2eq")
    
    return val_mean, val_min, val_max


def format_adpe(adpe: ADPe) -> Quantity:

    val_min = q(adpe.value.min, adpe.unit)
    val_max = q(adpe.value.max, adpe.unit)
    val_mean = (val_min + val_max)/2
    return val_mean, val_min, val_max


def format_pe(pe: PE) -> Quantity:

    val_min = q(pe.value.min, pe.unit)
    val_max = q(pe.value.max, pe.unit)
    val_mean = (val_min + val_max)/2
    
    if val_max < q("1 MJ"):
        val_min = val_min.to("kJ")
        val_max = val_max.to("kJ")
        val_mean = val_mean.to("kJ")
    
    return val_mean, val_min, val_max


def format_wcf(wcf: WCF) -> Quantity:
    val = q(wcf.value, wcf.unit)
    val_min = q(wcf.value.min, wcf.unit)
    val_max = q(wcf.value.max, wcf.unit)
    val_mean = (val_min + val_max)/2

    if val < q("1 L"):
        val = val.to("mL")
    return val_mean, val_min, val_max

def range_percent_impact_one_sided(impacts: Impacts) -> float:
    impacts_energy_mean = (impacts.energy.value.max + impacts.energy.value.min)/2
    range_percent_energy_one_sided = (impacts.energy.value.max - impacts.energy.value.min) / (2* impacts_energy_mean) * 100
    impacts_gwp_mean = (impacts.gwp.value.max + impacts.gwp.value.min)/2
    range_percent_gwp_one_sided = (impacts.gwp.value.max - impacts.gwp.value.min) / (2* impacts_gwp_mean) * 100
    impacts_adpe_mean = (impacts.adpe.value.max + impacts.adpe.value.min)/2
    range_percent_adpe_one_sided = (impacts.adpe.value.max - impacts.adpe.value.min) / (2* impacts_adpe_mean) * 100
    impacts_pe_mean = (impacts.pe.value.max + impacts.pe.value.min)/2
    range_percent_pe_one_sided = (impacts.pe.value.max - impacts.pe.value.min) / (2* impacts_pe_mean) * 100
    impacts_wcf_mean = (impacts.wcf.value.max + impacts.wcf.value.min)/2
    range_percent_wcf_one_sided = (impacts.wcf.value.max - impacts.wcf.value.min) / (2* impacts_wcf_mean) * 100
        
    results = {
        "energy" : range_percent_energy_one_sided,
        "gwp": range_percent_gwp_one_sided,
        "adpe": range_percent_adpe_one_sided,
        "pe": range_percent_pe_one_sided,
        "wcf" : range_percent_wcf_one_sided
    }
    return results



def format_impacts(impacts: Impacts) -> QImpacts:

    energy, energy_min, energy_max = format_energy(impacts.energy)
    gwp, gwp_min, gwp_max = format_gwp(impacts.gwp)
    adpe, adpe_min, adpe_max = format_adpe(impacts.adpe)
    pe, pe_min, pe_max = format_pe(impacts.pe)
    wcf, wcf_min, wcf_max = format_wcf(impacts.wcf)
    return QImpacts(
                energy= energy,
                energy_min=energy_min,
                energy_max=energy_max,
                gwp = gwp,
                gwp_min = gwp_min,
                gwp_max = gwp_max,
                adpe = adpe,
                adpe_min = adpe_min,
                adpe_max = adpe_max,
                pe = pe,
                pe_min = pe_min,
                pe_max = pe_max,
                wcf = wcf,
                wcf_min = wcf_min,
                wcf_max = wcf_max,
                                ), impacts.usage, impacts.embodied   
    


def split_impacts_u_e(impacts: Impacts) -> QImpacts:
    return impacts.usage, impacts.embodied


def average_range_impacts(x):
    if isinstance(x, float):
        return x
    else:
        return (x.max + x.min) / 2


def format_impacts_expert(impacts: Impacts, display_range: bool) -> QImpacts:
    if display_range:

        return (
            QImpacts(
                energy=format_energy(impacts.energy),
                gwp=format_gwp(impacts.gwp),
                adpe=format_adpe(impacts.adpe),
                pe=format_pe(impacts.pe),
                wcf=format_wcf(impacts.wcf)
            ),
            impacts.usage,
            impacts.embodied,
        )

    else:
        energy = {
            "value": (impacts.energy.value.max + impacts.energy.value.min) / 2,
            "unit": impacts.energy.unit,
        }
        gwp = (impacts.gwp.value.max + impacts.gwp.value.min) / 2
        adpe = (impacts.adpe.value.max + impacts.adpe.value.min) / 2
        pe = (impacts.pe.value.max + impacts.pe.value.min) / 2
        wcf = (impacts.wcf.value.max + impacts.wcf.value.min) / 2
        return (
            QImpacts(
                energy=format_energy(energy),
                gwp=format_gwp(gwp),
                adpe=format_adpe(adpe),
                pe=format_pe(pe),
                wcf=format_wcf(wcf)
            ),
            impacts.usage,
            impacts.embodied,
        )


#####################################################################################
### EQUIVALENT FORMATING
#####################################################################################


def format_energy_eq_physical_activity(
    energy: Quantity,
    company_multiplier: float = 1
) -> tuple[PhysicalActivity, Quantity]:
    energy = energy.to("kJ")
    running_eq = energy / RUNNING_ENERGY_EQ * company_multiplier
    if running_eq > q("1 km"):
        return PhysicalActivity.RUNNING, running_eq

    walking_eq = energy / WALKING_ENERGY_EQ
    if walking_eq < q("1 km"):
        walking_eq = walking_eq.to("meter")
    return PhysicalActivity.WALKING, walking_eq


def format_energy_eq_electric_vehicle(energy: Quantity, company_multiplier: float = 1) -> Quantity:
    energy = energy.to("kWh")
    ev_eq = energy / EV_ENERGY_EQ * company_multiplier
    if ev_eq < q("1 km"):
        ev_eq = ev_eq.to("meter")
    return ev_eq


def format_gwp_eq_streaming(gwp: Quantity, company_multiplier: float = 1) -> Quantity:
    gwp = gwp.to("kgCO2eq")
    streaming_eq = gwp * STREAMING_GWP_EQ * company_multiplier
    if streaming_eq < q("1 h"):
        streaming_eq = streaming_eq.to("min")
    if streaming_eq < q("1 min"):
        streaming_eq = streaming_eq.to("s")
    return streaming_eq


def format_wcf_eq_bottled_waters(wcf: Quantity, company_multiplier: float = 1) -> Quantity:
    wcf = wcf.to("L")
    bottled_water_eq = wcf / BOTTLED_WATERS_EQ * company_multiplier
    return bottled_water_eq


def format_energy_eq_electricity_production(
    energy: Quantity,
) -> tuple[EnergyProduction, Quantity]:
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

def format_wcf_eq_olympic_sized_swimming_pool(water: Quantity) -> Quantity:
    water_eq = water * ONE_PERCENT_WORLD_POPULATION * DAYS_IN_YEAR
    water_eq = water_eq.to("L")
    return water_eq / OLYMPIC_SWIMMING_POOL


##############################################################3

def format_energy_eq_electricity_production_company(
    energy: Quantity,
    company_multiplier: float = 1
) -> tuple[EnergyProduction, Quantity]:
    electricity_eq = energy * company_multiplier * WORKDAYS_IN_YEAR_FRANCE
    electricity_eq = electricity_eq.to("TWh")
    if electricity_eq > YEARLY_NUCLEAR_ENERGY_EQ:
        return EnergyProduction.NUCLEAR, electricity_eq / YEARLY_NUCLEAR_ENERGY_EQ
    electricity_eq = electricity_eq.to("GWh")
    return EnergyProduction.WIND, electricity_eq / YEARLY_WIND_ENERGY_EQ


def format_energy_eq_electricity_consumption_ireland_company(energy: Quantity, company_multiplier: float = 1) -> Quantity:
    electricity_eq = energy * company_multiplier * WORKDAYS_IN_YEAR_FRANCE
    electricity_eq = electricity_eq.to("TWh")
    return electricity_eq / YEARLY_IRELAND_ELECTRICITY_CONSUMPTION


def format_gwp_eq_airplane_paris_nyc_company(gwp: Quantity, company_multiplier: float = 1) -> Quantity:
    gwp_eq = gwp * company_multiplier * WORKDAYS_IN_YEAR_FRANCE
    gwp_eq = gwp_eq.to("kgCO2eq")
    return gwp_eq / AIRPLANE_PARIS_NYC_GWP_EQ

def format_wcf_eq_olympic_sized_swimming_pool_company(water: Quantity, company_multiplier: float = 1) -> Quantity:
    water_eq = water * company_multiplier * WORKDAYS_IN_YEAR_FRANCE
    water_eq = water_eq.to("L")
    return water_eq / OLYMPIC_SWIMMING_POOL

#####################################################################################
### UNIT CONVERSION
#####################################################################################

def impacts_energy_unit_conversion(impacts_energy_magnitude, impacts_energy_units, company_multiplier):
    energy_impact = impacts_energy_magnitude * company_multiplier
    if energy_impact >= 1000 and impacts_energy_units == "Wh":
        energy_impact /= 1000
        impacts_energy_units = "kWh"
    if energy_impact >= 1000 and impacts_energy_units == "kWh":
        energy_impact /= 1000
        impacts_energy_units = "MWh"
    if energy_impact >= 1000 and impacts_energy_units == "MWh":
        energy_impact /= 1000
        impacts_energy_units = "GWh"
    if energy_impact >= 1000 and impacts_energy_units == "GWh":
        energy_impact /= 1000
        impacts_energy_units = "TWh"
    if energy_impact >= 1000 and impacts_energy_units == "TWh":
        energy_impact /= 1000
        impacts_energy_units = "PWh"
    
    return (energy_impact, impacts_energy_units)

def impacts_gwp_unit_conversion(impacts_gwp_magnitude, impacts_ghg_units, company_multiplier):
    ghg_impact = impacts_gwp_magnitude * company_multiplier
    if ghg_impact >= 1000 and impacts_ghg_units == "gCO2eq":
        ghg_impact /= 1000
        impacts_ghg_units = "kgCO2eq"
    if ghg_impact >= 1000 and impacts_ghg_units == "kgCO2eq":
        ghg_impact /= 1000
        impacts_ghg_units = "tCO2eq"
    
    return (ghg_impact, impacts_ghg_units)

def impacts_adpe_unit_conversion(impacts_adpe_magnitude, impacts_adpe_units, company_multiplier):
    adpe_impact = impacts_adpe_magnitude * company_multiplier
    if adpe_impact <= 1 and impacts_adpe_units == "kgSbeq":
        adpe_impact *= 1000
        impacts_adpe_units = "gSbeq"
    if adpe_impact <= 1 and impacts_adpe_units == "gSbeq":
        adpe_impact *= 1000
        impacts_adpe_units = "mgSbeq"
    if adpe_impact <= 1 and impacts_adpe_units == "mgSbeq":
        adpe_impact *= 1000
        impacts_adpe_units = "μSbeq"
    if adpe_impact >= 1000 and impacts_adpe_units == "kgSbeq":
        adpe_impact /= 1000
        impacts_adpe_units = "tSbeq"
    
    return (adpe_impact, impacts_adpe_units)

def impacts_pe_unit_conversion(impacts_pe_magnitude, impacts_pe_units, company_multiplier):
    pe_impact = impacts_pe_magnitude * company_multiplier
    if pe_impact >= 1000 and impacts_pe_units == "kJ":
        pe_impact /= 1000
        impacts_pe_units = "MJ"
    if pe_impact >= 1000 and impacts_pe_units == "MJ":
        pe_impact /= 1000
        impacts_pe_units = "GJ"
    if pe_impact >= 1000 and impacts_pe_units == "GJ":
        pe_impact /= 1000
        impacts_pe_units = "TJ"
    if pe_impact >= 1000 and impacts_pe_units == "TJ":
        pe_impact /= 1000
        impacts_pe_units = "PJ"
    
    return (pe_impact, impacts_pe_units)

def impacts_wcf_unit_conversion(impacts_wcf_magnitude, impacts_wcf_units, company_multiplier):
    wcf_impact = impacts_wcf_magnitude * company_multiplier
    impacts_wcf_units = impacts_wcf_units
    if wcf_impact >= 1000 and impacts_wcf_units == "mL":
        wcf_impact /= 1000
        impacts_wcf_units = "L"
    if wcf_impact >= 1000 and impacts_wcf_units == "L":
        wcf_impact /= 1000
        impacts_wcf_units = "kL"
    if wcf_impact >= 1000 and impacts_wcf_units == "kL":
        wcf_impact /= 1000
        impacts_wcf_units = "ML"
    if wcf_impact >= 1000 and impacts_wcf_units == "ML":
        wcf_impact /= 1000
        impacts_wcf_units = "GL"
    if wcf_impact >= 1000 and impacts_wcf_units == "GL":
        wcf_impact /= 1000
        impacts_wcf_units = "TL"
    
    return (wcf_impact, impacts_wcf_units)


def format_no_sci_min_3_significant(x, total_sig=4):
    #to show at a minimum 3 significant digits 
    if x == 0:
        return f"{0:.{total_sig}f}"
    x = float(x)
    exp = math.floor(math.log10(abs(x)))
    # number of digits to reach the first significant number
    if exp >= 0:
        decimals = max(0, total_sig - (exp + 1))
    else:
        #if the number is below zero, need to count in the digits after decimal
        decimals = (-exp - 1) + total_sig
    return f"{x:.{decimals}f}"

def format_no_sci_ireland(x, total_sig=4):
    if x == 0:
        return f"{0:.{total_sig}f}"
    x = float(x)
    exp = math.floor(math.log10(abs(x)))
    if exp >= 0:
        decimals = max(0, total_sig - (exp + 1))
        return f"{x:.{decimals}f}"
    elif 0 > exp > -2:
        decimals = (-exp - 1) + total_sig
        return f"{x:.{decimals}f}"
    else : #exp <= -2
        #convert to percentage
        x = x*100
        exp = exp + 2 
        if exp >= 0:
            decimals = max(0, total_sig - (exp + 1))
            return f"{x:.{decimals}f} %"
        else:
            decimals = (-exp - 1) + total_sig
            return f"{x:.{decimals}f} %"

#####################################################################################
### VISUALIZATION
#####################################################################################
def range_plot(mean_val, min_val, max_val, unit):
    #prevents invalid values
    if min_val > max_val:
        min_val, max_val = max_val, min_val
    if any(map(lambda v: v is None or (isinstance(v, float) and math.isnan(v)),
               [mean_val, min_val, max_val])):
        st.warning("Valeurs invalides pour le range plot.")
        return
    mean_clamped = min(max(mean_val, min_val), max_val)

    fig = go.Figure()

    #background
    fig.add_trace(go.Bar(
        x=[max_val - min_val],
        y=[''],                  
        base=min_val,            
        orientation='h',
        marker=dict(color="#0B3B36"),
        showlegend=False,
        hoverinfo='skip',
    ))
    fig.update_layout(height=120, bargap=0.6)

    fig.add_shape(
        type="line",
        x0=mean_clamped, x1=mean_clamped,
        y0=0.2, y1=0.8,
        xref='x', yref='paper',
        line=dict(color='#00BF63', width=3)
    )
    

    for xval, label, ypaper in [(min_val, "Min", -0.10), (max_val, "Max", -0.10),
                                (min_val, f"{min_val:.3g} {unit}", -0.25),
                                (max_val, f"{max_val:.3g} {unit}", -0.25)]:
        fig.add_annotation(
            x=xval, y=ypaper,
            xref='x', yref='paper',
            text=label,
            showarrow=False,
            font=dict(color="black", size=14)
        )


    fig.add_annotation(
        x=mean_clamped, y=1.10,
        xref='x', yref='paper',
        text=f'{mean_val:.3g} {unit}',
        showarrow=False,
        font=dict(color="black", size=28)
    )

    fig.update_layout(
        height=160,
        width=400,
        xaxis=dict(range=[min_val, max_val], showgrid=False, showticklabels=False),
        yaxis=dict(showticklabels=False),
        plot_bgcolor='white',
        margin=dict(l=60, r=60, t=10, b=40),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)