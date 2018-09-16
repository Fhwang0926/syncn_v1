process.chdir(__dirname);
require('app-module-path').addPath(__dirname);
require('lib/common')

let mq = require('lib/channel');
let ready = mq.open()
const { spawnSync } = require('child_process')
ready.then((ch) => {
    console.log("account service start")
    ch.consume('account', (msg) => {
        
        let info = JSON.parse(msg.content.toString());
        console.log(info)
        let add_user = spawnSync('rabbitmqctl', ['add_user', info.id, info.pw]);
        let set_permissions = spawnSync('rabbitmqctl', ['set_permissions', "-p", "/syncn", info.id, info.q, info.q]);
        console.log(`stderr: ${add_user.stderr.toString()}`);
        console.log(`stdout: ${add_user.stdout.toString()}`);
        console.log(`stderr: ${set_permissions.stderr.toString()}`);
        console.log(`stdout: ${set_permissions.stdout.toString()}`);
        print("created user")
        mq.ack(msg)
    })
}).catch(e => {
    print(e)
})