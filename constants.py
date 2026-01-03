"""
Pipeline Design Tool - Physical Constants and Standards
Educational Template for Young Pipeline Engineers

This module contains fundamental constants, unit conversions,
and reference standards used in pipeline calculations.
"""

# ============================================================================
# PHYSICAL CONSTANTS
# ============================================================================

# Acceleration due to gravity
G_ACCELERATION = 9.81  # m/s²

# Water properties (at 15°C, 1 atm)
WATER_DENSITY = 1000  # kg/m³
WATER_VISCOSITY = 0.001  # Pa·s (1 centiPoise)

# Atmospheric pressure
ATM_PRESSURE_PA = 101325  # Pa
ATM_PRESSURE_BAR = 1.01325  # bar

# ============================================================================
# PIPE GRADES - API 5L SPECIFICATION
# ============================================================================

PIPE_GRADES = {
    "X42": {
        "name": "API 5L X42",
        "SMYS": 290,  # MPa - Specified Minimum Yield Strength
        "tensile_strength": 414,  # MPa
        "description": "Carbon Steel, Seamless/Welded"
    },
    "X52": {
        "name": "API 5L X52",
        "SMYS": 359,
        "tensile_strength": 455,
        "description": "Carbon Steel, Higher grade"
    },
    "X60": {
        "name": "API 5L X60",
        "SMYS": 414,
        "tensile_strength": 517,
        "description": "High Strength Carbon Steel"
    },
    "X65": {
        "name": "API 5L X65",
        "SMYS": 448,
        "tensile_strength": 531,
        "description": "High Strength Carbon Steel"
    },
}

# ============================================================================
# DESIGN STANDARDS - Safety Factors
# ============================================================================

DESIGN_FACTORS = {
    "ASME B31.8": {
        "name": "Gas Piping Code",
        "location_class_1": 0.72,  # 72% of SMYS [web:53]
        "location_class_2": 0.60,
        "location_class_3": 0.50,
    },
    "ASME B31.4": {
        "name": "Liquid Transportation Code",
        "normal_operation": 0.72,  # 72% of SMYS [web:47][web:50]
        "high_consequence_area": 0.60,
    },
}

# ============================================================================
# PIPE ROUGHNESS VALUES
# ============================================================================

PIPE_ROUGHNESS = {
    "new_steel": {
        "value": 0.045,  # mm
        "description": "New seamless steel"
    },
    "commercial_steel": {
        "value": 0.045,
        "description": "Commercial steel, typical condition"
    },
    "corroded_steel": {
        "value": 0.15,
        "description": "Steel after 10+ years, slight corrosion"
    },
    "heavily_corroded": {
        "value": 0.25,
        "description": "Steel with significant corrosion"
    },
    "galvanized": {
        "value": 0.15,
        "description": "Galvanized steel"
    },
}

# ============================================================================
# FLUID PROPERTIES
# ============================================================================

FLUID_TYPES = {
    "crude_oil": {
        "name": "Crude Oil",
        "density_range": (800, 950),  # kg/m³
        "viscosity_cSt": 5,  # Typical centiStokes at operating temp
        "default_density": 900,
    },
    "natural_gas": {
        "name": "Natural Gas",
        "density_range": (0.7, 1.0),  # kg/m³ at std conditions
        "viscosity_cSt": 0.015,
        "default_density": 0.85,
    },
    "water": {
        "name": "Water",
        "density_range": (990, 1000),
        "viscosity_cSt": 1.0,
        "default_density": 1000,
    },
}

# ============================================================================
# TERRAIN CLASSIFICATIONS
# ============================================================================

TERRAIN_TYPES = {
    "desert": {
        "name": "Desert/Sandy",
        "surface_roughness": 0.5,  # mm
        "burial_depth_min": 0.5,  # m
        "corrosion_class": "high",  # High UV, temperature fluctuation
        "description": "Low rainfall, high temperature variation, sand abrasion"
    },
    "rocky": {
        "name": "Rocky/Hard soil",
        "surface_roughness": 2.0,
        "burial_depth_min": 0.3,
        "corrosion_class": "medium",
        "description": "Hard ground, bedrock present, limited burial depth"
    },
    "sandy": {
        "name": "Sandy/Alluvial",
        "surface_roughness": 1.0,
        "burial_depth_min": 0.6,
        "corrosion_class": "medium",
        "description": "Alluvial deposits, easy excavation, settlement prone"
    },
}

# ============================================================================
# CROSSING TYPES AND SPECIFICATIONS
# ============================================================================

