# src/elements.py
import numpy as np


def compute_area(coords):
    """
    Compute the signed area of a triangle.

    Parameters
    ----------
    coords : ndarray, shape (3, 2)
        Node coordinates [[x0,y0], [x1,y1], [x2,y2]].

    Returns
    -------
    float
        Signed area of the triangle (positive if nodes are counter-clockwise).
    """
    #raise NotImplementedError
    x0, y0 = coords[0];
    x1, y1 = coords[1];
    x2, y2 = coords[2];

    area = 0.5 * (x0*(y1 - y2) + x1*(y2 -y0) + x2*(y0 -y1))
    return area


def compute_B(coords):
    """
    Compute the strain-displacement matrix B for a CST element.

    The CST element has constant strain throughout, so B is constant.
    B maps the 6x1 element displacement vector [u0,v0,u1,v1,u2,v2]
    to the 3x1 strain vector [eps_xx, eps_yy, gamma_xy].

    Parameters
    ----------
    coords : ndarray, shape (3, 2)
        Node coordinates.

    Returns
    -------
    ndarray, shape (3, 6)
        Strain-displacement matrix.

    Notes
    -----
    Derive B from the linear shape functions N_i(x,y) = (a_i + b_i*x + c_i*y) / (2A).
    The coefficients b_i and c_i come from cyclic permutations of the node coordinates.
    Refer to CIVL 537 Lecture Notes, Section 4.
    """
    #raise NotImplementedError
    x = coords[:, 0]
    y = coords[:, 1]
    bi= y[1] - y[2]
    bj= y[2] - y[0]
    bk= y[0] - y[1]

    ci= x[2] - x[1]
    cj= x[0] - x[2]
    ck= x[1] - x[0]

    #assemble B now. 

    B=np.array([[bi, 0, bj, 0, bk, 0], [0, ci, 0, cj, 0, ck], [ci, bi, cj, bj, ck, bk]]);
    return B/abs(2*compute_area(coords))

def compute_D(E, nu, mode="plane_stress"):
    """
    Compute the 3x3 constitutive (material stiffness) matrix D.

    Parameters
    ----------
    E : float
        Young's modulus.
    nu : float
        Poisson's ratio.
    mode : str
        Either "plane_stress" or "plane_strain".

    Returns
    -------
    ndarray, shape (3, 3)
        Constitutive matrix relating stress to strain.

    Notes
    -----
    Plane stress: sigma_zz = 0, eliminate eps_zz from 3D Hooke's law.
    Plane strain: eps_zz = 0, eliminate sigma_zz from 3D Hooke's law.
    The resulting D matrices are different. Implement them based on the course notes.
    """
    #raise NotImplementedError
    if mode == "plane_stress":
        factor = E / (1 - nu**2)
        D = factor * np.array([
            [1,  nu, 0],
            [nu, 1,  0],
            [0,  0,  (1 - nu) / 2]
        ])
    elif mode == "plane_strain":
        factor = E / ((1 + nu) * (1 - 2 * nu))
        D = factor * np.array([
            [1 - nu, nu,     0],
            [nu,     1 - nu, 0],
            [0,      0,      (1 - 2 * nu) / 2]
        ])
    return D


def compute_k(coords, D, thickness):
    """
    Compute the 6x6 element stiffness matrix for a CST element.

    Parameters
    ----------
    coords : ndarray, shape (3, 2)
        Node coordinates.
    D : ndarray, shape (3, 3)
        Constitutive matrix.
    thickness : float
        Element thickness (relevant for plane stress; set to 1 for plane strain).

    Returns
    -------
    ndarray, shape (6, 6)
        Element stiffness matrix: k = t * A * B^T D B.

    Notes
    -----
    Since B is constant over the element, the integral simplifies to
    a single multiplication (no numerical quadrature needed).
    """

    A = abs(compute_area(coords))
    B = compute_B(coords)
    k = thickness * A * (B.T @ D @ B)
    return k

