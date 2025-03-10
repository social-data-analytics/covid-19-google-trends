setwd(dirname(rstudioapi::getSourceEditorContext()$path))
library(dplyr)
num_non_zero_para <- c()
num_non_zero_para_Y1 <- c()
symptoms_name <- colnames(temp_window_df)
symptoms_name <- symptoms_name[symptoms_name!="Long.Covid"]
symptoms_name <- gsub("\\."," ",symptoms_name)


para_count_df <- data.frame(array(dim=c(nrow(covid_case_agg),length(symptoms_name))))
rownames(para_count_df) <- rownames(covid_case_agg)
colnames(para_count_df) <- symptoms_name

for(t in 180:nrow(covid_case_agg)){
  temp_model <- readRDS(paste0("fitted model/LASSO day Long COVID ",t," p 180,.rds")) 
  temp_para <- coef(temp_model)
  num_non_zero_para[t-180+1] <- sum(temp_para[,-1]!=0)
  # temp_para[,-1][temp_para[,-1]!=0]
  
  temp_para_Y1 <- temp_para[21,-1]
  num_non_zero_para_Y1[t-180+1] <- sum(temp_para_Y1!=0)
  
  #Check which symptoms contained in temp_para_Y1?
  for(i in 1:20){
    para_count_df[t,i+1] <- sum( temp_para_Y1 %>% dplyr::select(contains(paste0("Y",i))) !=0)
  }
  print(t)
}

para_count_df <- para_count_df[180:nrow(covid_case_agg),]

par(mfrow=c(5,4))
for(i in 1:20){
  plot(para_count_df[,i],main=colnames(para_count_df)[i])
}

par(mfrow=c(1,1))
plot(num_non_zero_para_Y1)
plot(num_non_zero_para)

par(mfrow=c(1,1))
heatmap_df <- data.frame(array(dim=c(nrow(para_count_df),length(symptoms_name))))
rownames(heatmap_df) <- as.Date(rownames(para_count_df))
colnames(heatmap_df) <- colnames(para_count_df)

heatmap_df$Date <- as.Date(rownames(para_count_df))

for(i in 1:20){
  heatmap_df[,i+1] <- ifelse(para_count_df[,i+1]>0,1,0)
}

heatmap_df_melt <- melt(heatmap_df,id.vars="Date")
# levels(heatmap_df_melt$variable) <- gsub("."," ",levels(heatmap_df_melt$variable))
# str_replace_all(levels(heatmap_df_melt$variable),"."," ")
library(ggplot2)
library(scales)
heatmap_df_melt <- heatmap_df_melt[heatmap_df_melt$variable!="Long Covid",]
temp_levels <- unique(as.character(heatmap_df_melt$variable))
temp_levels <- temp_levels[rev(order(temp_levels))]
heatmap_df_melt$variable <- factor(heatmap_df_melt$variable,levels=temp_levels)
heatmap_df_melt <- heatmap_df_melt[heatmap_df_melt$variable!="date",]

levels(heatmap_df_melt$variable)[levels(heatmap_df_melt$variable)=="Aching Muscle Pain"] <- "Aching muscle pain"
levels(heatmap_df_melt$variable)[levels(heatmap_df_melt$variable)=="Chest Tightness"] <- "Chest tightness"

ggplot(heatmap_df_melt,aes(x=Date,y=variable,fill=value)) + geom_tile() +
  scale_fill_gradient(low = "white", high = "black") + theme_light() + 
  geom_hline(yintercept = 0.5 + 1:19, colour = "grey", size = 1) + 
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank()) +
  ylab("Related topic") + scale_x_date(breaks="6 months",labels = date_format("%m/%Y"))

ggsave("result/heatmap.png",units="cm",width=22,height=15)
max(heatmap_df_melt$Date)
plot(heatmap_df$Fatigue)

para_count_df$Fatigue
