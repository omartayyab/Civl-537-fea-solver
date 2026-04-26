# src/mesh.py
import numpy as np
import os


def generate_rect_mesh(L, h, nx, ny):
    """
    Generate a structured triangular mesh over a rectangular domain [0, L] x [-h/2, h/2].

    Each rectangular cell is split into 2 triangles. The split direction must be
    consistent across the mesh (e.g., always along the same diagonal).

    Parameters
    ----------
    L : float
        Length of the plate (x-direction).
    h : float
        Height of the plate (y-direction).
    nx : int
        Number of element divisions in x.
    ny : int
        Number of element divisions in y.

    Returns
    -------
    nodes : ndarray, shape (n_nodes, 2)
        Nodal coordinates.
    elements : ndarray, shape (n_elems, 3)
        Element connectivity (node indices per triangle).
    boundary_tags : dict
        Must contain at minimum:
        - 'fixed': list of node indices on the x=0 boundary (cantilever root)
        - 'loaded': list of node indices on the x=L boundary (cantilever tip)
    """
    #raise NotImplementedError


    dx = np.linspace(0,L,nx+1) # dx+1 or dy + 1 nodes
    dy = np.linspace(-h/2,h/2,ny+1) # centerline y = 0 such that truss is  [-h/2, h/2]
    X,Y = np.meshgrid(dx,dy)
    nodes = np.column_stack((X.flatten(), Y.flatten()))

    # Build connectivity matrix
    elements = []
    nodes_per_row = nx + 1

    for i in range (ny):
        for j in range (nx):
            n0= i*nodes_per_row + j
            n1 = n0 + 1
            n2 = n0 + nodes_per_row
            n3 = n2 + 1
            elements.append([n0, n1, n3])
            elements.append([n0, n3, n2])
            
    elements = np.array(elements)

    # Define boundary conditions.
    fixed_nodes = []
    loading_nodes = []

    for j in range (ny+1):

        fixed_nodes.append(j*nodes_per_row) #1st node of each row.
        loading_nodes.append(j*nodes_per_row + nx) #last node of each row.

    boundary_tags = {
        'fixed': fixed_nodes,
        'loaded': loading_nodes
    }

    return nodes, elements, boundary_tags



def generate_plate_with_hole_mesh(W, H, R, n_radial, n_angular):
    """
    Generate a triangular mesh for a rectangular plate [0, W] x [0, H]
    with a circular hole of radius R centered at the origin.

    Due to symmetry, only the quarter-plate (first quadrant) needs to be meshed.
    The hole boundary and plate edges must be tagged for boundary conditions.

    Parameters
    ----------
    W : float
        Half-width of the plate (x-direction extent from center).
    H : float
        Half-height of the plate (y-direction extent from center).
    R : float
        Radius of the circular hole.
    n_radial : int
        Number of element divisions in the radial direction (from hole to edge).
    n_angular : int
        Number of element divisions in the angular direction (quarter circle).

    Returns
    -------
    nodes : ndarray, shape (n_nodes, 2)
        Nodal coordinates.
    elements : ndarray, shape (n_elems, 3)
        Element connectivity.
    boundary_tags : dict
        Must contain:
        - 'hole': list of node indices on the hole boundary
        - 'right': list of node indices on the x=W boundary (applied tension)
        - 'sym_x': list of node indices on the y=0 boundary (symmetry: v=0)
        - 'sym_y': list of node indices on the x=0 boundary (symmetry: u=0)

    Notes
    -----
    Option A (manual): Create a structured mesh in (r, theta) space for
    r in [R, outer] and theta in [0, pi/2], then map to (x, y) using
    x = r cos(theta), y = r sin(theta). The outer boundary must conform to the
    rectangular plate edges.

    Option B (Gmsh): Use the gmsh Python API to define the geometry
    (rectangle minus circle), set mesh sizes, generate the mesh, and
    extract nodes, elements, and physical groups for boundary tagging.
    See https://gmsh.info/doc/textures/gmsh_api.html for the Python API docs.
    If you use Gmsh, add 'gmsh' to your requirements.txt.

    Option C (fallback): Use load_fallback_hole_mesh() below to load the
    pre-generated mesh from data/plate_with_hole_mesh.npz. This lets you
    proceed with the rest of the project while you work on your own mesher.
    """

    # 1. Setup Grid in (r, theta) space
    # Theta goes from 0 to 90 degrees (pi/2) for the first quadrant
    r_vals = np.linspace(R, W, n_radial)
    theta_vals = np.linspace(0, np.pi/2, n_angular)
    
    nodes = []
    for i in range(n_radial):
        # radial_factor goes from 0 (hole) to 1 (outer edge)
        radial_factor = i / (n_radial - 1)
        for j in range(n_angular):
            theta = (np.pi / 2) * (j / (n_angular - 1))
            
            # 1. Start with the hole radius
            r_inner = R
            
            # 2. Calculate the "target" distance to the rectangular edge
            # This is the "Magic Step" to make it square
            r_outer = min(W / np.cos(theta), H / np.sin(theta)) if 0 < theta < np.pi/2 else (W if theta == 0 else H)
            
            # 3. Interpolate between the hole and the square edge
            r = r_inner + radial_factor * (r_outer - r_inner)
            
            # 4. Map to Cartesian
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            nodes.append([x, y])
        
    nodes = np.array(nodes)

    # 2. Connectivity (Triangles)
    elements = []
    for i in range(n_radial - 1):
        for j in range(n_angular - 1):
            p1 = i * n_angular + j
            p2 = i * n_angular + (j + 1)
            p3 = (i + 1) * n_angular + (j + 1)
            p4 = (i + 1) * n_angular + j
            elements.append([p1, p4, p2])
            elements.append([p4, p3, p2])
    elements = np.array(elements)

