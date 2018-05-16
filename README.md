# alchemy_myriad

This repository has scripts to map affinities between Myriad Live conference attendees based on their registration data. 
All the interest tags are merged into a list of all tags for each person.
An 'affinity network' is created by linking people if they share similar tags similar interest tags.
That network is used to identify clusters (or 'communities') of people that tend to share similar interests.
Each cluster is named by the most commonly shared tags of the group.

The affinity network generation uses the open source 'Tag2Network' code which can be found here:
https://github.com/foodwebster/Tag2Network

The 'myriad.py' script cleans the registration data, runs Tag2Network, and creates files with the network results:

Results output:
'myriadNetwork.xls' - has 2 sheets 
	- the 'nodes' sheet has the nodes with their attributes, including network metrics and cluster membership.
      - the 'cluster_name' field is the cluster membership with the auto-labeled cluster name. 
	- the 'links' sheet is a list of links - where the source and target id’s are the same as the node id’s in the nodes sheet

'myriadNodes.csv' and 'myriadEdges.csv' - are the same as above but in 2 separate csv’s

