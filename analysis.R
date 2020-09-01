#install.packages("tidytext")
#install.packages("stringr", dependencies = TRUE)
#install.packages("quanteda", dependencies = T)
#install.packages("pastecs")
#install.packages("xtable")

library(xtable) # creates latex tables automatically from output
options(xtable.floating = FALSE)
options(xtable.timestamp = "")
library(stringr) # string manipulation
library(dplyr)
library(tidytext)
library(quanteda) # for sparse doc-term matrixS
library(ggplot2) #plots
library(gridExtra) # for combining plots  
library(moments) #for skewness, kurtosis etc.

#gets all relevant csv files
my_files<-list.files(pattern = "\\.csv$", path="csv")

getwd()
setwd("csv")

dat<-read.csv("reviews_all.csv",encoding = "UTF-8", na.strings = "N/A",stringsAsFactors = FALSE) #smartphones
dat_TV<-read.csv("reviews_TV.csv",encoding = "UTF-8", na.strings = "N/A",stringsAsFactors = FALSE)
dat_headphones<-read.csv("reviews_headphones.csv",encoding = "UTF-8", na.strings = "N/A",stringsAsFactors = FALSE)
dat_monitors<-read.csv("reviews_monitors.csv",encoding = "UTF-8", na.strings = "N/A",stringsAsFactors = FALSE)
dat_tablets<-read.csv("reviews_tablets.csv",encoding = "UTF-8", na.strings = "N/A",stringsAsFactors = FALSE)
dat_routers<-read.csv("reviews_routers.csv",encoding = "UTF-8", na.strings = "N/A",stringsAsFactors = FALSE)
dat_processors<-read.csv("reviews_processors.csv",encoding = "UTF-8", na.strings = "N/A",stringsAsFactors = FALSE)
dat_consoles<-read.csv("reviews_consoles.csv",encoding = "UTF-8", na.strings = "N/A",stringsAsFactors = FALSE)
dat_microphones<-read.csv("reviews_microphones.csv",encoding = "UTF-8", na.strings = "N/A",stringsAsFactors = FALSE)
dat_hemmabio<-read.csv("reviews_hemmabio.csv",encoding = "UTF-8", na.strings = "N/A",stringsAsFactors = FALSE)
dat_smartwatch<-read.csv("reviews_smartwatch.csv",encoding = "UTF-8", na.strings = "N/A",stringsAsFactors = FALSE)
dat_activityband<-read.csv("reviews_activityband.csv",encoding = "UTF-8", na.strings = "N/A",stringsAsFactors = FALSE)
dat_pulsewatches<-read.csv("reviews_pulsewatches.csv",encoding = "UTF-8", na.strings = "N/A",stringsAsFactors = FALSE)

setwd("..")


#########################################
#OMIT NA

omit_missing<-function(df){
    print("rows before omit:")
    before<-nrow(df)
    print(before)
    df<-na.omit(df)
    print("rows after omit:")
    after<-nrow(df)
    print(after)
    print("diff:")
    print(before-after)
    return(df)
}

#nrow(dat)

dat_monitors<-omit_missing(dat_monitors)
dat_tablets<-omit_missing(dat_tablets)
dat_routers<-omit_missing(dat_routers)
dat_processors<-omit_missing(dat_processors)
dat_consoles<-omit_missing(dat_consoles)
dat_microphones<-omit_missing(dat_microphones)
dat_hemmabio<-omit_missing(dat_hemmabio)
dat_smartwatch<-omit_missing(dat_smartwatch)
dat_activityband<-omit_missing(dat_activityband)
dat_pulsewatches<-omit_missing(dat_pulsewatches)
dat<-omit_missing(dat)



dat_TV<-na.omit(dat_TV)
dat_headphones<-na.omit(dat_headphones)


nrow(dat_TV)
nrow(dat_headphones)


summary(dat)
typeof(dat$rating)

#########################################
#DESCRIPTIVE STATS BEFORE CONVERTING TO FACTOR

sm<-as.data.frame.character(summary(dat$rating, digits=2))
sm<-t(sm)
#t() = transposes
# as.data.frame.character() = convert char to data frame
actband<-t(as.data.frame.character(summary(dat_activityband$rating, digits=2)))
consoles<-t(as.data.frame.character(summary(dat_consoles$rating, digits=2)))
headphones<-t(as.data.frame.character(summary(dat_headphones$rating, digits=2)))
hemmabio<-t(as.data.frame.character(summary(dat_hemmabio$rating, digits=2)))
#summary(dat_laptops$rating)
monitors<-t(as.data.frame.character(summary(dat_monitors$rating, digits=2)))
routers<-t(as.data.frame.character(summary(dat_routers$rating, digits=2)))
smwatch<-t(as.data.frame.character(summary(dat_smartwatch$rating, digits=2)))
tablets<-t(as.data.frame.character(summary(dat_tablets$rating, digits=2)))
tv<-t(as.data.frame.character(summary(dat_TV$rating, digits=2)))
pulsew<-t(as.data.frame.character(summary(dat_pulsewatches$rating, digits=2)))
str(pulsew)
pulsew


# in rbind the columns need to have the same name
all_descr<-rbind(sm, actband, consoles, headphones, hemmabio, monitors, routers, smwatch, tablets, tv, pulsew) 
all_descr
all_descr[,c("Median", "Mean")]

xtable(all_descr[,c("Median", "Mean")])


