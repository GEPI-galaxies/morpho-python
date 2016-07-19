
import numpy as np
from functions import clean_char, clean_list

def readlog(file):

    def extract_param(line, line_err, type):
    
        char_to_remove = ["[","]","(",")",";",":",",",str()]
        param = {}
    
        line = line.rstrip('\n').split(" ")
        line_err = line_err.rstrip('\n').split(" ")
    
        clean_list(line, *char_to_remove)  # suppression de la liste des caracteres definis dans char_to_remove
        clean_list(line_err, *char_to_remove)

        # extraction des parametres

        param["type"] = type

        if type != "sky":
            param["xc"] = float(clean_char(line[1],char_to_remove))
            param["yc"] = float(clean_char(line[2],char_to_remove))
            param["err_xc"] = float(clean_char(line_err[0],char_to_remove))
            param["err_yc"] = float(clean_char(line_err[1],char_to_remove))
            param["mag"] = float(clean_char(line[3],char_to_remove))
            param["err_mag"] = float(clean_char(line_err[2],char_to_remove))
            
            if type == "sersic":
                param["re"] = float(clean_char(line[4],char_to_remove))
                param["n"] = float(clean_char(line[5],char_to_remove))
                param["ratio_b_over_a"] = float(clean_char(line[6],char_to_remove))
                param["pa"] = float(clean_char(line[7],char_to_remove))
        
                param["err_re"] = float(clean_char(line_err[3],char_to_remove))
                param["err_n"] = float(clean_char(line_err[4],char_to_remove))
                param["err_ratio_b_over_a"] = float(clean_char(line_err[5],char_to_remove))
                param["err_pa"] = float(clean_char(line_err[6],char_to_remove))
        
            elif type == "expdisk":
                param["rd"] = float(clean_char(line[4],char_to_remove))
                param["ratio_b_over_a"] = float(clean_char(line[5],char_to_remove))
                param["pa"] = float(clean_char(line[6],char_to_remove))
        
                param["err_rd"] = float(clean_char(line_err[3],char_to_remove))
                param["err_ratio_b_over_a"] = float(clean_char(line_err[4],char_to_remove))
                param["err_pa"] = float(clean_char(line_err[5],char_to_remove))
        
        elif type == "sky":
            param["sky_value"] = float(clean_char(line[3],char_to_remove))
            param["dxsky"] = float(clean_char(line[4],char_to_remove))
            param["dysky"] = float(clean_char(line[5],char_to_remove))
            param["err_sky_value"] = float(clean_char(line_err[0],char_to_remove))
            param["err_dxsky"] = float(clean_char(line_err[1],char_to_remove))
            param["err_dysky"] = float(clean_char(line_err[2],char_to_remove))


        return param

    def extract_chi2(line):

        chi_values = {}
        
        line = line.rstrip('\n').split("=")
        
        name = clean_char(line[0], " ")
        if clean_char(line[0], " ") == "Chi^2":
            chi = float(line[1].split(",")[0])
            chi_values["chi^2"] = chi
        elif clean_char(line[0], " ") == "Chi^2/nu":
            chi_reduced = float(line[1])
            chi_values["chi^2/nu"] = chi_reduced


        return chi_values

    """ comment to be added """

    f = open(file,'r')         # open the file
    lines = f.readlines()      # read the lines stored in a list
    components = []            # components will consist of a list of dictionnaries, one dictionnary per component + one dictionnary for the chi square and reduced chi square values

    for index, l in enumerate(lines):

        if "sersic" in l: 
            components.append(extract_param(lines[index], lines[index+1], "sersic"))
            
        if "expdisk" in l: 
            components.append(extract_param(lines[index], lines[index+1], "expdisk"))

        if "psf" in l: 
            components.append(extract_param(lines[index], lines[index+1], "psf"))

        if "sky" in l:
            components.append(extract_param(lines[index], lines[index+1], "sky"))

        if "Chi^2" in l:
            components.append(extract_chi2(lines[index]))

    return(components)
