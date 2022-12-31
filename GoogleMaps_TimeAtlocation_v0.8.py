#%% import

import json
import datetime
from datetime import datetime
import os
import csv
import math


#%% def (fonction)
#%%% def generate_path
def GenerateReadPath(year, i):
    # Génération du chemin d'accès en fonctions de variables tels que l'année et le mois
    FolderData = 'GoogleMaps_TimeAtlocation_JsonData'
    FolderYear = year
    # Liste de texte des mois pour ouvrir les fichiers google takeout "Historique des positions"
    Month = ['JANUARY','FEBRUARY','MARCH','APRIL','MAY','JUNE','JULY'
              ,'AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER']
    Month_index = i # 1 Janvier 2 Février ...
    Month_index = Month_index-1
    # print(Month[Month_index])
    FileName = f'{FolderYear}_{Month[Month_index]}.json'
    FullPath = f'{FolderData}/{FolderYear}/{FileName}'
    # print(FullPath) 
    return FullPath

#%%% def ExtractDataJson
def ExtractDataJson(year):
 # exemple de viewer https://codebeautify.org/jsonviewer
   
    data = ['']*13 # permet de stocker 12 dict pour les 12 mois
    dataExist = [0]*13 # flag permenant de savoir quels mois on été extraits
    
    for i in range(1, 13):
        # print(i)
        FullPath = GenerateReadPath(year, i) # Retournera par exemple 'Test_Json_Data/2022/2022_JANUARY.json'
        # Permet de vérifier si le fichier existe avant l'ouverture du fichier
        # print(os.path.exists(FullPath))
        if (os.path.exists(FullPath)==True) :
            dataExist[i] = 1 # Lève un flag pour savoir par la suite si le mois existe
            # Ouvre le fichier JSON
            # with open(f'Test_Json_Data/2022/2022_JANUARY.json', 'r', encoding="utf8") as f: # r = read
            with open(FullPath, 'r', encoding="utf8") as f: # r = read        
                data[i] = json.load(f)      
                # debug print
                # print('dataType' , type(data[i])) # Doit être de type <class 'dict'> (dictionnaire)
                # print(data[i]['timelineObjects'][1]['placeVisit']['duration']) # print limité pour visu
                # print(data)
                # print(data['timelineObjects'])
                # print(data['timelineObjects'][0]['activitySegment'])
                # print(data['timelineObjects'][1]['placeVisit'])
    
    return data, dataExist

#%%% def TimeDiff
def TimeDiff(Start_time, End_time):
  # Convertir les variables de temps en objets datetime
  Start_time = datetime.fromisoformat(Start_time)
  End_time = datetime.fromisoformat(End_time)

  # Calculer la différence de temps entre les deux objets datetime
  time_difference = End_time - Start_time

  # Renvoyer la différence de temps en secondes
  # return time_difference.total_seconds()
  return time_difference

#%%% def WriteCsv
def WriteCsv(nom_fichier, ligne):
  # Ouvre le fichier en mode écriture
  with open(nom_fichier, 'a', newline='', encoding='utf-8' ) as csvfile:
    # Crée un objet écrivain pour écrire dans le fichier CSV
    writer = csv.writer(csvfile)
    # Écris la ligne dans le fichier CSV
    writer.writerow([ligne])
    
#%%% def TimeFormat_DeleteMilisecond   
def TimeFormat_DeleteMilisecond(ma_chaine):
  # Convertis la chaîne en objet datetime
  mon_datetime = datetime.strptime(str(ma_chaine), "%H:%M:%S.%f")
  # Extrais l'objet time de l'objet datetime et formate l'objet time au format HH:MM:SS
  temps_sans_microsecondes = mon_datetime.time().strftime("%H:%M:%S")
  # Retourne l'objet time au format HH:MM:SS
  return temps_sans_microsecondes    

#%%% def ExtractDayNumber
def ExtractDayNumber(ma_chaine):
  # Convertis la chaîne en objet datetime
  mon_datetime = datetime.fromisoformat(ma_chaine)
  # Extrais le numéro du jour de l'objet datetime
  numero_jour = mon_datetime.day
  # Retourne le numéro du jour
  return numero_jour

#%%% def DataLocation
def ReadDataLocation(dataDict,month,cpt_TimelineObjects):
    
    try:
        Address = data[month]['timelineObjects'][cpt_TimelineObjects]['placeVisit']['location']['address']
        latitudeE7 = data[month]['timelineObjects'][cpt_TimelineObjects]['placeVisit']['location']['latitudeE7']
        longitudeE7 = data[month]['timelineObjects'][cpt_TimelineObjects]['placeVisit']['location']['longitudeE7']
        latitudeE7Dec = latitudeE7/10000000
        longitudeE7Dec = longitudeE7/10000000
        pass
    except Exception:
        pass

    return Address,latitudeE7,longitudeE7,latitudeE7Dec,longitudeE7Dec