#########################################
# CONVERT TO FACTOR
# 
# dat$rating<-factor(dat$rating) #factor makes the numbers sortable
# dat_TV$rating<-factor(dat_TV$rating)
# dat_headphones$rating<-factor(dat_headphones$rating) #factor makes the numbers sortable
# dat_monitors$rating<-factor(dat_monitors$rating)
# dat_tablets$rating<-factor(dat_tablets$rating)
# dat_routers$rating<-factor(dat_routers$rating)
# dat_processors$rating<-factor(dat_processors$rating)
# dat_consoles$rating<-factor(dat_consoles$rating)
# dat_hemmabio$rating<-factor(dat_hemmabio$rating)
# dat_smartwatch$rating<-factor(dat_smartwatch$rating)
# dat_activityband$rating<-factor(dat_activityband$rating)
# dat_pulsewatches$rating<-factor(dat_pulsewatches$rating)



?ggplot2

plot_nice_histogram<-function(input_data, title_name ){
    output<-ggplot(data=input_data, aes(x=rating)) + 
        geom_bar() +
        labs(
             title= title_name,
             subtitle= paste("n =", nrow(input_data)),
             x= "Rating",
             y="Count"
        ) + 
        theme_minimal() + 
        theme(
              text = element_text(size=14),
              axis.text.x = element_text(size=14),
              axis.text.y = element_text(size=14),
              plot.subtitle = element_text(hjust = 0.5),
              plot.title = element_text(hjust = 0.5)
              ) #+
        #ylim(0,260)
    
    return(output)
}

phone_plot<-plot_nice_histogram(dat, "Smartphones")
tv_plot<-plot_nice_histogram(dat_TV, "TV:s")
hp_plot<-plot_nice_histogram(dat_headphones, "Headphones")
monitor_plot<-plot_nice_histogram(dat_monitors, "Monitors")
tablets_plot<-plot_nice_histogram(dat_tablets, "Tablets")
routers_plot<-plot_nice_histogram(dat_routers, "Routers")
processors_plot<-plot_nice_histogram(dat_processors, "Processors") # kanske inte så bra att inludera, vi får se.
consoles_plot<-plot_nice_histogram(dat_consoles, "Consoles")
hemmabio_plot<-plot_nice_histogram(dat_hemmabio, "Home Cinema")
smartwatch_plot<-plot_nice_histogram(dat_smartwatch, "Smartwatches") # "wearables" 
activityband_plot<-plot_nice_histogram(dat_activityband, "Activity bands")
pulsew_plot<-plot_nice_histogram(dat_pulsewatches, "Pulse Watches")

grid.arrange(hp_plot, monitor_plot, tv_plot,
             phone_plot, tablets_plot, routers_plot,
             processors_plot, consoles_plot, hemmabio_plot, 
             smartwatch_plot, activityband_plot, pulsew_plot, nrow=4, ncol=3)

str(dat_headphones$rating)

total_reviews <- rbind(dat, dat_activityband, dat_consoles, dat_headphones, dat_hemmabio, dat_monitors, dat_processors, dat_pulsewatches, dat_routers, dat_smartwatch, dat_tablets, dat_TV)

?summary
tot<-t(as.data.frame.character(summary(total_reviews$rating, digits=3)))
tot
str(tot)
tot[, c("Median", "Mean")]
xtable(tot[, c("Median", "Mean")])

kurtosis(total_reviews$rating)
skewness(total_reviews$rating)

log(10)
log(2)
log(5)
#total_reviews$rating <- numeric(total_reviews$rating)
typeof(total_reviews$rating)


#plot_nice_histogram(total_reviews, "Total reviews")
# custom plot for total 
ggplot(data=total_reviews, aes(x=rating)) + 
    geom_bar() +
    labs(
        title= "Total reviews",
        subtitle= paste("n =", nrow(total_reviews)),
        x= "Rating",
        y="Count"
    ) + 
    theme_minimal() +
    theme(
        text = element_text(size=16),
        axis.text.x = element_text(size=14),
        axis.text.y = element_text(size=14),
        plot.subtitle = element_text(hjust = 0.5),
        plot.title = element_text(hjust = 0.5)
    ) #+
#ylim(0,260)
#hh<-"hej ehj rej"
#str_match(hh, "[:space:]+")
library(tidyverse)

total_reviews %>%
    ggplot(aes(x=log(rating))) +
    geom_bar()

#str_detect(product_review, "[:space:]")
#total_reviews$product_review[562]

plot(density(total_reviews$rating))

# REMOVING EMPTY AND WHITESPACE REVIEWS, before=4738, after=4664
total_reviews<-subset(total_reviews, product_review!="" & product_review!=str_match(product_review, "[:space:]+") )

numm<-as.numeric(total_reviews$rating)
plot(density(numm))

ggplot(total_reviews, aes(x=rating)) + geom_density()

ggplot(total_reviews, aes(rating)) +
    geom_density(adjust = 2)
####################
ggplot(data=total_reviews, aes(x=rating, y=..density..)) +  
    stat_density(alpha = 0.5, fill = "#FF6666") 



aa<-log(numm)
plot(x=aa)
#colnames(total_reviews)<-c("comment_id","date_published","link_prev_num_reviews","prev_num_reviews","product_review","rating","user")

xy.coords(y = as.numeric(total_reviews$rating))
total_reviews$comment_id
total_reviews$product_review[total_reviews$comment_id==1159490]
total_reviews$product_review[total_reviews$comment_id==1180615] 
total_reviews$product_review[total_reviews$comment_id==1171624]
total_reviews$product_review[total_reviews$comment_id==1155791]

#write.csv(x = total_reviews, file = "total_reviews.csv", fileEncoding = "UTF-8")
