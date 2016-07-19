
import numpy as np
from scipy import interpolate
from astropy.cosmology import FlatLambdaCDM


def pix2kpc(pixscale,redshift,value):
    """ attention if faut verifier qu'il n'y a pas de risque aue la valeur soit trop elevee pour interpoler (comparaison entre value*pixscale et max de size_kpc)"""

    size_kpc=np.arange(1000000)/1000.
    ang=angular_diameter(size_kpc,redshift)
    interpfunc = interpolate.interp1d(ang,size_kpc, kind='linear')
    result=interpfunc(value*pixscale)
    to_return = np.float32(result)
    
    return to_return


def angular_diameter(size,redshift): ## size must be in kpc

    cosmo = FlatLambdaCDM(H0=70, Om0=0.3)  ## defining the cosmology  => see the documentation and details of the parameters and their values
    lumdist=cosmo.luminosity_distance(redshift)  ## value in kpc

    zang=size*(1+redshift)**2/(1000.*lumdist)*180./np.pi*3600. ## arcsec

    return zang

def mask_ellipse(nrow,ncol,yc,xc,ratio,ang):
    
    ## nrow is the number of rows (vertical axis) and ncol is the number of columns (horizontal axis), xc is the horizontal center coordinate and yc is the vertical center coordinate
    ## angle origin is the horizontal axis right and positive counterclockwise
    ## ratio is a/b > 1 where a is the semi major axis of the ellipse and b the semi minor axis

   
    radang=ang*np.pi/180.
    cosang=np.cos(radang)
    sinang=np.sin(radang)

    y=np.arange(nrow,dtype=np.float64)-yc
    x=np.arange(ncol,dtype=np.float64)-xc

    im=np.zeros((nrow,ncol),np.float64)

    ycosang=y*cosang
    ysinang=y*sinang
    
    for i in np.arange(ncol):
        ytemp=ysinang+x[i]*cosang
        xtemp=-ycosang+x[i]*sinang
        im[:,i]=np.sqrt( (xtemp*ratio)**2 + ytemp**2 )

    return im
    

def clean_char(char, char_to_remove):
        
    for c in char_to_remove:
            
        if char.find(c) != -1:
            char = char.replace(c,"")
                
    return char

def clean_list(list, *to_remove):

    for char in to_remove:
        while char in list:
            list.remove(char)
