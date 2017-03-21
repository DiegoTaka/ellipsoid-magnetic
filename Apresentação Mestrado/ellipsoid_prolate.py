"""
The potential fields of a triaxial ellipsoid.
"""

from __future__ import division
import numpy as np
from scipy import linalg

from .. import utils

import scipy.special

def bx_c(xp,yp,zp,inten,inc,dec,ellipsoids):
    '''
    Calculates the X component of the magnetic field generated by n-ellipsoid.
    
    Parameters:
    
    * xp,yp,zp: arrays
        Grid of observation points x, y, and z.
    * inten,inc,dec: floats
        Intensity, inclination and declination of the Earth's magnetic field.
    * ellipsoids: list of :class:`fatiando.mesher.Sphere` 
        Ellipsoid model.
    
    Returns:
    
    * bx: array
        The X component of the magnetic field generated by n-ellipsoid.
    '''
    
    if xp.shape != yp.shape != zp.shape:
        raise ValueError("Input arrays xp, yp, and zp must have same shape!")
    size = len(xp)
    res = np.zeros(size, dtype=np.float)
    ctemag = 100.
    
    for ellipsoid in ellipsoids:
        b1,b2,b3,V,N1,N2 = ellipsoid_def (xp,yp,zp,inten,inc,dec,ellipsoid)
        bx = b1*V[0,0]+b2*V[0,1]+b3*V[0,2]
        res += bx 
    res = res*ctemag
    return res
    
def by_c(xp,yp,zp,inten,inc,dec,ellipsoids):
    '''
    Calculates the Y component of the magnetic field generated by n-ellipsoid.
    
    Parameters:
    
    * xp,yp,zp: arrays
        Grid of observation points x, y, and z.
    * inten,inc,dec: floats
        Intensity, inclination and declination of the Earth's magnetic field.
    * ellipsoids: list of :class:`fatiando.mesher.Sphere` 
        Ellipsoid model.
    
    Returns:
    
    * by: array
        The Y component of the magnetic field generated by n-ellipsoid.
    '''
    
    if xp.shape != yp.shape != zp.shape:
        raise ValueError("Input arrays xp, yp, and zp must have same shape!")
    size = len(xp)
    res = np.zeros(size, dtype=np.float)
    ctemag = 100.
    
    for ellipsoid in ellipsoids:
        b1,b2,b3,V,N1,N2 = ellipsoid_def (xp,yp,zp,inten,inc,dec,ellipsoid)
        by = b1*V[1,0]+b2*V[1,1]+b3*V[1,2]
        res += by
    res = res*ctemag
    return res

def bz_c(xp,yp,zp,inten,inc,dec,ellipsoids):
    '''
    Calculates the Z component of the magnetic field generated by n-ellipsoid.
    
    Parameters:
    
    * xp,yp,zp: arrays
        Grid of observation points x, y, and z.
    * inten,inc,dec: floats
        Intensity, inclination and declination of the Earth's magnetic field.
    * ellipsoids: list of :class:`fatiando.mesher.Sphere` 
        Ellipsoid model.
    
    Returns:
    
    * bz: array
        The Z component of the magnetic field generated by n-ellipsoid.
    '''
    
    if xp.shape != yp.shape != zp.shape:
        raise ValueError("Input arrays xp, yp, and zp must have same shape!")
    size = len(xp)
    res = np.zeros(size, dtype=np.float)
    ctemag = 100.
    
    for ellipsoid in ellipsoids:
        b1,b2,b3,V,N1,N2 = ellipsoid_def (xp,yp,zp,inten,inc,dec,ellipsoid)
        bz = b1*V[2,0]+b2*V[2,1]+b3*V[2,2]
        res += bz
    res = res*ctemag
    return res
    
