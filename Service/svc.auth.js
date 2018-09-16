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

fs.readFile('mail_format/auth_link.html', (err, data) => {
    if (err) throw err;
    auth_link = data.toString();

});

let auth_cleaner = () => {
    print('auth cleaner running', auth)
    _.forEach(_.keys(auth), key => {
        if (auth[key].expire < timestamp() || auth[key].status) { auth = _.omit(auth, [key]) }
    })
    // setTimeout(() => {
    //     auth_cleaner()
    // }, 10000);
}

let auth_generator = (email) => {
    let sha256_email = forge.md.sha256.create().update(email).update(email.split("@")[0]);
    let queue_name = `c.${forge.md.md5.create().update(sha256_email).digest().toHex()}.${timestamp()}`;
    let otp = forge.md.md5.create().update(sha256_email + timestamp()).digest().toHex();
    auth[otp] = { msg_id: '', status: false, expire: timestamp() + (1000 * 60 * 5), info: { q: queue_name, id: queue_name + timestamp(), pw: otp }} // expire 5 min
    auth[otp].msg_id = forge.md.md5.create().update(timestamp()).digest().toHex();
    print("auth gen ok", auth[otp].msg_id);
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
            res.end(JSON.stringify(_.assign(_.pick(req, ['headers', 'method', 'url']), { body: auth[otp].msg_id })))


        } catch (e) {
            console.log(e)
            res.writeHead(404);
            res.end();
        }
        
    });
}

let get = (req, res) => {
    try {
        if (req.url.indexOf('/code/') == -1) { return; }
        let code = req.url.split("/")[2];
        
        if (!auth[code]) {
            res.writeHead(404);
            res.write("Auth timeout so, expired this link"); }
        else if (code == auth[code].mes_id) {
            if (auth[code].status) {
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.write(auth[code].info);
                console.log("auth!!!!!, " + code, auth[code])
                mq.publish("cmd", "account", JSON.stringify(_.pick(auth[code], ['id', 'pw', 'q'])))
            }else { 
                res.writeHead(404, { 'Content-Type': 'application/text' });
                res.write("chk_e");
            }
        }
        else if (_.has(auth, code)) { res.writeHead(200); res.write(auth_link); auth[code].status = true; }
        else { res.writeHead(404); return; }
        res.end();    
    } catch (e) {
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
    let middleware = http.createServer('/code', (req, res) => {
        switch (req.method) {
            case 'POST':
                post(req, res);
                break;

            case 'GET':
                get(req, res);
                break;
        
            default:
                print("check attacking using http")
                // mq.send("mail", '', { type: "notice", headers: { to: email } }) // using cmd
                break;
        }
            
    });
    middleware.listen(9759);
    auth_cleaner();

}).catch(e => {
    print(e)
})

// auth from agents