#!/usr/bin/env bats

load helpers

@test "Info Basic" {

    query='/'
    response="info.json"
    pattern=.

    run compare ${query} ${response} ${pattern}

    [[ "$status" = 0 ]]

}

@test "Info Basic 2" {

    query='/info'
    response="info.json"
    pattern=.

    run compare ${query} ${response} ${pattern}

    [[ "$status" = 0 ]]

}

@test "Service info " {

    query='/service-info'
    response="info-service.json"
    pattern=.

    run compare ${query} ${response} ${pattern}

    [[ "$status" = 0 ]]

}

@test "Services" {

    query='/services'
    response="services.json"
    pattern=.

    run compare ${query} ${response} ${pattern}

    [[ "$status" = 0 ]]

}
