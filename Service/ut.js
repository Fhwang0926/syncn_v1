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

let sendPost = () => {
    let request = require('request');
    console.log("send post")
    request.post(
        'http://localhost:9759/code',
        { form : 'hdh0926@naver.com' },
        (error, response, body) => {
            if (!error && response.statusCode == 200) {
                // console.log("res", response, response.statusCode);
                console.log(body)
            }
        }
    );
    setTimeout(() => {
        sendPost()
    }, 30000);
}


sendPost();
// consumer();