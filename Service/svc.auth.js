process.chdir(__dirname);
require('app-module-path').addPath(__dirname);
require('lib/common')
let fs = require('fs')
let mq = require('lib/channel');
let mail = require('lib/sendmail');
let forge = require('node-forge')
let regx = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,5}$/i;
let auth = {}
let auth_link = '';
let auth_exfire = 1000 * 60 * 3; // expire 3 min

fs.readFile('mail_format/auth_link.html', (err, data) => {
    if (err) throw err;
    auth_link = data.toString();

});

let auth_cleaner = () => {
    print('auth cleaner running', auth)
    _.forEach(_.keys(auth), key => {
        if (auth[key].expire < timestamp()) { auth = _.omit(auth, [key]) }
    })
    setTimeout(() => {
        auth_cleaner()
    }, auth_exfire/3 );
}

let auth_generator = (email) => {
    let sha256_email = forge.md.sha256.create().update(email).update(email.split("@")[0]);
    let queue_name = `c.${forge.md.md5.create().update(sha256_email).digest().toHex()}.${timestamp()}`;
    let otp = forge.md.md5.create().update(sha256_email + timestamp()).digest().toHex();
    let id = forge.md.md5.create().update(queue_name).digest().toHex();
    auth[otp] = { status: false, expire: timestamp() + auth_exfire, info: { q: queue_name, id: id, pw: otp }} // expire 5 min
    print("auth gen ok", otp);
    return otp;
}

let post = (req, res) => {
    let data = '';
    
    req.on('data', (raw) => {
        data += raw.toString();
    });

    req.on('socket', (s) => {
        s.setTimeout(3);
        s.on('timeout', () => {
            req.abort();
        });
    })


    req.on('end', () => {
        try {
            let email = data.match(regx)[0];
            if (email == null) { return; }
            
            let otp = auth_generator(email);
            mail.send_auth(email, otp)

            
            res.on('error', (e) => {
                throw e
            });
            
            res.writeHead(200, {'Content-Type': 'application/json'})
            res.end(JSON.stringify(_.assign(_.pick(req, ['headers', 'method', 'url']), { res : 'ok.'+otp })))


        } catch (e) {
            console.log(e)
            res.writeHead(404);
            res.end();
        }
        
    });
}

let get = (req, res) => {
    try {
        let code = req.url.split("/");
        if (code[1] == 'code') { // md5
            if (_.has(auth, code[2])) {
                res.writeHead(200); res.write(auth_link);
                auth['ok.' + code[2]] = { info: auth[code[2]].info, status: true, expire: timestamp() + auth_exfire } // expire 3 min
                auth = _.omit(auth, code[2])
                console.log(auth['ok.' + code[2]], "222")
            } else {
                res.writeHead(404);
                res.write(JSON.stringify({ e: "Expired this URL" }));
            }
        }
        if (code[1] == 'account') { // ok.md5
            if (_.has(auth, code[2]) && auth[code[2]].status) {
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.write(JSON.stringify({ res: auth[code[2]].info }));
                
                print("auth!!!!!, " + code[2], JSON.stringify(auth[code[2]]))
                auth = _.omit(auth, code[2])
                mq.publish("cmd", "account", JSON.stringify(_.pick(auth[code[2]], ['id', 'pw', 'q']))) //send account service
            } else {
                res.writeHead(404, { 'Content-Type': 'application/json' });
                res.write(JSON.stringify({ e: "Check Email auth URL, Or maybe it was expireded" }));
            }
        }
        res.end();  
    } catch (e) {
        console.log(e)
        res.writeHead(404);
        res.end();
    }
    
    req.on('socket', (s) => {
        s.setTimeout(3);
        s.on('timeout', () => {
            req.abort();
        });
    })
}

mq.open().then((ch) => {
    let http = require('http');
    let middleware = http.createServer('/', (req, res) => {
        switch (req.method) {
            case 'POST':
                post(req, res);
                break;

            case 'GET':
                get(req, res);
                break;
        
            default:
                print("check attacking using http")
                mq.send("mail", '', { type: "notice", headers: { to: nconf.get('manager') } }) // using cmd
                break;
        }
            
    });
    middleware.listen(9759);
    auth_cleaner();

}).catch(e => {
    print(e)
})

// auth from agents