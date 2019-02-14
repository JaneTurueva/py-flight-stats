py-flight-stats
===============

Console client for flightstats.com API


Installation
------------
.. code-block:: shell

    git clone git@github.com:JaneTurueva/py-flight-stats.git
    cd py-flight-stats
    git checkout feature/wip
    make devenv


Command line usage
------------------
.. code-block:: shell

    source env/bin/activate
    export ID=1
    export KEY=1
    flight-stats --app-id=$ID --app-key=$KEY get-airports
    flight-stats --app-id=$ID --app-key=$KEY get-arrivals --airport=1
    flight-stats --app-id=$ID --app-key=$KEY get-departures --airport=1
    flight-stats --app-id=$ID --app-key=$KEY get-flight --flight-id=1
