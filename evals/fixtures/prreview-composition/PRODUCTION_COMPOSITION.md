# Production composition

Desktop startup never calls `launch_detached()`. Its startup barrier owns candidate creation and
always calls `launch_owned(close_on_launcher_exit=True)`. `launch_owned()` creates the lifetime
pipe only when an optional inherited lease descriptor is present. Normal desktop startup has no
lease descriptor, so `close_on_launcher_exit=True` currently changes no production behavior.
