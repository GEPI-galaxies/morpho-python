ellipse_par = {}

ellipse_par["geom"] = {}
ellipse_par["isoimap"] = {}

ellipse_par["geom"]["X0"] = "INDEF"     # initial isophote center X
ellipse_par["geom"]["Y0"] = "INDEF"     # initial isophote center Y
ellipse_par["geom"]["ellip0"] = 0.2   # initial ellipticity
ellipse_par["geom"]["pa0"] = 0.0      # initial position angle (degrees)
ellipse_par["geom"]["sma0"] = 10.0    # initial semi-major axis lenght
ellipse_par["geom"]["minsma"] = 0.0   # minimum semi-major axis lenght
ellipse_par["geom"]["maxsma"] = 300.0 #  maximum semi-major axis lenght
ellipse_par["geom"]["step"] = 1.0     # sma step between successive ellipses
ellipse_par["geom"]["linear"] = "yes"   # linear sma step ?
ellipse_par["geom"]["maxrit"] = "INDEF" # maximum sma lenght for iterative mode
ellipse_par["geom"]["recenter"] = "yes" # allows finding routine to re-center x0-y0 ?
ellipse_par["geom"]["xylearn"] = "no"  # updates pset with new x0-y0 ?
ellipse_par["geom"]["physical"] = "yes" # physical coordinate system ?

ellipse_par["isoimap"]["image"] = ""          # input image
ellipse_par["isoimap"]["table"] = ""          # input table
ellipse_par["isoimap"]["fulltable"] = "yes"   # use full range of `SMA' from table ?
ellipse_par["isoimap"]["minsma"] = 10.0      # minimum semi-major axis
ellipse_par["isoimap"]["maxsma"] = 50.0    # maximum semi-major axis
ellipse_par["isoimap"]["nlevels"] = 50.0    # number of levels
ellipse_par["isoimap"]["color"] = "r"         # overlay color
ellipse_par["isoimap"]["frame"] = 1         # image display frame
