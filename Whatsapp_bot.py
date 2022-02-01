from flask import Flask, request , session
from twilio.twiml.messaging_response import Message, MessagingResponse
SECRET_KEY = 'whatsapp_bot_by_mayhul'
lst = []
data = {
    'a':{
            "nmc":[{"1": 48,"2" : 50.4,"3" : 60,"4":61.2,"5":72},
                    {"1": 20,"2" : 23,"3" : 25 , "4":26 ,"5":27,"6":28,"7":30,"8":35,"9":40,"10":45}],


            "lfp":[{"1": 48,"2" : 51.2,"3" : 60.8,"4": 64,"5":73.6},
                    {"1": 12,"2": 18,"3" : 24,"4" : 30,"5" : 36,"6" : 42}]  
        },
    'b':"We have range of both NMC (LiNiMnCoO2) & LFP (LiFePO4) storage battery packs. For details & best OEM price mail us at info@likraft.com.",
    'c': '''We have complete range of Li-ion NMC (LiNiMnCoO2) & LFP (LiFePO4) cells.

NMC (LiNiMnCoO2):
BAK 18650 2550 mAh 3C
BAK 18650 2900 mAh 3C
BAK 21700 5000 mAh 3C
GP 18650 2500 mAh 3C
HLY 26650 5000 mAh 3C
DHR 18650 2600 mAh 3C
DHR 18650 1800 mAh 1C
DHR 18650 2000 mAh 1C
DHR 18650 2200 mAh 1C
DHR 18650 2500 mAh 1C
DHR 18650 2600 mAh 1C

LFP (LiFePO4):
FbTech 32650 6000 mAh EV
FbTech 32650 6000 mAh Storage
HX 32650 6000 mAh EV
HX 32650 6000 mAh Storage
Welson 32650 6000 mAh EV
Welson 32650 6000 mAh Storage

For best prices mail us at info@likraft.com with you contact details.'''
}

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def hello():
    return "whatsapp_bot_server"

@app.route("/sms", methods=['POST'])
def sms_reply():
    global lst
    counter = session.get('counter', 0)
    msg = request.form.get('Body').lower()
    resp = MessagingResponse()

    if counter==0:#-----------------------------------------------------------------------------------
        resp.message('''
        Welcome to LiKraft !!
One of the leading Lithium ion Battery Packs OEM. 

How can I help you, please choose from the below list :

A) Electric Scooter Li-ion Battery.
B) Storage Li-ion Battery for Solar.
C) Li-ion Cells.
        ''')
    if counter==1:#-----------------------------------------------------------------------------------
        
        if(msg == "a"):
            resp.message('''
Which Chemistry Li-ion Battery:
1) NMC (LiNiMnCoO2)
2) LFP (LiFePO4)''')
        elif(msg == "b"):
            resp.message(data['b'])
            counter = -1
        elif(msg == "c"):
            resp.message(data['c'])
            counter = -1
        else:
            resp.message('''
        Welcome to LiKraft !!
One of the leading Lithium ion Battery Packs OEM. 

How can I help you, please choose from the below list :

A) Electric Scooter Li-ion Battery.
B) Storage Li-ion Battery for Solar.
C) Li-ion Cells.
        ''')
            counter = 0

    if counter==2:#-----------------------------------------------------------------------------------
        
        if msg == '1' :
            lst.append(msg)
            resp.message('''
NMC (LiNiMnCoO2):
1) 48.0V (13S)
2) 50.4V (14S)
3) 60.0V (16S)
4) 61.2V (17S)
5) 72.0V (20S)
''')
        elif msg == '2':
            lst.append(msg)
            resp.message('''
LFP (LiFePO4):
1) 48.0V (15S)
2) 51.2V (16S)
3) 60.8V (19S)
4) 64.0V (20S)
5) 73.6V (23S)''')
            
        else:
            resp.message('''
Which Chemistry Li-ion Battery:
1) NMC (LiNiMnCoO2)
2) LFP (LiFePO4)''')
            counter = 1

    if counter==3:#-----------------------------------------------------------------------------------
        
        if msg in  ["1","2","3","4","5"] and lst[0] == '1':
            lst.append(msg)
            resp.message('''
NMC (LiNiMnCoO2):
1) 20AH
2) 23AH
3) 25AH
4) 26AH
5) 27AH
6) 28AH
7) 30AH 
8) 35AH
9) 40AH
10) 45AH ''')
        elif msg in  ["1","2","3","4","5"] and lst[0] == '2':
            lst.append(msg)
            resp.message('''
LFP (LiFePO4):
1) 18AH
2) 24AH
3) 30AH
4) 36AH
5) 42AH''')
        else:
            if lst[0] == '1':
                resp.message('''
NMC (LiNiMnCoO2):
1) 48.0V (13S)
2) 50.4V (14S)
3) 60.0V (16S)
4) 61.2V (17S)
5) 72.0V (20S)
''')        
            elif lst[0] == '2':
                resp.message('''
LFP (LiFePO4):
1) 48.0V (15S)
2) 51.2V (16S)
3) 60.8V (19S)
4) 64.0V (20S)
5) 73.6V (23S)''')
            
            counter = 2 

    if counter==4:#-----------------------------------------------------------------------------------
        if  msg in ["1","2","3","4","5","6","7","8","9","10"] and lst[0] == '1':
            lst.append(msg)
            price = data['a']['nmc'][0][lst[1]] * data['a']['nmc'][1][lst[2]]  * 15
            resp.message(f'''
You choose  {data['a']['nmc'][0][lst[1]]}V {data['a']['nmc'][1][lst[2]]}AH 
This Battery reference price Rs {format(price , '.2f')}

For more details & best OEM price mail us with required monthly quantity at info@likraft.com.''')
            resp.message('''
Type 'hi' to start again.
Type 'end' to stop.
            ''')
            lst =  []
        elif msg in ["1","2","3","4","5"] and lst[0] == '2':
            lst.append(msg)
            price = data['a']['lfp'][0][lst[1]] * data['a']['lfp'][1][lst[2]]  * 13
            resp.message(f'''
You choose  {data['a']['lfp'][0][lst[1]]}V {data['a']['lfp'][1][lst[2]]}AH 
This Battery reference price Rs {format(price , '.2f')}

For more details & best OEM price mail us with required monthly quantity at info@likraft.com.''')
            resp.message('''
Type 'hi' to start again.
Type 'end' to stop.
            ''')
            lst =  []
        else:
            if lst[0] == '1':
                resp.message('''
NMC (LiNiMnCoO2):
1) 20AH
2) 23AH
3) 25AH
4) 26AH
5) 27AH
6) 28AH
7) 30AH 
8) 35AH
9) 40AH
10) 45AH ''')    
            elif lst[0] == '2':
                resp.message('''
LFP (LiFePO4):
1) 18AH
2) 24AH
3) 30AH
4) 36AH
5) 42AH''')
            counter = 3

    if counter >= 5:
        if msg == "hi":
            counter = 0
            resp.message("welcome back!!")
            resp.message('''
        Welcome to LiKraft !!
One of the leading Lithium ion Battery Packs OEM. 

How can I help you, please choose from the below list :

A) Electric Scooter Li-ion Battery.
B) Storage Li-ion Battery for Solar.
C) Li-ion Cells.
        ''')
        else:
            counter = -1
            resp.message("Bye!")


    counter = counter + 1
    session['counter'] =counter
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
