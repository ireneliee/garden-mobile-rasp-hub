let connected = 0
let data = 0



bluetooth.onBluetoothConnected(function () {
    connected = 1
    basic.showIcon(IconNames.Giraffe)
})



bluetooth.onBluetoothDisconnected(function () {
    connected = 0
    basic.showIcon(IconNames.No)
})



// bluetooth.onUartDataReceived(serial.delimiters(Delimiters.NewLine), function () {
//     data = bluetooth.uartReadUntil(serial.delimiters(Delimiters.NewLine))
//     basic.showString("R")
// })



input.onButtonPressed(Button.A, function () {
    if (connected == 1) {
        data = pins.analogReadPin(AnalogPin.P0)
        bluetooth.uartWriteNumber(data)
        basic.showString("T")
    }
})



input.onButtonPressed(Button.B, function () {
    basic.showString("RX:" + data)
    basic.showIcon(IconNames.Giraffe)
})



bluetooth.setTransmitPower(7)
bluetooth.startUartService()
data = 0
connected = 0
basic.showIcon(IconNames.Yes)

basic.forever(function () {

})
