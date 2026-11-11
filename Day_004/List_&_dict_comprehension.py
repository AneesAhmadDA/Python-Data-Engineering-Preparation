##Use list and dictionary comprehensions to filter and aggregate synthetic telemetry records.
telemetry = [
    {"ambulance_id": "AMB001", "speed": 65, "status": "ACTIVE"},
    {"ambulance_id": "AMB002", "speed": 0, "status": "IDLE"},
    {"ambulance_id": "AMB003", "speed": 80, "status": "ACTIVE"},
    {"ambulance_id": "AMB004", "speed": 45, "status": "ACTIVE"},
    {"ambulance_id": "AMB005", "speed": 0, "status": "IDLE"}
]



#Logic building using fpr loop
'''Active_ambulances=[]
for i in telemetry:
    for keys,values in i.items():
        if i['status'] and values=='ACTIVE':
            Active_ambulances.append(i)
        else:
            pass'''
##Use a list comprehension to extract ambulances with ACTIVE status
Active_amubalnces=[x for x in telemetry if x['status']=='ACTIVE']
print(Active_amubalnces)
##Extract ambulances with speeds greater than 50;
Speed_50=[x for x in telemetry if x['speed']>50]
print(Speed_50)
print("=====================================================")

##Build an ambulance_id → speed mapping.
Ambulance_speed={x['ambulance_id']:x['speed'] for x in telemetry}
print(Ambulance_speed)
print("=====================================================")
##Count how many ambulances currently have ACTIVE status.
counter=len(Active_amubalnces)
print(f" the total number of records for active ambulances arre :{counter}")
print("=====================================================")

##Reimplement everything using traditional for loops
act_ambulances=[]
for i in telemetry:
    if i['status']=="ACTIVE":
        act_ambulances.append(i)
    else:
        pass
print(f"THE ACTIVE AMBULANCES ARE \n{act_ambulances}")
print("=====================================================")
##task2 for speed >50
loop_speed=[]
for i in telemetry:
    if i['speed']>50:
        loop_speed.append(i)
    else:
        pass
print(f"THE AMBULANCES with Speed>50 are \n{loop_speed}")
print("=====================================================")

ambulance_speed_loop = {}

for i in telemetry:
    ambulance_speed_loop[i['ambulance_id']] = i['speed']
print(ambulance_speed_loop)

print("=====================================================")
counter=len(Active_amubalnces)
print(f" the total number of records for active ambulances arre :{counter}")
print("=====================================================")