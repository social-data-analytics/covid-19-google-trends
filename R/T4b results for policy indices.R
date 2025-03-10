setwd(dirname(rstudioapi::getSourceEditorContext()$path))

temp_rds <- readRDS("all_pvalues.rds")
H1_pvalue_tGCL <- temp_rds[[1]]
H2_pvalue_tGCL <- temp_rds[[2]]
H3_pvalue_tGCL <- temp_rds[[3]]
H4_pvalue_tGCL <- temp_rds[[4]]
H1_pvalue_AIC <- temp_rds[[5]]
H2_pvalue_AIC <- temp_rds[[6]]
H3_pvalue_AIC <- temp_rds[[7]]
H4_pvalue_AIC <- temp_rds[[8]]
H1_pvalue_BIC <- temp_rds[[9]]
H2_pvalue_BIC <- temp_rds[[10]]
H3_pvalue_BIC <- temp_rds[[11]]
H4_pvalue_BIC <- temp_rds[[12]]
H1_pvalue_HQC <- temp_rds[[13]]
H2_pvalue_HQC <- temp_rds[[14]]
H3_pvalue_HQC <- temp_rds[[15]]
H4_pvalue_HQC <- temp_rds[[16]]





#1. For each test, determine the best p

H1_best_lag <- array(dim=c(20,4))
H2_best_lag <- array(dim=c(20,4))
H3_best_lag <- array(dim=c(20,4))
H4_best_lag <- array(dim=c(20,4))
rownames(H1_best_lag) <- RT_no_long_covid
rownames(H2_best_lag) <- RT_no_long_covid
rownames(H3_best_lag) <- RT_no_long_covid
rownames(H4_best_lag) <- RT_no_long_covid


for(ind in 1:4){
  for(symi in 1:20){

    
    H1_best_lag[symi,ind] <- which.min(sapply(H1_pvalue_BIC[1:60],function(x) x[symi,ind]))
    H2_best_lag[symi,ind] <- which.min(sapply(H2_pvalue_BIC[1:60],function(x) x[symi,ind]))
    H3_best_lag[symi,ind] <- which.min(sapply(H3_pvalue_BIC[1:60],function(x) x[symi,ind]))
    H4_best_lag[symi,ind] <- which.min(sapply(H4_pvalue_BIC[1:60],function(x) x[symi,ind]))
    

  }
}

H1_pvalue_best <- array(dim=c(20,4))
H2_pvalue_best <- array(dim=c(20,4))
H3_pvalue_best <- array(dim=c(20,4))
H4_pvalue_best <- array(dim=c(20,4))

rownames(H1_pvalue_best) <- RT_no_long_covid
rownames(H2_pvalue_best) <- RT_no_long_covid
rownames(H3_pvalue_best) <- RT_no_long_covid
rownames(H4_pvalue_best) <- RT_no_long_covid

CF_name_for_table <- c("Local communication policies","Non-pharmacological interventions",
                       "Health system policies","Vaccine policies")
colnames(H1_pvalue_best) <- CF_name_for_table
colnames(H2_pvalue_best) <- CF_name_for_table
colnames(H3_pvalue_best) <- CF_name_for_table
colnames(H4_pvalue_best) <- CF_name_for_table


for(ind in 1:4){
  for(symi in 1:20){
    
    H1_pvalue_best[symi,ind] <- H1_pvalue_tGCL[[H1_best_lag[symi,ind]]][symi,ind]
    H2_pvalue_best[symi,ind] <- H2_pvalue_tGCL[[H2_best_lag[symi,ind]]][symi,ind]
    H3_pvalue_best[symi,ind] <- H3_pvalue_tGCL[[H3_best_lag[symi,ind]]][symi,ind]
    H4_pvalue_best[symi,ind] <- H4_pvalue_tGCL[[H4_best_lag[symi,ind]]][symi,ind]
  
  }
}


H1_sig <- H1_pvalue_best < 0.05
H2_sig <- H2_pvalue_best < 0.05
H3_sig <- H3_pvalue_best < 0.05
H4_sig <- H4_pvalue_best < 0.05

colSums(H1_sig)/nrow(H1_sig)
colSums(H2_sig)/nrow(H2_sig)

#Reject H1, Cannot reject H3 => confounders

