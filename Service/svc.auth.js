process.chdir(__dirname);
require('app-module-path').addPath(__dirname);
require('lib/common')
let mq = require('lib/channel');
let mail = require('lib/sendmail');
let forge = require('node-forge')
let regx = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,5}$/i;
let auth = {}

let auth_cleaner = () => {
    print('auth cleaner running', auth)
    _.forEach(_.keys(auth), key => {
        if (auth[key].expire < timestamp() || auth[key].status) { auth = _.omit(auth, [key]) }
    })
    setTimeout(() => {
        auth_cleaner()
    }, 3000);
}

let auth_generator = (email) => {
    let sha256_email = forge.md.sha256.create().update(email).update(email.split("@")[0]);
    let md5_email = forge.md.md5.create().update(sha256_email+timestamp()).digest().toHex();
    auth[md5_email] = { status: false, expire: timestamp() + (1000 * 60 * 5) } // expire 5 min
    return md5_email;
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
        let email = data.match(regx)[0];
        if (email == null) { return; }
        // print("auth code : ", auth_generator(email))
        mail.send_auth(email, auth_generator(email))
        data = '';
        res.writeHead(200);
        res.end();
    });
}

let get = (req, res) => {
    let code = req.url.split("/")[2];
    if (!auth[code]) { return; }
    else {
        auth[code].status = true;
        console.log("auth!!!!!, " + code, auth[code] )
        //create client queue
    }
    // output message

    res.writeHead(200);
    res.end();

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