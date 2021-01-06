import csv

def get_roles(filename="avalon_roles.csv"):
    roles = {}

    with open(filename) as csvfile:
        rolesfile = csv.reader(csvfile, delimiter=",")
        for row in rolesfile:
            if row[0] == "Name":
                continue

            role_info = {
                "Name": row[0],
                "Team": row[1],
                "Number": row[2],
                "Knoweldge": row[3]
            }
            
            roles[row[0]] = role_info
    return roles

# # testing only
# roles = get_roles()
# print(roles.values())