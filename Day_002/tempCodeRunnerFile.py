
##readin the file in a normal way 
with open ("event.txt","r") as file:
    Login_count=0
    Logout_count=0
    count=0
    for line in file:
        print(line.strip()) # strip remove the unnecessary lines in between since we have used /n already
        count=count+1
        if line.count("Login"):
            Login_count=Login_count+1
        elif line.count("Logout"):
            Logout_count=Logout_count+1
        else:
            pass
    print(f"The total number of records are {count}")
    print(f"The total number of Login records are {Login_count}")
    print(f"The total number of Logout records are {Logout_count}")