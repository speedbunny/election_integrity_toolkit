#Load in data table library
library(data.table)

#Get all Clark County Data
tmp<-fread("~/Datasets/NV/county_all.txt")

#Remove Confidential Addresses
tmp2 <- tmp[!(tmp$RES_STREET_NAME=="CONFIDENTIAL"),]

#Remove People who Didn't Vote in the General Election
tmp3 <- tmp2[!(tmp2$ELECTION1==""),]

#Create A Combined Address Field
NVA <- within(tmp3,  address <- paste(RES_UNIT, RES_STREET_NUM, RES_DIRECTION, RES_STREET_NAME, RES_ADDRESS_TYPE, sep=" "))

#Find Clusters
cluster<-NVA[, .N, by=address]