# Define boundary nodes using your loop style
    sym_x_nodes = [] # The bottom edge (y=0)
    right_nodes = [] # The right edge (x=W)
    sym_y_nodes = [] # The left edge (x=0)
    hole_nodes  = [] # The inner circle (r=R)

    for i in range(n_radial):
        for j in range(n_angular):
            node_idx = i * n_angular + j
            
            # 1. The Hole is the very first radial ring (i = 0)
            if i == 0:
                hole_nodes.append(node_idx)
            
            # 2. sym_x is the first angular line (theta = 0)
            if j == 0:
                sym_x_nodes.append(node_idx)
            
            # 3. sym_y is the last angular line (theta = pi/2)
            if j == n_angular - 1:
                sym_y_nodes.append(node_idx)
            
            # 4. right is the last radial ring (i = n_radial - 1)
            if i == n_radial - 1:
                right_nodes.append(node_idx)

    boundary_tags = {
        'hole': hole_nodes,
        'right': right_nodes,
        'sym_x': sym_x_nodes,
        'sym_y': sym_y_nodes
    }
    return nodes, elements, boundary_tags

def load_fallback_hole_mesh(filepath=None):
    """
    Load the pre-generated plate-with-hole mesh from the .npz file.

    Parameters
    ----------
    filepath : str, optional
        Path to the .npz file. Defaults to data/plate_with_hole_mesh.npz
        relative to the project root.

    Returns
    -------
    nodes : ndarray, shape (n_nodes, 2)
    elements : ndarray, shape (n_elems, 3)
    boundary_tags : dict with keys 'hole', 'right', 'sym_x', 'sym_y'

    Notes
    -----
    This is a fallback so you can work on the solver and validation plots
    without being blocked by mesh generation. Your final submission should
    include your own mesh generator (Option A or B above).
    """
    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__), '..', 'data', 'plate_with_hole_mesh.npz')
    data = np.load(filepath)
    nodes = data['nodes']
    elements = data['elements']
    boundary_tags = {
        'hole': data['hole'].tolist(),
        'right': data['right'].tolist(),
        'sym_x': data['sym_x'].tolist(),
        'sym_y': data['sym_y'].tolist(),
    }
    return nodes, elements, boundary_tags


