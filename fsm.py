from transitions.extensions import GraphMachine

from utils import send_text_message, send_image_url, send_button_message

import datetime
import requests
import urllib
import re
import ast

class TocMachine(GraphMachine):
    month = 1
    day = 1
    num = 1
    num_games = 0
    team = ""
    today_scores = {}

    team_id = {'BOS':'1610612738', 'NET':'1610612751', 'KNICK':'1610612752',
            '76ER':'1610612755', 'RAPTOR':'1610612761', 'BULL':'1610612741',
            'CAVALIER':'1610612739', 'PISTON':'1610612765', 'PACER':'1610612754',
            'BUCK':'1610612749', 'HAWK':'1610612737', 'HORNET':'1610612766',
            'HEAT':'1610612748', 'MAGIC':'1610612753', 'WIZARD':'1610612764',
            'NUGGET':'1610612743', 'TIMBERWOLVE':'1610612750', 'THUNDER':'1610612760',
            'TRAIL BLAZER':'1610612757', 'JAZZ':'1610612762', 'WARRIOR':'1610612744',
            'CLIPPER':'1610612746', 'LAKER':'1610612747', 'SUN':'1610612756',
            'KING':'1610612758', 'MAVERICK':'1610612742', 'ROCKET':'1610612745',
            'GRIZZLIE':'1610612763', 'PELICAN':'1610612740', 'SPUR':'1610612759'
            }

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            ignore_invalid_triggers=True,
            model=self,
            **machine_configs
        )

    def is_going_to_state0(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'scores'
        return False

    def is_going_to_state1(self, event):
        if event.get("message"):
            text = event['message']['text']
            if( int(text) < 0 or int(text) > 12):
                sender_id = event['sender']['id']
                send_text_message(sender_id, "您輸入的月份格式不符")
                return False
            else:
                self.month = int(text)
                return True
        return False

    def is_going_to_state2(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'today scores'
        return False

    def is_going_to_state3(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'team'
        return False

    def is_going_to_state4(self, event):
        if event.get("message"):
            text = event['message']['text']
            self.date = int(text)
            return True
        return False

    def is_going_to_state5(self, event):
        if event.get("message"):
            text = event['message']['text']
            self.num = int(text)
            return True
        return False

    def is_going_to_state6(self, event):
        if event.get("message"):
            text = event['message']['text']
            self.team = text
            return True
        return False

    def on_enter_state1(self, event):
        print("I'm entering state1")

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "請輸入想要查詢的是幾日的賽事")
    
    def on_enter_state0(self, event):
        print("I'm entering state0")

        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "請輸入想要查詢的是幾月的賽事")

    def on_enter_state2(self, event):
        print("I'm entering state2")
        self.month = datetime.datetime.now().month
        self.day = datetime.datetime.now().day

        url = "https://stats.nba.com/scores/" #+str(self.month)+"/"+str(self.day)+"/2018"
        with urllib.request.urlopen(url) as urls:
            html = urls.read()
        str1 = "window.nbaStatsLineScore"
    
        str_html = str(html, encoding = "utf-8")
    
        index = str_html.find(str1)
        new = str_html[index:]
        
        index2 = new.find(";")
        new2 = new[27:index2]

        self.today_scores = ast.literal_eval(new2)
        self.num_games = int((len(self.today_scores) - 1)/2)
        response_str = ""
        for i in range(0, self.num_games):
            response_str = response_str + str(i+1) + "\n" 
            response_str = response_str + self.today_scores[i*2]['TEAM_ABBREVIATION'] + " " + str(self.today_scores[i]['PTS']) + "\n"
            response_str = response_str + self.today_scores[i*2+1]['TEAM_ABBREVIATION'] + " " + str(self.today_scores[i*2+1]['PTS']) + "\n"
            

        sender_id = event['sender']['id']
        send_text_message(sender_id, response_str)
        send_text_message(sender_id, "想要看哪場的各節比分?")
    
    def on_enter_state3(self, event):
        print("I'm entering state3")

        sender_id = event['sender']['id']
        send_text_message(sender_id, "想看哪個球隊的目前戰績?")
    
    def on_enter_state4(self, event):
        print("I'm entering state4")
        url = "https://stats.nba.com/scores/"+str(self.month)+"/"+str(self.day)+"/2018"
        with urllib.request.urlopen(url) as urls:
            html = urls.read()
        str1 = "window.nbaStatsLineScore"
    
        str_html = str(html, encoding = "utf-8")
    
        index = str_html.find(str1)
        new = str_html[index:]
        
        index2 = new.find(";")
        new2 = new[27:index2]

        self.today_scores = ast.literal_eval(new2)
        self.num_games = int((len(self.today_scores) - 1)/2)
        response_str = ""
        for i in range(0, self.num_games):
            response_str = response_str + str(i+1) + "\n" 
            response_str = response_str + self.today_scores[i*2]['TEAM_ABBREVIATION'] + " " + str(self.today_scores[i]['PTS']) + "\n"
            response_str = response_str + self.today_scores[i*2+1]['TEAM_ABBREVIATION'] + " " + str(self.today_scores[i*2+1]['PTS']) + "\n"
            

        sender_id = event['sender']['id']
        send_text_message(sender_id, response_str)
        send_text_message(sender_id, "想要看哪場的各節比分?")

    
    def on_enter_state5(self, event):
        print("I'm entering state5")

        response_str = ""

        team_A = self.today_scores[(self.num - 1)*2]
        team_B = self.today_scores[(self.num - 1)*2 + 1]
        response_str = "TEAM   1   2   3   4   ALL\n"
        response_str = response_str + team_A['TEAM_ABBREVIATION'].ljust(5) + " " + str(team_A['PTS_QTR1']).ljust(2) + " " + str(team_A['PTS_QTR2']).ljust(2) + " " + str(team_A['PTS_QTR3']).ljust(2) + " " + str(team_A['PTS_QTR4']).ljust(2) + " " + str(team_A['PTS']) + "\n"
        response_str = response_str + team_B['TEAM_ABBREVIATION'].ljust(5) + " " + str(team_B['PTS_QTR1']).ljust(2) + " " + str(team_B['PTS_QTR2']).ljust(2) + " " + str(team_B['PTS_QTR3']).ljust(2) + " " + str(team_B['PTS_QTR4']).ljust(2) + " " + str(team_B['PTS'])

        sender_id = event['sender']['id']
        send_text_message(sender_id, response_str)
        send_button_message(sender_id, "https://stats.nba.com/game/"+team_A['GAME_ID'], "")
        send_text_message(sender_id, "請輸入\'scores\' 或 \'today scores\' 或 \'team\'")
        self.go_back()
    
    def on_enter_state6(self, event):
        print("I'm entering state6")
        url = "https://stats.nba.com/team/" + self.team_id[self.team]
        with urllib.request.urlopen(url) as urls:
            html = urls.read()
        str1 = "Record"
    
        str_html = str(html, encoding = "utf-8")
    
        index = str_html.find(str1)
        new = str_html[index:index+200]

        regex = re.compile(r'\d* - \d*')
        match = regex.search(new)
        standings = match.group(0)

        regex2 = re.compile(r'\d+')
        match2 = regex2.findall(standings)
        win = match2[0]
        lose = match2[1]

        response_str = win + "W : " + lose + "L\n"

        sender_id = event['sender']['id']
        send_image_url(sender_id, "http://content.sportslogos.net/logos/6/213/thumbs/slhg02hbef3j1ov4lsnwyol5o.gif")
        send_text_message(sender_id, response_str)
        send_text_message(sender_id, "請輸入\'scores\' 或 \'today scores\' 或 \'team\'")

        self.go_back()
    
    '''
    send_image_url(sender_id, "https://enjoy123.tw/wp-content/uploads/2018/10/Google-logo.jpg")
    send_text_message(sender_id, "enter state4")
    send_button_message(sender_id, "Try URL", "")
    self.go_back()

    http://www.sportslogos.net/teams/list_by_league/6/National_Basketball_Association/NBA/logos/
    '''

