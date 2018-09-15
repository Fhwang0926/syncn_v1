process.chdir(__dirname);
require('app-module-path').addPath(__dirname);
require('lib/common')
let mq = require('lib/channel');
let express = require('express');
let middleware = express();
let forge = require('node-forge')
mq.open().then((ch) => {
    
    

    middleware.post('/email', (ctx) => {
        console.log(ctx.request)
        let sha = forge.md.sha256.create().update('The quick brown fox jumps over the lazy dog');
        console.log("sha : ", sha)
        let md = forge.md.md5.create().update(sha).digest().toHex();
        console.log("sha : ", md)
        
        // ch.send("mail", { type : auth, headers : { to : req.body.to } })
        res.send('Hello World!');
    });


    middleware.listen(9759, () => {
        console.log('start auth service');
    });
}).catch(e => {
    print(e)
})