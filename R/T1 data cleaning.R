setwd(dirname(rstudioapi::getSourceEditorContext()$path))
MSV <- read.csv("data/joined_msvs.csv")
MSV$date <- as.Date(MSV$date,"%d/%m/%Y")
RT <- colnames(MSV)[-c(1)]
RT_no_long_covid <- RT[RT!="Long.Covid"]




plot(MSV$date,MSV$Aching.Muscle.Pain)

library(tseries)
library(forecast)

diff_order <- c()
p_values <- c()
MSV_stationary <- MSV

for(RT_i in RT){
  #Start for loop
  temp_ts <- ts(MSV[,RT_i])
  temp_adf <- adf.test(temp_ts)
  diff_order[RT_i] <- 0
  while(temp_adf$p.value > 0.05){
    diff_order[RT_i] <- diff_order[RT_i] + 1
    temp_ts <- diff(temp_ts)
    temp_adf <- adf.test(temp_ts)
  }
  p_values[RT_i] <- temp_adf$p.value
  MSV_stationary[,RT_i] <- NA
  MSV_stationary[(diff_order[RT_i]+1):nrow(MSV_stationary),RT_i] <- temp_ts
}
