#%% import

import json
import datetime
from datetime import datetime
import os
import csv
import math


#%% def / class
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

#%%% class CsvFileManager
class CsvFileManager:
  def __init__(self, nom_fichier):
    self.nom_fichier = nom_fichier

  def EraseCsv(self):
    if os.path.exists(self.nom_fichier):
      os.remove(self.nom_fichier)
      # print("Le fichier ", self.nom_fichier ,"est supprimé")
      pass
    else:
      # print("Le fichier ", self.nom_fichier ,"n'existe pas")
      pass
    
  def WriteCsv(self, ligne):
    # Ouvre le fichier en mode écriture
    with open(self.nom_fichier, 'a', newline='', encoding='utf-8' ) as csvfile:
      # Crée un objet écrivain pour écrire dans le fichier CSV
      writer = csv.writer(csvfile)
      # Écris la ligne dans le fichier CSV
      writer.writerow([ligne])
      
#%%% OLD def EraseCsv #!!! A supprimer
# def EraseCsv(nom_fichier):
#     if os.path.exists(nom_fichier):
#       os.remove(nom_fichier)
#       print("Le fichier ", nom_fichier ," est supprimé")
#     else:
#       print("Le fichier ", nom_fichier ,"n'existe pas")
    
# #%%% def WriteCsv
# def WriteCsv(nom_fichier, ligne):
#   # Ouvre le fichier en mode écriture
#   with open(nom_fichier, 'a', newline='', encoding='utf-8' ) as csvfile:
#     # Crée un objet écrivain pour écrire dans le fichier CSV
#     writer = csv.writer(csvfile)
#     # Écris la ligne dans le fichier CSV
#     writer.writerow([ligne])
    
#%%% def TimeFormat_DeleteMilisecond   
def TimeFormat_DeleteMilisecond(ma_chaine):
    
    # Liste des formats de chaîne de temps à essayer
    formats = ["%H:%M:%S.%f", "%d days, %H:%M:%S.%f", "%d day, %H:%M:%S.%f", "%H:%M:%S"]

    # Essaie chaque format de chaîne de temps jusqu'à ce qu'un format fonctionne
    for fmt in formats:
        try:
            # Convertit la chaîne en objet datetime
            mon_datetime = datetime.strptime(str(ma_chaine), fmt)
            print(ma_chaine)
           
            # Extrais l'objet time de l'objet datetime et formate l'objet time au format HH:MM:SS
            temps_sans_microsecondes = mon_datetime.time().strftime("%d 'jour' :%H:%M:%S")
            print(temps_sans_microsecondes)
           
            # Retourne l'objet time au format HH:MM:SS
            return temps_sans_microsecondes
        except ValueError:
            # Si le format ne fonctionne pas, passe au suivant
            pass
           
    # Si aucun format ne fonctionne, lève une exception ValueError
    raise ValueError("Format de chaîne de temps non reconnu")
    
    

    
    
    # # Convertis la chaîne en objet datetime
    # # mon_datetime = datetime.strptime(str(ma_chaine), "%H:%M:%S.%f")
    # # mon_datetime = datetime.strptime(str(ma_chaine), "%d days, %H:%M:%S.%f")
   
    # print("ma_chaine" , ma_chaine)
    # try:
    #     print("try1")
    #     mon_datetime = datetime.strptime(str(ma_chaine), "%H:%M:%S.%f")
    #     pass
    # except Exception:
    #     print("exp1")
    #     pass
    # try:
    #     print("try2")
    #     mon_datetime = datetime.strptime(str(ma_chaine), "%d days, %H:%M:%S.%f")
    #     pass
    # except Exception:
    #     print("exp2")
    #     pass
   
    # try:
    #     print("try3")
    #     mon_datetime = datetime.strptime(str(ma_chaine), "%d day, %H:%M:%S.%f")
    #     pass
    # except Exception:
    #     print("exp3")
    #     pass   
    
    # try:
    #     print("try4")
    #     mon_datetime = datetime.strptime(str(ma_chaine), "%H:%M:%S")
    #     pass
    # except Exception:
    #     print("exp4")
    #     pass
   
    # # Extrais l'objet time de l'objet datetime et formate l'objet time au format HH:MM:SS
    # temps_sans_microsecondes = mon_datetime.time().strftime("%H:%M:%S")
    # print("temps_sans_microsecondes" , temps_sans_microsecondes)
    
    # # # Retourne l'objet time au format HH:MM:SS
    # # return temps_sans_microsecondes    



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

#%%% def TargetLocationOK
def DatetimeToString(dt):
    total_seconds = dt.total_seconds()
    hours = int(total_seconds / 3600)
    minutes = int((total_seconds - (hours * 3600)) / 60)
    seconds = int(total_seconds - (hours * 3600) - (minutes * 60)) 
    # print("datetime_to_string", hours,minutes,seconds,total_seconds)
    time_str = f"{hours}:{minutes}:{seconds}"
    # print("time_str", time_str)

    return time_str

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

MaxDays = 31+1 # Nombre de jours max par mois + 1 car la liste commence à 0
MaxMonths = 12+1

#%%%  Extraction des .json d'une année dans des dictionnaires (dict)
Year = 2022
data, dataExist = ExtractDataJson(Year)  

#%%% CsvFileManager
TargetCsvOutput = 'GoogleMaps_TimeAtlocation.csv'
CsvFileManager_1 = CsvFileManager(TargetCsvOutput)
CsvFileManager_1.EraseCsv()
# header CSV row
CsvFileManager_1.WriteCsv("Address" + ";" + "End_time" + ";" + "Year" + ";" +
                          "Month" + ";" + "Day" + ";" + "TotalHoursPerDay" + ";" + "TotalHoursPerMonth")

