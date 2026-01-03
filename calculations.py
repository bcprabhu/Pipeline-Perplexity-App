"""
Pipeline Design Tool - Core Calculation Engine
Educational Template for Young Pipeline Engineers

This module contains the fundamental pipeline design calculations:
- Pressure drop analysis
- Pipe sizing
- Flow velocity calculations
- Safety compliance checks
- Economic analysis basics

Reference: ASME B31.4 (Liquid), ASME B31.8 (Gas)
"""

import math
from constants import *

# ============================================================================
# SECTION 1: BASIC FLUID FLOW CALCULATIONS
# ============================================================================

class FlowCalculations:
    """
    Calculate fluid flow properties in pipelines.
    
    Educational Note: These are fundamental formulas every pipeline engineer
    must understand. Reynolds number determines flow regime (laminar/turbulent).
    """
    
    @staticmethod
    def calculate_reynolds_number(velocity, diameter, viscosity):
        """
        Calculate Reynolds Number to determine flow regime.
        
        Formula: Re = (ρ × V × D) / μ
        
        Args:
            velocity: Flow velocity (m/s)
            diameter: Pipe internal diameter (m)
            viscosity: Dynamic viscosity (Pa·s)
            
        Returns:
            float: Reynolds number (dimensionless)
            
        Note:
            Re < 2300: Laminar flow
            2300 < Re < 4000: Transition
            Re > 4000: Turbulent flow
        """
        if viscosity == 0:
            return float('inf')
        
        re = (velocity * diameter) / viscosity
        return re
    
    @staticmethod
    def calculate_flow_velocity(flow_rate_m3_s, internal_diameter_m):
        """
        Calculate flow velocity in the pipe.
        
        Formula: V = Q / A, where A = π × (D/2)²
        
        Args:
            flow_rate_m3_s: Volumetric flow rate (m³/s)
            internal_diameter_m: Internal diameter (m)
            
        Returns:
            float: Velocity (m/s)
        """
        if internal_diameter_m <= 0:
            return 0
        
        area = math.pi * (internal_diameter_m / 2) ** 2
        velocity = flow_rate_m3_s / area
        return velocity
    
    @staticmethod
    def flow_regime_classification(reynolds_number):
        """
        Classify flow regime based on Reynolds number.
        
        Returns:
            str: Flow regime description
        """
        if reynolds_number < 2300:
            return "Laminar (smooth, organized)"
        elif reynolds_number < 4000:
            return "Transitional (unstable)"
        else:
            return "Turbulent (chaotic, faster mixing)"


# ============================================================================
# SECTION 2: FRICTION FACTOR CALCULATIONS
# ============================================================================