def tf_c(xp,yp,zp,inten,inc,dec,ellipsoids):
    '''
    Calculates the approximated total-field anomaly generated by n-ellipsoid.
    
    Parameters:
    
    * xp,yp,zp: arrays
        Grid of observation points x, y, and z.
    * inten,inc,dec: floats
        Intensity, inclination and declination of the Earth's magnetic field.
    * ellipsoids: list of :class:`fatiando.mesher.Sphere` 
        Ellipsoid model.
    
    Returnss:

    * tf : array
        The total-field anomaly
    '''
    
    if xp.shape != yp.shape != zp.shape:
        raise ValueError("Input arrays xp, yp, and zp must have same shape!")
    size = len(xp)
    res = np.zeros(size, dtype=np.float)
    ctemag = 100.
    
    for ellipsoid in ellipsoids:
        b1,b2,b3,V,N1,N2 = ellipsoid_def (xp,yp,zp,inten,inc,dec,ellipsoid)
        bx = (b1*V[0,0]+b2*V[0,1]+b3*V[0,2])*ctemag
        by = (b1*V[1,0]+b2*V[1,1]+b3*V[1,2])*ctemag
        bz = (b1*V[2,0]+b2*V[2,1]+b3*V[2,2])*ctemag
        tf = bx*np.cos(np.deg2rad(inc))*np.cos(np.deg2rad(dec)) + by*np.cos\
        (np.deg2rad(inc))*np.sin(np.deg2rad(dec)) + bz*np.sin(np.deg2rad(inc))
        res += tf
    res = res
    return res,N1,N2
    
def ellipsoid_def (xp,yp,zp,inten,inc,dec,ellipsoid):
    '''
    Calculate the potential fields of a homogeneous ellipsoid.

    **Magnetic**

    Calculates the magnetic effect produced by a triaxial, a prolate or/and 
    an oblate ellipsoid. The functions are
    based on Clark et al. (1986).
    '''

    axis = ellipsoid.axis
    center = ellipsoid.center
    alpha, delta, gamma = structural_angles(ellipsoid.strike, ellipsoid.dip, ellipsoid.rake)
    V = ellipsoid.V(angles = [alpha, delta, gamma])
    
    # Remanence values
    intensity_rem = ellipsoid.props['remanence'][0]
    incli_rem = ellipsoid.props['remanence'][1]
    decli_rem = ellipsoid.props['remanence'][2]
    ln, mn, nn = utils.dircos(incli_rem, decli_rem)
    
    k_int = np.array([ellipsoid.props['k'][0],ellipsoid.props['k'][1],\
    ellipsoid.props['k'][2]])
    #isotropic case
    if k_int[0] == (k_int[1] and k_int[2]):
        km = np.diag(k_int)
    #anisotropic case
    else:
        U = ellipsoid.V(angles = [ellipsoid.props['k'][3],\
        ellipsoid.props['k'][4],ellipsoid.props['k'][5]])
        km = k_matrix(U,V,np.diag(k_int))
        
    # Ellipsoid cartesian body coordinates
    x1,x2,x3 = x_e(xp,yp,zp,center,V)
    
    # Auxiliar calculations
    r = r_e (x1,x2,x3)
    delta = delta_e (r,axis,x1,x2,x3)

    # Largest real root of the cubic equation (Lambda)
    lamb = lamb_e (r,axis,delta)

    # Derivatives of lambda
    dlambx1,dlambx2,dlambx3 = dlambx_e (axis,x1,x2,x3,lamb,r,delta)
    
    # Calculate the eliptical integral parameters
    N1,N2 = N_desmag (axis)
    
    # Earth's field and total body magnetization (including demagnetization) 
    #in the body's coordinate
    JN = JN_e (intensity_rem,ln,mn,nn,V)
    lt,mt,nt = utils.dircos(inc, dec)
    Ft = F_e (inten,lt,mt,nt,V)
    JR = JR_e (km,JN,Ft)
    JRD = JRD_e (km,N1,N2,JR)
    JRD_carte = (V.T).dot(JRD)
    JRD_ang = utils.vec2ang(JRD_carte)
    
    # Auxiliar calculations of the magnetic field
    log = log_m (axis,lamb)
    A,B,C = matrix_d (axis,lamb,log)
    m11,m12,m13,m21,m22,m23,m31,m32,m33 = mx(axis,x1,x2,x3,dlambx1,dlambx2,\
    dlambx3,A,B,C,lamb)
    
    # Components of the magnetic field in the body coordinates
    B1 = B1_e (m11,m12,m13,JRD,axis)
    B2 = B2_e (m21,m22,m23,JRD,axis)
    B3 = B3_e (m31,m32,m33,JRD,axis)
    
    return B1,B2,B3,V,N1,N2

