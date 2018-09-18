process.chdir(__dirname);
require('app-module-path').addPath(__dirname);
require('lib/common')

let mq = require('lib/channel');
let ready = mq.open()

let consumer = () => {
    ready.then((ch) => {
        console.log("mail service start")
        mq.consume('mail', (msg) => {
            console.log(msg)
            mq.ack(msg)
        })
    }).catch(e => {
        print(e)
    })
}

// console.log(Math.floor(Math.random() * 10000) + 1)

// let amqp = require("amqplib/callback_api")
// amqp.connect('amqp://syncn:syncn@jis5376.iptime.org:5672/syncn', function (err, conn) {
//     if(err) { return console.log(err) }
//     conn.createChannel(function (err, ch) {
//         if(err) { return console.log(err) }
//         var q = 'hello';

//         ch.assertQueue(q, {
//             durable: false
//         });
//         // Note: on Node 6 Buffer.from(msg) should be used
//         ch.sendToQueue(q, new Buffer('Hello World!'));
//         console.log(" [x] Sent 'Hello World!'");c
//     });
// });
let request = require('request');
let sendPost = () => {
    
    console.log("send post")
    request.post('http://syncn.club:9759/code/', { form : 'hdh0926@naver.com' }, (e, res, body) => {
        
        body = JSON.parse(body);
        console.log(res.statusCode, body)
        let url = 'http://syncn.club:9759/account/' + body.res;
        console.log("url : ", url)
        let auth = () => request.get(url, (e, res, body) => {
            body = JSON.parse(body);
            console.log(res.statusCode, body);
            setTimeout(auth, 3000);
        });
        auth();
    });
    
    
}


sendPost();
// consumer();