class FrictionFactorCalculations:
    """
    Calculate friction factor for pressure drop computation.
    
    The friction factor depends on flow regime (Re) and pipe roughness.
    Key formulas: Hagen-Poiseuille (laminar), Colebrook-White (turbulent).
    """
    
    @staticmethod
    def calculate_friction_factor_laminar(reynolds_number):
        """
        Calculate friction factor for LAMINAR flow.
        
        Formula: f = 64 / Re
        
        Applies when: Re < 2300
        
        Args:
            reynolds_number: Reynolds number
            
        Returns:
            float: Darcy friction factor
        """
        if reynolds_number <= 0:
            return 0
        
        f = 64 / reynolds_number
        return f
    
    @staticmethod
    def calculate_friction_factor_turbulent_colebrook(reynolds_number, relative_roughness):
        """
        Calculate friction factor for TURBULENT flow using Colebrook-White equation.
        
        Formula: 1/√f = -2 × log₁₀[(ε/3.7D) + (2.51/(Re×√f))]
        
        Where:
            ε = absolute roughness (m)
            D = diameter (m)
            ε/D = relative roughness
            
        This requires iterative solution. We use approximation or iteration.
        
        Args:
            reynolds_number: Reynolds number (should be > 4000)
            relative_roughness: ε/D ratio (absolute roughness / diameter)
            
        Returns:
            float: Darcy friction factor
        """
        
        # For smooth pipes (relative_roughness ≈ 0), use Blasius equation
        if relative_roughness < 0.00001:
            return 0.316 * (reynolds_number ** -0.25)
        
        # Iterative solution of Colebrook-White
        # Initial guess using Swamee-Jain approximation
        f_guess = 0.25 / (math.log10(relative_roughness / 3.7 + 5.74 / (reynolds_number ** 0.9))) ** 2
        
        # Refine using Newton-Raphson (2-3 iterations usually sufficient)
        for _ in range(5):
            term1 = 2.0 * math.log10(relative_roughness / 3.7)
            term2_denom = reynolds_number * math.sqrt(f_guess)
            
            if term2_denom == 0:
                break
                
            term2 = 2.0 * math.log10(2.51 / term2_denom)
            
            f_new = 1.0 / ((term1 + term2) ** 2)
            
            # Check convergence
            if abs(f_new - f_guess) < 1e-6:
                break
            
            f_guess = f_new
        
        return f_guess
    
    @staticmethod
    def calculate_friction_factor(reynolds_number, absolute_roughness, diameter):
        """
        Select appropriate friction factor calculation method.
        
        Args:
            reynolds_number: Reynolds number
            absolute_roughness: Pipe roughness (m)
            diameter: Pipe diameter (m)
            
        Returns:
            tuple: (friction_factor, flow_regime)
        """
        
        if diameter <= 0:
            return 0, "Invalid diameter"
        
        if reynolds_number < 2300:
            # Laminar flow
            f = FrictionFactorCalculations.calculate_friction_factor_laminar(reynolds_number)
            regime = "Laminar"
        else:
            # Turbulent flow
            relative_roughness = absolute_roughness / diameter
            f = FrictionFactorCalculations.calculate_friction_factor_turbulent_colebrook(
                reynolds_number, relative_roughness
            )
            regime = "Turbulent"
        
        return f, regime


# ============================================================================
# SECTION 3: PRESSURE DROP CALCULATIONS
# ============================================================================

class PressureDropCalculations:
    """
    Calculate pressure drop along the pipeline.
    
    Main components:
    1. Friction losses (Darcy-Weisbach)
    2. Elevation changes (hydrostatic)
    3. Acceleration (typically negligible)
    """
    
    @staticmethod
    def calculate_friction_pressure_drop(friction_factor, length_m, diameter_m, 
                                         velocity_ms, density_kg_m3):
        """
        Calculate pressure drop due to friction.
        
        Formula (Darcy-Weisbach): ΔP = f × (L/D) × (ρ × V²/2)
        
        Args:
            friction_factor: Darcy friction factor (dimensionless)
            length_m: Pipe length (m)
            diameter_m: Internal diameter (m)
            velocity_ms: Flow velocity (m/s)
            density_kg_m3: Fluid density (kg/m³)
            
        Returns:
            float: Pressure drop (Pa)
        """
        
        if diameter_m <= 0 or density_kg_m3 <= 0:
            return 0
        
        # ΔP = f × (L/D) × (ρ × V²/2)
        pressure_drop = friction_factor * (length_m / diameter_m) * \
                       (density_kg_m3 * velocity_ms ** 2 / 2)
        
        return pressure_drop
    
    @staticmethod
    def calculate_elevation_pressure_drop(elevation_gain_m, density_kg_m3):
        """
        Calculate pressure required to overcome elevation change.
        
        Formula: ΔP_elev = ρ × g × Δh
        
        Positive when going uphill (pressure required)
        Negative when going downhill (pressure assistance)
        
        Args:
            elevation_gain_m: Elevation gain (m) [positive = uphill, negative = downhill]
            density_kg_m3: Fluid density (kg/m³)
            
        Returns:
            float: Pressure change (Pa)
        """
        
        pressure_change = density_kg_m3 * G_ACCELERATION * elevation_gain_m
        return pressure_change
    
    @staticmethod
    def calculate_total_pressure_drop(friction_dp_pa, elevation_dp_pa):
        """
        Calculate total pressure drop combining all effects.
        
        Total: ΔP_total = ΔP_friction + ΔP_elevation + ΔP_minor_losses
        
        Note: Minor losses (fittings, valves) typically 5-15% of friction losses.
        For this tool, we add 10% as typical estimate.
        
        Args:
            friction_dp_pa: Friction pressure drop (Pa)
            elevation_dp_pa: Elevation pressure drop (Pa)
            
        Returns:
            tuple: (total_dp_pa, minor_losses_estimate_pa)
        """
        
        # Estimate minor losses as 10% of friction losses
        minor_losses = abs(friction_dp_pa) * 0.10
        
        total_dp = friction_dp_pa + elevation_dp_pa + minor_losses
        
        return total_dp, minor_losses
    
    @staticmethod
    def convert_pressure_drop_to_bar_per_km(pressure_drop_pa, length_km):
        """
        Convert pressure drop to common engineering unit: bar/100km
        
        Args:
            pressure_drop_pa: Pressure drop (Pa)
            length_km: Distance (km)
            
        Returns:
            float: Pressure drop (bar per 100 km)
        """
        
        if length_km <= 0:
            return 0
        
        # Convert Pa to bar
        pressure_drop_bar = pressure_drop_pa / 100000
        
        # Normalize to 100 km
        pressure_per_100km = (pressure_drop_bar / length_km) * 100
        
        return pressure_per_100km


