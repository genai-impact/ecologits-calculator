from dataclasses import dataclass
from enum import Enum

from ecologits.impacts.modeling import Impacts, Energy, GWP, ADPe, PE, WCF, Usage, Embodied

from pint import UnitRegistry, Quantity
import streamlit as st
import plotly.graph_objects as go

#####################################################################################
### UNITS DEFINITION
#####################################################################################

u = UnitRegistry()
u.define("Wh = watt_hour")
u.define("mWh = milliwatt_hour")
u.define("kWh = kilowatt_hour")
u.define("MWh = megawatt_hour")
u.define("GWh = gigawatt_hour")
u.define("TWh = terawatt_hour")
u.define("gCO2eq = gram")
u.define("mgCO2eq = milligram")
u.define("kgCO2eq = kilogram")
u.define("tCO2eq = metricton")
u.define("kgSbeq = kilogram")
u.define("gSbeq = gram")
u.define("mgSbeq = milligram")
u.define("µgSbeq = microgram")
u.define("kJ = kilojoule")
u.define("MJ = megajoule")
u.define("L = liter")
u.define("mL = milliliter")
u.define("m = meter")
u.define("km = kilometer")
u.define("s = second")
u.define("min = minute")
u.define("h = hour")
q = u.Quantity


@dataclass
class QImpacts:
    energy: Quantity
    gwp: Quantity
    adpe: Quantity
    pe: Quantity
    wcf: Quantity
    ranges: bool = False
    energy_min: Quantity | None = None
    energy_max: Quantity | None = None
    gwp_min: Quantity | None = None
    gwp_max: Quantity | None = None
    adpe_min: Quantity | None = None
    adpe_max: Quantity | None = None
    pe_min: Quantity | None = None
    pe_max: Quantity | None = None
    wcf_min: Quantity | None = None
    wcf_max: Quantity | None = None



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


def format_energy(energy_value: float, energy_unit = Energy(value=0.).unit) -> Quantity:
    val = q(energy_value, energy_unit)
    if val < q("1 kWh"):
        val = val.to("Wh")
    if val < q("1 Wh"):
        val = val.to("mWh")
    return val
 

def format_gwp(gwp_value: float, gwp_unit = GWP(value=0.).unit) -> Quantity:
    val = q(gwp_value, gwp_unit)
    if val < q("1 kgCO2eq"):
        val = val.to("gCO2eq")
    if val < q("1 gCO2eq"):
        val = val.to("mgCO2eq")
    return val


def format_adpe(adpe_value: float, adpe_unit = ADPe(value=0.).unit) -> Quantity:
    val = q(adpe_value, adpe_unit)
    if val < q("1 kgSbeq"):
        val = val.to("gSbeq")
    if val < q("1 gSbeq"):
        val = val.to("mgSbeq")
    if val < q("1 mgSbeq"):
        val = val.to("µgSbeq")
    return val


def format_pe(pe_value: float, pe_unit = PE(value=0.).unit) -> Quantity:
    val = q(pe_value, pe_unit)
    if val < q("1 MJ"):
        val = val.to("kJ")
    return val


def format_wcf(wcf_value: float, wcf_unit = WCF(value=0.).unit) -> Quantity:
    val = q(wcf_value, wcf_unit)
    if val < q("1 L"):
        val = val.to("mL")
    return val


def format_impacts(impacts: Impacts) -> tuple[QImpacts, Usage, Embodied]:
    if isinstance(impacts.energy.value, float):
        return QImpacts(
            energy=format_energy(impacts.energy.value),
            gwp=format_gwp(impacts.gwp.value),
            adpe=format_adpe(impacts.adpe.value),
            pe=format_pe(impacts.pe.value),
            wcf=format_wcf(impacts.wcf.value)
        ), impacts.usage, impacts.embodied

    else:
        energy = format_energy(impacts.energy.value.mean)
        gwp = format_gwp(impacts.gwp.value.mean)
        adpe = format_adpe(impacts.adpe.value.mean)
        pe = format_pe(impacts.pe.value.mean)
        wcf = format_wcf(impacts.wcf.value.mean)

        return QImpacts(
            energy=energy,
            energy_min=format_energy(impacts.energy.value.min).to(energy.units),
            energy_max=format_energy(impacts.energy.value.max).to(energy.units),
            gwp=gwp,
            gwp_min=format_gwp(impacts.gwp.value.min).to(gwp.units),
            gwp_max=format_gwp(impacts.gwp.value.max).to(gwp.units),
            adpe=adpe,
            adpe_min=format_adpe(impacts.adpe.value.min).to(adpe.units),
            adpe_max=format_adpe(impacts.adpe.value.max).to(adpe.units),
            pe=pe,
            pe_min=format_pe(impacts.pe.value.min).to(pe.units),
            pe_max=format_pe(impacts.pe.value.max).to(pe.units),
            wcf=wcf,
            wcf_min=format_wcf(impacts.wcf.value.min).to(wcf.units),
            wcf_max=format_wcf(impacts.wcf.value.max).to(wcf.units),
            ranges=True
        ), impacts.usage, impacts.embodied


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
    return gwp_eq / AIRPLANE_PARIS_NYC_GWP_EQ

#####################################################################################
### VISUALIZATIONS
#####################################################################################

def range_plot (mean_val, min_val, max_val, unit):
    
    fig = go.Figure()

    # Background bar
    fig.add_trace(go.Bar(
        x=[max_val],
        y=[''],
        orientation='h',
        marker=dict(color="#0B3B36"),
        showlegend=False,
        hoverinfo='skip',
    ))
    
    # Vertical line 
    fig.add_shape(
        type="line",
        x0=mean_val, y0=-1,
        x1=mean_val, y1=1,
        line=dict(color='#00BF63', width=3, dash="solid"),
        #name="Average"
    )

    # Add labels
    for val, pos, text in zip([max_val, min_val]*2,[0.85,0.85,1.6,1.6], ["Max", "Min", f'{max_val:.3g} {unit}', f'{min_val:.3g} {unit}']):
        fig.add_annotation(
            x=val,
            y=-pos,
            text=text,
            showarrow=False,
            font=dict(color="black", size=16)
    )
        
    fig.add_annotation(
            x=mean_val,
            y=1.65,
            text=f'{mean_val:.3g} {unit}',
            showarrow=False,
            font=dict(color="black",  size=35)
    )
     
    # Layout adjustments
    fig.update_layout(
        height=160,
        width = 400,
        xaxis=dict(range=[min_val, max_val], showgrid=False, showticklabels=False),
        yaxis=dict(showticklabels=False),
        plot_bgcolor='white',
        margin=dict(l=100, r=100, t=0, b=20),
        showlegend=False
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)
