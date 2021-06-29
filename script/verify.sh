#!/usr/bin/env bash

source $(dirname -- "$0")/java_use.sh

export JAVA_VERSION=$(test -f .java-version && cat .java-version || echo 16)

java_use $JAVA_VERSION
test ! -f pom.xml || mvn -q verify
test ! -f build.gradle || ./gradlew build
