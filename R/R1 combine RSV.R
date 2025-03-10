library('stringr')
setwd(dirname(rstudioapi::getSourceEditorContext()$path))
keyword_vec <- c("Long%20COVID",
                 "Clouding%20of%20consciousness",
                 "Fatigue",
                 "Myalgia",
                 "Chest%20pain",
                 "Mental%20health",
                 "Anxiety",
                 "Hypochondriasis",
                 "Lightheadedness",
                 "Hip%20pain",
                 "Aching%20Muscle%20Pain",
                 "Insomnia",
                 "Palpitations",
                 "Shortness%20of%20breath",
                 "Dizziness",
                 "Headache",
                 "Ageusia",
                 "Chest%20Tightness",
                 "Major%20depressive disorder",
                 "Sleep%20disorder",
                 "Anosmia"
)

keyword_vec <- str_replace_all(keyword_vec,"%20"," ")

start_day_vec <- seq(from=as.POSIXct("2020-01-01"), by=as.difftime(89, units="days"), to=as.POSIXct("2023-12-31"))
end_day_vec <- start_day_vec + as.difftime(88, units="days")
end_day_vec[length(end_day_vec)] <- as.POSIXct("2023-12-31")
n_day <- length(start_day_vec)
n_keyword <- length(keyword_vec)

n_rep <- 10

RSV_list <- list()


for(k in 1:n_keyword){
  RSV_list[[k]] <- data.frame(array(dim=c(0,n_rep)))
    for(t in 1:n_day){
      for(r in 1:n_rep){
        temp_csv <- read.csv(paste0("RSV\\window ",r,"\\RSV_kw_",k,"_t_",t,"_rep_",r,".csv"))
        if(nrow(temp_csv)>=2 & !is.null(nrow(temp_csv)) ){
        temp_csv <- temp_csv[2:90,,drop=FALSE]
        temp_csv[,1][temp_csv[,1]=="<1"] <- 0
        temp_csv[,1] <- as.numeric(temp_csv[,1])
        colnames(temp_csv) <- paste0("r",r)
        }else{
          temp_csv <- data.frame(rep(0,89))
          colnames(temp_csv) <- paste0("r",r)
        }
        if(r==1){
          master_read <- temp_csv 
        }else{
          master_read <- cbind(master_read,temp_csv)
        }
      }
      if(t==1){
        RSV_list[[k]] <- master_read
      }else{
        RSV_list[[k]] <- rbind(RSV_list[[k]],master_read)
      }
      print(paste0("k=",k,"; t=",t))
    }
}

#Remove extra rows and calculate correlations
IC_df <- data.frame(array(dim=c(n_rep*(n_rep-1)/2,n_keyword)))

for(k in 1:n_keyword){
  RSV_list[[k]] <- RSV_list[[k]][complete.cases(RSV_list[[k]]),]
  temp_cor <- cor(RSV_list[[k]])
  IC_df[,k] <- temp_cor[upper.tri(temp_cor)]
}

colnames(IC_df) <- keyword_vec

names(RSV_list) <- keyword_vec

# RSV_list[["Aching Muscle Pain"]]
# 
# RSV_list[["Clouding of consciousness"]]



library(reshape2)
IC_df$t <- 1:nrow(IC_df)
IC_df_melt <- melt(IC_df,id.vars="t")


keyword_vec <- c("Long%20COVID",
                 "Clouding%20of%20consciousness",
                 "Fatigue",
                 "Myalgia",
                 "Chest%20pain",
                 "Mental%20health",
                 "Anxiety",
                 "Hypochondriasis",
                 "Lightheadedness",
                 "Hip%20pain",
                 "Aching%20muscle%20pain",
                 "Insomnia",
                 "Palpitations",
                 "Shortness%20of%20breath",
                 "Dizziness",
                 "Headache",
                 "Ageusia",
                 "Chest%20Tightness",
                 "Major%20depressive disorder",
                 "Sleep%20disorder",
                 "Anosmia"
)


levels(IC_df_melt$variable)[levels(IC_df_melt$variable)=="Aching Muscle Pain"] <- "Aching muscle pain"
levels(IC_df_melt$variable)[levels(IC_df_melt$variable)=="Chest Tightness"] <- "Chest tightness"

IC_df_melt$variable <- factor(IC_df_melt$variable,levels=levels(IC_df_melt$variable)[order(levels(IC_df_melt$variable))])

library(ggplot2) 
ggplot(IC_df_melt,aes(x=variable,y=value)) + geom_boxplot()+ theme_light()+ 
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)) +
  xlab("Related topic") + ylab("Intra-correlation residual")

ggsave("boxplots.jpg",width=25,height=20,units="cm")

#Time series for the three
keyword_vec

for(i in c(2,8,11)){

  jpeg(paste0(keyword_vec[i],".jpg"),width=2000,height=1000)
  par(mfrow=c(5,2),mar=c(2,3,2,2),cex=2)
  for(r in 1:(n_rep)){
    plot(RSV_list[[i]][,r],type="l",xlab="",ylab="",yaxt="n")
    axis(2, at = c(0,50,100), las=2)
  }
  dev.off()
}


