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
            this.cursor.execute(f"select * from {this.databaseName}.{this.tableName}")
            this.columns=[i[0]for i in this.cursor.description]
            print(this.columns)
        except mariadb.Error as e:
            print(f"Error connecting to the database: {e}")
            sys.exit(1)

    
    #DB.addNewUser(self : DB, userid : int, guildid : int) : boolean
    #
    #Attempts to add a new user to the database.  If the user already has an entry with
    #a guild, however, then the potential-duplicate row will not be added.
    #If an entry is added, returns True.  Otherwise, returns False.
    def addNewUser(this,userid,guildid):
        this.cursor.execute(f"select * from {this.databaseName}.{this.tableName} where {this.columns[0]}={userid} and {this.columns[1]}={guildid}")
        data=this.cursor.fetchall()

        if len(data)==0:
            this.cursor.execute(f"insert ignore into {this.databaseName}.{this.tableName} ({this.columns[0]},{this.columns[1]},{this.columns[2]},{this.columns[3]},{this.columns[4]},{this.columns[5]}) values ('{userid}','{guildid}','{0}','{0}','{0.0}','{0}')")
            this.database.commit()
            return True
        return False
    
    def addWin(this,userid,guildid):
        data=this.getRowById(userid,guildid)

        #get Wins
        wins=data[2]
        
        #get Losses
        losses=data[3]
        if losses==0:
            losses=1
        #print("Data from wins at ("+str(userid)+"): "+str(wins))
        this.cursor.execute(f"update {this.databaseName}.{this.tableName} set wins={wins+1} where id={userid} and guild={guildid}")

        #update win/loss ratio
        w_l_ratio=float(wins+1)/float(losses)
        #print("New win/loss ratio is:"+str(w_l_ratio))
        this.cursor.execute(f"update {this.databaseName}.{this.tableName} set w_l_ratio={w_l_ratio} where id={userid} and guild={guildid}")
        this.database.commit()

    def addLoss(this,userid,guildid):
        data=this.getRowById(userid,guildid)

        #get Wins
        wins=data[2]
        #get Losses
        losses=data[3]+1

        this.cursor.execute(f"update {this.databaseName}.{this.tableName} set losses={losses} where id={userid} and guild={guildid}")
        w_l_ratio=float(wins)/float(losses)
        this.cursor.execute(f"update {this.databaseName}.{this.tableName} set w_l_ratio={w_l_ratio} where id={userid} and guild={guildid}")
        this.database.commit()

    def addMoyai(this,userid,guildid,amount):
        data=this.getRowById(userid,guildid)

        this.cursor.execute(f"update {this.databaseName}.{this.tableName} set moyai={data[5]+amount} where id={userid} and guild={guildid}")
        this.database.commit()

    def getRowById(this,userid,guildid):
        this.cursor.execute(f"select * from {this.databaseName}.{this.tableName} where id={userid} and guild={guildid}")
        data=this.cursor.fetchall()
        return data[0]

    def getOrderBy(this,ind):
        this.cursor.execute(f"select * from {this.databaseName}.{this.tableName} order by {this.columns[ind]} desc")
        return this.cursor.fetchall()

    def close(this):
        this.database.close()

class Row:
    def __init__(this,id,guild,wins,losses,wlratio,moyai):
        this.id=id
        this.guild=guild
        this.wins=wins
        this.losses=losses
        this.wlratio=wlratio
        this.moyai=moyai

    def toString(this):
        return "id: "+str(this.id)+" | guild: "+str(this.guild)+" | wins: "+str(this.wins)+" | losses: "+str(this.losses)+" | w/l_ratio: "+str(this.wlratio)+" | Moyai:"+str(this.moyai)


def main():
    print("Main function from [Database.py] called!")

    db=DB()

    added=db.addNewUser(1337,1)
    if added:
        setWins(db,1337,1,5)
        setLosses(db,1337,1,3)
    
    added=db.addNewUser(6669,1)
    if added:
        setWins(db,6669,1,10)
        setLosses(db,6669,1,6)

    added=db.addNewUser(9001,1)
    if added:
        setWins(db,9001,1,5)
        setLosses(db,9001,1,4)

    rows=db.getOrderBy(2) #sort by # of wins
    rowObs=[]
    for row in rows:
        rowObs.append(Row(row[0],row[1],row[2],row[3],row[4],row[5]))

    print("User data sorted by wins:")
    for el in rowObs:
        print(el.toString())

    db.close()

def setWins(db,id,guild,amount):
    for i in range(amount):
        db.addWin(id,guild)
def setLosses(db,id,guild,amount):
    for i in range(amount):
        db.addLoss(id,guild)

if __name__=="__main__":
    main()
