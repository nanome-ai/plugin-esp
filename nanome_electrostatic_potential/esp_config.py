import os

apbs_config = {
    "path": os.getenv("APBS", "apbs"),
    "template": """
read
    mol pqr "{}"
end
elec
    mg-auto
    mol 1

    fgcent mol 1    # fine grid center
    cgcent mol 1    # coarse grid center
    fglen {:f} {:f} {:f}
    cglen {:f} {:f} {:f}
    dime {:d} {:d} {:d}
    lpbe          # l=linear, n=non-linear Poisson-Boltzmann equation
    bcfl sdh      # "Single Debye-Hueckel" boundary condition
    pdie 2.0      # protein dielectric
    sdie 78.0     # solvent dielectric
    chgm spl2     # Cubic B-spline discretization of point charges on grid
    srfm smol     # smoothed surface for dielectric and ion-accessibility coefficients
    swin 0.3
    temp 310.0    # temperature
    sdens 10.0
    calcenergy no
    calcforce no
    srad 1.40000   # solvent radius

    ion charge +1 conc 0.15 radius 2.0
    ion charge -1 conc 0.15 radius 1.8

    write pot dx "{}"
end
quit
    """
}

pdb2pqr_config = {
    "path": os.getenv("PDB2PQR", "pdb2pqr"),
    "args": ["--ff=AMBER", "--chain", "--drop-water"]
}