def structural_angles(strike, dip, rake):
    '''
    Calculates the orientation angles alpha, gamma
    and delta (Clark et al., 1986)
    as functions of the geological angles strike, dip and
    rake (Clark et al., 1986; Allmendinger et al., 2012).
    The function implements the formulas presented by
    Clark et al. (1986).

    Parameters:

    *strike: float
             strike direction (in degrees).
    *dip: float
          true dip (in degrees).
    *rake: float
           angle between the strike and the semi-axis a
           of the body (in degrees).

    Returns:

    *alpha, gamma, delta: float, float, float
            orientation angles (in radians) defined according
            to Clark et al. (1986).

    References:

    Clark, D., Saul, S., and Emerson, D.: Magnetic and gravity anomalies
    of a triaxial ellipsoid, Exploration Geophysics, 17, 189-200, 1986.

    Allmendinger, R., Cardozo, N., and Fisher, D. M.:
    Structural geology algorithms : vectors and tensors,
    Cambridge University Press, 2012.
    '''

    strike_r = np.deg2rad(strike)
    cos_dip = np.cos(np.deg2rad(dip))
    sin_dip = np.sin(np.deg2rad(dip))
    cos_rake = np.cos(np.deg2rad(rake))
    sin_rake = np.sin(np.deg2rad(rake))

    aux = sin_dip*sin_rake
    aux1 = cos_rake/np.sqrt(1 - aux*aux)
    aux2 = sin_dip*cos_rake

    if aux1 > 1.:
        aux1 = 1.
    if aux1 < -1.:
        aux1 = -1.

    alpha = strike_r - np.arccos(aux1)
    if aux2 != 0:
        gamma = -np.arctan(cos_dip/aux2)
    else:
        if cos_dip >= 0:
            gamma = np.pi/2
        if cos_dip <= 0:
            gamma = -np.pi/2
    delta = np.arcsin(aux)

    assert delta <= np.pi/2, 'delta must be lower than \
or equalt to 90 degrees'

    assert (gamma >= -np.pi/2) and (gamma <= np.pi/2), 'gamma must lie between \
-90 and 90 degrees.'

    return alpha, gamma, delta
	
def x_e (xp,yp,zp,center,V):
        '''
        Calculates the new coordinates with origin at the center 
        of the ellipsoid.

        Parameters:
        
        * xp,yp,zp: arrays
            Grid of observation points x, y, and z.
        * center: float
            Origin of the center of the ellipsoid.
        * V: array
            Matrix of conversion.
        
        Returns:
        
        * x1, x2, x3: arrays
            The three grid points of the body's coordinates.
        '''
        x1 = (xp-center[0])*V[0,0]+(yp-center[1])*V[1,0]-(zp+center[2])*V[2,0]
        x2 = (xp-center[0])*V[0,1]+(yp-center[1])*V[1,1]-(zp+center[2])*V[2,1]
        x3 = (xp-center[0])*V[0,2]+(yp-center[1])*V[1,2]-(zp+center[2])*V[2,2]
        return x1, x2, x3
        
def JN_e (intensity_rem,ln,mn,nn,V):
        '''
        Changes the remanent magnetization vector to the body coordinate.
        
        Parameters:
        
        * ln,nn,mn:
            Direction cosines of the remanent magnetization vector.
        * V:
            Matrix of conversion.
        
        Returns:
        
        * JN:
            Remanent magnetization vector in the body coordinate.         
        '''
        
        JN = intensity_rem*np.array([[(ln*V[0,0]+mn*V[1,0]+nn*V[2,0])], \
        [(ln*V[0,1]+mn*V[1,1]+nn*V[2,1])], [(ln*V[0,2]+mn*V[1,2]+nn*V[2,2])]])
        return JN

def N_desmag (axis):
        '''
        Calculates the three demagnetization factor along major, 
        intermediate and minor axis.
        
        Parameters:
        
        * a,b,c: float
            Major, intermediate and minor axis, respectively.
        * F2, E2: float
            Lagrange's normal eliptic integrals of first and second order.
        
        Returns:
        
        * N1, N2, N3: floats
            Major, intermediate and minor demagnetization factors, respectively.      
        '''
        
        N1 = ((4*np.pi*axis[0]*axis[1]**2)/((axis[0]**2-axis[1]**2)**1.5)) * \
        (np.log(((axis[0]**2/axis[1]**2)-1.)**0.5 + (axis[0]/axis[1])) - \
        (1. - (axis[1]**2/axis[0]**2))**0.5)
        
        N2 = (2.*np.pi - N1/2.)
        return N1/(4*np.pi), N2/(4*np.pi)

