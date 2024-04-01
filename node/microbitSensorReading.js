// 0 -> disconnected; 1 -> connected
let connected_status = 0

// setup
bluetooth.setTransmitPower(7)
bluetooth.startUartService()

bluetooth.onBluetoothConnected(function () {
    connected_status = 1
    basic.showIcon(IconNames.Giraffe)
})

bluetooth.onBluetoothDisconnected(function () {
    connected_status = 0
    basic.showIcon(IconNames.No)
})

const TEMPERATURE_ = "temp"
const MOISTURE_ = "mois"
const SALINITY_ = "sali"
const SOILPH_ = "soil"

// mock send temperature data
input.onButtonPressed(Button.A, function () {
    if (connected_status == 1) {
        bluetooth.uartWriteString("temp:23.4")
        basic.showString("T")
    }
})

// mock send temperature data
input.onButtonPressed(Button.B, function () {
    if (connected_status == 1) {
        bluetooth.uartWriteString("mois:90.1")
        basic.showString("T")
    }
})

// mock send salinity data
input.onButtonPressed(Button.AB, function () {
    if (connected_status == 1) {
        bluetooth.uartWriteString("sali:56.1")
        basic.showString("T")
    }
})