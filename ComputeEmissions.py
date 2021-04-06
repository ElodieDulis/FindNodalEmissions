import numpy as np
import geopy
from geopy.distance import geodesic 

## Load node coordinates and Steel and Cement sites coord + emissions
NodeData = np.loadtxt('Nodes.txt',  delimiter=',', converters=None, skiprows=1, usecols=(1,2))
SteelSiteData = np.loadtxt('SteelData.csv',  delimiter=',', converters=None, skiprows=1, usecols=(0,1,2))
CementSiteData = np.loadtxt('CementData.csv',  delimiter=',', converters=None, skiprows=1, usecols=(0,1,2))
#SitesCoord = np.loadtxt('Test.csv',  delimiter=',', converters=None, skiprows=1, usecols=(0,1,2))



def ComputeNodalEmissions(NodesCoord,SitesCoord, EmissionSource):
    ## Find closest node to each site 
    DistNodeToSite = np.zeros((NodesCoord.shape[0],SitesCoord.shape[0]))
    for node in range(NodesCoord.shape[0]):
        for site in range(SitesCoord.shape[0]):
            DistNodeToSite [node,site] = geodesic(NodesCoord[node],SitesCoord[site,0:2]).km

    IndexMinDist = DistNodeToSite.argmin(axis = 0)

    ## Emissions of each node
    NodeEmissions = np.zeros(NodesCoord.shape[0])
    for site in range(SitesCoord.shape[0]):
        NodeEmissions[IndexMinDist[site]]+=SitesCoord[site,2]

    ## Export results
    np.savetxt('NodeEmissions' + EmissionSource +'.csv', NodeEmissions, delimiter=',' , header = 'CO2 emissions per nodes in kg')

ComputeNodalEmissions(NodeData, SteelSiteData, 'Steel')
ComputeNodalEmissions(NodeData, CementSiteData, 'Cement')