def k_matrix (U,V,K):
        '''
        Build the susceptibility tensor for the anisotropic case.
        
        Parameters:
        
        * U: array
            Direction cosines of the susceptibilities.
        * V: array
            Matrix of coordinates conversion.
        * K: array
            Diagonal matrix with k1,k2,k3 (intensity of the susceptibilities).
        
        Returns:
        
        * km: array
            Susceptibility tensors matrix.
        '''
        
        km = np.dot(np.dot(np.dot(V.T,U), K), np.dot(U.T,V))
        return km

def r_e (x1,x2,x3):
    '''
    Calculates the distance between the observation point and the center 
    of the ellipsoid.
      
    Parameters:
    x1, x2, x3 - Axis of the body coordinate system.
      
    Returns:
    r - Distance between the observation point and the center of the ellipsoid.        
    '''
    
    r = ((x1)**2+(x2)**2+(x3)**2)**0.5
    return r
    
def delta_e (r,axis,x1,x2,x3):
    '''
    Calculates an auxiliar constant for lambda.
        
    Parameters:
    a, b - Major, intermediate and minor axis, respectively.
    r - Distance between the observation point and the center of the ellipsoid.
    x1, x2, x3 - Axis of the body coordinate system.
       
    Returns:
    delta - Auxiliar constant for lambda.        
    '''

    delta = (r**4 + (axis[0]**2-axis[1]**2)**2 - 2*(axis[0]**2-axis[1]**2) * \
    (x1**2 - x2**2 - x3**2))**0.5
    return delta    
    
def lamb_e (r,axis,delta):
    '''
    Calculates the Larger root of the cartesian ellipsoidal equation.
    Used in the prolate ellipsoids.
      
    Parameters:
    a, b - Major, intermediate and minor axis, respectively.
    delta - Auxiliar constant for lambda.
    r - Distance between the observation point and the center of the ellipsoid.
     
    Returns:
    lamb - Larger root of the cartesian ellipsoidal equation.
    '''
    lamb = (r**2 - axis[0]**2 - axis[1]**2 + delta)/2.
    return lamb

def dlambx_e (axis,x1,x2,x3,lamb,r,delta):
    '''
    Calculates the derivatives of the ellipsoid equation for each body 
    coordinates in realation to lambda.
    
    Parameters:
    a, b, c - Major, intermediate and minor axis, respectively.
    x1, x2, x3 - Axis of the body coordinate system.
    delta - Auxiliar constant for lambda.
    lamb - Larger root of the cartesian ellipsoidal equation.
    r - Distance between the observation point and the center of the ellipsoid.
    
    Returns:
    dlambx1,dlambx2,dlambx3 - Derivatives of the ellipsoid equation for each 
    body coordinates in realation to x1,x2 and x3.        
    '''
        
    dlambx1 = x1*(1+(r**2-axis[0]**2+axis[1]**2)/delta)
    dlambx2 = x2*(1+(r**2+axis[0]**2-axis[1]**2)/delta)
    dlambx3 = x3*(1+(r**2+axis[0]**2-axis[1]**2)/delta)
    return dlambx1, dlambx2, dlambx3
        
