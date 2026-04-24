#! /bin/bash

#lint
cargo check

#test
cargo test

#Build
cargo build --release

#run
cargo runcd