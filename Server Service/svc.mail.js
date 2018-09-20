process.chdir(__dirname);
require('app-module-path').addPath(__dirname);
require('lib/common')
let mq = require('lib/channel');
let mail = require('lib/sendmail');

mq.open().then((ch) => {
    console.log("Mail service start")
    ch.consume('mail', async msg => {
        rs = await mail.send_login(msg.properties.headers.to)
        mq.ack(msg)
    })
}).catch(e => {
    print(e)
})