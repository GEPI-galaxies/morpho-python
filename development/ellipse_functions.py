### developpement progressif
### niveau 1 : execution automatique avec des parametres par defaut
### niveau 2 : interaction avec l'utilisateur : verification, possibilite de changer les parametres

import matplotlib.pyplot as plt
from pyraf import iraf
from subprocess import Popen,PIPE
import time
from astropy.io import ascii
import numpy as np
from functions import *


def ellipse_iraf0(objname, file_in, path_out, zp, step="guess"):

    if step=="guess":
        file_cl = path_out + objname + "_guess.cl"
        file_tab = path_out + objname + "_ellipse_Guess.tab"
        file_dat = path_out + objname + "_ellipse_Guess.dat"
    elif step=="final":
        file_cl = path_out + objname + "_ellipse.cl"
        file_tab = path_out + objname + "_ellipse.tab"
        file_dat = path_out + objname + "_ellipse.dat"
        file_guess = path_out + objname + "_ellipse_Guess.dat"

    file_tmp = path_out + objname + "_temp.fits"
    
    Cmd_FileIN="s%$FILE_IN%"+file_in+"%"
    Cmd_FileEllipse="s%$FILE_ELLIPSE%"+file_tab+"%"
    Cmd_FileTmp="s%$FILE_TMP%"+file_tmp+"%"
    Cmd_FileFinal="s%$FILE_DAT%"+file_dat+"%"
    Cmd_mag0="s%$mag0%"+str(zp)+"%"

    if step=="guess":
        Cmd_X0="s%$XCENTER%INDEF%"
        Cmd_Y0="s%$YCENTER%INDEF%"
        Cmd_centerFlag="s%$recente_FLAG%yes%"
    elif step=="final":
        table=ascii.read(file_guess,Reader=ascii.NoHeader,names=['row','sma','Int','Int_err','E', 'E_err', 'PA', 'PA_err', 'Xc', 'Yc', 'Tflux', 'Tmag', 'Npix'])

        centerX = str(np.mean(table['Xc']))
        centerY = str(np.mean(table['Yc']))

        Cmd_X0="s%$XCENTER%"+centerX+"%"
        Cmd_Y0="s%$YCENTER%"+centerY+"%"
        Cmd_centerFlag="s%$recente_FLAG%no%"
        
    f=open("script_sed","w")
    f.write(Cmd_FileIN+"\n")
    f.write(Cmd_FileEllipse+"\n")
    f.write(Cmd_FileTmp+"\n")
    f.write(Cmd_FileFinal+"\n")
    f.write(Cmd_X0+"\n")
    f.write(Cmd_Y0+"\n")
    f.write(Cmd_mag0+"\n")
    f.write(Cmd_centerFlag+"\n")
    f.close()

    f=open("script_shell","w")
    f.write("#!/bin/bash \n")
    f.write("sed -f script_sed < Template_ellipse.dat > "+file_cl+"\n")
    f.write("chmod 755 "+file_cl+"\n")
    f.close()

    p=Popen(["sh script_shell"],shell=True) 
    p.wait()


def set_iraf_param(ellipse_par):

    iraf.geompar.ellip0 = ellipse_par["geom"]["ellip0"]
    iraf.geompar.pa0 = ellipse_par["geom"]["pa0"]
    iraf.geompar.sma0 = ellipse_par["geom"]["sma0"]
    iraf.geompar.minsma = ellipse_par["geom"]["minsma"]
    iraf.geompar.maxsma = ellipse_par["geom"]["maxsma"]
    iraf.geompar.step = ellipse_par["geom"]["step"]
    iraf.geompar.linear = ellipse_par["geom"]["linear"]
    iraf.geompar.xylearn = ellipse_par["geom"]["xylearn"]
    iraf.geompar.physical = ellipse_par["geom"]["physical"]
    iraf.geompar.maxrit = ellipse_par["geom"]["maxrit"]
    
    iraf.geompar.x0 = ellipse_par["geom"]["X0"]
    iraf.geompar.y0 = ellipse_par["geom"]["Y0"]
    iraf.geompar.recenter = ellipse_par["geom"]["recenter"]

    iraf.isoimap.image = ellipse_par["isoimap"]["image"]
    iraf.isoimap.table = ellipse_par["isoimap"]["table"]
    iraf.isoimap.frame = ellipse_par["isoimap"]["frame"]
    iraf.isoimap.nlevels = ellipse_par["isoimap"]["nlevels"]
    iraf.isoimap.minsma = ellipse_par["isoimap"]["minsma"]
    iraf.isoimap.maxsma = ellipse_par["isoimap"]["maxsma"]
    iraf.isoimap.fulltab = ellipse_par["isoimap"]["fulltable"]
    iraf.isoimap.color = ellipse_par["isoimap"]["color"]


