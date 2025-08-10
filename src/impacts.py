import streamlit as st
from src.utils import (
    format_energy_eq_electric_vehicle,
    format_energy_eq_electricity_consumption_ireland,
    format_energy_eq_electricity_production,
    format_energy_eq_physical_activity,
    format_gwp_eq_airplane_paris_nyc,
    format_wcf_eq_bottled_waters,
    format_wcf_eq_olympic_sized_swimming_pool,
    format_gwp_eq_streaming, 
    format_energy_eq_electricity_consumption_ireland_company,
    format_energy_eq_electricity_production_company,
    format_gwp_eq_airplane_paris_nyc_company,
    format_wcf_eq_olympic_sized_swimming_pool_company,
    impacts_energy_unit_conversion,
    impacts_gwp_unit_conversion,
    impacts_adpe_unit_conversion,
    impacts_pe_unit_conversion,
    impacts_wcf_unit_conversion,
    format_no_sci_min_3_significant,
    format_no_sci_ireland,
    range_plot,
    PhysicalActivity,
    EnergyProduction,
)

############################################################################################################


def get_impacts(model, active_params, total_params, mix_ghg, mix_adpe, mix_pe):
    return 1


############################################################################################################


def display_impacts(impacts, range_percent_impact_one_sided_calculated, company_multiplier: float = 1):

    st.divider()

    col1, col_energy, col_ghg, col2 = st.columns([1,2,2,1])


    with col_energy:
        st.markdown(f"""<p style='font-size:30px;text-align: center;margin-bottom :2px'>⚡️</p><p style='font-size:30px;text-align: center;margin-bottom :2px'><strong>Energy</p>""", unsafe_allow_html = True)
        st.markdown(f'<p align="center">Electricity consumption</p>', unsafe_allow_html = True)
        energy_impact, impacts_energy_units = impacts_energy_unit_conversion(impacts.energy.magnitude,impacts.energy.units, company_multiplier)
        st.markdown(f"""
        <div style="text-align: center;">
        <div style="font-size: 10px;">Error range ±{range_percent_impact_one_sided_calculated["energy"]:.3g} %</div>
        </div>
        """, unsafe_allow_html = True)
        range_plot(energy_impact,energy_impact*(1 - (range_percent_impact_one_sided_calculated["energy"]/100)), 
                   energy_impact*(1 + (range_percent_impact_one_sided_calculated["energy"]/100)), impacts_energy_units)

    with col_ghg:
        st.markdown(f"""<p style='font-size:30px;text-align: center;margin-bottom :2px'>🌍️</p><p style='font-size:30px;text-align: center;margin-bottom :2px'><strong>GHG Emissions</p>""", unsafe_allow_html = True)
        st.markdown(f'<p align="center">Effect on global warming</p>', unsafe_allow_html = True) 
        ghg_impact, impacts_ghg_units = impacts_gwp_unit_conversion(impacts.gwp.magnitude,impacts.gwp.units, company_multiplier)
        st.markdown(f"""
        <div style="text-align: center;">
        <div style="font-size: 10px;">Error range ±{range_percent_impact_one_sided_calculated["gwp"]:.3g} %</div>
        </div>
        """, unsafe_allow_html = True)
        range_plot(ghg_impact,ghg_impact*(1-range_percent_impact_one_sided_calculated["gwp"]/100), 
                   ghg_impact*(1+range_percent_impact_one_sided_calculated["gwp"]/100), impacts_ghg_units)
             

    st.markdown(f'<br>', unsafe_allow_html = True)

    col_adpe, col_pe, col_wcf = st.columns(3)

    with col_adpe:
        st.markdown(f"""<p style='font-size:30px;text-align: center;margin-bottom :2px'>🪨</p>""", unsafe_allow_html = True)
        st.markdown(f"""<p style='font-size:25px;text-align: center;margin-bottom :2px'><strong>Abiotic Resources</p>""", unsafe_allow_html = True)
        st.markdown('<p align="center">Use of metals and minerals</p>', unsafe_allow_html = True)
        adpe_impact, impacts_adpe_units = impacts_adpe_unit_conversion(impacts.adpe.magnitude, impacts.adpe.units, company_multiplier)
        st.markdown(f"""
        <div style="text-align: center;">
        <div style="font-size: 10px;">Error range ±{range_percent_impact_one_sided_calculated["adpe"]:.3g} %</div>
        </div>
        """, unsafe_allow_html = True)
        range_plot(adpe_impact,adpe_impact*(1-range_percent_impact_one_sided_calculated["adpe"]/100), 
                   adpe_impact*(1+range_percent_impact_one_sided_calculated["adpe"]/100), impacts_adpe_units)
             

    with col_pe:
        st.markdown(f"""<p style='font-size:30px;text-align: center;margin-bottom :2px'>⛽️</p>""", unsafe_allow_html = True)
        st.markdown(f"""<p style='font-size:30px;text-align: center;margin-bottom :2px'><strong>Primary Energy</p>""", unsafe_allow_html = True)
        st.markdown(f"""<p style='font-size:15px;text-align: center'>Use of natural energy resources</p>""", unsafe_allow_html = True)
        pe_impact, impacts_pe_units = impacts_pe_unit_conversion(impacts.pe.magnitude, impacts.pe.units, company_multiplier)
        st.markdown(f"""
        <div style="text-align: center;">
        <div style="font-size: 10px;">Error range ±{range_percent_impact_one_sided_calculated["pe"]:.3g} %</div>
        </div>
        """, unsafe_allow_html = True)
        range_plot(pe_impact,pe_impact*(1-range_percent_impact_one_sided_calculated["pe"]/100), 
                   pe_impact*(1+range_percent_impact_one_sided_calculated["pe"]/100), impacts_pe_units)
             

    with col_wcf: 
        st.markdown(f"""<p style='font-size:30px;text-align: center;margin-bottom :2px'>💧</p>""", unsafe_allow_html = True)
        st.markdown(f"""<p style='font-size:30px;text-align: center;margin-bottom :2px'><strong>Water</p>""", unsafe_allow_html = True)
        st.markdown(f'<p align="center">Evaluates the use of water</p>', unsafe_allow_html = True)
        wcf_impact, impacts_wcf_units = impacts_wcf_unit_conversion(impacts.wcf.magnitude, impacts.wcf.units, company_multiplier)

        st.markdown(f"""
        <div style="text-align: center;">
        <div style="font-size: 10px;">Error range ±{range_percent_impact_one_sided_calculated["wcf"]:.3g} %</div>
        </div>
        """, unsafe_allow_html = True)
        range_plot(wcf_impact,wcf_impact*(1-range_percent_impact_one_sided_calculated["wcf"]/100), 
                   wcf_impact*(1+range_percent_impact_one_sided_calculated["wcf"]/100), impacts_wcf_units)
             

