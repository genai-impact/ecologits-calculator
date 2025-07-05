import streamlit as st
import ecologits
from src.utils import (
    format_energy_eq_electric_vehicle,
    format_energy_eq_electricity_consumption_ireland,
    format_energy_eq_electricity_production,
    format_energy_eq_physical_activity,
    format_gwp_eq_airplane_paris_nyc,
    format_gwp_eq_streaming,
    format_water_eq_bottled_waters,
    format_water_eq_olympic_sized_swimming_pool,
    PhysicalActivity,
    EnergyProduction,
    AI_COMPANY_TO_DATA_CENTER_PROVIDER,
    PROVIDER_PUE,
    PROVIDER_WUE_ONSITE
)
from src.electricity_mix import COUNTRY_CODES, find_electricity_mix, dataframe_electricity_mix


############################################################################################################

def get_impacts(model, active_params, total_params, mix_ghg, mix_adpe, mix_pe):

    return 1

############################################################################################################


def display_impacts(impacts, provider, location):

    st.divider()

    col_energy, col_ghg, col_adpe, col_pe, col_water = st.columns(5)

    with col_energy:
        st.markdown('<h4 align="center">⚡️ Energy</h4>', unsafe_allow_html = True)
        st.latex(f'\Large {impacts.energy.magnitude:.3g} \ \large {impacts.energy.units}')
        st.markdown(f'<p align="center"><i>Evaluates the electricity consumption<i></p>', unsafe_allow_html = True)

    with col_ghg:
        st.markdown('<h4 align="center">🌍️ GHG Emissions</h4>', unsafe_allow_html = True)
        st.latex(f'\Large {impacts.gwp.magnitude:.3g} \ \large {impacts.gwp.units}')
        st.markdown(f'<p align="center"><i>Evaluates the effect on global warming<i></p>', unsafe_allow_html = True)

    with col_adpe:
        st.markdown('<h4 align="center">🪨 Abiotic Resources</h4>', unsafe_allow_html = True)
        st.latex(f'\Large {impacts.adpe.magnitude:.3g} \ \large {impacts.adpe.units}')
        st.markdown(f'<p align="center"><i>Evaluates the use of metals and minerals<i></p>', unsafe_allow_html = True)

    with col_pe:
        st.markdown('<h4 align="center">⛽️ Primary Energy</h4>', unsafe_allow_html = True)
        st.latex(f'\Large {impacts.pe.magnitude:.3g} \ \large {impacts.pe.units}')
        st.markdown(f'<p align="center"><i>Evaluates the use of energy resources<i></p>', unsafe_allow_html = True)


    with col_water: #je sais pas où se trouve magnitude ou impact, donc j'ai commencé par une approche locale
        st.markdown('<h4 align="center">🚰 Water</h4>', unsafe_allow_html = True)
        water = water_impact(impacts, provider, location)
        if water >= 1 : 
            st.latex(f'\Large {water:.3g} \ \large {"Liters"}')
        else :
            st.latex(f'\Large {water * 1000 :.3g} \ \large {"mLiters"}')
        st.markdown(f'<p align="center"><i>Evaluates the use of water<i></p>', unsafe_allow_html = True)


# WCF = E_server * [WUE_on-site + PUE * WUE_off-site] + embodied (embodied not yet implemented, embodied = T * WCF_embodied / lifetime)
# WCF : Water Consumption Footprint for the request
# E_server : energy cost at the server for the request 
# WUE_on-site : Water usage efficiency at the data center 
# PUE: Power usage efficiency at the data center 
# WUE_off-site: Water usage efficiency of the local electricity mix 
def water_impact(impacts, provider, location):
    energy = impacts.energy.magnitude 
    PUE = PROVIDER_PUE[AI_COMPANY_TO_DATA_CENTER_PROVIDER[provider.lower()]]
    WUE_onsite = PROVIDER_WUE_ONSITE[AI_COMPANY_TO_DATA_CENTER_PROVIDER[provider.lower()]]
    #WUE_on-site = 
    #pas de variation régionale pour le simulateur simple mais oui pour le simulateur expert mode
    try:
        WUE_offsite = float(find_electricity_mix([x[1] for x in COUNTRY_CODES if x[0] ==location][0])[4])
    except :    
        WUE_offsite = float(find_electricity_mix(["WOR"][0])[4])
        st.warning(f"Lacking data on {location}, showing global average data.")

    water_consumption = energy * (WUE_onsite + PUE * WUE_offsite) /1000 #5.04 est la valeur WUF moyenne du globe

    #/1000 parce que les WUE et PUE sont en kWh
    return water_consumption

