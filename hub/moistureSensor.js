serial.onDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    data = serial.readLine()
    basic.showString("D")

    if (data.includes('cmd:')) {
        if (state == 2) {
            if (data.includes('cmd:ideal=')) {
                state = 3
                commandStartTime = input.runningTime()
                sensorValues = []
            }
            ideal = data.split('=')
            idealValue = parseInt(ideal[1])
            moisture = pins.analogReadPin(AnalogPin.P0)
            basic.showString("M:" + moisture)
            serial.writeLine("" + moisture)

            if (moisture < idealValue) {
                while (pins.analogReadPin(AnalogPin.P0) < idealValue) {
                    pins.digitalWritePin(DigitalPin.P1, 1)
                    basic.pause(100) // give time for moisture level to change
                    moisture = pins.analogReadPin(AnalogPin.P0)
                    // sensorValues.push("" + moisture)

                    if (pins.analogReadPin(AnalogPin.P0) >= idealValue) {
                        pins.digitalWritePin(DigitalPin.P1, 0)
                        moisture = pins.analogReadPin(AnalogPin.P0)
                        // sensorValues.push("" + moisture)
                        serial.writeLine("" + moisture)

                    }
                }
            }
            state = 2
        }
    }
})

let line = ''
let ideal: string[] = []
let moisture = 0
let idealValue = 0
let response = ""
let microbitDevices: string[] = []
let sensorValues: string[] = []
let state = 2
let commandStartTime = 0
let handshakeStartTime = 0
let data = ""
let buffer: string[] = []
radio.setGroup(19)
radio.setTransmitSerialNumber(true)
radio.setTransmitPower(7)
handshakeStartTime = 0
commandStartTime = 0
serial.redirectToUSB()
basic.showIcon(IconNames.Yes)
// basic.forever(function () {
//     if (state == 3) {
//         if (input.runningTime() - commandStartTime > 6 * 1000) {
            
//             response = ""
//             for (let sensorValue of sensorValues) {
//                 if (response.length > 0) {
//                     response = "" + response + "," + sensorValue
//                 } else {
//                     response = sensorValue
//                 }
//             }
//             serial.writeLine("" + response)
//         }
//     }
// })

