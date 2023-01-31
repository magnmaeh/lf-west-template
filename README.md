# Lingua Franca West Template

This repository contains a template for Lingua Franca applications using the
Zephyr target platform. It contains a `west` extensions which takes care of
invoking `lfc`.

## Requirements
- Linux system (or WSL). Should be fine on macos also, but not tested yet.
- An installation of `lfc` which is more recent than commit `788ba74` where
  zephyr support was added

### Zephyr
- In order to use this template the following Zephyr dependencies are needed:
1. West meta build tool
2. Zephyr SDK and toolchains

Please refer to [Zephyr Getting Started Guide](https://docs.zephyrproject.org/latest/getting_started/index.html). NB. You can skip steps 5,6,7 which clones the entire Zephyr project. Instead we will clone Zephyr into this workspace using west.

If `west` is installed in a virtual environment, this environment is assumed activated for the rest of this guide.
### Initialization
1. Clone this template and remove old git history
```
git clone https://github.com/lf-lang/lf-zephyr-template/ lf-zephyr-app
cd lf-zephyr-app
```

2. Clone the Zephyr project into `deps/zephyr`
```
west update
```

### Build & Run

#### QEMU emulation
```
cd application
west lf-build src/HelloWorld.lf -w "-t run"
```

#### Nrf52 blinky
```
cd application
west lf-build src/NrfBlinky.lf -w "-b nrf52dk_nrf52832"
west flash
```

The custom `lf-build` west command can be inspected in `scripts/lf_build.py`. It
invokes `lfc` on the provided LF source file. It then invokes `west build` on
the generated sources. See `west lf-build -h` for more information.