#%%% Parcours des dictionnaires (12 dict si année complète)
# print(dataExist) # Affiche les mois ayans pu être extraits
for Month in range(0, 13): # traitement du dict data du mois (i=month)
    if (dataExist[Month]==True) :# Si dict exist alors 
        print('Month-----------------------------' , Month, '\r')
        # print(data[i])
        # if (True) : # Forçage focus sur Février
        
        # CountTimelineObjects(data,i) # fonction inutile si itération
        
        # INIT var tous les mois
        cpt_TimelineObjects = 0
        
        # FlagFirstMonthCycle = 0
        # TotalHoursPerMonth = ''
        
        arrayTotalHoursPerMonth = [TimeDiff('2022-01-01T00:00:00.000Z', '2022-01-01T00:00:00.000Z')  ]*MaxMonths
        
        FlagFirstDayCycle = 0
        FlagPrevElapsedTime = 0
        # TotalHoursPerDay = ''             
        
        arrayAddress= ['']*MaxDays
        arrayTotalHoursPerDay = [TimeDiff('2022-01-01T00:00:00.000Z', '2022-01-01T00:00:00.000Z')  ]*MaxDays
        arrayEnd_time= ['']*MaxDays
       
        PrevElapsedTime = ''
        OldDay = 0
        
        for TimelineObjects in data[Month]['timelineObjects']:  # itération sur tous le 'timelineObjects' 
            # print('cpt_TimelineObjects-----------------------------' , cpt_TimelineObjects, '\r')            
            try: # Tentative de lecture si par exemple <> de placeVisit pas de remonté d'érreur
                # print('ReadDataLocation' ,ReadDataLocation(data,Month,cpt_TimelineObjects))
                # print('ReadDataDuration' ,ReadDataDuration(data,Month,cpt_TimelineObjects))
                Address,latitudeE7,longitudeE7,latitudeE7Dec,longitudeE7Dec = ReadDataLocation(data,Month,cpt_TimelineObjects)
                Start_time,DayNumber,End_time,ElapsedTime = ReadDataDuration(data,Month,cpt_TimelineObjects)
                # print("ElapsedTime", type(ElapsedTime), ElapsedTime) # <class 'datetime.timedelta'> 1 day, 12:29:13.170000 0:24:24.403000
                
                Distance = Dist2Geopoints(target_lat, target_lng, latitudeE7Dec, longitudeE7Dec)
                # print('Distance',Distance) 
                
                AddresOK, GeoPosOK = TargetLocationOK(Address, TargetAdress, Distance, radius)
                # print('TargetLocationOK' , DayNumber, AddresOK, GeoPosOK , Address, TargetAdress )
                
                if (AddresOK)or(GeoPosOK) : # Adresse ou position géographique ok
                    # print('-TargetLocOK',  'Address' , Address , 'DayNumber=',DayNumber , 'FlagFirstDayCycle=' , FlagFirstDayCycle , 'ElapsedTime' , ElapsedTime)  
                    # print('-TargetLocOK', 'DayNumber=',DayNumber , 'FlagFirstDayCycle=' , FlagFirstDayCycle , 'ElapsedTime' , ElapsedTime)  
 
                    arrayAddress[DayNumber] = Address
                    arrayTotalHoursPerDay[DayNumber] += ElapsedTime 
                    # arrayStart_time[DayNumber] = Start_time
                    arrayEnd_time[DayNumber] = End_time      
                    # print('-DayNumber' ,DayNumber ,arrayTotalHoursPerDay[DayNumber])
                    
                    arrayTotalHoursPerMonth[Month] += ElapsedTime
                    # print('-Month', Month , DayNumber , arrayTotalHoursPerMonth[Month])
                          
                    # print(Month , DayNumber ,arrayTotalHoursPerDay[DayNumber], arrayTotalHoursPerMonth[Month])
                    
                    pass       
                        
                pass
            except Exception:
                
                pass
            
            # Fin doucle for      
            cpt_TimelineObjects = cpt_TimelineObjects+1
            
        
        
        for Day in range(1, MaxDays):
            NonNull = arrayTotalHoursPerDay[Day] != TimeDiff('2022-01-01T00:00:00.000Z', '2022-01-01T00:00:00.000Z')   
            if (NonNull) :

                csvAdress = str(arrayAddress[Day]).replace(',','.')
                csvEnd_time = str(arrayEnd_time[Day])
                csvYear = str(Year)
                csvMonth = str(Month)
                csvDay = str(Day)
  
                csvTotalHoursPerMonth = DatetimeToString(arrayTotalHoursPerMonth[Month])                
                csvTotalHoursPerDay = DatetimeToString(arrayTotalHoursPerDay[Day])        
                
                print('-WriteCsv', csvAdress[0:10], csvEnd_time, csvYear, csvMonth, csvDay, csvTotalHoursPerMonth, csvTotalHoursPerDay)

                try:
                    # Ecrit dans un CSV address + year + mois + jour + Start_time + ElapsedTime
                    # print('print CSV')
                    # CsvFileManager_1.WriteCsv(str(arrayAddress[Day]).replace(',','.') + ";" + str(arrayEnd_time[Day]) + ";" + str(Year) + ";" + str(Month) + ";" + str(Day) + ";" + str(TimeFormat_DeleteMilisecond(arrayTotalHoursPerDay[Day])) + ";" + str(TimeFormat_DeleteMilisecond(arrayTotalHoursPerMonth[Month])) )
                    CsvFileManager_1.WriteCsv( csvAdress + ";" + csvEnd_time  + ";" + csvYear + ";" + csvMonth + ";" + csvDay + ";" + csvTotalHoursPerDay + ";" + csvTotalHoursPerMonth)
                    
                    pass
                except Exception:
                    pass
    
            pass   
    
