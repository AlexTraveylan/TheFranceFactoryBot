import gspread
from googleapiclient.discovery import build
from google.oauth2 import service_account
from models.Message_guild import Message_guild
from models.PowerClash import PowerClash
from models.Result_clash import Result_clash
from varEnviron.environ import *


class GoogleSheet:

    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # clash Ennemies from settings/setClash.recupPowers -> list of PowerClash (see model on models.PowerClash)
    def writeInSheetForSetClash(clashEnnemiesPowers: list[PowerClash]):

        # Format tabClash [[name, power1, power2, power3 ], .. ]
        tabClash=[]
        for ennemy in clashEnnemiesPowers:
            id_member = ennemy.id_member
            power1 = ennemy.powers[0]
            power2 = ennemy.powers[1]
            power3 = ennemy.powers[2]
            tabClash.append([id_member, power1, power2, power3])

        request = GoogleSheet.sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Bot LOG!A2", valueInputOption="USER_ENTERED", body={"values": tabClash})
        request.execute()
    
    def writeInSheetForGetClashDatas(results_clash : list[Result_clash]) -> str:

        results_clash = list(map(lambda x:x.toArray(), results_clash))

        oldClashLogs = GoogleSheet.sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="Bot LOG!BL:BM").execute()['values'][1:]
        oldClashLogs = list(filter(lambda x : x[0] != '', oldClashLogs))
        oldClashLogs = list(map(lambda x : [int(y) for y in x], oldClashLogs))

        currentLine = max(oldClashLogs, key= lambda x : x[0])
        # currentLine [last Seq, last Line]
        datas = list(filter(lambda x : x[-1] > currentLine[0], results_clash))
    
        request = GoogleSheet.sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"Bot LOG!BF{currentLine[1]+1}", valueInputOption="USER_ENTERED", body={"values": datas})
        request.execute()

        return f"`{len(datas)} nouvelles attaques enregistrées, pour un total de {currentLine[1] + len(datas) - 2 }`"
    
    def recupLastSeqFromGuildChat() -> int:

        last_message_recorded = GoogleSheet.sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range="Bot LOG!B28:C28").execute()['values'][0][1]
        return int(last_message_recorded)
    
    def updateLastSeqFromGuildChat(newseq: int):

        datas = [["last_seq_guild", newseq]]
        request = GoogleSheet.sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"Bot LOG!B28", valueInputOption="USER_ENTERED", body={"values": datas})
        request.execute()
    
    def addOneToSeqForGuildChat():

        GoogleSheet.updateLastSeqFromGuildChat(GoogleSheet.recupLastSeqFromGuildChat())


    






