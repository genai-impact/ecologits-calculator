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
    format_energy_eq_electricity_production_company,
    format_energy_eq_electricity_consumption_ireland_company,
    format_gwp_eq_airplane_paris_nyc_company,
    format_water_eq_olympic_sized_swimming_pool_company,
    format_energy_eq_physical_activity_company,
    format_gwp_eq_streaming_company,
    format_energy_eq_electric_vehicle_company,
    format_water_eq_bottled_waters_company,
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
        st.markdown("""
        <div style="text-align: center;">
        <div style="font-size: 30px;">⚡️</div>
        <div style="font-size: 25px;">Energy</div>
        </div>
        """, unsafe_allow_html = True)
        st.latex(f'\Large {impacts.energy.magnitude:.3g} \ \large {impacts.energy.units}')
        st.markdown("""
        <div style="height: 10px;"></div>            
        <div style="text-align: center;"><i>Evaluates the electricity consumption<i>
        </div>
        """, unsafe_allow_html = True)

    with col_ghg:
        st.markdown("""
        <div style="text-align: center;">
        <div style="font-size: 30px;">🌍️</div>
        <div style="font-size: 18px;">GHG Emissions</div>
        </div>
        """, unsafe_allow_html = True)
        st.latex(f'\Large {impacts.gwp.magnitude:.3g} \ \large {impacts.gwp.units}')
        st.markdown("""
        <div style="text-align: center;"><i>Evaluates the effect on climate change<i>
        </div>
        """, unsafe_allow_html = True)

    with col_adpe:
        st.markdown("""
        <div style="text-align: center;">
        <div style="font-size: 30px;">🪨</div>
        <div style="font-size: 16px;">Abiotic Resources</div>
        </div>
        """, unsafe_allow_html = True)
        company_impact = impacts.adpe.magnitude
        impacts_adpe_units = impacts.adpe.units
        #errornique 
        if company_impact <= 1 and impacts_adpe_units == "kgSbeq":
            company_impact *= 1000
            impacts_adpe_units = "gSbeq"
        if company_impact <= 1 and impacts_adpe_units == "gSbeq":
            company_impact *= 1000
            impacts_adpe_units = "mgSbeq"
        if company_impact <= 1 and impacts_adpe_units == "mgSbeq":
            company_impact *= 1000
            impacts_adpe_units = "μSbeq"
    ################################################
        if company_impact >= 1000 and impacts_adpe_units == "kgSbeq":
            company_impact /= 1000
            impacts_adpe_units = "tSbeq"
        st.latex(f'\Large {company_impact:.3g} \ \large {impacts_adpe_units}')
        st.markdown("""
        <div style="text-align: center;"><i>Evaluates the use of metals and minerals<i>
        </div>
        """, unsafe_allow_html = True)

    with col_pe:
        st.markdown("""
        <div style="text-align: center;">
        <div style="font-size: 30px;">⛽️</div>
        <div style="font-size: 18px;">Primary Energy</div>
        </div>
        """, unsafe_allow_html = True)
        st.latex(f'\Large {impacts.pe.magnitude:.3g} \ \large {impacts.pe.units}')
        st.markdown("""
        <div style="height: 10px;"></div>
        <div style="text-align: center;"><i>Evaluates the use of energy resources<i>
        </div>
        """, unsafe_allow_html = True)

    with col_water: 
        st.markdown("""
        <div style="text-align: center;">
        <div style="font-size: 30px;">🚰</div>
        <div style="font-size: 25px;">Water</div>
        </div>
        """, unsafe_allow_html = True)
        st.latex(f'\Large {impacts.water.magnitude:.3g} \ \large {impacts.water.units}')
        st.markdown("""
        <div style="text-align: center;"><i>Evaluates the use of water<i>
        </div>
        """, unsafe_allow_html = True)


