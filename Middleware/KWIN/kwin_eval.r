#es necesario installar con el comando R estas librerías primero scales al momento no tiene release apar R 4.2 que es la que usa ec2
#é necessário instalar previamente R essas bibliotecas. scales no momento não tem um release apar R 4.2 que é o usado por AWS ec2
#it is necessary to previously install R these libraries.scales at the moment does not have a release apar R 4.2 which is the one used by ec2

require(data.table)
#require(ggplot2)
#require(scales)

#lee la base de adverity
#inDB = data.table(read.csv("adverity2020.csv"))
inDB = data.table(read.csv("KWIN/kwin90.csv"))

#crea y da formato a las columnas de fecha
#Format specifications ------------------------------
## Date
inDB$Daily = format(inDB$Daily, format = "%d-%m-%Y")
inDB$Daily = as.Date(inDB$Daily)
inDB$Daily2 = format(inDB$Daily, format="%Y-%m-%d")
inDB$Month = format(inDB$Daily, format="%Y-%m")
inDB$Quarter = quarter(inDB$Daily)
inDB$Year = format(inDB$Daily, format="%Y")
print(inDB$Year[2000])


#crea una función para partir el campo de Campaign Name
get_country = function(camp){
    s = strsplit(camp, "_")[[1]][3]
    return(s)
}

#aplica la función get_country
inDB$Country = apply(inDB[,"Campaign.Name"], 1, get_country)
inDB[Country == "Brasil", Country:= "BRA"]
inDB[Country == "Several", Country:= "CENAM"]
inDB = inDB[!is.na(Country)]
inDB = inDB[Platform.Cost > 0]
country_list = inDB[, .(.N), by = Country]$Country

inDB[Country %like%"MEX|ARG|COL|LATAM", Region:="LATAM"]
inDB[Country=="BRA", Region:="BRA"]
inDB[Country %like% "PRI|GTM|PAN|CRI|DOM|SLV|ECU|HND|ANDINO|MERCOSUR|CENAM|JAM|NIC|BHS|BMU", Region:="CENAM"]
inDB = inDB[!is.na(Region)]
region_list = inDB[, .(.N), by = Region]$Region
region_list

#crea la función cost_type
cost_type = function(camp_s){
    type = "undefined"
    if (camp_s %like% "CPM"){
        type = "CPM"
    }
    if (camp_s %like% "CPV"){
        type = "CPV"
    }
    if (camp_s %like% "CPCV"){
        type = "CPCV"
    }
    if (camp_s %like% "CPE"){
        type = "CPE"
    }
    if (camp_s %like% "CPC_"){
        type = "CPC"
    }
    return(type)
}

cost_kpi = function(camp_s){
    type = "undefined"
    if (camp_s %like% "CPM"){
        type = "Impressions"
    }
    if (camp_s %like% "CPV"){
        type = "Video Views"
    }
    if (camp_s %like% "CPCV"){
        type = "Video Completions"
    }
    if (camp_s %like% "CPE"){
        type = "Engagements"
    }
    if (camp_s %like% "CPC_"){
        type = "Clicks"
    }
    return(type)
}

#Aplica la función cost_type
inDB[,"Cost.Type"] = apply(inDB[, "Campaign.Name"], 1, cost_type)
inDB[,"Cost.KPI"] = apply(inDB[, "Campaign.Name"], 1, cost_kpi)
inDB[, "Unit.KPI"] = as.numeric(0.0)

inDB[Campaign.Name %like% "Awareness", Cost.Type := "CPM"]
inDB[Campaign.Name %like% "Views", Cost.Type := "CPV"]
inDB[Campaign.Name %like% "Clics", Cost.Type := "CPE"]

