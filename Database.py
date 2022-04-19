from asyncio.windows_events import NULL
import mariadb
import sys

class DB:
    def __init__(this):
        print("Connecting to the database...")
        file=open("db.creds","r")
        creds=[]
        while(True):
            line=file.readline()
            if not line:
                break
            #print("Read from db.creds: "+line)
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
            #print(this.columns)
            print("Connection successful!")
        except mariadb.Error as e:
            print(f"Error connecting to the database: {e}")
            sys.exit(1)

    
    #DB.addNewUser(self : DB, userid : int, guildid : int) : boolean
    #
    #Attempts to add a new user to the database.  If the user already has an entry with
    #the same guild, however, then the duplicate row will not be added.  Returns a boolean
    #based on this: if an entry is added, returns True.  Otherwise, returns False.
    def addNewUser(this,userid,guildid):
        this.cursor.execute(f"select * from {this.databaseName}.{this.tableName} where {this.columns[0]}='{userid}' and {this.columns[1]}='{guildid}'")
        data=this.cursor.fetchall()
        #print(f"Attempting to add user {userid} from {guildid} to database.\nDuplicate entries found:{len(data)}")

        if len(data)==0:
            this.cursor.execute(f"insert ignore into {this.databaseName}.{this.tableName} ({this.columns[0]},{this.columns[1]},{this.columns[2]},{this.columns[3]},{this.columns[4]},{this.columns[5]}) values ('{userid}','{guildid}','{0}','{0}','{0.0}','{0}')")
            this.database.commit()
            return True
        return False
    
    def removeUser(this,userid,guildid):
        this.cursor.execute(f"select * from {this.databaseName}.{this.tableName} where {this.columns[0]}={userid} and {this.columns[1]}={guildid}")
        data=this.cursor.fetchall()

        if len(data)!=0:
            this.cursor.execute(f"delete from {this.databaseName}.{this.tableName} where {this.columns[0]}={userid} and {this.columns[1]}={guildid}")
            this.database.commit()
            return True
        return False

    def removeAllofUser(this,userid):
        this.cursor.execute(f"select * from {this.databaseName}.{this.tableName} where {this.columns[0]}={userid}")
        data=this.cursor.fetchall()

        if len(data)!=0:
            this.cursor.execute(f"delete from {this.databaseName}.{this.tableName} where {this.columns[0]}={userid}")
            this.database.commit()
            return True
        return False

    def removeAllInServer(this,guildid):
        this.cursor.execute(f"select * from {this.databaseName}.{this.tableName} where {this.columns[1]}={guildid}")
        data=this.cursor.fetchall()

        if len(data)!=0:
            this.cursor.execute(f"delete from {this.databaseName}.{this.tableName} where {this.columns[1]}={guildid}")
            this.database.commit()
            return True
        return False
    
    def addWin(this,userid,guildid):
        rowFound,data=this.getRowById(userid,guildid)

        if rowFound:
            #get Wins
            wins=data[2]
            
            #get Losses
            losses=data[3]
            if losses==0:
                losses=1
            #print("Data from wins at ("+str(userid)+"): "+str(wins))
            this.cursor.execute(f"update {this.databaseName}.{this.tableName} set {this.columns[2]}={wins+1} where {this.columns[0]}={userid} and {this.columns[1]}={guildid}")

            #update win/loss ratio
            w_l_ratio=float(wins+1)/float(losses)
            #print("New win/loss ratio is:"+str(w_l_ratio))
            this.cursor.execute(f"update {this.databaseName}.{this.tableName} set {this.columns[4]}={w_l_ratio} where {this.columns[0]}={userid} and {this.columns[1]}={guildid}")
            this.database.commit()

    def addLoss(this,userid,guildid):
        rowFound,data=this.getRowById(userid,guildid)

        if rowFound:
            #get Wins
            wins=data[2]
            #get Losses
            losses=data[3]+1

            this.cursor.execute(f"update {this.databaseName}.{this.tableName} set {this.columns[3]}={losses} where {this.columns[0]}={userid} and {this.columns[1]}={guildid}")
            w_l_ratio=float(wins)/float(losses)
            this.cursor.execute(f"update {this.databaseName}.{this.tableName} set {this.columns[4]}={w_l_ratio} where {this.columns[0]}={userid} and {this.columns[1]}={guildid}")
            this.database.commit()

    def addMoyai(this,userid,guildid,amount):
        rowFound,data=this.getRowById(userid,guildid)

        if rowFound:
            this.cursor.execute(f"update {this.databaseName}.{this.tableName} set {this.columns[5]}={data[5]+amount} where {this.columns[0]}={userid} and {this.columns[1]}={guildid}")
            this.database.commit()

    def getRowById(this,userid,guildid):
        this.cursor.execute(f"select * from {this.databaseName}.{this.tableName} where {this.columns[0]}={userid} and {this.columns[1]}={guildid}")
        data=this.cursor.fetchall()

        if len(data)>0:
            return True,data[0]
        return False,NULL

    def getOrderBy(this,ind):
        this.cursor.execute(f"select * from {this.databaseName}.{this.tableName} order by {this.columns[ind]} desc")
        return this.cursor.fetchall()

    def getOrderByWins(this,guildid):
        this.cursor.execute(f"select * from {this.databaseName}.{this.tableName} where {this.columns[1]}={guildid} order by {this.columns[2]} desc, {this.columns[3]} asc limit 5")
        return this.cursor.fetchall()

    def getOrderByWinLossRatio(this,guildid):
        this.cursor.execute(f"select * from {this.databaseName}.{this.tableName} where {this.columns[1]}={guildid} order by {this.columns[4]} desc, {this.columns[2]} asc, {this.columns[3]} desc limit 5")
        return this.cursor.fetchall()

    def getOrderByLosses(this,guildid):
        this.cursor.execute(f"select * from {this.databaseName}.{this.tableName} where {this.columns[1]}={guildid} order by {this.columns[3]} desc, {this.columns[2]} asc limit 5")
        return this.cursor.fetchall()

    def getOrderByMoyai(this,guildid):
        this.cursor.execute(f"select * from {this.databaseName}.{this.tableName} where {this.columns[1]}={guildid} order by {this.columns[5]} desc, {this.columns[2]} desc, {this.columns[3]} asc limit 5")
        return this.cursor.fetchall()

    def clearTestData(this):
        this.cursor.execute(f"delete from {this.databaseName}.{this.tableName} where {this.columns[1]}=1")
        this.database.commit()

    def close(this):
        this.database.close()
