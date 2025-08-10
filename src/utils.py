from dataclasses import dataclass
from enum import Enum

from ecologits.impacts.modeling import Impacts, Energy, GWP, ADPe, PE

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
# 1.77t for one passenger (round-trip) x 100 passenger
AIRPLANE_PARIS_NYC_GWP_EQ = q("177000 kgCO2eq")

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


def format_impacts(impacts: Impacts) -> QImpacts:
    energy, energy_min, energy_max = format_energy(impacts.energy)
    gwp, gwp_min, gwp_max = format_gwp(impacts.gwp)
    adpe, adpe_min, adpe_max = format_adpe(impacts.adpe)
    pe, pe_min, pe_max = format_pe(impacts.pe)
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
                pe_max = pe_max
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
        return (
            QImpacts(
                energy=format_energy(energy),
                gwp=format_gwp(gwp),
                adpe=format_adpe(adpe),
                pe=format_pe(pe),
            ),
            impacts.usage,
            impacts.embodied,
        )


#####################################################################################
### EQUIVALENT FORMATING
#####################################################################################


def format_energy_eq_physical_activity(
    energy: Quantity,
) -> tuple[PhysicalActivity, Quantity]:
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
    return gwp_eq / AIRPLANE_PARIS_NYC_GWP_EQ####################################################################################### MODELS PARAMETER####################################################################################

#####################################################################################
### VISUALIZATIONS
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