// SyncN Project
// auth : Fhwang in SyncN

const nodemailer = require('nodemailer');
const smtpPool = require('nodemailer-smtp-pool');
const fs = require('fs');
let auth_html = '';
// smtpPool는 smtp서버를 사용하기 위한 모듈로
// transporter객체를 만드는 nodemailer의 createTransport메소드의 인자로 사용된다.
// config 정보로 바뀌어야 함
const config = {
    mailer: {
        service: 'syncn_mail',
        host: 'smtp.gmail.com',
        port: '587',
        user: 'syncn2018@gmail.com',
        password: '8102@syncn',
    },
};

const transporter = nodemailer.createTransport(smtpPool({
    service: config.mailer.service,
    host: config.mailer.host,
    port: config.mailer.port,
    auth: {
        user: config.mailer.user,
        pass: config.mailer.password,
    },
    tls: {
        rejectUnauthorize: false,
    },
    maxConnections: 5,
    maxMessages: 10,
}));
fs.readFile('mail_format/auth.html', (err, data) => {
    if (err) throw err;
    auth_html = data.toString();
    
});
let mail = {
    send_auth: (to) => {
        return new Promise((resolve, reject) => {
            const from = 'syncn2018 < syncn2018@gmail.com >';
            let code = Math.floor(Math.random() * 10000) + 1;
            
            auth_html = auth_html.replace('%code%', code)
            subject = 'SyncN Notify auth code(this code remove to after 10 min)';
            const mailOptions = {
                from,
                to,
                subject,
                html: auth_html,
                //text
            };

            transporter.sendMail(mailOptions, (err, res) => {
                if (err) {
                    console.log('failed... => ', err);
                } else {
                    print(JSON.stringify(res))
                }

                err ? reject(0) : resolve(res);
            });
        })
        
    },
    send_login: (to, code) => {
        const from = 'syncn2018 < syncn2018@gmail.com >';
        auth_html = auth_html.replace('%code%', code)
        subject = 'SyncN Notify Login Code';
        const mailOptions = {
            from,
            to,
            subject,
            html : auth_html,
            // text,
        };

        transporter.sendMail(mailOptions, (err, res) => {
            if (err) {
                console.log('failed... => ', err);
            } else {
                console.log('succeed... => ', res);
            }

            transporter.close();
        });
    }
}
module.exports  = mail;