#END CLASS: DB

#EVERYTHING BELOW THIS LINE IS ONLY USED TO TEST THE CODE ABOVE.
#---------------------------------------------------------------

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
        db.addMoyai(1337,1,3)
    
    added=db.addNewUser(6669,1)
    if added:
        setWins(db,6669,1,10)
        setLosses(db,6669,1,6)
        db.addMoyai(6669,1,1)

    added=db.addNewUser(9001,1)
    if added:
        setWins(db,9001,1,5)
        setLosses(db,9001,1,4)
        db.addMoyai(9001,1,3)

    rows=db.getOrderBy(2) #sort by # of wins
    rowObs=[]
    for row in rows:
        rowObs.append(Row(row[0],row[1],row[2],row[3],row[4],row[5]))

    print("User data sorted by wins:")
    for el in rowObs:
        print(el.toString())

    rows=db.getOrderByWins(1)
    print("Generating user data from guild 1, sorted by wins (max:5)\n"+generateLeaderboardData(rows))

    rows=db.getOrderByMoyai(1)
    print("Generating user data from guild 1, sorted by Moyai (max:5)\n"+generateLeaderboardData(rows))


    prompt="Would you like to delete this test data? (enter either: [Y]/[N])"    
    while True:
        print(prompt)
        response=input().strip().lower()
        if response=="y":
            db.clearTestData()
            print("Test data cleared!")
            break
        elif response=="n":
            print("Test data will remain in the database.")
            break
        else:
            prompt="Input error: enter either [Y] or [N]."

    db.close()

def generateLeaderboardData(data):
    outputString="{:^4s}|{:^25s}|{:^6s}|{:^6s}|{:^9s}|{:^5s}\n{hf:-^4s}+{hf:-^25s}+{hf:-^6s}+{hf:-^6s}+{hf:-^9s}+{hf:-^5s}\n".format("Pos.","User","Wins","Losses","W/L Ratio","Moyai",hf="")
    for i in range(len(data)):
        outputString+="{:>4d}|".format(i+1)
        outputString+="{:^25d}|{:^6d}|{:^6d}|{:^9.2f}|{:^5d}\n".format(data[i][0],data[i][2],data[i][3],data[i][4],data[i][5])
    return outputString

def setWins(db,id,guild,amount):
    for i in range(amount):
        db.addWin(id,guild)
def setLosses(db,id,guild,amount):
    for i in range(amount):
        db.addLoss(id,guild)

if __name__=="__main__":
    main()
