from calculations import PipelineAnalysis

# Basic sample: 12" crude oil line
results = PipelineAnalysis.analyze_pipeline(
    flow_rate_m3_s=0.05,          # 50 L/s
    pipe_od_mm=323.9,             # 12.75" OD
    wall_thickness_mm=6.4,        # 1/4" wall
    pipe_length_km=50.0,          # 50 km
    elevation_start_m=0,          # start level
    elevation_end_m=100,          # 100 m uphill
    operating_pressure_bar=20,    # 20 bar inlet
    fluid_density_kg_m3=900,      # crude oil
    fluid_viscosity_pa_s=0.001,   # 1 cP
    pipe_roughness_m=0.045e-3,    # new steel
    pipe_grade="X52",             # API 5L X52
)

print("=" * 60)
print("CASE 02 - LONGER 50 KM LINE")
print("=" * 60)

print("\nInlet pressure (bar): ", results['outlet_pressure']['inlet_pressure_bar'])
print("Outlet pressure (bar):", results['outlet_pressure']['outlet_pressure_bar'])
print("Total ΔP (bar):       ", results['pressure_drop']['total_pressure_drop_bar'])
print("Velocity (m/s):       ", results['flow_properties']['velocity_ms'])
print("Safe?                 ", "YES" if results['pressure_containment']['safe'] else "NO")
print("Safety margin (%):    ", results['pressure_containment']['safety_margin_percent'])
