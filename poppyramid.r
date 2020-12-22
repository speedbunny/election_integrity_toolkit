library(ggplot2)
#Add an age field
GAVOTES[, AGE := 2020 - BIRTHDATE]
#Add age grouping
GAVOTES$AGEbreak <- cut(GAVOTES$AGE, breaks = seq(18, 118, 5), right = FALSE)
#Each record represents population value of 1
GAVOTES$POPULATION <- 1
# aggregate by gender and age group
GAVOTES <- aggregate(formula = POPULATION ~ GENDER + AGEbreak, data = GAVOTES, FUN = sum)
#Sort by Gender and Age
GAVOTES <- with(GAVOTES, GAVOTES[order(GENDER,AGEbreak),])
#There are only two genders in this pyramid
GAVOTES<-GAVOTES[!grepl("O", GAVOTES$GENDER),]

#Plot female to left
GAVOTES$POPULATION <- ifelse(GAVOTES$GENDER == "F", -1*GAVOTES$POPULATION, GAVOTES$POPULATION)
# Create Pyramid as two bar charts with axes flipped

pyramidGA <- ggplot(GAVOTES, aes(x = AGEbreak, y = POPULATION, fill = GENDER)) + 
     geom_bar(data = subset(GAVOTES, GENDER == "F"), stat = "identity",fill = "#779ECB") +
     geom_bar(data = subset(GAVOTES, GENDER == "M"), stat = "identity",fill = "#E17F93") + 
     xlab("Age Group") +
   scale_fill_manual("legend", values = c("A" = "black", "B" = "orange", "C" = "blue")) +
     scale_y_continuous(breaks=c(-300000,-200000,-100000,-50000,0,50000,100000,200000,300000), labels=expression("-300K","-200K","-100K","-50K","0", "50K", "100K","200K","300K")) + 
     coord_flip()
  
pyramidGA