# ============================================================================
# SECTION 4: PIPE SIZING AND WALL THICKNESS
# ============================================================================

class PipeSizingCalculations:
    """
    Select appropriate pipe size and wall thickness.
    
    Design philosophy:
    1. Choose diameter to limit velocity to reasonable values
    2. Choose wall thickness based on pressure and material strength
    3. Apply safety factors per ASME B31 codes
    """
    
    @staticmethod
    def calculate_internal_diameter(outside_diameter_mm, wall_thickness_mm):
        """
        Calculate internal diameter from nominal size and wall thickness.
        
        ID = OD - 2 × t
        
        Args:
            outside_diameter_mm: Outside diameter (mm)
            wall_thickness_mm: Wall thickness (mm)
            
        Returns:
            float: Internal diameter (mm)
        """
        
        id_mm = outside_diameter_mm - 2 * wall_thickness_mm
        return id_mm
    
    @staticmethod
    def calculate_required_wall_thickness(internal_pressure_mpa, outside_diameter_mm, 
                                         smys_mpa, design_factor=0.72):
        """
        Calculate minimum wall thickness to resist internal pressure.
        
        Formula (ASME B31.4/B31.8): t = (P × D) / (2 × f × SMYS) + corrosion_allowance
        
        Where:
            P = Design pressure (MPa)
            D = Outside diameter (mm)
            f = Design factor (typically 0.72 for B31.4, location-dependent for B31.8)
            SMYS = Specified Minimum Yield Strength (MPa)
            
        Args:
            internal_pressure_mpa: Design pressure (MPa)
            outside_diameter_mm: Outside diameter (mm)
            smys_mpa: SMYS of pipe material (MPa)
            design_factor: Safety factor (default 0.72)
            
        Returns:
            float: Required wall thickness (mm)
        """
        
        if smys_mpa <= 0 or design_factor <= 0:
            return 0
        
        # Minimum thickness per formula (before corrosion allowance)
        t_min = (internal_pressure_mpa * outside_diameter_mm) / \
                (2 * design_factor * smys_mpa)
        
        return t_min
    
    @staticmethod
    def calculate_hoop_stress(internal_pressure_mpa, outside_diameter_mm, wall_thickness_mm):
        """
        Calculate hoop stress in pipe wall due to internal pressure.
        
        Formula: σ = (P × D) / (2 × t)
        
        This is the primary stress in pipelines. Must be < (design_factor × SMYS)
        
        Args:
            internal_pressure_mpa: Internal pressure (MPa)
            outside_diameter_mm: Outside diameter (mm)
            wall_thickness_mm: Wall thickness (mm)
            
        Returns:
            float: Hoop stress (MPa)
        """
        
        if wall_thickness_mm <= 0:
            return float('inf')
        
        hoop_stress = (internal_pressure_mpa * outside_diameter_mm) / (2 * wall_thickness_mm)
        
        return hoop_stress
    
    @staticmethod
    def check_pressure_containment(hoop_stress_mpa, smys_mpa, design_factor=0.72):
        """
        Check if pipe can safely contain the pressure.
        
        Safe if: hoop_stress ≤ (design_factor × SMYS)
        
        Args:
            hoop_stress_mpa: Calculated hoop stress (MPa)
            smys_mpa: Material SMYS (MPa)
            design_factor: Applied safety factor
            
        Returns:
            dict: {'safe': bool, 'margin': float, 'message': str}
        """
        
        allowable_stress = design_factor * smys_mpa
        margin = (allowable_stress - hoop_stress_mpa) / allowable_stress * 100 if allowable_stress > 0 else 0
        
        safe = hoop_stress_mpa <= allowable_stress
        
        return {
            'safe': safe,
            'margin_percent': max(0, margin),
            'hoop_stress': hoop_stress_mpa,
            'allowable_stress': allowable_stress,
            'message': f"{'✓ SAFE' if safe else '✗ UNSAFE'}: Hoop stress {hoop_stress_mpa:.2f} MPa vs allowable {allowable_stress:.2f} MPa"
        }


