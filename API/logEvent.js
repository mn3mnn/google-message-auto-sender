const { format } = require('date-fns')
const { v4: uuid } = require('uuid')
const fs = require('fs')
const fsPromises = require('fs').promises
const path = require('path')




const logEvents = async (msg) => {
    time = `${format(new Date(), 'yyyyMMdd\tHH:mm:ss')}`
    logItem = `${time}\t${uuid()}\t${msg}\n`
    console.log(logItem)
    try{
        if (!fs.existsSync(path.join(__dirname, 'logs'))){
            await fsPromises.mkdir(path.join(__dirname, 'logs'))
        }
        await fsPromises.appendFile(path.join(__dirname, 'logs', 'reqLog.txt'), logItem)

    }
    catch(err){
        console.error(err);
    }
}


module.exports = logEvents;