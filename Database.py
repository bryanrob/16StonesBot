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
        this.host=creds[0]
        this.port=int(creds[1])
        this.user=creds[2]
        this.password=creds[3]
        this.databaseName=creds[4]
        this.tableName=creds[5]
        try:
            this.database=mariadb.connect(
                user=this.user,
                password=this.password,
                host=this.host,
                port=this.port
            )
            this.cursor=this.database.cursor()
            this.cursor.execute(f"use {this.databaseName}")
        except mariadb.Error as e:
            print(f"Error connecting to the database: {e}")
            sys.exit(1)

    def addNewUser(this,userid):
        this.cursor.execute(f"insert into {this.databaseName}.{this.tableName}(id,wins,losses,w_l_ratio,moyai) values ('{userid}','{0}','{0}','{0.0}','{0}')")
        this.database.commit()
    
    def addWin(this,userid):
        #this.cursor.execute(f"select * from {this.databaseName}.{this.tableName} where id={userid} ")
        #data=this.cursor.fetchall()
        #print("Retrieved dataL")
        #for element in data:
        #    print(element)
        
        data=this.getRow(userid)

        #get Wins
        wins=data[1]
        
        #get Losses
        losses=data[2]
        if losses==0:
            losses=1
        #print("Data from wins at ("+str(userid)+"): "+str(wins))
        this.cursor.execute(f"update {this.databaseName}.{this.tableName} set wins={wins+1} where id={userid}")

        #update win/loss ratio
        w_l_ratio=float(wins+1)/float(losses)
        #print("New win/loss ratio is:"+str(w_l_ratio))
        this.cursor.execute(f"update {this.databaseName}.{this.tableName} set w_l_ratio={w_l_ratio} where id={userid}")
        this.database.commit()

    def addLoss(this,userid):
        data=this.getRow(userid)

        #get Wins
        wins=data[1]
        #get Losses
        losses=data[2]+1

        this.cursor.execute(f"update {this.databaseName}.{this.tableName} set losses={losses} where id={userid}")
        w_l_ratio=float(wins)/float(losses)
        this.cursor.execute(f"update {this.databaseName}.{this.tableName} set w_l_ratio={w_l_ratio} where id={userid}")
        this.database.commit()

    def getRow(this,userid):
        this.cursor.execute(f"select * from {this.databaseName}.{this.tableName} where id={userid} ")
        data=this.cursor.fetchall()
        return data[0] 

    def close(this):
        this.database.close()


def main():
    print("Main function from [Database.py] called!")
    db=DB()

    #db.addNewUser(1337)
    db.addWin(1337)
    db.addWin(1337)
    db.addWin(1337)
    db.addWin(1337)
    db.addLoss(1337)
    db.addLoss(1337)
    db.addLoss(1337)
    db.close()

if __name__=="__main__":
    main()
