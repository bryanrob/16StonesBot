import mariadb
import sys

class DB:
    def __init__(this):
        file=open("db.creds","r")
        creds=[]
        while(True):
            line=file.readline()
            if not line:
                break
            print("Read from db.creds: "+line)
            line=line.split("=")[1].strip()
            creds.append(line)
        file.close()
        try:
            database=mariadb.connect(
                user=creds[2],
                password=creds[3],
                host=creds[0],
                port=int(creds[1])
            )
            this.cursor=database.cursor()
        except mariadb.Error as e:
            print(f"Error connecting to the database: {e}")
            sys.exit(1)


def main():
    print("Main function from [Database.py] called!")
    db=DB()

if __name__=="__main__":
    main()
