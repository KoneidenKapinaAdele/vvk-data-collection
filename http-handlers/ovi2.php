<?php

file_put_contents("event.log", "{$_GET[sensor]},{$_GET[state]}\n", FILE_APPEND);
echo "yes: {$_GET[sensor]},{$_GET[state]}";

