library(readxl)
OxCGRT <- read.csv("data/OxCGRT_compact_national_v1.csv")

par(mfrow=c(1,1))
hist(OxCGRT$EconomicSupportIndex)

table(
100*((OxCGRT$E1_Income.support-0.5*(1-OxCGRT$E1_Flag))/2+(OxCGRT$E2_Debt.contract.relief)/2)/2 - OxCGRT$EconomicSupportIndex
)


# table(OxCGRT$E1_Income.support)
Fj <- c(1,1,1,1,1,1,1,0,1,0,1,0,0,1,1,1)
names(Fj) <- c("C1","C2","C3","C4","C5","C6","C7","C8","E1","E2","H1","H2","H3","H6","H7","H8")

Nj <- c(3,3,2,4,2,3,2,4,2,2,2,3,2,4,5,3)
names(Nj) <- names(Fj)

local_communication_policies_index <- 100*ifelse(!is.na(OxCGRT$H1_Flag),(OxCGRT$H1_Public.information.campaigns - 0.5*(Fj["H1"]-OxCGRT$H1_Flag))/Nj["H1"],0)

non_pharmac_index <- 100*(
  ifelse(!is.na(OxCGRT$C1M_Flag),(OxCGRT$C1M_School.closing-0.5*(Fj["C1"]-OxCGRT$C1M_Flag))/Nj["C1"],0) +
    ifelse(!is.na(OxCGRT$C1M_Flag),(OxCGRT$C2M_Workplace.closing-0.5*(Fj["C2"]-OxCGRT$C1M_Flag))/Nj["C2"],0) +
    ifelse(!is.na(OxCGRT$C1M_Flag),(OxCGRT$C3M_Cancel.public.events-0.5*(Fj["C3"]-OxCGRT$C1M_Flag))/Nj["C3"],0) +
    ifelse(!is.na(OxCGRT$C1M_Flag),(OxCGRT$C4M_Restrictions.on.gatherings-0.5*(Fj["C4"]-OxCGRT$C1M_Flag))/Nj["C4"],0) +
    ifelse(!is.na(OxCGRT$C1M_Flag),(OxCGRT$C5M_Close.public.transport-0.5*(Fj["C5"]-OxCGRT$C1M_Flag))/Nj["C5"],0) +
    ifelse(!is.na(OxCGRT$C1M_Flag),(OxCGRT$C6M_Stay.at.home.requirements-0.5*(Fj["C6"]-OxCGRT$C1M_Flag))/Nj["C6"],0) +
    ifelse(!is.na(OxCGRT$C1M_Flag),(OxCGRT$C7M_Restrictions.on.internal.movement-0.5*(Fj["C7"]-OxCGRT$C1M_Flag))/Nj["C7"],0) +
    (OxCGRT$C8EV_International.travel.controls)/Nj["C8"]
)/8


health_system_policy_index <- (
  ifelse(!is.na(OxCGRT$H1_Flag),100*(OxCGRT$H1_Public.information.campaigns - 0.5*(Fj["H1"]-OxCGRT$H1_Flag))/Nj["H1"],0)+
    100*(OxCGRT$H2_Testing.policy)/Nj["H2"]+
    100*(OxCGRT$H3_Contact.tracing )/Nj["H3"]+
  ifelse(!is.na(OxCGRT$H6M_Flag),100*(OxCGRT$H6M_Facial.Coverings- 0.5*(Fj["H6"]-OxCGRT$H6M_Flag))/Nj["H6"],0)+
  ifelse(!is.na(OxCGRT$H7_Flag),100*(OxCGRT$H7_Vaccination.policy - 0.5*(Fj["H7"]-OxCGRT$H7_Flag))/Nj["H7"],0)+
  ifelse(!is.na(OxCGRT$H8M_Flag),100*(OxCGRT$H8M_Protection.of.elderly.people - 0.5*(Fj["H8"]-OxCGRT$H8M_Flag))/Nj["H8"],0)
)/6

vaccine_policy_index <- (
  100*(OxCGRT$V1_Vaccine.Prioritisation..summary.)/2+
    100*(OxCGRT$V3_Vaccine.Financial.Support..summary.)/5+
    ifelse(!is.na(OxCGRT$V4_Mandatory.Vaccination..summary.),100*(OxCGRT$V4_Mandatory.Vaccination..summary. )/1,0)
)/3

OxCGRT[,"local_communication_policies_index"] <- local_communication_policies_index
OxCGRT[,"non_pharmac_index"] <- non_pharmac_index
OxCGRT[,"health_system_policy_index"] <- health_system_policy_index
OxCGRT[,"vaccine_policy_index"] <- vaccine_policy_index

OxCGRT_sub <- OxCGRT[,c("Date","local_communication_policies_index","non_pharmac_index","health_system_policy_index","vaccine_policy_index")]
OxCGRT_agg <- aggregate(OxCGRT_sub[,2:5],by=list(Date=OxCGRT_sub$Date),FUN=mean)
OxCGRT_agg$Date <- as.Date(as.character(OxCGRT_agg$Date),format="%Y%m%d")

# jpeg("",width=1000,heigth=500)
# plot(OxCGRT_agg$Date,OxCGRT_agg$local_communication_policies_index,type="l",main="Local communication policies",xlab="",y)
# dev.off()
plot(OxCGRT_agg$Date,OxCGRT_agg$non_pharmac_index,type="l")
plot(OxCGRT_agg$Date,OxCGRT_agg$health_system_policy_index,type="l")
plot(OxCGRT_agg$Date,OxCGRT_agg$vaccine_policy_index,type="l")

library(reshape2)
library(ggplot2)
OxCGRT_melt <- melt(OxCGRT_agg,id.vars="Date")
levels(OxCGRT_melt$variable) <- c(
  "Local communication policy","Non-pharmacological intervention",
  "Health system policy","Vaccine policy"
)
OxCGRT_melt$Date <- as.Date(OxCGRT_melt$Date)
colnames(OxCGRT_melt) <- c("Date","Index","Value")
ggplot(OxCGRT_melt,aes(x=Date,y=Value,color=Index)) + geom_line() + theme_light() + ylab("Index value")
ggsave("index_ts.jpg",units="cm",width=30,height=12)
# table(OxCGRT$Date) #185 countries


#Check if the CFs are stationary?
adf.test(OxCGRT_agg$local_communication_policies_index)
adf.test(OxCGRT_agg$non_pharmac_index)
adf.test(OxCGRT_agg$health_system_policy_index)
adf.test(diff(OxCGRT_agg$vaccine_policy_index)) 
OxCGRT_agg$vaccine_policy_index[1] <- NA
OxCGRT_agg$vaccine_policy_index[2:nrow(OxCGRT_agg)] <- diff(OxCGRT_agg$vaccine_policy_index)
adf.test(OxCGRT_agg$vaccine_policy_index)