def jrd_cartesiano (inten,inc,dec,ellipsoids):
    '''
    Calculates the intensity and direction of the resultant 
    vector of magnetization.
    
    Parameters:
    
    * inten:
        Intensity of the Earth's magnetic field.
    * inc:
        Inclination of the Earth's magnetic field.
    * dec:
        Declination of the Earth's magnetic field.
    * ellipsoid:
        magnetic ellipsoid model.
    
    Returns:
    
    * JRD_ang:
        Vector with intensity and direction of the resultant 
        vector of magnetization 
        in the cartesian coordinates(degrees).    
    '''
    
    inc = np.deg2rad(inc)
    dec = np.deg2rad(dec)
    lt,mt,nt = utils.dircos (dec, inc)
    Ft = []
    JR = []
    JRD = []
    JRD_carte = []
    JRD_ang = []
    for ellipsoid in ellipsoids:
    
        Ft.append(F_e (inten,lt,mt,nt,ellipsoids[i].mcon[0,0],\
        ellipsoids[i].mcon[1,0],ellipsoids[i].mcon[2,0],\
        ellipsoids[i].mcon[0,1],ellipsoids[i].mcon[1,1],\
        ellipsoids[i].mcon[2,1],ellipsoids[i].mcon[0,2],\
        ellipsoids[i].mcon[1,2],ellipsoids[i].mcon[2,2]))
        
        JR.append(JR_e (ellipsoids[i].km,ellipsoids[i].JN,Ft[i]))
        
        JRD.append(JRD_e (ellipsoids[i].km,ellipsoids[i].N1,\
        ellipsoids[i].N2,ellipsoids[i].N3,JR[i]))
        
        JRD_carte.append((ellipsoids[i].mconT).dot(JRD[i]))
        
        JRD_ang.append(utils.vec2ang(JRD_carte[i]))
    return JRD_ang
    
def F_e (inten,lt,mt,nt,V):
    '''
    Change the magnetization vetor of the Earth's field 
    to the body coordinates.
    
    Parameters:
    
    * inten: float
        Intensity of the Earth's magnetic field.
    * lt,mt,nt: floats
        Direction cosines of the Earth's magnetic field.
    * V: array
        Matrix of body coordinates change.
    
    Returns:
    
    * Ft: array
    The magnetization vetor of the Earth's field to the body coordinates.    
    '''
	
    intT= inten/(4*np.pi*100)   
    Ft = intT*np.array([[(lt*V[0,0]+mt*V[1,0]+nt*V[2,0])], \
    [(lt*V[0,1]+mt*V[1,1]+nt*V[2,1])], [(lt*V[0,2]+mt*V[1,2]+nt*V[2,2])]])
    return Ft
    
def JR_e (km,JN,Ft):
    '''
    Calculates the resultant magnetization vector without 
    self-demagnetization correction.
    
    Parameters:
    
    * km: array
        matrix of susceptibilities tensor.
    * JN: array
        Remanent magnetization
    * Ft: array
        Magnetization vetor of the Earth's field in the body coordinates.
    
    Returns:
    
    * JR: array
        Resultant magnetization vector without 
        self-demagnetization correction.  
    '''
    
    JR = km.dot(Ft) + JN
    return JR
    
def JRD_e (km,N1,N2,JR):
    '''
    Calculates resultant magnetization vector with 
    self-demagnetization correction.
    
    Parameters:
    
    * km: array
        matrix of susceptibilities tensor.
    * N1,N2,N3: floats
        Demagnetization factors in relation to a, b and c, respectively.
    * JR: array
        resultant magnetization vector without self-demagnetization correction.
    
    Returns:
    
    * JRD: array
        Resultant magnetization vector without self-demagnetization correction.   
    '''
    
    I = np.identity(3)
    kn0 = km[:,0]*N1
    kn1 = km[:,1]*N2
    kn2 = km[:,2]*N2
    kn = (np.vstack((kn0,kn1,kn2))).T
    A = I + kn
    JRD = (linalg.inv(A)).dot(JR)
    return JRD
    
def log_m (axis,lamb):
    '''
    Auxiliar calculus of magnetic field generated by a prolate ellipsoid.

    Parameters:
    
    * a,b:
        Major and minor axis, respectively.
    * lamb:
        Larger root of the cartesian ellipsoidal equation.
    
    Returns:
    
    * log:
        Auxiliar calculus of magnetic field generated by a prolate ellipsoid.
    '''
    
    log = np.log(((axis[0]**2-axis[1]**2)**0.5+(axis[0]**2+lamb)**0.5)/\
    ((axis[1]**2+lamb)**0.5))
    return log
    