def ellipse_iraf(objname, file_in, path_out, zp, step="guess", **ellipse_par):
 
    file_tab = path_out + objname + "_ellipse_Guess.tab"
    file_dat = path_out + objname + "_ellipse_Guess.dat"

    if step == "guess":
        file_tab = path_out + objname + "_ellipse_Guess.tab"
        file_dat = path_out + objname + "_ellipse_Guess.dat"

        ellipse_par["geom"]["X0"] = "INDEF"
        ellipse_par["geom"]["Y0"] = "INDEF"
        ellipse_par["geom"]["recenter"] = "yes"

    elif step == "final":
        file_tab = path_out + objname + "_ellipse.tab"
        file_dat = path_out + objname + "_ellipse.dat"
        file_guess = path_out + objname + "_ellipse_Guess.dat"

        print(file_guess)
        ## reading the results of guess file
        table=ascii.read(file_guess,Reader=ascii.NoHeader,names=['row','sma','Int','Int_err','E', 'E_err', 'PA', 'PA_err', 'Xc', 'Yc', 'Tflux', 'Tmag', 'Npix'])

        centerX = str(np.mean(table['Xc']))
        centerY = str(np.mean(table['Yc']))

        ellipse_par["geom"]["X0"] = str(centerX)
        ellipse_par["geom"]["Y0"] = str(centerY)
        ellipse_par["geom"]["recenter"] = "no"

    
    run_ell(file_in, file_tab, file_dat, zp, **ellipse_par)


def run_ell(file_in, file_tab, file_dat, mag, **ellipse_par):    

    # prochaine etape : mettre en argument sous une certaine forme les parametres associes epar des taches 1) strict minimum sous forme de dico fixe 2) tout pouvoir changer sous forme de dictionnaire et tester les cles ...

    # import iraf packages
 
    iraf.stsdas()
    iraf.analysis()
    iraf.isophote()

    p = Popen("ds9", shell = True)
    time.sleep(5)

    iraf.display(file_in, 1)  

    set_iraf_param(ellipse_par)

    # iraf.lpar(iraf.geompar)

    iraf.ellipse(file_in, file_tab, mag0 = str(mag), verbose = "no")
    
    # iraf.lpar(iraf.isoimap)
    
    iraf.isoimap(file_in, file_tab)

    iraf.tproject(file_tab, "temp.fits", "SMA,INTENS,INT_ERR,ELLIP,ELLIP_ERR, PA, PA_ERR, X0, Y0, TFLUX_C, TMAG_E,NPIX_E")
    
    iraf.tprint("temp.fits", pwidth = 200, Stdout = file_dat)
    
    iraf.imdel("temp.fits")

    p.kill()


def SB_profile(file_dat, file_profile, zp, pixscale, redshift, save_plot = "", cosmo_dimming = False):


    # reading the output from ellipse

    table = np.transpose(np.genfromtxt(file_dat, dtype=str))
    table[table == "INDEF"] = "-999."
    table = np.float32(table)

    sma = table[1]
    intens = table[2]
    intens_err = table[3]
    e = table[4]
    e_err = table[5]
    pa = table[6]
    pa_err = table[7]
    xc = table[8]
    yc = table[9]

    pa_err[pa_err == -999.] = 0.
    e_err[e_err == -999.] = 0.
    intens_err[intens_err == -999.] = 0

    # convert pix into kpc
    x_kpc = [0] * len(sma)
    #print(x_kpc)
    
    for l in np.arange(len(x_kpc)):
        x_kpc[l] = pix2kpc(pixscale, redshift, sma[l])
    ## attention la conversion en kpc est vraiment tres tres lente => trouver une optimisation

    # convert flux into surface brightness
    sb = intens
    sb = np.where(sb != -999., -2.5*np.log10(sb) + zp + 2.5*np.log10(pixscale**2), sb)
    ### attention au cas ou sb serait nan => rendre la routine plus robuste
    #sb = -2.5*np.log10(intens) + zp + 2.5*np.log10(pixscale**2)
    sb_low = -2.5*np.log10(intens - intens_err) + zp + 2.5*np.log10(pixscale**2)
    sb_high = -2.5*np.log10(intens + intens_err) + zp + 2.5*np.log10(pixscale**2)
    # correcting for dimming if asked
    if cosmo_dimming == True:
        sb = sb - 10*np.log10(1 + redshift)
        sb_low = sb_low - 10*np.log10(1 + redshift)
        sb_high = sb_high - 10*np.log10(1 + redshift)

    # write output file
    file = open(file_profile, "w")
    file.write('# sma_p \t sma_kpc \t Intens \t Intens_err \t SB \t SB_err_low \t SB_err_high \t PA \t PA_err \t Ellip \t Ellip_err \t X0 \t Y0 \n')
    file.write('# [pixel] \t [kpc] \t [flux] \t [flux] \t [mag/arcsec^2] \t [mag/arcsec^2] \t [mag/arcsec^2] \t [degree] \t [degree] \t [] \t [] \t [pixel] \t [pixel] \n')
    for l in np.arange(len(sma)):
        file.write("%8.3f \t % 8.3f \t %8.3e \t %8.3e \t %8.3f \t %8.3f \t %8.3f \t %8.3f \t %8.3f \t %8.3f \t %8.3f \t %8.3f  \t %8.3f \n" %  (sma[l], x_kpc[l], intens[l], intens_err[l], sb[l], sb_low[l], sb_high[l], pa[l], pa_err[l], e[l], e_err[l], xc[l], yc[l]))

    file.close

    if len(save_plot) != 0: plot_sb(file_profile, save_plot)
  
