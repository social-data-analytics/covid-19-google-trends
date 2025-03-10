library(ggplot2)
T <- nrow(covid_case_agg)
# 
# lasso_list <- list()
# arima_list <- list()
predicted_df_null <- readRDS(paste0("result/predicted_df_null_p=",p,"_VAR_LONG_COVID.RDS"))
predicted_df <- readRDS(paste0("result/predicted_df_p=",p,"_VAR_LONG_COVID.RDS"))


lasso_df <- array(dim=c(T,n_ahead))
arima_df <- array(dim=c(T,n_ahead))
lasso_cum_df <- array(dim=c(T,n_ahead))
arima_cum_df <- array(dim=c(T,n_ahead))
for(t in p:T){
  #Lasso
  Z_lasso_pred <- c(diag(as.matrix(predicted_df[(t+1):(t+n_ahead),1:n_ahead])))
  Y_lasso_pred <- c()
  Y_lasso_pred[1] <- (Z_lasso_pred[1] + sqrt(store_count[t]))^2
  for(tau in 2:n_ahead){
    Y_lasso_pred[tau] <- (Z_lasso_pred[tau] + sqrt(Y_lasso_pred[tau-1]))^2
  }
  lasso_df[t,] <- Y_lasso_pred
  lasso_cum_df[t,] <- sum(store_count[1:(t-1)])+cumsum(Y_lasso_pred)
  #Arima
  Z_arima_pred <- c(diag(as.matrix(predicted_df_null[(t+1):(t+n_ahead),1:n_ahead])))
  Y_arima_pred <- c()
  Y_arima_pred[1] <- (Z_arima_pred[1] + sqrt(store_count[t]))^2
  for(tau in 2:n_ahead){
    Y_arima_pred[tau] <- (Z_arima_pred[tau] + sqrt(Y_arima_pred[tau-1]))^2
  }
  arima_df[t,] <- Y_arima_pred
  arima_cum_df[t,] <- sum(store_count[1:(t-1)])+cumsum(Y_arima_pred)
  print(t)
}

# plot(arima_df[,1],type="l",col="blue")
# lines(store_count,col="black")
# lines(lasso_df[,1],col="orange")

#RMSE
RMSE_df <- data.frame(array(dim=c(n_ahead,2)))
colnames(RMSE_df) <- c("LASSO","ARMA")

MAPE_df <- data.frame(array(dim=c(n_ahead,2)))
colnames(MAPE_df) <- c("LASSO","ARMA")

for(h in 1:n_ahead){
  RMSE_df[h,"ARMA"] <- sqrt(mean((arima_df[,h]-store_count)^2,na.rm=TRUE)) 
  RMSE_df[h,"LASSO"] <- sqrt(mean((lasso_df[,h]-store_count)^2,na.rm=TRUE)) 
  
  MAPE_df[h,"ARMA"] <- mean(abs((arima_df[,h]-store_count)/store_count),na.rm=TRUE)
  MAPE_df[h,"LASSO"] <- mean(abs((lasso_df[,h]-store_count)/store_count),na.rm=TRUE)
  
}

range(arima_df,na.rm=TRUE)



#Get a cumulative version?
# plot(arima_cum_df[,1],type="l",col="blue")
# lines(cumsum(store_count),col="black")
# lines(lasso_cum_df[,1],col="orange")
# 
# plot(arima_cum_df[,7],type="l",col="blue")
# lines(cumsum(store_count),col="black")
# lines(lasso_cum_df[,7],col="orange")
h<- 1

for(h in c(1,7,14,21)){
# plot(store_count[(p+1):T],col="black",type="l",
#      ylim=range(store_count[(p+1):T],lasso_df[(p+1):T,h],arima_df[(p+1):T,h]))
# lines((lasso_df[(p+1):T,h]),col="orange")
# lines((arima_df[(p+1):T,h]),type="l",col="blue",lty="dashed")

temp_df <- data.frame(Date=rep(MSV$date[(p+2):(T+1)],3),
  values=c(store_count[(p+1):T],lasso_df[(p+1):T,h],arima_df[(p+1):T,h]),
  type =rep(c("True value","Lasso-VAR","ARIMA(p,d,q)"),each=T-p)
  )
temp_df$Date <- as.Date(temp_df$Date)

ggplot(temp_df,aes(x=Date,y=values,color=type)) + geom_line()  +
  theme_light()+ theme(legend.title=element_blank(),legend.key.size=unit(3,"lines"),
                       text = element_text(size = 35),legend.spacing.x = unit(1,"cm")) + ylab("MSV") +
  scale_x_date(breaks=as.Date(c("2020-07-01","2021-07-01","2022-07-01","2023-07-01")),minor_breaks = NULL,
               limits=c(as.Date("2020-06-20"),as.Date("2024-01-01"))) + 
  ylim(c(0,20000)) + scale_color_manual(values=c( "#9999CC" , "#CC3333", "#88AA11"))+ guides(color = guide_legend(override.aes = list(size = 20)))


ggsave(paste0("result/prediction ",h,".jpg"),width=18,height=10)
}
range(store_count)

# plot(store_count,type="l")