############################################################################################################

def display_equivalent_energy(impacts, company_multiplier: float = 1, display_company: bool = False):
    st.markdown('<br>', unsafe_allow_html = True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        impacts_energy_magnitude, impacts_energy_units = impacts_energy_unit_conversion(impacts.energy.magnitude, impacts.energy.units, company_multiplier)
        st.markdown(f"""<p style='font-size:30px;text-align: center;margin-bottom :2px'><strong>⚡️Energy</p>""", unsafe_allow_html = True)
        st.markdown(f"""<p style='font-size:35px;text-align: center'> {impacts_energy_magnitude:.3g} {impacts_energy_units} </p>""", unsafe_allow_html = True)
        

    with col2:
        physical_activity, distance = format_energy_eq_physical_activity(impacts.energy*company_multiplier)
        if physical_activity == PhysicalActivity.WALKING:
            physical_activity = "🚶 " + physical_activity.capitalize()
        if physical_activity == PhysicalActivity.RUNNING:
            physical_activity = "🏃 " + physical_activity.capitalize()

        st.markdown(f'<h4 align="center">{physical_activity}</h4>', unsafe_allow_html = True)
        st.markdown(f"""<p style='font-size:35px;text-align: center'>≈  {distance.magnitude:.3g} <i>{distance.units} </p>""", unsafe_allow_html = True)
    

    with col3:
        ev_eq = format_energy_eq_electric_vehicle(impacts.energy*company_multiplier)
        st.markdown(f"""<p style='font-size:30px;text-align: center;margin-bottom :2px'><strong>🔋 Electric Vehicle</p>""", unsafe_allow_html = True)
        st.markdown(f"""<p style='font-size:35px;text-align: center'>≈ {ev_eq.magnitude:.3g} <i>{ev_eq.units} </p>""", unsafe_allow_html = True)
    

   
    st.divider()
    
    if display_company == True:
        st.markdown('<h3 align="center">What if the company does this request everyday for 251 days (number of work days per year in France in 2025) ?</h3>', unsafe_allow_html = True)
    #TODO add here
    else:
        st.markdown('<h3 align="center">What if 1% of the planet does the same everyday for 1 year ?</h3>', unsafe_allow_html = True)
        st.markdown(f"""<p align="center"> {impacts.energy.magnitude:.3g} {impacts.energy.units} x 1% of 8 billion people x 365 days is ≈ equivalent to</p><br>""", unsafe_allow_html = True)

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        if display_company == True:
            electricity_production, count = format_energy_eq_electricity_production_company(impacts.energy, company_multiplier)
        else:    
            electricity_production, count = format_energy_eq_electricity_production(impacts.energy)            
        if electricity_production == EnergyProduction.NUCLEAR:
            emoji = "☢️"
            name = "Nuclear power plants"
        if electricity_production == EnergyProduction.WIND:
            emoji = "💨️ "
            name = "Wind turbines"
        if display_company == True:
            st.markdown(f'<h4 align="center">{emoji} {format_no_sci_min_3_significant(count.magnitude)} {name} </h4>', unsafe_allow_html = True)            
        else:
            st.markdown(f'<h4 align="center">{emoji} {count.magnitude:.0f} {name} </h4>', unsafe_allow_html = True)
        st.markdown(f'<p align="center">Energy produced yearly </p>', unsafe_allow_html = True)
        
    with col6:
        if display_company == True :
            ireland_count = format_energy_eq_electricity_consumption_ireland_company(impacts.energy, company_multiplier)
            st.markdown(f'<h4 align="center">⚡️ 🇮🇪 {format_no_sci_ireland(ireland_count.magnitude)} x Ireland </h4>', unsafe_allow_html = True)

        else :    
            ireland_count = format_energy_eq_electricity_consumption_ireland(impacts.energy)
            st.markdown(f'<h4 align="center">⚡️ 🇮🇪 {ireland_count.magnitude:.3f} x Ireland </h4>', unsafe_allow_html = True)
        st.markdown(f'<p align="center">Yearly electricity consumption</p>', unsafe_allow_html = True)

    
def display_equivalent_ghg(impacts, company_multiplier: float = 1, display_company: bool = False):
    st.markdown('<br>', unsafe_allow_html = True)
      
    col1, col2, col3 = st.columns(3)

    
    with col1:
        impacts_ghg_magnitude, impacts_ghg_units = impacts_gwp_unit_conversion(impacts.gwp.magnitude, impacts.gwp.units, company_multiplier)        
        st.markdown(f"""<p style='font-size:30px;text-align: center;margin-bottom :2px'><strong>🌍️GHG Emissions</p>""", unsafe_allow_html = True)
        st.markdown(f"""<p style='font-size:35px;text-align: center'> {impacts_ghg_magnitude:.3g} {impacts_ghg_units} </p>""", unsafe_allow_html = True)
       
    
    with col2:
        streaming_eq = format_gwp_eq_streaming(impacts.gwp*company_multiplier)
        st.markdown(f"""<p style='font-size:30px;text-align: center;margin-bottom :2px'><strong>⏯️ Streaming</p>""", unsafe_allow_html = True)
        st.markdown(f"""<p style='font-size:35px;text-align: center'>≈ {streaming_eq.magnitude:.3g} <i>{streaming_eq.units} </p>""", unsafe_allow_html = True)
        
    
    st.divider()
    
    if display_company == True:
        st.markdown('<h3 align="center">What if the company does this request everyday for 251 days (number of work days per year in France in 2025) ?</h3>', unsafe_allow_html = True)
        st.markdown(f"""<p align="center"> {impacts_ghg_magnitude:.3g} {impacts_ghg_units} x 251 days is ≈ equivalent to</p><br>""", unsafe_allow_html = True)
    else:
        st.markdown('<h3 align="center">What if 1% of the planet does the same everyday for 1 year ?</h3>', unsafe_allow_html = True)
        st.markdown(f"""<p align="center"> {impacts.gwp.magnitude:.3g} {impacts.gwp.units} x 1% of 8 billion people x 365 days is ≈ equivalent to</p><br>""", unsafe_allow_html = True)
 

    col4, col5, col6 = st.columns(3)

    with col5:
        if display_company == True:
            paris_nyc_airplane = format_gwp_eq_airplane_paris_nyc_company(impacts.gwp, company_multiplier)
            st.markdown(f"""
                <div style="text-align: center;">
                    <div style="font-size: 30px;">
                        ✈️
                    </div>
                    <div style="font-size: 30px;">
                        {format_no_sci_min_3_significant(paris_nyc_airplane.magnitude)}
                    </div>
                    <div style="font-size: 25px;">
                        Paris ↔ NYC
                    </div>
                </div>
            """, unsafe_allow_html=True)         
        else: 
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

def display_equivalent_wcf(impacts, company_multiplier: float = 1, display_company: bool = False):
    st.markdown('<br>', unsafe_allow_html = True)
      
    col1, col2, col3 = st.columns(3)

    
    with col1:
        impacts_wcf_magnitude, impacts_wcf_units = impacts_gwp_unit_conversion(impacts.wcf.magnitude, impacts.wcf.units, company_multiplier)        
        st.markdown(f"""<p style='font-size:30px;text-align: center;margin-bottom :2px'><strong>💧Water Consumption Footprint</p>""", unsafe_allow_html = True)
        st.markdown(f"""<p style='font-size:35px;text-align: center'> {impacts_wcf_magnitude:.3g} {impacts_wcf_units} </p>""", unsafe_allow_html = True)
       #TODO : fix every on of them so it has the right unit and the right magnitude after multiplying by company multiplyer
    
    with col2:
        bottled_waters_eq = format_wcf_eq_bottled_waters(impacts.wcf*company_multiplier)
        st.markdown(f"""<p style='font-size:30px;text-align: center;margin-bottom :2px'><strong>🚰 Bottled Waters</p>""", unsafe_allow_html = True)
        st.markdown(f"""<p style='font-size:35px;text-align: center'>≈ {bottled_waters_eq.magnitude:.3g} <i> bottles </p>""", unsafe_allow_html = True)

        
    
    st.divider()
    
    if display_company == True:
        st.markdown('<h3 align="center">What if the company does this request everyday for 251 days (number of work days per year in France in 2025) ?</h3>', unsafe_allow_html = True)
        st.markdown(f"""<p align="center"> {impacts_wcf_magnitude:.3g} {impacts_wcf_units} x 251 days is ≈ equivalent to</p><br>""", unsafe_allow_html = True)

    else:
        st.markdown('<h3 align="center">What if 1% of the planet does the same everyday for 1 year ?</h3>', unsafe_allow_html = True)
        st.markdown(f"""<p align="center"> {impacts.wcf.magnitude:.3g} {impacts.wcf.units} x 1% of 8 billion people x 365 days is ≈ equivalent to</p><br>""", unsafe_allow_html = True)

    col4, col5, col6 = st.columns(3)

    with col5:
        if display_company == True:
            olympic_swimming_pool = format_wcf_eq_olympic_sized_swimming_pool_company(impacts.wcf, company_multiplier)
            st.markdown(f"""
                <div style="text-align: center;">
                    <div style="font-size: 30px;">
                        🏊🏼  
                    </div>
                    <div style="font-size: 30px;">
                        {format_no_sci_min_3_significant(olympic_swimming_pool.magnitude)}
                    </div>
                    <div style="font-size: 22px;">
                        Olympic-sized swimming pools
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else :
            olympic_swimming_pool = format_wcf_eq_olympic_sized_swimming_pool(impacts.wcf)
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