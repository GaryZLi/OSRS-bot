const robot = require('robotjs');
const Jimp = require('jimp');
const fs = require('fs');
const currentDate = (new Date()).toLocaleDateString().split('/').join('-');
const path = './endResults/' + currentDate + '/';
const resultPath = (str) => path + str + '.png';

class Time {
    constructor() {
        this.val = 0;
        this.MILLISECOND = 1;
        this.SECOND = this.MILLISECOND * 1000;
        this.MINUTE = this.SECOND * 60;
        this.HOUR = this.MINUTE * 60;
        this.DAY = this.HOUR * 24;
    }

    setMilliseconds(ms) {
        this.val += ms;
        return this;
    }

    setSeconds(sec) {
        this.val += sec * this.SECOND;
        return this;
    }

    setMinutes(min) {
        this.val += min * this.MINUTE;
        return this;
    }

    setHours(hr) {
        this.val += hr * this.HOUR;
        return this;
    }

    setDays(day) {
        this.val += day * this.DAY;
        return this;
    }

    getTime() {
        return this.val;
    }
}

function screenCaptureToFile2(robotScreenPic) {
    let length;

    try {
        length = fs.readdirSync(path).length;
    }
    catch {
        fs.mkdirSync(path);
        length = 0;
    }

    return new Promise((resolve, reject) => {
        try {
            const image = new Jimp(robotScreenPic.width, robotScreenPic.height);
            let pos = 0;
            image.scan(0, 0, image.bitmap.width, image.bitmap.height, (x, y, idx) => {
                image.bitmap.data[idx + 2] = robotScreenPic.image.readUInt8(pos++);
                image.bitmap.data[idx + 1] = robotScreenPic.image.readUInt8(pos++);
                image.bitmap.data[idx + 0] = robotScreenPic.image.readUInt8(pos++);
                image.bitmap.data[idx + 3] = robotScreenPic.image.readUInt8(pos++);
            });
            image.write(resultPath(length), resolve);
        } catch (e) {
            console.error(e);
            reject(e);
        }
    });
}

const sleep = time => new Promise(res => setTimeout(res, time.getTime()));
let running = true;

const run = async () => {
    while (running) {
        robot.mouseClick()
        const tick = 500 + Math.random() * 140;
        await sleep(new Time().setMilliseconds(tick));
        robot.mouseClick();

        const wait = 12000 + Math.random() * 6000;
        await sleep(new Time().setMilliseconds(wait));
    }
};

setTimeout(run, 2000);

const turnOffTime = new Time()
.setHours(1)
.setMinutes(10)
.getTime();


const {
    exec
} = require('child_process');

const turnOff = () => setTimeout(() => {
    exec('rundll32.exe powrprof.dll, SetSuspendState Sleep', () => {});
    screenCaptureToFile2(robot.screen.capture());
    running = false;
}, turnOffTime);


turnOff();