#Asigna valores la variable Unit.KPI
inDB[Cost.Type == "CPCV", Unit.KPI:=as.numeric(inDB[Cost.Type =="CPCV", Video.Completions])]
inDB[Cost.Type == "CPC", Unit.KPI:=as.numeric(inDB[Cost.Type =="CPC", Clicks])]
inDB[Cost.Type == "CPV", Unit.KPI:=as.numeric(inDB[Cost.Type =="CPV", Video.Views])]
inDB[Cost.Type == "CPM", Unit.KPI:=as.numeric(inDB[Cost.Type =="CPM", Impressions])]
inDB[Cost.Type == "CPE", Unit.KPI:=as.numeric(inDB[Cost.Type =="CPE", Engagements])]


inDB[,"Unit.Cost"] = 0
inDB[Cost.Type == "CPM", Unit.Cost:=as.numeric(Platform.Cost*1000/Unit.KPI)]
inDB[Cost.Type != "CPM", Unit.Cost:=as.numeric(Platform.Cost/Unit.KPI)]

inDB = inDB[Cost.Type != "undefined"]

inDB[is.na(inDB)] <- 0

################# TESTING #################################################################



inDB$MaxDate = inDB$Daily
inDB$MinDate = inDB$Daily - 90

get_90_days_tendency = function(cost.type, region, datasource, mindate, maxdate){

  days_set_90 = inDB[Cost.Type == cost.type & Region == region & Datasource == datasource & (Daily >= mindate & Daily < maxdate)]

  central.impressions = median(days_set_90$Impressions)
  central.clicks = median(days_set_90$Clicks)
  central.views = median(days_set_90$Video.Views)
  central.completions = median(days_set_90$Video.Completions)
  central.engagements = median(days_set_90$Engagements)
  central.cost = median(days_set_90$Unit.Cost)
  central.goal = median(days_set_90$Unit.KPI)

  return(list(central.impressions, central.clicks, central.views, central.completions, central.engagements, central.cost, central.goal))
  #return(central.impressions)
}
#makes a subset to make faster the processing

inDBtrimmed = inDB[, .(Central.Goal=sum(Unit.KPI)
                           , Central.Cost=sum(Unit.Cost)
                           , Central.Impressions = sum(Impressions)
                           , Central.Clicks = sum(Clicks)
                           , Central.Video.Views = sum(Video.Views)
                           , Central.Video.Completions = sum(Video.Completions)
                           , Central.Engagements = sum(Engagements)
                          ),
                       by=c("Datasource","Region", "Cost.Type","Daily2", "MinDate","MaxDate")]


#Execute the function to get the daily central tendency from the last 90 days it takes over 10 minutes to finish in google colab.
inDBtrimmed$Central.Impressions = as.numeric(mapply(get_90_days_tendency,inDBtrimmed$Cost.Type,inDBtrimmed$Region, inDBtrimmed$Datasource, inDBtrimmed$MinDate, inDBtrimmed$MaxDate)[1,])
inDBtrimmed$Central.Clicks = as.numeric(mapply(get_90_days_tendency,inDBtrimmed$Cost.Type,inDBtrimmed$Region, inDBtrimmed$Datasource, inDBtrimmed$MinDate, inDBtrimmed$MaxDate)[2,])
inDBtrimmed$Central.Video.Views = as.numeric(mapply(get_90_days_tendency,inDBtrimmed$Cost.Type,inDBtrimmed$Region, inDBtrimmed$Datasource, inDBtrimmed$MinDate, inDBtrimmed$MaxDate)[3,])
inDBtrimmed$Central.Video.Completions = as.numeric(mapply(get_90_days_tendency,inDBtrimmed$Cost.Type,inDBtrimmed$Region, inDBtrimmed$Datasource, inDBtrimmed$MinDate, inDBtrimmed$MaxDate)[4,])
inDBtrimmed$Central.Engagements = as.numeric(mapply(get_90_days_tendency,inDBtrimmed$Cost.Type,inDBtrimmed$Region, inDBtrimmed$Datasource, inDBtrimmed$MinDate, inDBtrimmed$MaxDate)[5,])
inDBtrimmed$Central.Cost = as.numeric(mapply(get_90_days_tendency,inDBtrimmed$Cost.Type,inDBtrimmed$Region, inDBtrimmed$Datasource, inDBtrimmed$MinDate, inDBtrimmed$MaxDate)[6,])
inDBtrimmed$Central.Goal = as.numeric(mapply(get_90_days_tendency,inDBtrimmed$Cost.Type,inDBtrimmed$Region, inDBtrimmed$Datasource, inDBtrimmed$MinDate, inDBtrimmed$MaxDate)[7,])
####################################################### END TESTING ######

