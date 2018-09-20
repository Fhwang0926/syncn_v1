process.chdir(__dirname);
require('app-module-path').addPath(__dirname);
require('lib/common')




main = () =>{
    const rabbit = require('axios').create({
        baseURL: 'http://' + config.get('mq:host') + ':9999/api',
        timeout : 2000,
        auth: { username: config.get('mq:id'), password: config.get('mq:pw') }
    })
    
    
    
    await rabbit.put(`/users/${account.id}`, { password: account.pw, tags : '' })
    // 큐 생성 및 exchange, cmd 바인딩
    // .then(() => rabbit.put(`/permissions/${config.get('mq:vhost')}/${rs_c.license}`, perm))
    // .then(() => rabbit.put(`/exchanges/${config.get('mq:vhost')}/${account.q}`, { type: 'fanout', durable: true }))
    .catch(() => { throw new Error('MQ error'); })
}

main()