#################################################################################################
def display_impacts_company(impacts, provider, company_multiplier, location):

    st.divider()

    col_energy, col_ghg, col_adpe, col_pe, col_water = st.columns(5)

    with col_energy:
        st.markdown("""
        <div style="text-align: center;">
        <div style="font-size: 30px;">⚡️</div>
        <div style="font-size: 25px;">Energy</div>
        </div>
        """, unsafe_allow_html = True)
        company_impact = impacts.energy.magnitude * company_multiplier
        impacts_energy_units = impacts.energy.units
        if company_impact >= 1000 and impacts_energy_units == "Wh":
            company_impact /= 1000
            impacts_energy_units = "kWh"
        if company_impact >= 1000 and impacts_energy_units == "kWh":
            company_impact /= 1000
            impacts_energy_units = "MWh"
        if company_impact >= 1000 and impacts_energy_units == "MWh":
            company_impact /= 1000
            impacts_energy_units = "GWh"
        if company_impact >= 1000 and impacts_energy_units == "GWh":
            company_impact /= 1000
            impacts_energy_units = "TWh"
        if company_impact >= 1000 and impacts_energy_units == "TWh":
            company_impact /= 1000
            impacts_energy_units = "PWh"
        st.latex(f'\Large {company_impact:.3g} \ \large {impacts_energy_units}')
        st.markdown("""
        <div style="height: 10px;"></div>            
        <div style="text-align: center;"><i>Evaluates the electricity consumption<i>
        </div>
        """, unsafe_allow_html = True)

    with col_ghg:
        st.markdown("""
        <div style="text-align: center;">
        <div style="font-size: 30px;">🌍️</div>
        <div style="font-size: 18px;">GHG Emissions</div>
        </div>
        """, unsafe_allow_html = True)
        impacts_ghg_units = impacts.gwp.units
        company_impact = impacts.gwp.magnitude * company_multiplier
        if company_impact >= 1000 and impacts_ghg_units == "gCO2eq":
            company_impact /= 1000
            impacts_ghg_units = "kgCO2eq"
        if company_impact >= 1000 and impacts_ghg_units == "kgCO2eq":
            company_impact /= 1000
            impacts_ghg_units = "tCO2eq"
        st.latex(f'\Large {company_impact:.3g} \ \large {impacts_ghg_units}')
        st.markdown("""
        <div style="text-align: center;"><i>Evaluates the effect on climate change<i>
        </div>
        """, unsafe_allow_html = True)

    with col_adpe:
        st.markdown("""
        <div style="text-align: center;">
        <div style="font-size: 30px;">🪨</div>
        <div style="font-size: 16px;">Abiotic Resources</div>
        </div>
        """, unsafe_allow_html = True)
        company_impact = impacts.adpe.magnitude * company_multiplier
        impacts_adpe_units = impacts.adpe.units
        if company_impact <= 1 and impacts_adpe_units == "kgSbeq":
            company_impact *= 1000
            impacts_adpe_units = "gSbeq"
        if company_impact <= 1 and impacts_adpe_units == "gSbeq":
            company_impact *= 1000
            impacts_adpe_units = "mgSbeq"

        ##############    
        if company_impact <= 1 and impacts_adpe_units == "mgSbeq":
            company_impact *= 1000
            impacts_adpe_units = "μSbeq"
        if company_impact >= 1000 and impacts_adpe_units == "kgSbeq":
            company_impact /= 1000
            impacts_adpe_units = "tSbeq"
        st.latex(f'\Large {company_impact:.3g} \ \large {impacts_adpe_units}')
        st.markdown("""
        <div style="text-align: center;"><i>Evaluates the use of metals and minerals<i>
        </div>
        """, unsafe_allow_html = True)

    with col_pe:
        st.markdown("""
        <div style="text-align: center;">
        <div style="font-size: 30px;">⛽️</div>
        <div style="font-size: 18px;">Primary Energy</div>
        </div>
        """, unsafe_allow_html = True)
        company_impact = impacts.pe.magnitude * company_multiplier
        impacts_pe_units = impacts.pe.units
        if company_impact >= 1000 and impacts_pe_units == "kJ":
            company_impact /= 1000
            impacts_pe_units = "MJ"
        if company_impact >= 1000 and impacts_pe_units == "MJ":
            company_impact /= 1000
            impacts_pe_units = "GJ"
        if company_impact >= 1000 and impacts_pe_units == "GJ":
            company_impact /= 1000
            impacts_pe_units = "TJ"
        if company_impact >= 1000 and impacts_pe_units == "TJ":
            company_impact /= 1000
            impacts_pe_units = "PJ"
        st.latex(f'\Large {company_impact:.3g} \ \large {impacts_pe_units}')
        st.markdown("""
        <div style="height: 10px;"></div>
        <div style="text-align: center;"><i>Evaluates the use of energy resources<i>
        </div>
        """, unsafe_allow_html = True)

    with col_water: 
        st.markdown("""
        <div style="text-align: center;">
        <div style="font-size: 30px;">🚰</div>
        <div style="font-size: 25px;">Water</div>
        </div>
        """, unsafe_allow_html = True)
        company_impact = impacts.water.magnitude * company_multiplier
        impacts_water_units = impacts.water.units
        if company_impact >= 1000 and impacts_water_units == "mL":
            company_impact /= 1000
            impacts_water_units = "L"
        if company_impact >= 1000 and impacts_water_units == "L":
            company_impact /= 1000
            impacts_water_units = "kL"
        if company_impact >= 1000 and impacts_water_units == "kL":
            company_impact /= 1000
            impacts_water_units = "ML"
        if company_impact >= 1000 and impacts_water_units == "ML":
            company_impact /= 1000
            impacts_water_units = "GL"
        if company_impact >= 1000 and impacts_water_units == "GL":
            company_impact /= 1000
            impacts_water_units = "TL"
        st.latex(f'\Large {company_impact:.3g} \ \large {impacts_water_units}')
        st.markdown("""
        <div style="text-align: center;"><i>Evaluates the use of water<i>
        </div>
        """, unsafe_allow_html = True)