#joining two bases
finalDB = merge(inDB, inDBtrimmed, by=c("Datasource", "Daily2", "Region", "Cost.Type", "MaxDate", "MinDate"), all.x=TRUE, allow.cartesian=TRUE)

lastdate = max(finalDB$Daily)
print(lastdate)
lastdate = as.Date(lastdate)
finalDB = finalDB[finalDB$Daily == lastdate]
#finalDB = finalDB[finalDB$Daily >= '2021-05-26']

#Add the factor calculations from the central tendencies and write the final database

finalDB$Eval1 = -1*finalDB$Unit.Cost /finalDB$Central.Cost
finalDB$Eval2 = finalDB$Impressions / finalDB$Central.Impressions
finalDB$Eval3 = finalDB$Clicks / finalDB$Central.Clicks
finalDB$Eval4 = finalDB$Engagements / finalDB$Central.Engagements
finalDB$Eval5 = finalDB$Video.Completions/ finalDB$Central.Video.Completions
finalDB$Eval6 = finalDB$Video.Views / finalDB$Central.Video.Views

finalDB[is.na(finalDB)] <- 0
finalDB[finalDB==Inf] <- 0

####Calculo de los factores de kwin
finalDB$EvalTotal = 0

####IMPORTANTE:Las ponderaciones de los facotres fueron asignadas previamente en un análisis cualitativo del equipo

#Calculo del factor general

finalDB$Eval1 = -1*finalDB$Unit.Cost /finalDB$Central.Cost
finalDB$Eval2 = finalDB$Impressions / finalDB$Central.Impressions
finalDB$Eval3 = finalDB$Clicks / finalDB$Central.Clicks
finalDB$Eval4 = finalDB$Engagements / finalDB$Central.Engagements
finalDB$Eval5 = finalDB$Video.Completions/ finalDB$Central.Video.Completions
finalDB$Eval6 = finalDB$Video.Views / finalDB$Central.Video.Views

finalDB[is.na(finalDB)] <- 0
finalDB[finalDB==Inf] <- 0
##

finalDB$EvalTotal = 0

finalDB[Cost.Type == "CPM", EvalTotal:= Eval1 + Eval2 + (0.1*Eval3) + (0.01*Eval4) + (0.001)*Eval5 + (0.0001*Eval6)]
finalDB[Cost.Type == "CPE", EvalTotal:= Eval1 + Eval4 + (0.1)*Eval6 + (0.01)*Eval5 + (0.001)*Eval3 + (0.0001)*Eval2]
finalDB[Cost.Type == "CPV", EvalTotal:= Eval1 + (0.1)*Eval4 + Eval6 + (0.01)*Eval5 + (0.001)*Eval3 + (0.0001)*Eval2]
finalDB[Cost.Type == "CPCV", EvalTotal:= Eval1 + (0.1)*Eval4 + (0.01)*Eval6 + Eval5 + (0.001)*Eval3 + (0.0001)*Eval2]
finalDB[Cost.Type == "CPC", EvalTotal:= Eval1 + (0.1)*Eval4 + (0.01)*Eval6 + Eval3 + (0.001)*Eval5 + (0.0001)*Eval2]