############################################################################################################

def display_equivalent(impacts, provider, location):

    st.divider()

    ev_eq = format_energy_eq_electric_vehicle(impacts.energy)
    
    streaming_eq = format_gwp_eq_streaming(impacts.gwp)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        physical_activity, distance = format_energy_eq_physical_activity(impacts.energy)
        if physical_activity == PhysicalActivity.WALKING:
            physical_activity = "🚶 " + physical_activity.capitalize()
        if physical_activity == PhysicalActivity.RUNNING:
            physical_activity = "🏃 " + physical_activity.capitalize()

        st.markdown(f'<h4 align="center">{physical_activity}</h4>', unsafe_allow_html = True)
        st.latex(f'\Large {distance.magnitude:.3g} \ \large {distance.units}')
        st.markdown(f'<p align="center"><i>Based on energy consumption<i></p>', unsafe_allow_html = True)

    with col2:
        ev_eq = format_energy_eq_electric_vehicle(impacts.energy)
        st.markdown(f'<h4 align="center">🔋 Electric Vehicle</h4>', unsafe_allow_html = True)
        st.latex(f'\Large {ev_eq.magnitude:.3g} \ \large {ev_eq.units}')
        st.markdown(f'<p align="center"><i>Based on energy consumption<i></p>', unsafe_allow_html = True)

    with col3:
        streaming_eq = format_gwp_eq_streaming(impacts.gwp)
        st.markdown(f'<h4 align="center">⏯️ Streaming</h4>', unsafe_allow_html = True)
        st.latex(f'\Large {streaming_eq.magnitude:.3g} \ \large {streaming_eq.units}')
        st.markdown(f'<p align="center"><i>Based on GHG emissions<i></p>', unsafe_allow_html = True)
    
    with col4:
        water = water_impact(impacts, provider, location)
        water_eq = format_water_eq_bottled_waters(water)
        st.markdown(f'<h4 align="center">🚰 Bottled waters</h4>', unsafe_allow_html = True)
        st.latex(f'\Large {water_eq:.3g} \ \large {"bottles"}')
        st.markdown(f'<p align="center"><i>Based on water consumption, measured in 0.75 L bottles.<i></p>', unsafe_allow_html = True)
    

    st.divider()
    
    st.markdown('<h3 align="center">What if 1% of the planet does this request everyday for 1 year ?</h3>', unsafe_allow_html = True)
    st.markdown('<p align="center">If this use case is largely deployed around the world, the equivalent impacts would be the impacts of this request x 1% of 8 billion people x 365 days in a year.</p>', unsafe_allow_html = True)

    col5, col6, col7, col8 = st.columns(4)

    with col5:

        electricity_production, count = format_energy_eq_electricity_production(impacts.energy)
        if electricity_production == EnergyProduction.NUCLEAR:
            emoji = "☢️"
            name = "Nuclear power plants"
        if electricity_production == EnergyProduction.WIND:
            emoji = "💨️ "
            name = "Wind turbines"
        st.markdown(f'<h4 align="center">{emoji} {count.magnitude:.0f} {name} <span style="font-size: 12px">\n (yearly ⚡️ production)</span></h2></h4>', unsafe_allow_html = True)
        st.markdown(f'<p align="center"><i>Based on energy consumption<i></p>', unsafe_allow_html = True)
        
    with col6:
        ireland_count = format_energy_eq_electricity_consumption_ireland(impacts.energy)
        st.markdown(f'<h4 align="center">🇮🇪 {ireland_count.magnitude:.3f} x Irelands <span style="font-size: 12px">\n (yearly ⚡️ consumption)</span></h2></h4>', unsafe_allow_html = True)
        st.markdown(f'<p align="center"><i>Based on energy consumption<i></p>', unsafe_allow_html = True)

    with col7:
        paris_nyc_airplane = format_gwp_eq_airplane_paris_nyc(impacts.gwp)
        st.markdown(f'<h4 align="center">✈️ {round(paris_nyc_airplane.magnitude):,} Paris ↔ NYC</h4>', unsafe_allow_html = True)
        st.markdown(f'<p align="center"><i>Based on GHG emissions<i></p>', unsafe_allow_html = True)

    with col8:
        water = water_impact(impacts, provider, location)
        water_eq = format_water_eq_olympic_sized_swimming_pool(water)
        st.markdown(f'<h4 align="center">🏊🏼 {round(water_eq):,} Olympic-sized swimming pools</h4>', unsafe_allow_html = True)
        st.markdown(f'<p align="center"><i>Based on water consumption<i></p>', unsafe_allow_html = True)

