# given EPIC #, pull data for that star from archive.stsci.edu
# then convert it into the format we are using:
# 3197 features, each being a light reading over time
# y = 2 for confirmed planet, 1 for not

from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import csv
import math

PLANETS_LIST = "k2names_2019.12.01_11.38.13.csv"

def get(epic, campaign):
	epic_first_four = str(int(epic / 100000) * 100000)
	epic_last_five = str(int((epic % 100000) / 1000) * 1000)
	campaign_str = str(campaign)
	epic_str = str(epic)

	# pad with zeros
	while len(epic_first_four) < 9:
		epic_first_four = "0" + epic_first_four
	while len(epic_last_five) < 5:
		epic_last_five = "0" + epic_last_five
	while len(campaign_str) < 2:
		campaign_str = "0" + campaign_str
	while len(epic_str) < 9:
		epic_str = "0" + epic_str

	url = "https://archive.stsci.edu/missions/k2/lightcurves/c%d/%s/%s"
	url += "/ktwo%s-c%s_llc.fits"
	fits_file = url % (campaign, epic_first_four, epic_last_five, epic_str, campaign_str)
	
	with fits.open(fits_file, mode="readonly") as hdulist:
		pdcsap_fluxes = hdulist[1].data['PDCSAP_FLUX']
		pdcsap_fluxes = pdcsap_fluxes[1:]

	# we want exactly 3197 features, following standard from Kaggle dataset
	if len(pdcsap_fluxes) > 3197:
		pdcsap_fluxes = pdcsap_fluxes[:3197]
	while len(pdcsap_fluxes) < 3197:
		pdcsap_fluxes.append(0.0)

	# is this in the current list of confirmed exoplanets?
	y = -1 # "all suspects are non-exoplanet until proven exoplanet"
	with open(PLANETS_LIST) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				line_count += 1
				continue
			repic = int(row[0])
			rcampaign = int(row[1])
			rname = row[2]
			if repic == epic and rcampaign == campaign:
				y = 1
				break
	pdcsap_fluxes = pdcsap_fluxes.tolist()
	for i in range(len(pdcsap_fluxes)):
		if math.isnan(float(pdcsap_fluxes[i])):
			pdcsap_fluxes[i] = 0.0
	return (pdcsap_fluxes, y)

def getall():
	X = []
	Y = []
	with open(PLANETS_LIST) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				line_count += 1
				continue
			repic = int(row[0])
			rcampaign = int(row[1])
			if (rcampaign == -1):
				continue
			if (repic < 100000000):
				continue
			try:
				pdcsap_fluxes, y = get(repic, rcampaign)
			except:
				print("error")
				continue
			X.append(pdcsap_fluxes)
			Y.append(y)
	return (X, Y)