finalDB[Cost.Type == "CPM", second.Eval:= (0.1*Eval3) + (0.01*Eval4) + (0.001)*Eval5 + (0.0001*Eval6)]
finalDB[Cost.Type == "CPE", second.Eval:= (0.1)*Eval6 + (0.01)*Eval5 + (0.001)*Eval3 + (0.0001)*Eval2]
finalDB[Cost.Type == "CPV", second.Eval:= (0.1)*Eval4 + (0.01)*Eval5 + (0.001)*Eval3 + (0.0001)*Eval2]
finalDB[Cost.Type == "CPCV",second.Eval:= (0.1)*Eval4 + (0.01)*Eval6 +  (0.001)*Eval3 + (0.0001)*Eval2]
finalDB[Cost.Type == "CPC", second.Eval:= (0.1)*Eval4 + (0.01)*Eval6 +  (0.001)*Eval5 + (0.0001)*Eval2]

finalDB[Cost.Type == "CPM", first.Eval:= Eval2]
finalDB[Cost.Type == "CPE", first.Eval:= Eval4 ]
finalDB[Cost.Type == "CPV", first.Eval:= Eval6 ]
finalDB[Cost.Type == "CPCV", first.Eval:= Eval5 ]
finalDB[Cost.Type == "CPC", first.Eval:= Eval3 ]

#presDB = finalDB[, .(Eval = median(EvalTotal), Central.Goal = median(Central.Goal), Total.Units = sum(Unit.KPI), Unit.Cost = sum(Costs)/sum(Unit.KPI), Central.Cost = median(Central.Cost)), by=c("Campaign.Name", "Country", "Cost.Type")][order(-Eval)]
finalDB = finalDB[EvalTotal > 0]

#scmin = min(presDB$Eval)
#presDB$Eval = presDB$Eval - scmin


#scmax = max(presDB$Eval)
#presDB$Eval = log(ceiling(presDB$Eval*100 / scmax)+0.001)


#liminf = median(presDB$Eval)*0.7
#limsup = median(presDB$Eval)*1.3

#presDB$Status = "Good"
#presDB[Eval > limsup, Status:= "Great"]
#presDB[Eval < liminf, Status:= "Could be Better"]


#aplica logaritmos a los factores y reescala del 1 al 10
finalDB$lEvalTotal = log(finalDB$EvalTotal)

finalDB[second.Eval == 0, lsecondEval:= 0]
finalDB[second.Eval != 0, lsecondEval:= log(second.Eval)]

finalDB[first.Eval == 0, lfirstEval:= 0]
finalDB[first.Eval != 0, lfirstEval:= log(first.Eval)]

#finalDB$Eval_scale <- rescale(finalDB$lEvalTotal,
#                                 to = c(0, 10))
finalDB$Eval_scale <- pnorm(finalDB$lEvalTotal, mean = mean(finalDB$lEvalTotal), sd = sd(finalDB$lEvalTotal))*10
finalDB$firstEval_scale <- pnorm(finalDB$lfirstEval, mean = mean(finalDB$lfirstEval), sd = sd(finalDB$lfirstEval))*10
finalDB$secondEval_scale <- pnorm(finalDB$lsecondEval, mean = mean(finalDB$lsecondEval), sd = sd(finalDB$lsecondEval))
#escribe los archivos para subir a la plataforma
#write.csv(presDB, "grouped_results.csv", row.names=FALSE)
finalDB = finalDB[Brand != "<undefined>"]

pastDB = data.table(read.csv("KWIN/kwin_basecumulative.csv"))

pastDB$Daily = format(pastDB$Daily, format = "%d-%m-%Y")
pastDB$Daily = as.Date(pastDB$Daily)
pastDB$MaxDate = format(pastDB$MaxDate, format = "%d-%m-%Y")
pastDB$MaxDate = as.Date(pastDB$MaxDate)
pastDB$MinDate = format(pastDB$MinDate, format = "%d-%m-%Y")
pastDB$MinDate = as.Date(pastDB$MinDate)
pastDB$Daily2 = format(pastDB$Daily2, format = "%Y-%m-%d")

new = finalDB
write.csv(new, "KWIN/kwinnew.csv", row.names = FALSE)

finalDB = rbind(finalDB,pastDB)
write.csv(finalDB, "KWIN/kwin_basecumulative.csv", row.names = FALSE)