############################################################################################################

def display_equivalent(impacts, provider, location):

    st.divider()

    ev_eq = format_energy_eq_electric_vehicle(impacts.energy)
    
    streaming_eq = format_gwp_eq_streaming(impacts.gwp)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        physical_activity, distance = format_energy_eq_physical_activity(impacts.energy)
        if physical_activity == PhysicalActivity.WALKING:
            physical_activity_emoji = "🚶 " 
            physical_activity = physical_activity.capitalize()
        if physical_activity == PhysicalActivity.RUNNING:
            physical_activity_emoji = "🏃 " 
            physical_activity = physical_activity.capitalize()

        st.markdown(f"""
        <div style="text-align: center;">
        <div style="font-size: 30px;">{physical_activity_emoji}</div>
        <div style="font-size: 25px;">{physical_activity}</div>
        </div>
        """, unsafe_allow_html = True)
        st.latex(f'\Large {distance.magnitude:.3g} \ \large {distance.units}')
        st.markdown(f'<p align="center"><i>Based on energy consumption<i></p>', unsafe_allow_html = True)

    with col2:
        ev_eq = format_energy_eq_electric_vehicle(impacts.energy)
        st.markdown(f"""
        <div style="text-align: center;">
        <div style="font-size: 30px;">🔋</div>
        <div style="font-size: 22px;">Electric Vehicle</div>
        </div>
        """, unsafe_allow_html = True)
        st.latex(f'\Large {ev_eq.magnitude:.3g} \ \large {ev_eq.units}')
        st.markdown(f'<p align="center"><i>Based on energy consumption<i></p>', unsafe_allow_html = True)

    with col3:
        streaming_eq = format_gwp_eq_streaming(impacts.gwp)
        st.markdown(f"""
        <div style="text-align: center;">
        <div style="font-size: 30px;">⏯️</div>
        <div style="font-size: 25px;">Streaming</div>
        </div>
        """, unsafe_allow_html = True)
        st.latex(f'\Large {streaming_eq.magnitude:.3g} \ \large {streaming_eq.units}')
        st.markdown(f'<p align="center"><i>Based on GHG emissions<i></p>', unsafe_allow_html = True)
    
    with col4:
        #water = water_impact(impacts, provider, location)
        water_eq = format_water_eq_bottled_waters(impacts.water)
        st.markdown(f"""
        <div style="text-align: center;">
        <div style="font-size: 30px;">🚰</div>
        <div style="font-size: 25px;">Bottled Waters</div>
        </div>
        """, unsafe_allow_html = True)
        st.latex(f'\Large {water_eq.magnitude:.3g} \ \large {"bottles"}')
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
        st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 30px;">
                    {emoji} 
                </div>
                <div style="font-size: 30px;">
                    {count.magnitude:.3g} 
                </div>
                <div style="font-size: 25px;">
                    {name}
                </div>
                <div style="font-size: 12px;">
                    (yearly ⚡️ production)
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<p align="center"><i>Based on energy consumption<i></p>', unsafe_allow_html = True)
        
    with col6:
        ireland_count = format_energy_eq_electricity_consumption_ireland(impacts.energy)
        st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 30px;">
                    ☘️🇮🇪
                </div>
                <div style="font-size: 30px;">
                    {ireland_count.magnitude:.3g} 
                </div>
                <div style="font-size: 25px;">
                    Irelands
                </div>
                <div style="font-size: 12px;">
                    (yearly ⚡️ consumption)
                </div>
            </div>
        """, unsafe_allow_html=True)        
        st.markdown(f'<p align="center"><i>Based on energy consumption<i></p>', unsafe_allow_html = True)

    with col7:
        paris_nyc_airplane = format_gwp_eq_airplane_paris_nyc(impacts.gwp)
        st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 30px;">
                    ✈️
                </div>
                <div style="font-size: 30px;">
                    {paris_nyc_airplane.magnitude:.3g}
                </div>
                <div style="font-size: 25px;">
                    Paris ↔ NYC
                </div>
            </div>
        """, unsafe_allow_html=True)        
        st.markdown(f'<p align="center"><i>Based on GHG emissions<i></p>', unsafe_allow_html = True)

    with col8:
        olympic_swimming_pool = format_water_eq_olympic_sized_swimming_pool(impacts.water)
        st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 30px;">
                    🏊🏼  
                </div>
                <div style="font-size: 30px;">
                    {olympic_swimming_pool.magnitude:.3g}
                </div>
                <div style="font-size: 22px;">
                    Olympic-sized swimming pools
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<p align="center"><i>Based on water consumption<i></p>', unsafe_allow_html = True)