#%%% def DataDuration
def ReadDataDuration(dataDict,month,cpt_TimelineObjects):
    
    try:
        Start_time = data[month]['timelineObjects'][cpt_TimelineObjects]['placeVisit']['duration']['startTimestamp']
        # print('Start_time', type(Start_time), Start_time)
        DayNumber = ExtractDayNumber(Start_time) 
        # print('DayNumber', DayNumber)
        End_time = data[month]['timelineObjects'][cpt_TimelineObjects]['placeVisit']['duration']['endTimestamp']
        ElapsedTime = TimeDiff(Start_time, End_time)
        # print('ElapsedTime', type(ElapsedTime), ElapsedTime)
        pass
    except Exception:
        pass

    return Start_time,DayNumber,End_time,ElapsedTime

#%%% def GeoIsInsideRadius
def Dist2Geopoints(target_lat, target_lng, lat, lng):
    # Convertir les degrés en radians
    target_lat_radians = math.radians(target_lat)
    target_lng_radians = math.radians(target_lng)
    lat_radians = math.radians(lat)
    lng_radians = math.radians(lng)
    
    # Calculer la distance en utilisant la formule Haversine
    a = (math.sin((lat_radians - target_lat_radians) / 2)**2 + 
         math.cos(target_lat_radians) * math.cos(lat_radians) * 
         math.sin((lng_radians - target_lng_radians) / 2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371e3 * c  # 6371e3 est la distance de la Terre en mètres

    # Vérifier si la distance est inférieure au rayon
    return distance # en mètre

# # Exemple d'utilisation
# target_lat = 44.13860983334649 # Centre la position cible
# target_lng = 4.657463254390843
# radius = 1000  # en mètre
# lat = 44.1403615873381
# lng = 4.657216251417782

# Distance = GeoIsInsideRadius(target_lat, target_lng, lat, lng)

# print(round(Distance,1), 'm')

# if Distance<radius:
#     print("La position est à l'intérieur du rayon")
# else:
#     print("La position est à l'extérieur du rayon")

#%%% def TargetLocationOK
def TargetLocationOK(Address, TargetAdress, Distance, radius):
    
    # print('TargetLocationOK', Address,TargetAdress)
    # print('Address.find', Address.find(TargetAdress)) # Ok si >= à 0 ... ou -1 non trouvé
    if ((Address.find(TargetAdress)>=0)or(TargetAdress=='nofilter')) :
        AddresOK = 1
    else :
        AddresOK = 0
        
    if (Distance<radius) :
        GeoPosOK = 1
    else :
        GeoPosOK = 0        
    
    return AddresOK, GeoPosOK

#%% *********** Main ***********

#%%% Déclaration des variables globales

data = ['']*13 # permet de stocker 12 dict pour chaque mois
dataExist = [0]*13 # flag permenant de savoir quels mois on été extraits

TargetAdressList = ['nofilter',
                    'Parade, 30200 Orsan', # 'Parade, 30200 Orsan' permet de prendre en compte les adresses proches
                    '705 Chem. de la Parade, 30200 Orsan, France',
                    '29 Avenue de la Méditerranée, 30132 Caissargues, France',
                    '5 Rue des Genêts, 30132 Caissargues, Gard, Languedoc-Roussillon, France',
                    '11 Av. Galilée, 13310 Saint-Martin-de-Crau, France']

TargetAdress = TargetAdressList[1]

target_lat = 44.13860983334649 # Centre la position cible CLEO = 44.13860983334649 4.657463254390843
target_lng = 4.657463254390843
radius = 500  # en mètre
lat = 0 # lat = 44.1403615873381
lng =0 # lng = 4.657216251417782

TargetCsvOutput = 'GoogleMaps_TimeAtlocation.csv'

MaxDays = 31 # Nombre de jours max par mois


#%%%  Extraction des .json d'une année dans des dictionnaires (dict)
Year = 2014
data, dataExist = ExtractDataJson(Year)  
 

#%%% Parcours des dictionnaires (12 dict si année complète)
# print(dataExist) # Affiche les mois ayans pu être extraits
for Month in range(0, 13): # traitement du dict data du mois (i=month)
    if (dataExist[Month]==True) :# Si dict exist alors 
        # print('Month-----------------------------' , Month, '\r')
        # print(data[i])
        # if (True) : # Forçage focus sur Février
        
        # CountTimelineObjects(data,i) # fonction inutile si itération
        
        # INIT var tous les mois
        cpt_TimelineObjects = 0
        
        FlagFirstMonthCycle = 0
        TotalHoursPerMonth = ''
        
        FlagFirstDayCycle = 0
        FlagPrevElapsedTime = 0
        TotalHoursPerDay = ''             
        
        arrayAddress= ['']*MaxDays
        arrayTotalHoursPerDay = [TimeDiff('2022-01-01T00:00:00.000Z', '2022-01-01T00:00:00.000Z')  ]*MaxDays
        # arrayStart_time= ['']*MaxDays
        arrayEnd_time= ['']*MaxDays
        # arrayTotalHoursPerDay = [datetime.strptime('0:24:24.403000', "%H:%M:%S.%f")]*31
        # arrayTotalHoursPerDay = [timedelta()]*31
        # arrayTotalHoursPerDay = [datetime(1900, 1, 1)]*31
        # print(type(arrayTotalHoursPerDay) , arrayTotalHoursPerDay)
        # Convert the date strings to datetime objects
        # print(type(arrayTotalHoursPerDay) , type(arrayTotalHoursPerDay[1]) , str(arrayTotalHoursPerDay[1]))
       
        PrevElapsedTime = ''
        OldDay = 0
        
        for TimelineObjects in data[Month]['timelineObjects']:  # itération sur tous le 'timelineObjects' 
            # print('cpt_TimelineObjects-----------------------------' , cpt_TimelineObjects, '\r')            
            try: # Tentative de lecture si par exemple <> de placeVisit pas de remonté d'érreur
                # print(data[i]['timelineObjects'][cpt_TimelineObjects]['placeVisit'])
                # Récupération des datas year/month/cpt_TimelineObjects
                # print('ReadDataLocation' ,ReadDataLocation(data,Month,cpt_TimelineObjects))
                # print('ReadDataDuration' ,ReadDataDuration(data,Month,cpt_TimelineObjects))
                Address,latitudeE7,longitudeE7,latitudeE7Dec,longitudeE7Dec = ReadDataLocation(data,Month,cpt_TimelineObjects)
                Start_time,DayNumber,End_time,ElapsedTime = ReadDataDuration(data,Month,cpt_TimelineObjects)
                # print(type(ElapsedTime), ElapsedTime) # <class 'datetime.timedelta'> 1 day, 12:29:13.170000 0:24:24.403000
                
                Distance = Dist2Geopoints(target_lat, target_lng, latitudeE7Dec, longitudeE7Dec)
                # print('Distance',Distance) 
                
                AddresOK, GeoPosOK = TargetLocationOK(Address, TargetAdress, Distance, radius)
                # print('TargetLocationOK' , AddresOK, GeoPosOK )
                
                if (AddresOK)or(GeoPosOK) : # Adresse ou position géographique ok
                    # print('-TargetLocOK',  'Address' , Address , 'DayNumber=',DayNumber , 'FlagFirstDayCycle=' , FlagFirstDayCycle , 'ElapsedTime' , ElapsedTime)  
                    # print('-TargetLocOK', 'DayNumber=',DayNumber , 'FlagFirstDayCycle=' , FlagFirstDayCycle , 'ElapsedTime' , ElapsedTime)  
 
                    arrayAddress[DayNumber] = Address
                    arrayTotalHoursPerDay[DayNumber] += ElapsedTime 
                    # arrayStart_time[DayNumber] = Start_time
                    arrayEnd_time[DayNumber] = End_time
                    
                    # print(DayNumber ,arrayTotalHoursPerDay[DayNumber])
                                        
                    pass       
                        
                pass
            except Exception:
                
                pass
            
            # Fin doucle for      
            cpt_TimelineObjects = cpt_TimelineObjects+1
            
        for Day in range(1, MaxDays):
            NonNull = arrayTotalHoursPerDay[Day] != TimeDiff('2022-01-01T00:00:00.000Z', '2022-01-01T00:00:00.000Z')   
            if (NonNull) :
            # print(Year, Month, i, arrayTotalHoursPerDay[i])
                print(Year, Month, Day, arrayTotalHoursPerDay[Day])
                
                
                try:
                    # Ecrit dans un CSV address + year + mois + jour + Start_time + ElapsedTime
                    # print('print CSV')
                    WriteCsv(TargetCsvOutput, str(arrayAddress[Day]).replace(',','.') + ";" + str(arrayEnd_time[Day]) + ";" + str(Year) + ";" + str(Month) + ";" + str(Day) + ";" + str(TimeFormat_DeleteMilisecond(arrayTotalHoursPerDay[Day])))
                    pass
                except Exception:
                    pass
 
            pass   
    
