process.chdir(__dirname);
require('app-module-path').addPath(__dirname);
require('lib/common')
let mq = require('lib/channel');
let mail = require('lib/sendmail');
let ready = mq.open()


ready.then((ch) => {
    console.log("Mail service start")
    ch.consume('mail', async msg => {
        let type = msg.properties.type
        let ack = false;
        let content = msg.content.toString();
        if (type == 'login') {
            print('type : ', type);
            ack = true;
        }
        console.log(type + ' auth', (type == 'auth'), content)
        if (type == 'auth') {
            
            let to = msg.properties.headers.to;
            await mail.send_auth(to)
            ack = true;
        }
        ack ? mq.ack(msg) : print("No ack "+type, time());
    })
}).catch(e => {
    print(e)
})