#####################################################################################

def display_equivalent_company(impacts, provider, company_multiplier, location):

    st.divider()

    ev_eq = format_energy_eq_electric_vehicle(impacts.energy)
    
    streaming_eq = format_gwp_eq_streaming(impacts.gwp)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        physical_activity, distance = format_energy_eq_physical_activity_company(impacts.energy, company_multiplier)
        if physical_activity == PhysicalActivity.WALKING:
            physical_activity_emoji = "🚶 " 
            physical_activity = physical_activity.capitalize()
        if physical_activity == PhysicalActivity.RUNNING:
            physical_activity_emoji = "🏃 " 
            physical_activity = physical_activity.capitalize()

        st.markdown(f"""
        <div style="text-align: center;">
        <div style="font-size: 30px;">{physical_activity_emoji}</div>
        <div style="font-size: 25px;">{physical_activity}</div>
        </div>
        """, unsafe_allow_html = True)
        value = round(distance.magnitude, 3)
        st.latex(rf'\Large {value:.0g} \ \large {distance.units}')
        st.markdown(f'<p align="center"><i>Based on energy consumption<i></p>', unsafe_allow_html = True)

    with col2:
        ev_eq = format_energy_eq_electric_vehicle_company(impacts.energy, company_multiplier)
        st.markdown(f"""
        <div style="text-align: center;">
        <div style="font-size: 30px;">🔋</div>
        <div style="font-size: 22px;">Electric Vehicle</div>
        </div>
        """, unsafe_allow_html = True)
        value = round(ev_eq.magnitude, 3)
        st.latex(rf'\Large {value:.0f} \ \large {ev_eq.units}')
        st.markdown(f'<p align="center"><i>Based on energy consumption<i></p>', unsafe_allow_html = True)

    with col3:
        streaming_eq = format_gwp_eq_streaming_company(impacts.gwp, company_multiplier)
        st.markdown(f"""
        <div style="text-align: center;">
        <div style="font-size: 30px;">⏯️</div>
        <div style="font-size: 25px;">Streaming</div>
        </div>
        """, unsafe_allow_html = True)
        value = round(streaming_eq.magnitude, 3)
        st.latex(rf'\Large {value:.0f} \ \large {streaming_eq.units}')
        st.markdown(f'<p align="center"><i>Based on GHG emissions<i></p>', unsafe_allow_html = True)
    
    with col4:
        #water = water_impact(impacts, provider, location)
        water_eq = format_water_eq_bottled_waters_company(impacts.water, company_multiplier)
        st.markdown(f"""
        <div style="text-align: center;">
        <div style="font-size: 30px;">🚰</div>
        <div style="font-size: 25px;">Bottled Waters</div>
        </div>
        """, unsafe_allow_html = True)
        value = round(water_eq.magnitude, 3)
        st.latex(rf'\Large {value:.0f} \ \large {"bottles"}')
        st.markdown(f'<p align="center"><i>Based on water consumption, measured in 0.75 L bottles.<i></p>', unsafe_allow_html = True)

    st.divider()
    
    st.markdown('<h3 align="center">What if the company does this request everyday for 251 days (number of work days per year in France in 2025) ?</h3>', unsafe_allow_html = True)

    col5, col6, col7, col8 = st.columns(4)

    with col5:

        electricity_production, count = format_energy_eq_electricity_production_company(impacts.energy, company_multiplier)
        if electricity_production == EnergyProduction.NUCLEAR:
            emoji = "☢️"
            name = "Nuclear power plants"
        if electricity_production == EnergyProduction.WIND:
            emoji = "💨️ "
            name = "Wind turbines"
        st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 30px;">
                    {emoji} 
                </div>
                <div style="font-size: 30px;">
                    {count.magnitude:.3g} 
                </div>
                <div style="font-size: 25px;">
                    {name}
                </div>
                <div style="font-size: 12px;">
                    (yearly ⚡️ production)
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<p align="center"><i>Based on energy consumption<i></p>', unsafe_allow_html = True)
        
    with col6:
        ireland_count = format_energy_eq_electricity_consumption_ireland_company(impacts.energy, company_multiplier)
        st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 30px;">
                    ☘️🇮🇪
                </div>
                <div style="font-size: 30px;">
                    {ireland_count.magnitude:.3g} 
                </div>
                <div style="font-size: 25px;">
                    Irelands
                </div>
                <div style="font-size: 12px;">
                    (yearly ⚡️ consumption)
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<p align="center"><i>Based on energy consumption<i></p>', unsafe_allow_html = True)

    with col7:
        paris_nyc_airplane = format_gwp_eq_airplane_paris_nyc_company(impacts.gwp, company_multiplier)
        st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 30px;">
                    ✈️
                </div>
                <div style="font-size: 30px;">
                    {paris_nyc_airplane.magnitude:.3g}
                </div>
                <div style="font-size: 25px;">
                    Paris ↔ NYC
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<p align="center"><i>Based on GHG emissions<i></p>', unsafe_allow_html = True)

    with col8:
        olympic_swimming_pool = format_water_eq_olympic_sized_swimming_pool_company(impacts.water, company_multiplier)
        st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 30px;">
                    🏊🏼  
                </div>
                <div style="font-size: 30px;">
                    {olympic_swimming_pool.magnitude:.3g}
                </div>
                <div style="font-size: 22px;">
                    Olympic-sized swimming pools
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<p align="center"><i>Based on water consumption<i></p>', unsafe_allow_html = True)
