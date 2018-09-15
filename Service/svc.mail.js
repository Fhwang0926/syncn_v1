process.chdir(__dirname);
require('app-module-path').addPath(__dirname);
require('lib/common')
let mq = require('lib/channel');
let mail = require('lib/sendmail');
let ready = mq.open()


ready.then((ch) => {
    console.log("Mail service start")
    ch.consume('mail', async msg => {
        // let type = msg.properties.type
        
        let to = msg.properties.headers.to;
        let rs = await mail.send_auth(to)
        
        mq.ack(msg)
    })
}).catch(e => {
    print(e)
})