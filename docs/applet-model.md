# The Secret Life of Applets

In the current model, life is simple: we have an `AppletManager` and we have
`Applet`s.

In this world, `Applet`s exist as separate processes running in the background
on a user's desktop environment, parallel to the actual G13 Configurator
process. These applets are generally expected to be running all the time, and
maintain their registration status with the `AppletManager` via D-Bus.

When the configurator is running, the `AppletManager` is expected to be exposed
via D-Bus under the well-known bus name of `com.theonelab.g13.AppletManager`
(name subject to change), and `Applets` are expected to try to register to this
object as soon as they can.

## Applet Lifecycle

During normal operation, `Applet`s are mostly sleeping in the background,
waiting for one of their three exposed methods to be called by the
`AppletManager`. They don't render until told to by one of these methods, and
once they are called, then the applet can `Present` new frames periodically to
the `AppletManager` for display on the G13's LCD.

In essence, each `Applet` runs in the background, until it is made the
foreground applet by the user. Once there, it can push frames all it likes,
until it receives an `Unpresent` call from the `AppletManager`, in which case
then it's pushed into the background again. Further `Present` calls will fail
once this happens.

## AppletManager

The `AppletManager` is a simple object that exposes two methods via D-Bus:
`Register` and `Present`, while the `Applet`s are expected to expose three
endpoints for the `AppletManager` to call periodically: `Present`, `Unpresent`,
`KeyPressed` and `KeyReleased`.

### `Present` and `Unpresent`

These two methods essentially control the "foreground"/"background"-ness of the
applet. `Present` tells the applet it has moved into the foreground, and it
needs to return the first frame it plans to render immediately.

`Unpresent`, on the other hand, tells the applet it is now in the background,
and it should stop rendering.

### `KeyPressed` and `KeyReleased`

These two methods tell the applet which of the L1-L4 keys has been pressed. They
will only fire after the `Present` call has been made.