CROSSING_TYPES = {
    "road_bore": {
        "name": "Road Crossing - Boring",
        "method": "Horizontal Directional Drilling (HDD)",
        "typical_depth": 1.5,  # m below road
        "pipe_protection": "Casing required",
    },
    "road_open": {
        "name": "Road Crossing - Open",
        "method": "Cut and cover",
        "typical_depth": 1.2,  # m below road
        "pipe_protection": "Protection slab/cover",
    },
    "nalla_buried": {
        "name": "Nalla Crossing - Buried",
        "method": "Open trench",
        "typical_depth": 1.5,  # m below nalla bed
        "pipe_protection": "Burial + slope protection",
    },
    "nalla_aerial": {
        "name": "Nalla Crossing - Aerial",
        "method": "Above ground on trestle",
        "typical_depth": 0,
        "pipe_protection": "Support structure + insulation",
    },
}

# ============================================================================
# UNIT CONVERSION FACTORS
# ============================================================================

LENGTH_CONVERSIONS = {
    "mm_to_inch": 0.0394,
    "inch_to_mm": 25.4,
    "m_to_km": 0.001,
    "km_to_m": 1000,
    "m_to_ft": 3.28084,
}

PRESSURE_CONVERSIONS = {
    "bar_to_pa": 100000,
    "pa_to_bar": 1e-5,
    "mpa_to_bar": 10,
    "bar_to_mpa": 0.1,
    "psi_to_bar": 0.0689,
    "bar_to_psi": 14.5038,
}

VELOCITY_CONVERSIONS = {
    "ms_to_kmh": 3.6,
    "kmh_to_ms": 0.2778,
}

DENSITY_CONVERSIONS = {
    "kg_m3_to_lb_ft3": 0.0624,
    "lb_ft3_to_kg_m3": 16.0185,
}

# ============================================================================
# CALCULATION LIMITS AND RANGES (for validation)
# ============================================================================

VALID_RANGES = {
    "pipe_diameter": (0, 18),  # inches
    "pipe_length": (0, 100),  # km
    "operating_pressure": (0, 100),  # bar
    "design_pressure": (0, 150),  # bar
    "temperature": (-40, 80),  # °C
    "elevation_change": (-2000, 2000),  # m
    "velocity_limit": (0, 6),  # m/s (typical max for liquids)
    "pressure_drop_limit": (0, 50),  # bar per 100 km (indicative)
}

# ============================================================================
# FORMULA REFERENCES
# ============================================================================

FORMULA_REFERENCES = {
    "darcy_weisbach": {
        "equation": "ΔP = f × (L/D) × (ρ × V²/2)",
        "source": "Fluid Mechanics (Darcy–Weisbach equation)",  # [web:41][web:42]
        "where": {
            "ΔP": "Pressure drop (Pa)",
            "f": "Darcy friction factor (dimensionless)",
            "L": "Pipe length (m)",
            "D": "Pipe diameter (m)",
            "ρ": "Fluid density (kg/m³)",
            "V": "Fluid velocity (m/s)",
        }
    },
    "reynolds_number": {
        "equation": "Re = (ρ × V × D) / μ",
        "source": "Fluid Mechanics",
        "where": {
            "Re": "Reynolds Number (dimensionless)",
            "V": "Velocity (m/s)",
            "D": "Diameter (m)",
            "μ": "Dynamic viscosity (Pa·s)",
        }
    },
    "colebrook_white": {
        "equation": "1/√f = -2 × log₁₀[(k/3.7D) + (2.51/(Re×√f))]",
        "source": "Colebrook-White correlation (turbulent flow friction factor)",  # [web:60]
        "where": {
            "f": "Friction factor",
            "k": "Absolute roughness (m)",
            "D": "Diameter (m)",
            "Re": "Reynolds number",
        }
    },
    "hoop_stress": {
        "equation": "σ = (P × D) / (2 × t)",
        "source": "ASME B31 design formulas",
        "where": {
            "σ": "Hoop stress (MPa)",
            "P": "Internal pressure (MPa)",
            "D": "Outside diameter (mm)",
            "t": "Wall thickness (mm)",
        }
    },
}

# ============================================================================
# EDUCATIONAL TIPS
# ============================================================================

TIPS = {
    "pressure_drop": "Pressure drop increases with: higher flow rate, longer distance, higher viscosity. It decreases with larger diameter.",
    "velocity": "Typical velocity limits: Oil 3-4 m/s, Gas 10-15 m/s. Higher velocity increases erosion and pressure drop.",
    "design_pressure": "Design pressure = Operating pressure × Safety factor (typically 1.5). Always greater than operating pressure.",
    "wall_thickness": "Thicker walls resist higher pressure but increase cost and weight. Find balance through calculations.",
    "elevation": "Uphill sections require more pressure to push fluid. Downhill helps, but valve control becomes critical.",
}

if __name__ == "__main__":
    # Example: Display available pipe grades
    print("Available Pipe Grades:")
    for grade, specs in PIPE_GRADES.items():
        print(f"  {grade}: SMYS = {specs['SMYS']} MPa")

   