def matrix_d (axis,lamb,log):
    '''
    Auxiliar calculus of magnetic field generated by a prolate ellipsoid.
    
    Parameters:
    
    * a,b:
        Major and minor axis, respectively.
    * lamb:
        Larger root of the cartesian ellipsoidal equation.
    * log:
        Auxiliar calculus of magnetic field generated by a prolate ellipsoid.
    
    Returns:
    
    * A,B,C:
        Auxiliar calculus of magnetic field generated by a prolate ellipsoid.
    '''
    
    A = (2./(axis[0]*axis[0] - axis[1]*axis[1])**(1.5)) * \
    (log - (((axis[0]*axis[0] - axis[1]*axis[1])/(axis[0]*axis[0] + lamb))**0.5))
    
    B = (1./(axis[0]*axis[0] - axis[1]*axis[1])**(1.5)) * \
    (((((axis[0]**2-axis[1]**2)*(axis[0]**2+lamb))**0.5)/(axis[1]**2+lamb)) - log)
    
    C = (1./(axis[0]*axis[0] - axis[1]*axis[1])**(1.5)) * \
    (((((axis[0]**2-axis[1]**2)*(axis[0]**2+lamb))**0.5)/(axis[1]**2+lamb)) - log)
    return A, B, C
    
def mx(axis,x1,x2,x3,dlambx1,dlambx2,dlambx3,A,B,C,lamb):
    '''
    Additional calculations for the ellipsoid magnetic field.
        
    Parameters:
    
    * a, b, c:
        Major, intermediate and minor axis, respectively.
    * x1, x2, x3:
        Axis of the body coordinate system.
    * A,B,C:
        Integrals of the potential field of an homogeneous ellipsoid
    * lamb:
        Larger root of the cubic equation: s^3 + p2*s^2 + p1*s + p0 = 0.
        
    Returns:
    
    * m11, m12, m13, m21, m22, m23, m31, m32, m33, cte, V1, V2, V3:
    Calculus for the ellipsoid magnetic field.        
    '''
        
    V1 = x1/((axis[0]**2+lamb)**(1.5)*(axis[1]**2+lamb))
    V2 = x2/((axis[0]**2+lamb)**(0.5)*(axis[1]**2+lamb)**2)
    V3 = x3/((axis[0]**2+lamb)**(0.5)*(axis[1]**2+lamb)**2)
    m11 = (dlambx1*V1) - A
    m12 = dlambx1*V2
    m13 = dlambx1*V3
    m21 = dlambx2*V1
    m22 = (dlambx2*V2) - B
    m23 = dlambx2*V3
    m31 = dlambx3*V1
    m32 = dlambx3*V2
    m33 = (dlambx3*V3) - C
    return m11, m12, m13, m21, m22, m23, m31, m32, m33

def B1_e (m11,m12,m13,J,axis):
    '''
    Calculates the B1 component of the magnetic field generated by 
    n-ellipsoids in the body coordinates.
    
    Parameters:
    
    * m11,m12,m13:
        Calculus for the ellipsoid magnetic field.
    * J:
        Resultant magnetization vector without self-demagnetization correction.
    * a,b:
        Major and minor axis, respectively.
    
    Returns:
    
    * B1 - The B1 component of the magnetic field generated by 
    n-ellipsoids in the body coordinates.
    '''
    
    B1 = 2*np.pi*axis[0]*axis[1]*axis[1]*(m11*J[0]+m12*J[1]+m13*J[2])
    return B1

def B2_e (m21,m22,m23,J,axis):
    '''
    Calculates the B1 component of the magnetic field generated by 
    n-ellipsoids in the body coordinates.
    
    Parameters:
    
    * m21,m22,m23:
        Calculus for the ellipsoid magnetic field.
    * J:
        Resultant magnetization vector without self-demagnetization correction.
    * a,b:
        Major and minor axis, respectively.
    
    Returns:
    
    * B1 - The B1 component of the magnetic field generated by 
    n-ellipsoids in the body coordinates.
    '''
    
    B2 = 2*np.pi*axis[0]*axis[1]*axis[1]*(m21*J[0]+m22*J[1]+m23*J[2])
    return B2
    
def B3_e (m31,m32,m33,J,axis):
    '''
    Calculates the B1 component of the magnetic field generated by 
    n-ellipsoids in the body coordinates.
    
    Parameters:
    
    * m31,m32,m33:
        Calculus for the ellipsoid magnetic field.
    * J:
        Resultant magnetization vector without self-demagnetization correction.
    * a,b:
        Major and minor axis, respectively.
    
    Returns:
    
    * B1 - The B1 component of the magnetic field generated by 
    n-ellipsoids in the body coordinates.
    '''
    
    B3 = 2*np.pi*axis[0]*axis[1]*axis[1]*(m31*J[0]+m32*J[1]+m33*J[2])
    return B3