confounding_sym_GC_LC <- H1_sig & !H3_sig
confounding_LC_GC_sym <- H2_sig & !H4_sig

colSums(confounding_sym_GC_LC)/nrow(confounding_sym_GC_LC)
colSums(confounding_LC_GC_sym)/nrow(confounding_LC_GC_sym)

ifelse(confounding_sym_GC_LC,"C","")
ifelse(confounding_LC_GC_sym,"C","")

write.csv(ifelse(H1_sig,"G",""),"result/H1_sig.csv")
write.csv(ifelse(H2_sig,"G",""),"result/H2_sig.csv")

write.csv(ifelse(confounding_sym_GC_LC,"C",""),"result/confounding_sym_GC_LC.csv")
write.csv(ifelse(confounding_LC_GC_sym,"C",""),"result/confounding_LC_GC_sym.csv")


#Visaulize some confounding variables

OxCGRT_no_difference <- aggregate(OxCGRT_sub[,2:5],by=list(Date=OxCGRT_sub$Date),FUN=mean)
OxCGRT_no_difference$Date <- as.Date(as.character(OxCGRT_no_difference$Date),format="%Y%m%d")
date_vec <- OxCGRT_no_difference$Date
n_day <- nrow(OxCGRT_no_difference)

plot_df <- cbind(MSV[1:n_day,],OxCGRT_no_difference)
plot_df <- plot_df[,colnames(plot_df)!="Date"]
# sum(plot_df$date != plot_df$Date)
plot_df <- melt(plot_df,id.vars="date")
levels(plot_df$variable)[22:25] <- CF_name_for_table
levels(plot_df$variable)[1:21] <- gsub("\\."," ",levels(plot_df$variable)[1:21])

plot_df$value <- ave(plot_df$value,plot_df$variable,FUN=function(x) x/max(x)    )



library(dplyr)
library(ggrepel)
library(RColorBrewer)

levels(plot_df$variable)[levels(plot_df$variable)=="Long Covid"] <- "Long COVID"

#(I) symptom GC Long COVID
#1. Clouding.of.consciousness: (b)(d)

pal <- brewer.pal(6, "Set2")
pal[6] <-brewer.pal(9, "Set1")[1]


temp_level <- c("Clouding of consciousness",
                "Non-pharmacological interventions",
                "Vaccine policies",
                "Long COVID"
)

plot_df_copy <- plot_df[plot_df$variable %in% temp_level,]
plot_df_copy$variable <- factor(plot_df_copy$variable,levels=temp_level)


plot_df_copy %>%
  mutate(label = if_else(date == max(date), as.character(variable), NA_character_)) %>%
  ggplot(aes(x=date,y=value,color=variable,linetype=variable)) + geom_line() + 
  scale_color_manual(values=c(pal,pal))  +
  geom_label_repel(size = 8,aes(label = label),
                   nudge_x = 150,arrow = arrow(length = unit(0.015, "npc")),
                   na.rm = TRUE)+ theme_light() + theme(legend.position="none",text = element_text(size = 25)) +
  ylab("Normalized value") + xlab("Date") + 
  scale_x_date(breaks=as.Date(c("2020-01-01","2021-01-01","2022-01-01","2023-01-01")),minor_breaks = NULL,
                     limits=c(as.Date("2020-01-01"),as.Date("2024-06-30")))
ggsave("result/Clouding of consciousness CF.png",units="cm",width=40,height=18)





#2,3. Lightheadedness, Chest pain : All

temp_level <- c("Lightheadedness",
                                                "Non-pharmacological interventions",
                                                "Vaccine policies",
                                                "Long COVID",
                                                "Health system policies",
                                                "Local communication policies"
)
plot_df_copy <- plot_df[plot_df$variable %in% temp_level,]
plot_df_copy$variable <- factor(plot_df_copy$variable,levels=temp_level)

plot_df_copy %>%
  mutate(label = if_else(date == max(date), as.character(variable), NA_character_)) %>%
  ggplot(aes(x=date,y=value,color=variable,linetype=variable)) + geom_line() + 
  scale_color_manual(values=c(pal,pal))  +
  geom_label_repel(size = 8,aes(label = label),
                   nudge_x = 150,arrow = arrow(length = unit(0.015, "npc")),
                   na.rm = TRUE)+ theme_light() + theme(legend.position="none",text = element_text(size = 25)) +
  ylab("Normalized value") + xlab("Date") + 
  scale_x_date(breaks=as.Date(c("2020-01-01","2021-01-01","2022-01-01","2023-01-01")),minor_breaks = NULL,
               limits=c(as.Date("2020-01-01"),as.Date("2024-06-30")))
