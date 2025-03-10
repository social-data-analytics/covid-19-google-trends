library(dplyr)

covid_case_agg <- MSV
colnames(covid_case_agg)
covid_case_agg <- covid_case_agg %>% relocate(Long.Covid, .after = last_col())
store_count <- covid_case_agg$Long.Covid
covid_case_agg[2:nrow(covid_case_agg),2:ncol(covid_case_agg)] <- 
  sqrt(covid_case_agg[2:nrow(covid_case_agg),2:ncol(covid_case_agg)])-sqrt(covid_case_agg[2:nrow(covid_case_agg)-1,2:ncol(covid_case_agg)])
covid_case_agg <- covid_case_agg[-1,]
rownames(covid_case_agg) <- covid_case_agg$date
covid_case_agg <- covid_case_agg[,-1]

n_ahead <- 21
predicted_df_null <- data.frame(array(dim=c(nrow(covid_case_agg),n_ahead)))
predicted_df <- data.frame(array(dim=c(nrow(covid_case_agg),n_ahead)))
p <- 180
# l <- 10
max_lag <- 10
#create lagged columns

library(car)
library(vars)
library(BigVAR)
library(forecast)
for(t in p:nrow(covid_case_agg)){
  temp_window_df <- covid_case_agg[(t-p+1):t,]
  start_day <- as.Date(rownames(temp_window_df)[1])
  end_day <- as.Date(rownames(temp_window_df)[ncol(temp_window_df)])
  #Without predictors
  fit_null <- auto.arima(temp_window_df$Long.Covid,ic="aic",max.order=max_lag)
  saveRDS(fit_null,paste0("fitted model/null day Long COVID ",t," p ",p,",.rds"))
  
  null_pred_raw <- predict(fit_null,n.ahead=n_ahead,interval="prediction")
  null_pred <- cumsum(null_pred_raw$pred)
  
  
  #With predictors
  mod1 <- constructModel(as.matrix(temp_window_df),
                         p=max_lag,gran=c(50,10),struct="Basic",
                         cv="Rolling",IC=TRUE,loss = "L1",h=n_ahead)
  fit = cv.BigVAR(mod1)
  saveRDS(fit,paste0("fitted model/LASSO day Long COVID ",t," p ",p,",.rds"))

  for(l in 1:n_ahead){
    predicted_df_null[t+l,l] <- null_pred[l]
    predicted_df[t+l,l] <- predict(fit,n.ahead=l)[21,]
  }
      print(t)
}

saveRDS(predicted_df_null,paste0("result/predicted_df_null_p=",p,"_VAR_LONG_COVID.RDS"))
saveRDS(predicted_df,paste0("result/predicted_df_p=",p,"_VAR_LONG_COVID.RDS"))


