

class GalaxyFiles:
    """class defining all the files related to a galaxy"""

    def __init__(self, name):
        """ default names """
        self.infile = name + ".fits"
        self.objfile = name + "_obj.fits"
        self.segfile = name + "_seg.fits"
        self.maskfile = name + "_mask.fits"
        self.sexcat = name + ".ASC"

    def change_path(self, file, path):
        
        if file == "infile":
            path_list = self.infile.split("/")
            f = path_list[-1]
            self.infile = path + f

        if file == "objfile":
            path_list = self.objfile.split("/")
            f = path_list[-1]
            self.objfile = path + f

        if file == "segfile":
            path_list = self.segfile.split("/")
            f = path_list[-1]
            self.segfile = path + f

        if file == "maskfile":
            path_list = self.maskfile.split("/")
            f = path_list[-1]
            self.maskfile = path + f

        if file == "sexcat":
            path_list = self.sexcat.split("/")
            f = path_list[-1]
            self.sexcat = path + f

        if file == "all":
            path_list = self.infile.split("/")
            f = path_list[-1]
            self.infile = path + f
            path_list = self.objfile.split("/")
            f = path_list[-1]
            self.objfile = path + f
            path_list = self.segfile.split("/")
            f = path_list[-1]
            self.segfile = path + f
            path_list = self.maskfile.split("/")
            f = path_list[-1]
            self.maskfile = path + f
            path_list = self.sexcat.split("/")
            f = path_list[-1]
            self.sexcat = path + f



         