ggsave("result/Lightheadedness CF.png",units="cm",width=40,height=18)

temp_level <- c("Chest pain",
                "Non-pharmacological interventions",
                "Vaccine policies",
                "Long COVID",
                "Health system policies",
                "Local communication policies"
)
plot_df_copy <- plot_df[plot_df$variable %in% temp_level,]
plot_df_copy$variable <- factor(plot_df_copy$variable,levels=temp_level)


plot_df_copy %>%
  mutate(label = if_else(date == max(date), as.character(variable), NA_character_)) %>%
  ggplot(aes(x=date,y=value,color=variable,linetype=variable)) + geom_line() + 
  scale_color_manual(values=c(pal,pal))  +
  geom_label_repel(size = 8,aes(label = label),
                   nudge_x = 150,arrow = arrow(length = unit(0.015, "npc")),
                   na.rm = TRUE)+ theme_light() + theme(legend.position="none",text = element_text(size = 25)) +
  ylab("Normalized value") + xlab("Date") + 
  scale_x_date(breaks=as.Date(c("2020-01-01","2021-01-01","2022-01-01","2023-01-01")),minor_breaks = NULL,
               limits=c(as.Date("2020-01-01"),as.Date("2024-06-30")))
ggsave("result/Chest pain CF.png",units="cm",width=40,height=18)


#4. Ageusia: (b)(c)(d)
temp_level <- c("Ageusia",
                "Non-pharmacological interventions",
                "Vaccine policies",
                "Long COVID",
                "Health system policies"
)
plot_df_copy <- plot_df[plot_df$variable %in% temp_level,]
plot_df_copy$variable <- factor(plot_df_copy$variable,levels=temp_level)


plot_df_copy %>%
  mutate(label = if_else(date == max(date), as.character(variable), NA_character_)) %>%
  ggplot(aes(x=date,y=value,color=variable,linetype=variable)) + geom_line() + 
  scale_color_manual(values=c(pal,pal))  +
  geom_label_repel(size = 8,aes(label = label),
                   nudge_x = 150,arrow = arrow(length = unit(0.015, "npc")),
                   na.rm = TRUE)+ theme_light() + theme(legend.position="none",text = element_text(size = 25)) +
  ylab("Normalized value") + xlab("Date") + 
  scale_x_date(breaks=as.Date(c("2020-01-01","2021-01-01","2022-01-01","2023-01-01")),minor_breaks = NULL,
               limits=c(as.Date("2020-01-01"),as.Date("2024-06-30")))
ggsave("result/Ageusia CF.png",units="cm",width=40,height=18)




#5. Hypochondriasis: (a)
temp_level <- c("Hypochondriasis",
                "Long COVID",
                "Local communication policies"
)
plot_df_copy <- plot_df[plot_df$variable %in% temp_level,]
plot_df_copy$variable <- factor(plot_df_copy$variable,levels=temp_level)


plot_df_copy %>%
  mutate(label = if_else(date == max(date), as.character(variable), NA_character_)) %>%
  ggplot(aes(x=date,y=value,color=variable,linetype=variable)) + geom_line() + 
  scale_color_manual(values=c(pal[c(1,4,6)],pal[c(1,4,6)]))  +
  geom_label_repel(size = 8,aes(label = label),
                   nudge_x = 150,arrow = arrow(length = unit(0.015, "npc")),
                   na.rm = TRUE,direction  = "both")+ theme_light() + theme(legend.position="none",text = element_text(size = 25)) +
  ylab("Normalized value") + xlab("Date") + 
  scale_x_date(breaks=as.Date(c("2020-01-01","2021-01-01","2022-01-01","2023-01-01")),minor_breaks = NULL,
               limits=c(as.Date("2020-01-01"),as.Date("2024-06-30")))
ggsave("result/Hypochondriasis CF.png",units="cm",width=40,height=18)