# ============================================================================
# SECTION 5: COMPREHENSIVE PIPELINE ANALYSIS
# ============================================================================

class PipelineAnalysis:
    """
    Integrated pipeline design analysis combining all calculations.
    
    This is the main entry point for comprehensive design evaluation.
    """
    
    @staticmethod
    def analyze_pipeline(flow_rate_m3_s, pipe_od_mm, wall_thickness_mm,
                        pipe_length_km, elevation_start_m, elevation_end_m,
                        operating_pressure_bar, fluid_density_kg_m3, 
                        fluid_viscosity_pa_s, pipe_roughness_m, 
                        pipe_grade="X52"):
        """
        Comprehensive pipeline analysis.
        
        Args:
            flow_rate_m3_s: Volumetric flow rate (m³/s)
            pipe_od_mm: Pipe outside diameter (mm)
            wall_thickness_mm: Wall thickness (mm)
            pipe_length_km: Pipe length (km)
            elevation_start_m: Start elevation (m)
            elevation_end_m: End elevation (m)
            operating_pressure_bar: Operating pressure (bar)
            fluid_density_kg_m3: Fluid density (kg/m³)
            fluid_viscosity_pa_s: Dynamic viscosity (Pa·s)
            pipe_roughness_m: Absolute roughness (m)
            pipe_grade: API grade (e.g., "X52")
            
        Returns:
            dict: Comprehensive analysis results
        """
        
        results = {}
        
        # Step 1: Basic parameters
        results['input'] = {
            'flow_rate_m3_s': flow_rate_m3_s,
            'pipe_od_mm': pipe_od_mm,
            'wall_thickness_mm': wall_thickness_mm,
            'pipe_length_km': pipe_length_km,
            'elevation_start': elevation_start_m,
            'elevation_end': elevation_end_m,
            'operating_pressure_bar': operating_pressure_bar,
            'pipe_grade': pipe_grade,
        }
        
        # Step 2: Pipe dimensions
        id_mm = PipeSizingCalculations.calculate_internal_diameter(pipe_od_mm, wall_thickness_mm)
        id_m = id_mm / 1000
        
        results['pipe_dimensions'] = {
            'outside_diameter_mm': pipe_od_mm,
            'wall_thickness_mm': wall_thickness_mm,
            'internal_diameter_mm': id_mm,
            'internal_diameter_m': id_m,
        }
        
        # Step 3: Flow velocity
        velocity_ms = FlowCalculations.calculate_flow_velocity(flow_rate_m3_s, id_m)
        re = FlowCalculations.calculate_reynolds_number(velocity_ms, id_m, fluid_viscosity_pa_s)
        flow_regime = FlowCalculations().flow_regime_classification(re)
        
        results['flow_properties'] = {
            'velocity_ms': velocity_ms,
            'reynolds_number': re,
            'flow_regime': flow_regime,
            'fluid_density': fluid_density_kg_m3,
            'fluid_viscosity': fluid_viscosity_pa_s,
        }
        
        # Step 4: Friction factor
        f, regime = FrictionFactorCalculations.calculate_friction_factor(
            re, pipe_roughness_m, id_m
        )
        
        results['friction'] = {
            'friction_factor': f,
            'calculation_method': regime,
            'pipe_roughness_m': pipe_roughness_m,
        }
        
        # Step 5: Pressure drop
        length_m = pipe_length_km * 1000
        
        dp_friction = PressureDropCalculations.calculate_friction_pressure_drop(
            f, length_m, id_m, velocity_ms, fluid_density_kg_m3
        )
        
        elevation_change = elevation_end_m - elevation_start_m
        dp_elevation = PressureDropCalculations.calculate_elevation_pressure_drop(
            elevation_change, fluid_density_kg_m3
        )
        
        dp_total, dp_minor = PressureDropCalculations.calculate_total_pressure_drop(
            dp_friction, dp_elevation
        )
        
        dp_bar_per_100km = PressureDropCalculations.convert_pressure_drop_to_bar_per_km(
            dp_friction, pipe_length_km
        )
        
        results['pressure_drop'] = {
            'friction_loss_pa': dp_friction,
            'friction_loss_bar': dp_friction / 100000,
            'elevation_change_pa': dp_elevation,
            'elevation_change_bar': dp_elevation / 100000,
            'minor_losses_pa': dp_minor,
            'minor_losses_bar': dp_minor / 100000,
            'total_pressure_drop_pa': dp_total,
            'total_pressure_drop_bar': dp_total / 100000,
            'bar_per_100km': dp_bar_per_100km,
        }
        
        # Step 6: Final pressure at outlet
        inlet_pressure_pa = operating_pressure_bar * 100000
        outlet_pressure_pa = inlet_pressure_pa - dp_total
        outlet_pressure_bar = outlet_pressure_pa / 100000
        
        results['outlet_pressure'] = {
            'inlet_pressure_bar': operating_pressure_bar,
            'outlet_pressure_bar': max(0, outlet_pressure_bar),
            'pressure_loss_percent': (dp_total / inlet_pressure_pa * 100) if inlet_pressure_pa > 0 else 0,
        }
        
        # Step 7: Pressure containment check
        design_pressure_bar = operating_pressure_bar * 1.5  # Typical design margin
        design_pressure_mpa = design_pressure_bar / 10
        
        smys_mpa = PIPE_GRADES[pipe_grade]['SMYS']
        hoop_stress = PipeSizingCalculations.calculate_hoop_stress(
            design_pressure_mpa, pipe_od_mm, wall_thickness_mm
        )
        
        pressure_check = PipeSizingCalculations.check_pressure_containment(
            hoop_stress, smys_mpa, design_factor=0.72
        )
        
        results['pressure_containment'] = {
            'design_pressure_bar': design_pressure_bar,
            'design_pressure_mpa': design_pressure_mpa,
            'hoop_stress_mpa': hoop_stress,
            'allowable_stress_mpa': 0.72 * smys_mpa,
            'safe': pressure_check['safe'],
            'safety_margin_percent': pressure_check['margin_percent'],
            'compliance_message': pressure_check['message'],
        }
        
        # Step 8: Velocity checks (safety limits)
        velocity_check = {
            'velocity_ms': velocity_ms,
            'velocity_limit_typical_ms': 4.0,  # Typical limit for liquids
            'within_limit': velocity_ms <= 4.0,
        }
        
        if velocity_ms > 4.0:
            velocity_check['warning'] = f"⚠ High velocity ({velocity_ms:.2f} m/s). Consider larger diameter."
        
        results['velocity_check'] = velocity_check
        
        return results


