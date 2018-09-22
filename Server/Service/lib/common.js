// global
global._ = require("lodash");
global.config = require('nconf')


let moment = require("moment");
require('moment-timezone');
moment.tz.setDefault("Asia/Seoul");

global.timestamp = () => {
    moment().tz(moment())
    moment.tz("2014-06-01 12:00", "America/New_York");
    return moment().unix()
}
global.time = () => {
    return moment().format('YYYY-MM-DD HH:mm:ss')
}
global.date = () => {
    return moment().format('YYYY-MM-DD')
}

config.argv().env().file({
    file: 'config.json'
});

global.debug = config.get("debug")


global.print = (title, content = '') => { if (debug) { console.log(title, content); } }