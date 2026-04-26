# src/postprocess.py
import numpy as np
from src.elements import compute_B


def compute_stresses(nodes, elements, u, D):
    """
    Recover element stresses from the displacement solution.

    Parameters
    ----------
    nodes : ndarray, shape (n_nodes, 2)
    elements : ndarray, shape (n_elems, 3)
    u : ndarray, shape (n_dof,)
    D : ndarray, shape (3, 3)

    Returns
    -------
    stresses : ndarray, shape (n_elems, 3)
        Stress components [sigma_xx, sigma_yy, tau_xy] at each element centroid.
    """
    n_elems = len(elements)
    stresses = np.zeros((n_elems, 3))
    
    for i, el in enumerate(elements):
        coords = nodes[el]
        B = compute_B(coords)
        
        # 3. Extract the local displacements for these specific nodes
        # Interleaved [u0, v0, u1, v1, u2, v2]
        dofs = [
            2*el[0], 2*el[0]+1, 
            2*el[1], 2*el[1]+1, 
            2*el[2], 2*el[2]+1
        ]
        u_e = u[dofs]
        
        # 4. Calculate Stress: sigma = D * B * u_e
        stresses[i, :] = D @ B @ u_e
        
    return stresses


def compute_von_mises(stresses):
    """Von Mises stress from [sigma_xx, sigma_yy, tau_xy] per element."""
   # Extract the individual columns for readability
    sx = stresses[:, 0]
    sy = stresses[:, 1]
    txy = stresses[:, 2]
    
    # 2D Plane Stress Von Mises formula
    # sigma_v = sqrt(sx^2 - sx*sy + sy^2 + 3*txy^2)
    von_mises = np.sqrt(sx**2 - sx*sy + sy**2 + 3 * txy**2)
    
    return von_mises

def strain_energy(K, u):
    """Return 0.5 * u^T K u."""
    return 0.5 * np.dot(u, K.dot(u))


def compute_nodal_stresses(nodes, elements, element_stresses):
    """
    Smooths element stresses into nodal stresses by averaging.
    """
    n_nodes = len(nodes)
    nodal_stresses = np.zeros((n_nodes, 3))
    node_counts = np.zeros(n_nodes)
    
    # 1. Dump every triangle's stress into the buckets of its 3 corners
    for i, el in enumerate(elements):
        for node_idx in el:
            nodal_stresses[node_idx] += element_stresses[i]
            node_counts[node_idx] += 1
            
    # 2. Divide the buckets by the number of triangles that dumped into them
    for i in range(n_nodes):
        if node_counts[i] > 0:  # Prevent division by zero just in case
            nodal_stresses[i] /= node_counts[i]
            
    return nodal_stresses