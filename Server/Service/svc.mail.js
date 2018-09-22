process.chdir(__dirname);
require('app-module-path').addPath(__dirname);
require('lib/common')
let mq = require('lib/channel');
let mail = require('lib/sendmail');

mq.open().then((ch) => {
    console.log("Mail service start")
    ch.consume('mail', async msg => {
        if (msg.properties.type == "" || msg.properties.type == "default") {
            rs = await mail.send(JSON.parse(msg.content.toString()))
        } else {
            // rs = await mail.send(msg.properties.headers.to, msg.properties.headers.title)
            print("support default")
        }
        mq.ack(msg)
    })
}).catch(e => {
    print(e)
})