# ============================================================================
# TEST EXAMPLES
# ============================================================================

if __name__ == "__main__":
    # Example: Analyze a 12" crude oil pipeline
    print("=" * 70)
    print("PIPELINE ANALYSIS EXAMPLE - Educational Tool")
    print("=" * 70)
    
    results = PipelineAnalysis.analyze_pipeline(
        flow_rate_m3_s=0.05,  # 50 liters/second
        pipe_od_mm=323.9,  # 12.75" (12" nominal)
        wall_thickness_mm=6.4,  # 1/4"
        pipe_length_km=30.0,
        elevation_start_m=0,
        elevation_end_m=100,  # 100m uphill
        operating_pressure_bar=20,
        fluid_density_kg_m3=900,  # Crude oil
        fluid_viscosity_pa_s=0.001,  # 1 cP
        pipe_roughness_m=0.045e-3,  # 0.045 mm (new steel)
        pipe_grade="X52"
    )
    
    # Display results
    print("\n[INPUT PARAMETERS]")
    for key, val in results['input'].items():
        print(f"  {key}: {val}")
    
    print("\n[PIPE DIMENSIONS]")
    for key, val in results['pipe_dimensions'].items():
        print(f"  {key}: {val:.2f}" if isinstance(val, float) else f"  {key}: {val}")
    
    print("\n[FLOW PROPERTIES]")
    print(f"  Velocity: {results['flow_properties']['velocity_ms']:.3f} m/s")
    print(f"  Reynolds Number: {results['flow_properties']['reynolds_number']:.1f}")
    print(f"  Flow Regime: {results['flow_properties']['flow_regime']}")
    
    print("\n[PRESSURE DROP ANALYSIS]")
    pd = results['pressure_drop']
    print(f"  Friction Loss: {pd['friction_loss_bar']:.3f} bar ({pd['bar_per_100km']:.2f} bar/100km)")
    print(f"  Elevation Loss: {pd['elevation_change_bar']:.3f} bar (uphill)")
    print(f"  Minor Losses: {pd['minor_losses_bar']:.3f} bar")
    print(f"  TOTAL: {pd['total_pressure_drop_bar']:.3f} bar")
    
    print("\n[OUTLET PRESSURE]")
    print(f"  Inlet: {results['outlet_pressure']['inlet_pressure_bar']:.2f} bar")
    print(f"  Outlet: {results['outlet_pressure']['outlet_pressure_bar']:.2f} bar")
    print(f"  Loss %: {results['outlet_pressure']['pressure_loss_percent']:.1f}%")
    
    print("\n[PRESSURE CONTAINMENT - ASME B31.4]")
    pc = results['pressure_containment']
    print(f"  {pc['compliance_message']}")
    print(f"  Safety Margin: {pc['safety_margin_percent']:.1f}%")
    
    print("\n[VELOCITY CHECK]")
    vc = results['velocity_check']
    print(f"  {vc['velocity_ms']:.3f} m/s (limit: {vc['velocity_limit_typical_ms']} m/s) - {'✓ OK' if vc['within_limit'] else '✗ EXCESSIVE'}")
    
    print("\n" + "=" * 70)
