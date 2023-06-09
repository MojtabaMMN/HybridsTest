#!/usr/bin/env python3

from rhapi import RhApi
import pprint
import json
from datetime import datetime
import matplotlib.pyplot as plt
import calendar
import sys

class cumulativePlot:

    def __init__(self, hybridtype, dtbs):
    
        self.hybridtype  = hybridtype
        self.dtbs = dtbs

    def ConnectProductionDB(self):
    
        db_client = RhApi('https://cmsdca.cern.ch/trk_rhapi', False, sso='login')

        if self.hybridtype == "2SFEH":
            print("\n###  Creating query to get 2SFEH data from production database ###\n")
            query = ('SELECT c.START_TIME, c.END_TIME, c.QUALIFICATION FROM trker_cmsr.c9800 c')
            response = db_client.json2(query) # Get a JSON object
            
        elif self.hybridtype == "2SSEH":
            print("\n###  Creating query to get 2SSEH data from production database ###\n")
            query = ('SELECT c.START_TIME, c.END_TIME, c.QUALIFICATION FROM trker_cmsr.c12600 c')
            response = db_client.json2(query)
            
        elif self.hybridtype == "PSFEH":
            print("\n###  Creating query to get PSFEH data from production database ###\n")
            query = ('SELECT c.START_TIME, c.END_TIME, c.QUALIFICATION FROM trker_cmsr.c9820 c')
            response = db_client.json2(query)
            
        elif self.hybridtype == "PSROH":
            print("\n###  Creating query to get PSROH data from production database ###\n")
            query = ('SELECT c.START_TIME, c.END_TIME, c.QUALIFICATION FROM trker_cmsr.c9840 c')
            response = db_client.json2(query)
            
        elif self.hybridtype == "PSPOH":
            print("\n###  Creating query to get PSPOH data from production database ###\n")
            query = ('SELECT c.START_TIME, c.END_TIME, c.QUALIFICATION FROM trker_cmsr.c13000 c')
            response = db_client.json2(query)
    
        return response

            
    def ConnectDevelopmentDB(self):
    
        db_client = RhApi('https://cmsdca.cern.ch/trk_rhapi', False, sso='login')
    #    pprint = pprint.PrettyPrinter(indent=4)

        if self.hybridtype == "2SFEH":
            print("\n###  Creating query to get 2SFEH data from development database ###\n")
            query = ('SELECT c.START_TIME, c.END_TIME, c.QUALIFICATION FROM trker_int2r.c16220 c')
            response = db_client.json2(query)
            
        elif self.hybridtype == "2SSEH":
            print("\n###  Creating query to get 2SSEH data from development database ###\n")
            query = ('SELECT c.START_TIME, c.END_TIME, c.QUALIFICATION FROM trker_int2r.c20220 c')
            response = db_client.json2(query)
    
        elif self.hybridtype == "PSFEH":
            print("\n###  Creating query to get PSFEH data from development database ###\n")
            query = ('SELECT c.START_TIME, c.END_TIME, c.QUALIFICATION FROM trker_int2r.c16240 c')
            response = db_client.json2(query)
            
        elif self.hybridtype == "PSROH":
            print("\n###  Creating query to get PSROH data from development database ###\n")
            query = ('SELECT c.START_TIME, c.END_TIME, c.QUALIFICATION FROM trker_int2r.c16260 c')
            response = db_client.json2(query)
            
        elif self.hybridtype == "PSPOH":
            print("\n###  Creating query to get PSPOH data from development database ###\n")
            query = ('SELECT c.START_TIME, c.END_TIME, c.QUALIFICATION FROM trker_int2r.c21020 c')
            response = db_client.json2(query)
        
        return response

    def GettingInfo(self):
    
        tInspection = []
        NumberOfInspected = []
        NumberOfInspectedGood = []
        NumberOfInspectedBad = []
        QualityOfHybrid = []
        EndTime = []
        StartTime = []

        if self.dtbs == "production":
        
            response = self.ConnectProductionDB()
            
        elif self.dtbs == "development":

            response = self.ConnectDevelopmentDB()

        else:
        
            print("No correct database")


        for rr in response['data']:
        
            StartTime.append(rr["startTime"])
            EndTime.append(rr["endTime"])
            QualityOfHybrid.append(rr["qualification"])

        StartTime.sort(reverse=False)
        EndTime.sort(reverse=False)

        n = len(StartTime)
        for i in range(n):
            stt_time = datetime.fromisoformat(StartTime[i])
            end_time = datetime.fromisoformat(EndTime[i])
      #      tInspection.append(stt_time.strftime('Year:%y\nMonth:%m\nDay:%d'))
            tInspection.append(stt_time.strftime('%y\n%m\n%d'))

        j = 0
        nn = 0
        while j < n:
            if  QualityOfHybrid[j] == 'Bad' or QualityOfHybrid[j] == 'Good':
                nn+=1
                NumberOfInspected.append(nn)
            else:
                nn = nn
                NumberOfInspected.append(nn)
            j+=1

        m = 0
        ngood = 0
        while m < n:
            if QualityOfHybrid[m] == 'Good':
                ngood+=1
                NumberOfInspectedGood.append(ngood)
            else:
                ngood = ngood
                NumberOfInspectedGood.append(ngood)
            m+=1

        mm = 0
        nbad = 0
        while mm < n:
            if QualityOfHybrid[mm] == 'Bad':
                nbad+=1
                NumberOfInspectedBad.append(nbad)
            else:
                nbad = nbad
                NumberOfInspectedBad.append(nbad)
            mm+=1

        return tInspection, NumberOfInspected, NumberOfInspectedGood, NumberOfInspectedBad, QualityOfHybrid


    def plotting(self):
        

        
        tInspection, NumberOfInspected, NumberOfInspectedGood, NumberOfInspectedBad,QualityOfHybrid = self.GettingInfo()

        plt.figure(1)
        plt.tick_params(labelright=True, labelleft=True, length=5, width=2, direction='in')
        plt.ylabel('Number of inspected hybrids')
        pltTitle = "CMSDB,"+self.dtbs+", "+self.hybridtype
        plt.title(pltTitle)
        plotNTotal = plt.plot(tInspection,NumberOfInspected, label='Total Number of Inspected')
        plotNGood = plt.plot(tInspection,NumberOfInspectedGood, label='Number of Good Hybrids')
        plotNBad = plt.plot(tInspection,NumberOfInspectedBad, label='Number of Bad Hybrids')
        plt.setp(plotNBad, linestyle='--')
        plt.setp(plotNBad, linewidth=1, color='g')
        plt.xticks(tInspection, tInspection, rotation =30, fontsize=6)
        plt.legend(loc='upper left')
        outputplot = "NInspectedHybrid_Time_"+self.hybridtype+self.dtbs+".pdf"
        plt.savefig(outputplot)
        plt.close()
        
        tInspection.clear()
        NumberOfInspected.clear()
        NumberOfInspectedGood.clear()
        NumberOfInspectedBad.clear()
        QualityOfHybrid.clear()

 
 #      plt.show()



###################################################

tsfh_pr = cumulativePlot("2SFEH","production")
tsfh_pr.plotting()
del tsfh_pr


tssh_pr = cumulativePlot("2SSEH","production")
tssh_pr.plotting()
del tssh_pr


psfh_pr = cumulativePlot("PSFEH","production")
psfh_pr.plotting()
del psfh_pr

psrh_pr = cumulativePlot("PSROH","production")
psrh_pr.plotting()
del psrh_pr

psph_pr = cumulativePlot("PSPOH","production")
psph_pr.plotting()
del psph_pr

tsfh_de = cumulativePlot("2SFEH","development")
tsfh_de.plotting()
del tsfh_de

tssh_de = cumulativePlot("2SSEH","development")
tssh_de.plotting()
del tssh_de

psfh_de = cumulativePlot("PSFEH","development")
psfh_de.plotting()
del psfh_de

psrh_de = cumulativePlot("PSROH","development")
psrh_de.plotting()
del psrh_de

psph_de = cumulativePlot("PSPOH","development")
psph_de.plotting()
del psph_de



   
