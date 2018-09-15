process.chdir(__dirname);
require('app-module-path').addPath(__dirname);
require('lib/common')

let mq = require('lib/channel');
let ready = mq.open()

ready.then(() => {
    // _.forEach([1,2,3,4,5], r => {
    //     mq.send("test", Buffer.from(r.toString))
    // });
    console.log("mail service start")
    mq.consume('mail', (rs) => {
        console.log(rs)
    })
}).catch(e => {
    print(e)
})
console.log(Math.floor(Math.random() * 10000) + 1)

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
//         console.log(" [x] Sent 'Hello World!'");
//     });
// });