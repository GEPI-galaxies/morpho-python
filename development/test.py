from astropy.io import ascii

from objects import GalaxyFiles

from morpho_functions import *
from rhalf_functions import *
from ellipse_functions import *
from readlog import readlog

from ellipse_par import ellipse_par

def test_iraf(objname, galfiles, zp, pixscale, redshift):
    
    path_iraf = "../test/test_iraf/"
    path_morpho = "../test/test_sex/"

    galfiles.change_path("objfile", path_morpho)
    
    file_in = galfiles.objfile
    
    #ellipse_iraf(objname, file_in, path_iraf, zp, step="guess", **ellipse_par)
    #ellipse_iraf(objname, file_in, path_iraf, zp, step="final", **ellipse_par)
    
    file_dat = path_iraf + objname + "_ellipse.dat"
    file_profile = path_iraf + objname + "_profile.dat"
    file_plot =  path_iraf + objname + "_profile.png"
    #SB_profile(file_dat, file_profile, zp, pixscale, redshift, save_plot = "", cosmo_dimming = True)

    #plot_sb(file_profile, file_plot)
    sb_limit = 22.36 # value image GOODS
    result = PA_E_FromEllipse(file_profile, sb_limit)
    #print(result)
    
    write_ellipse("init", path_iraf + "PA_E_FromEllipse.dat")
    write_ellipse("add_line", path_iraf + "PA_E_FromEllipse.dat", ellipse = result, objname = objname)
    

def test_morpho(galfiles, zp):

    path_morpho = "../test/test_sex/"
    
    galfiles.change_path("objfile", path_morpho)
    galfiles.change_path("segfile", path_morpho)
    galfiles.change_path("maskfile", path_morpho)
    galfiles.change_path("sexcat", path_morpho)

    set_config_sex(galfiles, zp, config_file = path_morpho + "default.sex", param_file = path_morpho + "default.param", nnw_file = path_morpho + "default.nnw", conv_file = path_morpho + "default.conv")

    run_sextractor(galfiles, zp, config_file = path_morpho + "default.sex")

    sextractor_morpho(galfiles, input_mask = 0)


def test_rhalf(galfiles):
    
    path_rhalf = '../test/test_rhalf/'
    path_morpho = "../test/test_sex/"
    
    galfiles.change_path("objfile", path_morpho)
    galfiles.change_path("segfile", path_morpho)

    write_rhalf("init", path_rhalf + "cat_rhalf.cat")
    
    rhalf1,rhalf2=make_rhalf(galfiles, rhalf_fig = path_rhalf + "rhalf.png")
    #rhalf1,rhalf2=make_rhalf(galfiles)

    rhalf1_kpc=pix2kpc(pixscale,redshift,rhalf1)
    rhalf2_kpc=pix2kpc(pixscale,redshift,rhalf2)
    
    err_radiusKpc=abs(rhalf2_kpc-rhalf1_kpc)/2.
    print("Half light radius [kpc] (ellipses method)"+str(rhalf1_kpc))
    print("Half light radius [kpc] (from sextractor total flux estimation)"+str(rhalf2_kpc))
    print("Error : +/-"+str(err_radiusKpc))
    
    write_rhalf("add_line", path_rhalf + "cat_rhalf.cat", rhalf=[rhalf1_kpc,rhalf1,rhalf2_kpc,rhalf2],objname=objname)


def test_readlog():

    filetest = ['../test/test_log/J113543.11+494416.2.log', '../test/test_log/J012340.37+143637.2.log', '../test/test_log/J075806.15+422323.2.log', '../test/test_log/J075928.52+265322.6.log', '../test/test_log/J124055.45+552715.2.log', '../test/test_log/J225537.59+145711.4.log']
   
    index = 4

    file = filetest[index]
    print("----------------------------------")
    print(file)

    components = readlog(file)

    for comp in components:
        if "chi^2" in comp.keys(): 
            for key, value in comp.items(): print key, value
        if "chi^2/nu" in comp.keys(): 
            for key, value in comp.items(): print key, value
        print("----------------------------------")
        if "type" in comp.keys(): 
            print(comp["type"])
            if "sersic" in comp["type"]: 
                for key, value in comp.items(): print key, value
                print("----------------------------------")
            if "expdisk" in comp["type"]: 
                for key, value in comp.items(): print key, value
                print("----------------------------------")
            if "psf" in comp["type"]: 
                for key, value in comp.items(): print key, value
                print("----------------------------------")
            if "sky" in comp["type"]: 
                for key, value in comp.items(): print key, value
                print("----------------------------------")
            print("----------------------------------")

    

if __name__ == "__main__":

    path = "../test/"

    catalog_input = "../test/test.cat"

    table=ascii.read(catalog_input,Reader=ascii.NoHeader,names=['nam','file','redshift','pix','zp'])

    i=0

    filename=table['file'][i] 
    objname=table['nam'][i]

    galfiles = GalaxyFiles(objname)
    galfiles.change_path("infile", path)
        
    zp=table['zp'][i]
    redshift=table['redshift'][i]
    pixscale=table['pix'][i]

    #test_morpho(galfiles, zp)
    #test_rhalf(galfiles)

    test_iraf(objname, galfiles, zp, pixscale, redshift)

    #test_readlog()


### ecriture des fichiers : write_ellipse et write_rhalf sont similaires, penser a une uniaue function qui ouvre puis ajoute des lignes a un fichier
