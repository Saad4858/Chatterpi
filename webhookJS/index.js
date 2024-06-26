const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express().use(bodyParser.json());
const token ="";

app.listen(8000, () => 
    console.log('Webhook server is listening, port 8000')
);

app.get('/webhook', (req, res) => {
    let mode = req.query['hub.mode'];
    let challenge =req.query['hub.challenge'];
    let verify = req.query['hub.verify_token'];
    const mytoken = "chatterpi";
    if (mode && verify ){
        if (mode === 'subscribe' && verify === mytoken){
            console.log('webhook verified');
            res.status(200).send(challenge);
        } else {
            console.log('webhook failed');
            res.sendStatus(403);
        }

    }
});

app.post('/webhook', (req, res) => {
    let body = req.body;
    console.log(JSON.stringify(body));
    if(body.object){
        if (body.entry &&
            body.entry[0].changes &&
            body.entry[0].changes[0].value.message &&
            body.entry[0].changes[0].value.message[0]){
                let phone_number_id = body.entry[0].challenge[0].value.metadata.phone_number_id;
                let from = body.entry[0].changes[0].value.messages[0].from;
                let msg = body.entry[0].changes[0].value.message[0].messages[0].text.body;

                axios({
                    method: 'POST',
                    url: 'https://graph.facebook.com/v13.0/'+phone_number_id+'/messages?access_token='+token,
                    data : {
                       messaging_product: 'whatsapp',
                       to: from,
                       text :{
                            body: "Hello, I am a bot. I am currently not available. Please try again later."
                       }

                    },
                    headers : {
                        "Content-Type": "application/json"
                    }
                    
                })
                res.sendStatus(200);
            }
            else {
                console.log('webhook failed');
                res.sendStatus(403);
            }
    }
});