def plot_sb(file_profile, save_plot):  
    
    # plot (surface brightness profile)
    table = np.transpose(np.genfromtxt(file_profile , dtype=np.float32))
    
    sma = table[0]
    sma_kpc = table[1]
    intens = table[2]
    intens_err = table[3]
    sb = table[4]
    sb_low = table[5]
    sb_high = table[6]
    pa = table[7]
    pa_err = table[8]
    e = table[9]
    e_err = table[10]
    xc = table[11]
    yc = table[12]

    #X = [(1,2,1), (2,2,2), (2,2,4)]
    #for nrows, ncols, plot_nb in X:
    #    plt.subplot(nrows, ncols, plot_nb)

    ## verifier les barres d'erreur

    plt.subplot(121)
    plt.errorbar(sma_kpc, sb, yerr=[sb_high-sb, sb-sb_low])
    plt.xlabel("radius [kpc]")
    plt.ylabel("surface brightness [mag/arcsec^2]")
    plt.ylim([np.max(sb + 0.5), np.min(sb)-0.5])
    plt.xlim([0,30])

    plt.subplot(222)
    plt.errorbar(sma_kpc, pa, yerr=pa_err)
    plt.xlabel("radius [kpc]")
    plt.ylabel("PA [deg]")
    plt.xlim([0,30])
    plt.ylim([np.min(pa[np.where(pa != -999.)])-10., np.max(pa)+10.])

    plt.subplot(224)
    plt.errorbar(sma_kpc, e, yerr=e_err)
    plt.xlabel("radius [kpc]")
    plt.ylabel("Ellipticity")
    plt.xlim([0,30])
    plt.ylim([np.min(e[np.where(e != -999.)])-0.1, np.max(e)+0.1])

    plt.tight_layout()
#    plt.subplots_adjust(hspace = 0.001)
    
    plt.savefig(save_plot)


def PA_E_FromEllipse(file_profile, sb_limit):
    
    table = np.transpose(np.genfromtxt(file_profile , dtype=np.float32))
    
    sma = table[0]
    sma_kpc = table[1]
    intens = table[2]
    intens_err = table[3]
    sb = table[4]
    sb_low = table[5]
    sb_high = table[6]
    pa = table[7]
    pa_err = table[8]
    e = table[9]
    e_err = table[10]
    xc = table[11]
    yc = table[12]

    diff = np.abs(sb - sb_limit)
    min_value = np.min(np.abs(sb - sb_limit))

    index = np.where(np.abs(sb - sb_limit) == np.min(np.abs(sb - sb_limit)))

    index = index[0][0]  # conversion array to list to float
    ##print(len(index))
    ## robustesse : ajouter une condition dans le cas ou index a plusieurs valeurs => n'en garder qu'une seule qui correspondrait au sma_max si les valeurs ne se suivent pas ou une mediane si les valeurs se suivent

    radius_pix = sma[index]
    radius_kpc = sma_kpc[index]
    
    ii = np.arange(5) - 2 + index
    
    pa_ext = np.median(pa[ii])
    e_ext = np.median(e[ii])

    pa_err_ext = np.median(pa_err[ii][np.where(pa[ii] == pa_ext)])
    e_err_ext = np.median(e_err[ii][np.where(e[ii] == e_ext)])

    result = [index, radius_pix, radius_kpc, pa_ext, e_ext, pa_err_ext, e_err_ext, xc[index], yc[index]]

    return result
    
   
def write_ellipse(step, filename, ellipse = [], objname = ""):

    if step == "init":
        file=open(filename,"w")
        file.write("# name \t radius[kpc] \t PA[deg] \t Ellip[] \t PA_err[deg] \t E_err[] \n")
        file.close()

    if step == "add_line":
        file=open(filename, "a")
        file.write('%s \t %8.3f \t  %8.3f \t %8.3f \t  %8.3f \t  %8.3f \n' % (objname, ellipse[2], ellipse[3], ellipse[4], ellipse[5], ellipse[6]))
        file.close


def plot_ellipse():
    
    
